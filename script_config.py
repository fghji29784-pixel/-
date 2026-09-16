"""
기존 프로젝트(양산데이터추론코드.py 등)를 서버에서 그대로 실행시키기 위한 설정입니다.
코드 내용은 건드리지 않고, 아래 값들만 실제 환경에 맞게 확인/수정하세요.
"""

# 기존 프로젝트 전체(스크립트, environment.yml, requirements.txt, 기타 모듈)를
# 복사해 넣는 폴더 이름입니다. script_project 폴더 안에 그대로 붙여넣으세요.
PROJECT_DIR_NAME = "script_project"

# 평소 VS Code에서 F5로 실행하던 진입점 파일명
ENTRY_SCRIPT = "양산데이터추론코드.py"

# conda environment.yml 맨 위 name: 값
CONDA_ENV_NAME = "low_voltage"

# 입력 엑셀 경로를 받는 커맨드라인 인자 이름 (코드 안 add_argument('--input-csv', ...) 그대로)
INPUT_ARG_NAME = "--input-csv"

# 결과 파일이 저장될 때의 파일명 패턴 (스크립트 폴더 안에 생성됨, 타임스탬프 등으로 매번 달라져도 됨)
OUTPUT_GLOB_PATTERN = "양산판정_*.csv"

# 스크립트가 너무 오래 걸리면 중단시키기 위한 최대 대기 시간(초)
SCRIPT_TIMEOUT_SECONDS = 1800
