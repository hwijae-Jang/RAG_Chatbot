"""
Google Colab 환경 설정 스크립트
"""

import os
from getpass import getpass

def setup_openai_key():
    """
    OpenAI API 키를 안전하게 등록합니다.
    """
    # API 키가 이미 등록되어 있는지 확인
    if "OPENAI_API_KEY" in os.environ:
        print("✅ OPENAI_API_KEY가 이미 등록되어 있습니다.")
        return
    
    # 사용자로부터 API 키 입력받기 (보안 입력)
    api_key = getpass("OpenAI API 키를 입력하세요 (입력 내용은 숨겨집니다): ")
    
    if not api_key:
        raise ValueError("❌ API 키가 입력되지 않았습니다.")
    
    # 환경변수에 등록
    os.environ["OPENAI_API_KEY"] = api_key
    
    # 확인 (첫 10자만 표시)
    print(f"✅ OPENAI_API_KEY 등록 완료: {api_key[:10]}...")
    print("⚠️  이 API 키는 절대 GitHub에 업로드하지 마세요!")

if __name__ == "__main__":
    setup_openai_key()
