"""
여기에 기존에 VS Code에서 쓰시던 '메인코드'를 붙여넣고 아래 두 가지만 고치면 됩니다.

1) 코드 안에서 엑셀 경로를 직접 적던 부분
       excel_path = "C:/Users/.../input.xlsx"
   같은 줄을 지우고, 대신 아래 run() 함수의 매개변수 excel_path를 그 자리에 쓰세요.
   (웹페이지에서 업로드한 파일이 서버에 저장된 뒤, 그 경로가 excel_path로 들어옵니다.)

2) 메인코드가 만들어내는 최종 결과를 return 하세요. 둘 중 편한 방식을 쓰면 됩니다.
   - pandas.DataFrame을 그대로 return
   - 결과를 엑셀/CSV로 저장하는 코드라면, 저장한 파일 경로(문자열)를 return

예시)
    import pandas as pd

    def run(excel_path: str):
        df = pd.read_excel(excel_path)
        # ... 기존 메인코드의 처리 로직을 그대로 옮겨 적으세요 ...
        df["결과"] = df["어떤컬럼"] * 2
        return df

    # 또는 기존 코드가 파일로 저장하는 방식이었다면:
    def run(excel_path: str):
        df = pd.read_excel(excel_path)
        # ... 처리 ...
        df.to_excel("main_output.xlsx", index=False)
        return "main_output.xlsx"

주의: 결과 DataFrame(또는 결과 파일) 안에는 원본 엑셀과 매칭할 때 쓸 키 컬럼
(예: "ID")이 반드시 포함되어 있어야 합니다. 웹페이지에서 그 컬럼 이름을 입력하면
원본 엑셀과 이 결과를 그 키로 조인해서 하나의 파일로 합쳐 드립니다.
"""


def run(excel_path: str):
    raise NotImplementedError(
        "이 함수 안에 메인코드를 붙여넣어 완성해 주세요. "
        "자세한 방법은 이 파일 맨 위 설명과 README.md를 참고하세요."
    )
