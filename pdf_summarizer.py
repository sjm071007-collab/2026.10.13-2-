import os
import io
from typing import List, Union
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class PDFSummarizer:
    def __init__(self, api_key: str = None, model: str = None):
        """PDF 요약기 초기화

        Args:
            api_key: OpenAI API 키 (미지정 시 환경변수 OPENAI_API_KEY 사용)
            model: 사용할 OpenAI 모델명 (기본값: gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 입력하거나 직접 전달해주세요."
            )
        
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key)

    @staticmethod
    def extract_text_from_pdf(pdf_source: Union[str, io.BytesIO]) -> str:
        """PDF 파일 경로 또는 바이트 스트림에서 텍스트를 추출합니다.

        Args:
            pdf_source: PDF 파일 경로 (str) 또는 바이너리 스트림 (io.BytesIO)

        Returns:
            추출된 전체 텍스트
        """
        reader = PdfReader(pdf_source)
        extracted_pages = []

        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(f"--- [Page {page_idx + 1}] ---\n{text.strip()}")

        if not extracted_pages:
            raise ValueError("PDF에서 추출할 수 있는 텍스트가 없습니다. (스캔된 이미지 문서인 경우 OCR이 필요할 수 있습니다.)")

        return "\n\n".join(extracted_pages)

    @staticmethod
    def split_text_into_chunks(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
        """긴 텍스트를 일정 크기로 분할합니다."""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks

    def summarize(
        self,
        text: str,
        summary_style: str = "bullet",
        target_language: str = "한국어",
        custom_instructions: str = ""
    ) -> str:
        """추출된 텍스트를 요약합니다.

        Args:
            text: 요약할 원문 텍스트
            summary_style: 요약 형태 ('bullet', 'three_lines', 'detailed', 'executive')
            target_language: 요약 결과 언어 (기본: '한국어')
            custom_instructions: 추가 요청사항

        Returns:
            요약 결과 문자열
        """
        style_prompts = {
            "bullet": "핵심 내용을 가독성 좋은 불릿 포인트(개조식)로 정리하고, 중요한 키워드는 굵게 강조해주세요.",
            "three_lines": "가장 핵심적인 결론을 명확한 3줄로 압축해서 요약해주세요.",
            "detailed": "서론/배경, 핵심 내용 및 주요 데이터, 결론 및 시사점으로 항목을 나누어 상세히 요약해주세요.",
            "executive": "경영진 또는 의사결정자를 위한 1페이지 브리핑 보고서 형식으로 작성해주세요."
        }

        selected_style = style_prompts.get(summary_style, style_prompts["bullet"])

        # 텍스트가 매우 길 경우 분할 처리
        chunks = self.split_text_into_chunks(text, chunk_size=8000)

        if len(chunks) == 1:
            # 단일 청크 요약
            system_prompt = (
                f"당신은 전문 문서 분석 및 요약 전문가입니다. "
                f"문서의 내용을 명확하고 논리적으로 분석하여 {target_language}로 작성하세요.\n"
                f"요약 지침: {selected_style}\n"
                f"{f'추가 지침: {custom_instructions}' if custom_instructions else ''}"
            )
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"다음 문서를 요약해주세요:\n\n{text}"}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        else:
            # 다중 청크 단계별 요약 (Map-Reduce 방식)
            intermediate_summaries = []
            for i, chunk in enumerate(chunks):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"다음은 긴 문서의 파트 {i + 1}/{len(chunks)}입니다. 주요 내용을 요약하세요."
                        },
                        {"role": "user", "content": chunk}
                    ],
                    temperature=0.3
                )
                intermediate_summaries.append(response.choices[0].message.content.strip())

            combined_summary_text = "\n\n".join(intermediate_summaries)
            final_system_prompt = (
                f"당신은 전문 문서 분석 및 요약 전문가입니다. "
                f"각 파트별 중간 요약들을 취합하여 일관되고 완성도 높은 최종 요약본을 {target_language}로 작성하세요.\n"
                f"요약 지침: {selected_style}\n"
                f"{f'추가 지침: {custom_instructions}' if custom_instructions else ''}"
            )
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": final_system_prompt},
                    {"role": "user", "content": f"중간 요약 내용:\n\n{combined_summary_text}"}
                ],
                temperature=0.3
            )
            return final_response.choices[0].message.content.strip()
