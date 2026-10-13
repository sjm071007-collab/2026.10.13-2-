import os
import streamlit as st
from pdf_summarizer import PDFSummarizer

st.set_page_config(
    page_title="AI PDF 요약기",
    page_icon="📄",
    layout="wide"
)

# 커스텀 스타일링
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📄 AI PDF 문서 요약기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">긴 PDF 문서를 업로드하면 OpenAI 최신 모델을 활용하여 핵심 내용을 빠르고 정확하게 요약해 드립니다.</div>', unsafe_allow_html=True)

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정 (Settings)")
    
    # API 키 입력
    default_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API Key",
        value=default_api_key,
        type="password",
        help=".env 파일에 설정하지 않은 경우 여기에 직접 API 키를 입력하세요."
    )
    
    # 모델 선택
    model_choice = st.selectbox(
        "사용할 AI 모델",
        options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o-mini는 속도가 빠르고 비용이 매우 저렴하며 우수한 성능을 제공합니다."
    )
    
    # 요약 스타일
    style_mapping = {
        "핵심 불릿포인트 (추천)": "bullet",
        "핵심 3줄 요약": "three_lines",
        "구조화된 상세 요약": "detailed",
        "경영진 보고서 형식": "executive"
    }
    selected_style_label = st.selectbox(
        "요약 스타일",
        options=list(style_mapping.keys()),
        index=0
    )
    summary_style = style_mapping[selected_style_label]
    
    # 결과 언어
    target_language = st.selectbox(
        "요약 언어",
        options=["한국어", "English", "日本語", "中文"],
        index=0
    )
    
    # 커스텀 지침
    custom_instructions = st.text_area(
        "추가 요구사항 (선택사항)",
        placeholder="예: 수치 데이터와 통계 위주로 요약해줘 / 전문 용어는 쉽게 풀어서 설명해줘",
        help="요약 시 특별히 강조하거나 고려할 사항을 적어주세요."
    )

# --- 메인 영역: 파일 업로드 ---
uploaded_file = st.file_uploader(
    "PDF 파일을 드래그하거나 선택하세요",
    type=["pdf"],
    help="텍스트가 포함된 PDF 파일을 업로드해주세요."
)

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📑 원본 문서 정보")
        try:
            with st.spinner("PDF에서 텍스트를 추출하는 중입니다..."):
                raw_text = PDFSummarizer.extract_text_from_pdf(uploaded_file)
            
            st.success(f"파일 이름: **{uploaded_file.name}**")
            st.info(f"추출된 글자 수: **{len(raw_text):,}자**")
            
            with st.expander("추출된 텍스트 미리보기 (앞부분 1,000자)", expanded=False):
                st.text(raw_text[:1000] + ("..." if len(raw_text) > 1000 else ""))
                
        except Exception as e:
            st.error(f"PDF 텍스트 추출 실패: {e}")
            raw_text = ""

    with col2:
        st.subheader("✨ 요약 결과")
        if raw_text:
            if st.button("🚀 요약 생성하기", type="primary", use_container_width=True):
                if not api_key:
                    st.error("⚠️ OpenAI API 키가 필요합니다. 사이드바에 입력하거나 .env 파일에 추가해주세요.")
                else:
                    try:
                        with st.spinner(f"'{model_choice}' 모델로 문서를 분석 및 요약 중입니다..."):
                            summarizer = PDFSummarizer(api_key=api_key, model=model_choice)
                            summary_result = summarizer.summarize(
                                text=raw_text,
                                summary_style=summary_style,
                                target_language=target_language,
                                custom_instructions=custom_instructions
                            )
                        
                        st.markdown("### 📌 요약본")
                        st.markdown(summary_result)
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="📥 요약본 다운로드 (.md)",
                            data=summary_result,
                            file_name=f"summary_{uploaded_file.name}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"요약 중 오류가 발생했습니다: {e}")
        else:
            st.info("좌측에서 유효한 PDF 텍스트가 추출되면 요약을 시작할 수 있습니다.")
else:
    st.info("👆 분석할 PDF 파일을 업로드해주세요.")
