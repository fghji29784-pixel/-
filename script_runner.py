import glob
import os
import subprocess

import script_config as cfg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, cfg.PROJECT_DIR_NAME)


def _output_candidates():
    return set(glob.glob(os.path.join(PROJECT_DIR, cfg.OUTPUT_GLOB_PATTERN)))


def run_main_script(input_path: str) -> str:
    """
    conda 환경에서 기존 프로젝트를 그대로 실행하고,
    실행 중 새로 생성된 결과 파일의 경로를 반환합니다.
    """
    entry_path = os.path.join(PROJECT_DIR, cfg.ENTRY_SCRIPT)
    if not os.path.isfile(entry_path):
        raise FileNotFoundError(
            f"'{cfg.PROJECT_DIR_NAME}' 폴더 안에 '{cfg.ENTRY_SCRIPT}' 파일이 없습니다. "
            "기존 프로젝트 폴더 전체를 script_project 폴더에 복사해 넣었는지 확인해 주세요."
        )

    before = _output_candidates()

    cmd = [
        "conda", "run", "-n", cfg.CONDA_ENV_NAME, "--no-capture-output",
        "python", cfg.ENTRY_SCRIPT, cfg.INPUT_ARG_NAME, input_path,
    ]
    result = subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=cfg.SCRIPT_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"메인코드 실행이 실패했습니다 (종료 코드 {result.returncode}).\n\n"
            f"--- stderr ---\n{result.stderr[-4000:]}\n"
            f"--- stdout ---\n{result.stdout[-2000:]}"
        )

    after = _output_candidates()
    new_files = after - before
    if not new_files:
        if not after:
            raise RuntimeError(
                f"'{cfg.OUTPUT_GLOB_PATTERN}' 패턴에 맞는 결과 파일을 "
                f"'{cfg.PROJECT_DIR_NAME}' 폴더에서 찾을 수 없습니다."
            )
        # 타임스탬프가 없어 파일명이 항상 같은 경우 등: 기존 파일 중 가장 최근 걸 사용
        new_files = after

    return max(new_files, key=os.path.getmtime)
