# 📄 AI PDF Summarizer (AI PDF 요약기)

OpenAI 최신 모델(`gpt-4o-mini`, `gpt-4o`)을 활용하여 긴 PDF 문서의 핵심 내용을 빠르고 명확하게 추출·요약해 주는 애플리케이션입니다.  
**웹 UI(Streamlit)** 와 **명령줄 인터페이스(CLI)** 를 모두 지원합니다.

---

## ✨ 주요 기능 (Key Features)

- **다양한 실행 환경**: 브라우저에서 편리하게 사용하는 **Streamlit 웹 UI**와 터미널용 **CLI** 동시 제공
- **긴 문서 분할 요약 (Chunking)**: 수십 페이지에 달하는 대용량 문서도 단계별(Map-Reduce)로 안정적으로 요약
- **맞춤형 요약 스타일**:
  - 📌 **핵심 불릿포인트 (Bullet)**: 주요 내용을 읽기 쉽게 개조식으로 정리
  - 🎯 **3줄 요약 (Three Lines)**: 결론 위주의 초압축 3줄 요약
  - 📊 **구조화된 상세 요약 (Detailed)**: 배경, 핵심 데이터, 결론 및 시사점 분석
  - 💼 **경영진 보고서 형식 (Executive)**: 원페이지 브리핑 형식
- **다국어 지원**: 한국어, 영어, 일본어, 중국어 등 자유로운 결과 언어 선택
- **다운로드 기능**: 웹 앱에서 요약 결과를 마크다운(`.md`) 파일로 즉시 저장

---

## 📁 프로젝트 구조 (Project Structure)

```text
.
├── app.py              # Streamlit 기반 웹 애플리케이션
├── cli.py              # 터미널용 CLI 스크립트
├── pdf_summarizer.py   # PDF 텍스트 추출 및 OpenAI 요약 핵심 엔진
├── requirements.txt    # 의존성 패키지 목록
├── .env.example        # 환경 변수 템플릿
├── .gitignore          # Git 업로드 제외 목록 (.env, 가상환경 등)
└── README.md           # 프로젝트 문서
```

---

## 🚀 빠른 시작 (Getting Started)

### 1. 사전 요구사항
- Python 3.9 이상
- OpenAI API Key ([발급받기](https://platform.openai.com/api-keys))

### 2. 설치 (Installation)

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (Configuration)

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 OpenAI API 키를 입력합니다.

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

`.env` 파일 편집:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

---

## 💻 사용 방법 (Usage)

### 방법 A. 웹 애플리케이션 실행 (Streamlit)
브라우저에서 드래그 앤 드롭으로 간편하게 사용합니다:

```bash
streamlit run app.py
```
실행 후 브라우저 창(`http://localhost:8501`)이 자동으로 열립니다.

---

### 방법 B. CLI 터미널 실행

기본 요약 (불릿포인트 형식):
```bash
python cli.py sample.pdf
```

옵션 활용 예시:
```bash
# 3줄 요약
python cli.py sample.pdf --style three_lines

# 상세 요약 및 마크다운 파일로 결과 저장
python cli.py sample.pdf --style detailed -o summary_result.md

# 영어로 요약
python cli.py sample.pdf --lang English
```

---

## 🐙 GitHub에 프로젝트 올리는 방법

터미널에서 아래 명령어를 차례대로 입력하시면 됩니다:

```bash
# 1. Git 저장소 초기화
git init

# 2. 파일 추가 및 첫 커밋 (.env 파일은 .gitignore에 의해 자동 제외됩니다)
git add .
git commit -m "feat: Initial commit for AI PDF Summarizer"

# 3. 기본 브랜치를 main으로 설정
git branch -M main

# 4. GitHub 저장소 연결 (본인의 깃허브 레포지토리 URL 입력)
git remote add origin https://github.com/사용자이름/저장소이름.git

# 5. 푸시
git push -u origin main
```

> ⚠️ **주의**: `.env` 파일에 API 키가 포함되어 있으므로 절대로 GitHub에 커밋되지 않도록 주의하세요. (`.gitignore`에 이미 등록되어 안전하게 제외됩니다.)

---

## 📜 라이선스 (License)
이 프로젝트는 [MIT License](LICENSE)를 따릅니다.
