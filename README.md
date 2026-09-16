# 엑셀 처리 도구 모음

이 저장소에는 두 가지 도구가 있습니다.

- **`tools/matching_tool.html`** : 서버가 필요 없는 정적 HTML 도구. 메인코드는 실행하지
  않고, 이미 갖고 있는 원본 엑셀 + 메인코드 출력 결과 두 파일을 매칭·판정·샘플링해서
  정리해 줍니다. 자세한 사용법은 `tools/README.md` 참고.
- **`app.py` 웹앱** : 서버 한 대를 계속 켜두고, 브라우저에서 엑셀을 업로드하면 메인코드
  실행까지 자동으로 해주는 도구입니다. 항상 켜둘 서버(PC/VM)가 있을 때 사용하세요.

---

# (참고) 메인코드 자동 실행 웹앱

브라우저에서 엑셀을 업로드하면 서버가 (당신의) 메인코드를 실행하고, 지정한 키 컬럼으로
원본 엑셀과 처리 결과를 조인해서 다운로드해주는 사내용 웹앱입니다. 외부 인터넷 접속이
전혀 필요 없습니다 (전부 로컬 파일/로컬 패키지만 사용).

## 1. 메인코드 연결하기 (코드 수정/공개 불필요)

기존 프로젝트 폴더(`양산데이터추론코드.py`, `environment.yml`, `requirements.txt`,
그 외 모듈 파일들)를 **통째로** `script_project/` 폴더 안에 그대로 복사해 넣으세요.
코드는 한 줄도 고칠 필요가 없습니다 — 웹앱이 기존에 쓰시던 것과 똑같이

```
conda run -n low_voltage python 양산데이터추론코드.py --input-csv <업로드된 엑셀 경로>
```

형태로 그대로 실행시키고, 실행 중 `script_project/` 폴더에 새로 생기는
`양산판정_*.csv` 파일을 자동으로 찾아서 결과로 사용합니다.

- 실행 방식/파일명/conda 환경 이름 등은 `script_config.py`에 정리되어 있습니다.
  기본값이 이미 다음과 같이 맞춰져 있는데, 달라지면 이 파일만 고치면 됩니다.
  - `ENTRY_SCRIPT = "양산데이터추론코드.py"`
  - `CONDA_ENV_NAME = "low_voltage"`
  - `INPUT_ARG_NAME = "--input-csv"`
  - `OUTPUT_GLOB_PATTERN = "양산판정_*.csv"`

## 2. 설치 (사내망 PC/서버에서 1회만)

이 웹앱 자체(Flask 등)에 필요한 패키지:

```bash
pip install -r requirements.txt
```

기존 프로젝트가 쓰는 conda 환경도 서버에 한 번 만들어 둬야 합니다
(`script_project/environment.yml` 기준):

```bash
conda env create -f script_project/environment.yml
```

이미 `low_voltage`라는 이름의 conda 환경이 그 서버에 있다면 이 단계는 생략해도 됩니다.
`conda env list`로 확인하세요. 웹앱을 실행하는 터미널에서 `conda` 명령이 바로
동작해야 합니다 (`conda run -n low_voltage python --version`으로 미리 테스트해 보세요).

## 3. 실행

```bash
python app.py
```

- 기본적으로 `0.0.0.0:5000`에서 실행되어, 같은 사내망의 다른 PC에서도
  `http://<이 PC의 사내망 IP>:5000` 주소로 접속할 수 있습니다.
- 접속 안 되면 해당 PC의 방화벽에서 5000번 포트를 열어주세요.
- 여러 명이 평소에 계속 쓸 거라면, `python app.py` 대신 아래처럼 waitress(운영용 서버)로
  띄우는 걸 권장합니다.

```bash
python -m waitress --listen=0.0.0.0:5000 app:app
```

이 상태로 PC를 계속 켜두면 동료들이 브라우저로 접속해서 사용할 수 있습니다.
(작업 관리자나 서버 재부팅 시 자동 실행이 필요하면 Windows는 작업 스케줄러,
Linux는 systemd 서비스 등록을 이용하세요.)

## 4. 사용법

1. 웹페이지에서 엑셀 파일 선택
2. 원본 엑셀에서 매칭 기준이 되는 키 컬럼명 입력 (예: `ID`)
3. 메인코드 결과물의 키 컬럼명이 다르면 별도 입력, 같으면 비워두기
4. "처리 시작" 클릭 → 기존 프로젝트를 conda 환경에서 실행 → 키 기준으로 원본과 결과 조인
5. 결과 미리보기 확인 후 "결과 파일 다운로드"

## 폴더 설명

- `uploads/` : 업로드된 원본 엑셀 임시 저장 (자동 생성, 파일명에 타임스탬프 부여)
- `outputs/` : 매칭 완료된 최종 결과 엑셀 저장
- `script_project/` : 기존 프로젝트 전체(스크립트, environment.yml 등)를 그대로 복사해 넣는 곳
- `script_config.py` : 실행 파일명/conda 환경/인자 이름 등 설정
- `script_runner.py` : `script_config.py` 설정대로 기존 프로젝트를 실행시키는 코드 (건드릴 필요 없음)
