import datetime
import os
import traceback
import uuid

import pandas as pd
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

import script_runner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
ALLOWED_EXTENSIONS = {".xlsx", ".xls"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 업로드 파일 최대 50MB


def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def timestamped_name(original_filename: str) -> str:
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = secure_filename(original_filename)
    return f"{stamp}_{uuid.uuid4().hex[:6]}_{safe_name}"


def load_result_file(path: str) -> pd.DataFrame:
    """메인코드가 만들어낸 결과 파일(csv/xlsx)을 DataFrame으로 로드."""
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    uploaded = request.files.get("excel_file")
    key_column = (request.form.get("key_column") or "").strip()
    output_key_column = (request.form.get("output_key_column") or "").strip() or key_column

    if not uploaded or uploaded.filename == "":
        return render_template("index.html", error="엑셀 파일을 선택해 주세요.")
    if not allowed_file(uploaded.filename):
        return render_template("index.html", error="xlsx 또는 xls 파일만 업로드할 수 있습니다.")
    if not key_column:
        return render_template("index.html", error="매칭에 쓸 키 컬럼명을 입력해 주세요.")

    saved_name = timestamped_name(uploaded.filename)
    saved_path = os.path.join(UPLOAD_FOLDER, saved_name)
    uploaded.save(saved_path)

    try:
        original_df = pd.read_excel(saved_path)
    except Exception as exc:
        return render_template("index.html", error=f"엑셀을 읽는 중 오류가 발생했습니다: {exc}")

    if key_column not in original_df.columns:
        return render_template(
            "index.html",
            error=f"원본 엑셀에 '{key_column}' 컬럼이 없습니다. "
            f"원본 컬럼 목록: {list(original_df.columns)}",
        )

    try:
        result_path = script_runner.run_main_script(saved_path)
        result_df = load_result_file(result_path)
    except Exception:
        return render_template(
            "index.html",
            error="메인코드 실행 중 오류가 발생했습니다:\n" + traceback.format_exc(),
        )

    if output_key_column not in result_df.columns:
        return render_template(
            "index.html",
            error=f"메인코드 결과물에 '{output_key_column}' 컬럼이 없습니다. "
            f"결과 컬럼 목록: {list(result_df.columns)}",
        )

    merge_left = original_df.copy()
    merge_right = result_df.copy()
    merge_left["_join_key"] = merge_left[key_column].astype(str).str.strip()
    merge_right["_join_key"] = merge_right[output_key_column].astype(str).str.strip()
    if output_key_column != key_column:
        merge_right = merge_right.drop(columns=[output_key_column])

    merged = pd.merge(
        merge_left,
        merge_right,
        on="_join_key",
        how="left",
        suffixes=("", "_결과"),
    ).drop(columns=["_join_key"])

    matched_rows = pd.merge(
        original_df.assign(_join_key=original_df[key_column].astype(str).str.strip()),
        result_df.assign(_join_key=result_df[output_key_column].astype(str).str.strip())[["_join_key"]],
        on="_join_key",
        how="inner",
    ).shape[0]

    output_name = timestamped_name(os.path.splitext(uploaded.filename)[0] + "_매칭결과.xlsx")
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    merged.to_excel(output_path, index=False)

    preview_html = merged.head(20).to_html(classes="preview-table", index=False, na_rep="")

    return render_template(
        "result.html",
        download_url=url_for("download", filename=output_name),
        total_rows=len(original_df),
        matched_rows=matched_rows,
        preview_html=preview_html,
    )


@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # host="0.0.0.0" 으로 열어야 같은 사내망의 다른 PC에서도 접속 가능합니다.
    app.run(host="0.0.0.0", port=5000, threaded=True)
