import argparse
import sys
from pathlib import Path
from pdf_summarizer import PDFSummarizer


def main():
    parser = argparse.ArgumentParser(
        description="PDF 문서 AI 요약 도구 (OpenAI 기반)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("pdf_path", type=str, help="요약할 PDF 파일 경로")
    parser.add_argument(
        "--style",
        choices=["bullet", "three_lines", "detailed", "executive"],
        default="bullet",
        help="요약 형태: bullet (불릿포인트), three_lines (3줄 요약), detailed (상세 요약), executive (보고서 형식)"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="한국어",
        help="요약 결과 언어"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI 모델명 (예: gpt-4o-mini, gpt-4o)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="요약 결과를 저장할 파일 경로 (선택)"
    )

    args = parser.parse_args()

    pdf_file = Path(args.pdf_path)
    if not pdf_file.is_file():
        print(f"❌ 오류: 파일을 찾을 수 없습니다: {pdf_file}", file=sys.stderr)
        sys.exit(1)

    print(f"📖 PDF 텍스트 추출 중: {pdf_file.name}...")
    try:
        raw_text = PDFSummarizer.extract_text_from_pdf(str(pdf_file))
        print(f"✅ 추출 완료 (총 {len(raw_text):,} 자)")
    except Exception as e:
        print(f"❌ 텍스트 추출 실패: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"🤖 OpenAI ({args.model}) 요약 요청 중... (스타일: {args.style})")
    try:
        summarizer = PDFSummarizer(model=args.model)
        summary = summarizer.summarize(
            text=raw_text,
            summary_style=args.style,
            target_language=args.lang
        )
    except Exception as e:
        print(f"❌ 요약 실패: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 50)
    print(f"📌 요약 결과 ({args.style})")
    print("=" * 50 + "\n")
    print(summary)
    print("\n" + "=" * 50)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(summary, encoding="utf-8")
        print(f"\n💾 요약 결과가 '{out_path}' 에 저장되었습니다.")


if __name__ == "__main__":
    main()
