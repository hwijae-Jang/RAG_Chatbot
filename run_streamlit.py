"""
Google Colab에서 Streamlit 앱을 실행하고 ngrok으로 공개 URL 생성
"""

import os
import time
from pyngrok import ngrok

def kill_existing_processes():
    """기존 streamlit 및 ngrok 프로세스 종료"""
    print("🧹 기존 프로세스 정리 중...")
    
    # ngrok 터널 종료
    try:
        ngrok.kill()
        print("  ✓ ngrok 터널 종료")
    except Exception as e:
        print(f"  ℹ️  ngrok 종료 중 오류 (무시): {e}")
    
    # streamlit 프로세스 종료
    os.system("pkill -f streamlit >/dev/null 2>&1 || true")
    print("  ✓ streamlit 프로세스 종료")
    
    time.sleep(2)  # 프로세스 종료 대기

def start_streamlit():
    """Streamlit 앱 백그라운드 실행"""
    print("\n🚀 Streamlit 앱 시작 중...")
    
    # 백그라운드에서 streamlit 실행
    os.system("streamlit run app.py --server.address 0.0.0.0 --server.port 8501 &>/dev/null &")
    
    # 서버 시작 대기
    time.sleep(5)
    print("  ✓ Streamlit 서버 시작 완료 (포트: 8501)")

def create_ngrok_tunnel():
    """ngrok 터널 생성 및 공개 URL 반환"""
    print("\n🌐 ngrok 터널 생성 중...")
    
    try:
        # ngrok 터널 생성
        public_url = ngrok.connect(addr="http://127.0.0.1:8501", bind_tls=True)
        
        print("\n" + "="*60)
        print("✅ 배포 완료!")
        print("="*60)
        print(f"\n📱 공개 URL: {public_url}")
        print("\n💡 팁:")
        print("  - 위 URL을 클릭하거나 브라우저에 붙여넣으세요")
        print("  - URL은 ngrok 세션이 유지되는 동안 유효합니다")
        print("  - Colab 런타임이 종료되면 URL도 만료됩니다")
        print("="*60)
        
        return public_url
        
    except Exception as e:
        print(f"\n❌ ngrok 터널 생성 실패: {e}")
        print("\n해결 방법:")
        print("  1. ngrok 설치 확인: !pip install pyngrok")
        print("  2. ngrok 인증 토큰 설정 (선택사항)")
        print("     - https://dashboard.ngrok.com/get-started/your-authtoken")
        print("     - !ngrok authtoken YOUR_TOKEN")
        raise

def main():
    """메인 실행 함수"""
    print("🎯 항공권 환불 상담 RAG 챗봇 배포 시작\n")
    
    # API 키 확인
    if "OPENAI_API_KEY" not in os.environ:
        print("⚠️  경고: OPENAI_API_KEY가 설정되지 않았습니다!")
        print("먼저 setup_colab.py를 실행하여 API 키를 등록하세요.\n")
        return
    
    # 1. 기존 프로세스 정리
    kill_existing_processes()
    
    # 2. Streamlit 앱 시작
    start_streamlit()
    
    # 3. ngrok 터널 생성
    public_url = create_ngrok_tunnel()
    
    return public_url

if __name__ == "__main__":
    main()
