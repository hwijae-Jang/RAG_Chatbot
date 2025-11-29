# ✈️ 항공권 환불 상담 RAG 챗봇

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Contributors](https://img.shields.io/github/contributors/your-username/airline-refund-chatbot)
![Issues](https://img.shields.io/github/issues/your-username/airline-refund-chatbot)
![Stars](https://img.shields.io/github/stars/your-username/airline-refund-chatbot)

### **"아 몰랑~ 환불해줘~"**

**복잡한 항공권 환불 규정, AI가 쉽게 알려드립니다**

[데모 보기](#-데모) · [빠른 시작](#-빠른-시작) · [기여하기](CONTRIBUTING.md) · [문제 신고](https://github.com/your-username/airline-refund-chatbot/issues)

</div>

---

## 📖 목차

- [프로젝트 소개](#-프로젝트-소개)
  - [개발 동기](#-개발-동기)
  - [주요 기능](#-주요-기능)
  - [해결하는 문제](#-해결하는-문제)
  - [기술 스택](#-기술-스택)
- [데모](#-데모)
- [빠른 시작](#-빠른-시작)
  - [사전 요구사항](#사전-요구사항)
  - [설치 방법](#설치-방법)
  - [실행 방법](#실행-방법)
- [사용 방법](#-사용-방법)
- [프로젝트 구조](#-프로젝트-구조)
- [기여하기](#-기여하기)
- [라이센스](#-라이센스)
- [팀원](#-팀원)
- [문의하기](#-문의하기)

---

## 🎯 프로젝트 소개

### 🤔 개발 동기

항공권을 취소하거나 변경할 때 항공사마다 다른 복잡한 규정 때문에 고객들이 어려움을 겪는 경우가 많습니다. 특히 노쇼(No-Show) 위약금, 운임별 환불 조건, 변경 수수료 등은 항공사 웹사이트를 일일이 찾아봐도 이해하기 어렵습니다.

**이런 문제를 해결하고자 이 프로젝트를 시작했습니다.**

### ✨ 주요 기능

- **🔍 지능형 검색**: RAG(Retrieval-Augmented Generation) 기술로 정확한 정보 제공
- **🏢 다중 항공사 지원**: 대한항공, 제주항공, 아시아나, 진에어, 티웨이, 에어서울, 이스타항공
- **🌐 한영 자동 번역**: "노쇼"↔"No-Show", "환불"↔"refund" 자동 매칭
- **🎛️ 고급 필터**: 항공사, 노선, 운임 등급별 맞춤 검색
- **📊 투명한 근거**: 답변의 출처와 유사도 점수 확인
- **💬 대화 기억**: 이전 대화를 기억하여 자연스러운 상담
- **🚀 간편한 배포**: Google Colab에서 즉시 실행 가능

### 💡 해결하는 문제

1. **정보 접근성**: 흩어진 항공사 규정을 한 곳에서 검색
2. **이해의 어려움**: 복잡한 약관을 쉬운 말로 설명
3. **시간 절약**: 고객센터 대기 없이 즉시 답변 제공
4. **정확성**: AI가 공식 규정 문서를 기반으로 답변

### 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **프론트엔드** | Streamlit |
| **백엔드** | Python 3.8+ |
| **LLM** | OpenAI GPT-4 / GPT-3.5 |
| **임베딩** | OpenAI text-embedding-ada-002 |
| **벡터 DB** | ChromaDB |
| **프레임워크** | LangChain |
| **배포** | ngrok (Google Colab) |

---

## 🎬 데모

### 실행 화면

<div align="center">

![챗봇 메인 화면](https://via.placeholder.com/800x400?text=챗봇+메인+화면)
*챗봇 메인 화면: 간단한 UI로 누구나 쉽게 사용 가능*

![질문 예시](https://via.placeholder.com/800x400?text=질문+예시)
*질문 예시: 항공사별 환불 규정을 정확하게 답변*

![근거 문서](https://via.placeholder.com/800x400?text=근거+문서+표시)
*근거 문서 표시: 답변의 출처를 명확히 확인*

</div>

### 실제 대화 예시

```
👤 사용자: "진에어 노쇼 위약금은 얼마인가요?"

🤖 챗봇: 
진에어의 노쇼(No-Show) 위약금은 다음과 같습니다:

**국내선:**
- 편도 기준: 30,000원
- 왕복 기준: 60,000원

**국제선:**
- 편도 기준: 50,000원
- 왕복 기준: 100,000원

노쇼는 탑승수속을 완료했으나 탑승하지 않은 경우에 적용됩니다.

✅ 참고 근거: 진에어 환불 규정 (유사도: 0.89)
```

---

## 🚀 빠른 시작

### 사전 요구사항

시작하기 전에 다음이 설치되어 있는지 확인하세요:

- **Python 3.8 이상** - [다운로드](https://www.python.org/downloads/)
- **Git** - [다운로드](https://git-scm.com/downloads)
- **OpenAI API 키** - [발급받기](https://platform.openai.com/api-keys)

### 설치 방법

#### 방법 1: 로컬 환경 (Windows/Mac/Linux)

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/airline-refund-chatbot.git
cd airline-refund-chatbot

# 2. 가상환경 생성 (권장)
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
# .env 파일을 만들고 다음 내용 추가:
# OPENAI_API_KEY=your_api_key_here

# 또는 .env.example 파일을 복사
cp .env.example .env
# 그리고 .env 파일에 실제 API 키 입력
```

#### 방법 2: Google Colab (설치 불필요!)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/airline-refund-chatbot/blob/main/Colab_실행가이드.ipynb)

1. 위 배지를 클릭하여 Colab 노트북 열기
2. 첫 번째 셀부터 순서대로 실행
3. API 키 입력 (안전한 방식으로 입력 요청)
4. 생성된 공개 URL로 접속

### 실행 방법

#### 로컬 환경

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 챗봇 사용 가능!

#### Google Colab

```python
# 노트북에서 마지막 셀 실행 후 생성된 ngrok URL 클릭
```

---

## 📱 사용 방법

### 기본 사용법

1. **챗봇 실행** 후 화면 하단의 입력창에 질문 입력
2. 항공사명을 **명확히** 포함하여 질문
3. 답변 확인 및 **근거 문서** 펼쳐보기

### 질문 예시

#### ✅ 좋은 질문 (구체적)
```
"제주항공 국제선 BASIC 운임 출발 3일 전 변경 수수료는?"
"대한항공 특가 항공권 환불 가능한가요?"
"진에어 노쇼 위약금 얼마인가요?"
```

#### ❌ 나쁜 질문 (모호함)
```
"환불 되나요?"
"수수료는?"
"노쇼가 뭐예요?"
```

### 고급 기능: 필터 검색

사이드바에서 조건을 설정하여 정확한 검색 가능:

1. **항공사 선택**: 특정 항공사만 검색
2. **노선 구분**: 국내선/국제선
3. **운임 등급**: FLEX, STANDARD, BASIC 등
4. **유사도 조정**: 답변이 없으면 0.2~0.3으로 낮추기

### 문제 해결

답변이 나오지 않나요?

1. 유사도 임계값을 **0.2~0.3**으로 낮추세요
2. 검색 청크 수(k)를 **7~10**으로 높이세요
3. 질문을 더 구체적으로 수정하세요
4. 디버그 모드를 활성화하여 검색 과정 확인

---

## 📂 프로젝트 구조

```
airline-refund-chatbot/
│
├── 📄 app.py                       # 메인 Streamlit 애플리케이션
├── 📄 requirements.txt             # Python 패키지 의존성
├── 📄 README.md                    # 프로젝트 문서 (이 파일)
├── 📄 LICENSE                      # MIT 라이선스
├── 📄 CONTRIBUTING.md              # 기여 가이드
├── 📄 SECURITY.md                  # 보안 가이드 ⚠️ 중요!
│
├── 🔧 .env                         # 환경 변수 (절대 커밋 금지!)
├── 🔧 .env.example                 # 환경 변수 템플릿
├── 🔧 .gitignore                   # Git 제외 파일 목록
│
├── 🐍 setup_colab.py               # Google Colab API 키 설정
├── 🐍 run_streamlit.py             # Google Colab 실행 스크립트
├── 📓 Colab_실행가이드.ipynb       # Google Colab 노트북
│
├── 📁 data/                        # 항공사 규정 문서
│   ├── 대한항공_환불규정.txt
│   ├── 제주항공_환불규정.txt
│   ├── 아시아나_환불규정.txt
│   ├── 진에어_환불규정.txt
│   ├── 티웨이_환불규정.txt
│   ├── 에어서울_환불규정.txt
│   └── 이스타항공_환불규정.txt
│
└── 📁 chroma_db/                   # ChromaDB 벡터 저장소 (자동 생성)
```

---

## 🤝 기여하기

프로젝트에 기여하고 싶으신가요? 언제든 환영합니다! 🎉

### 기여 방법

1. 이 저장소를 **Fork** 하세요
2. Feature 브랜치를 생성하세요 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋하세요 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 브랜치에 Push 하세요 (`git push origin feature/AmazingFeature`)
5. **Pull Request**를 생성하세요

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

### 기여 아이디어

- 🆕 새로운 항공사 규정 추가
- 🌍 다국어 지원 (영어, 일본어, 중국어)
- 📊 사용 통계 대시보드
- 🎨 UI/UX 개선
- 🧪 테스트 코드 작성
- 📝 문서 개선

### 커밋 메시지 컨벤션

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 및 설정
```

---

## 📜 라이센스

이 프로젝트는 **MIT 라이센스**를 따릅니다.

```
MIT License

Copyright (c) 2024 아몰랑환불해줘팀

이 소프트웨어를 누구나 무상으로 제한없이 사용할 수 있습니다.
자세한 내용은 LICENSE 파일을 참조하세요.
```

---

## 👥 팀원

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/member1">
        <img src="https://via.placeholder.com/100" width="100px;" alt=""/>
        <br />
        <sub><b>팀원 1</b></sub>
      </a>
      <br />
      <sub>프로젝트 리드</sub>
    </td>
    <td align="center">
      <a href="https://github.com/member2">
        <img src="https://via.placeholder.com/100" width="100px;" alt=""/>
        <br />
        <sub><b>팀원 2</b></sub>
      </a>
      <br />
      <sub>AI 개발</sub>
    </td>
    <td align="center">
      <a href="https://github.com/member3">
        <img src="https://via.placeholder.com/100" width="100px;" alt=""/>
        <br />
        <sub><b>팀원 3</b></sub>
      </a>
      <br />
      <sub>데이터 수집</sub>
    </td>
  </tr>
</table>

**팀명**: 아몰랑환불해줘팀

---

## 📞 문의하기

프로젝트에 대한 질문이나 제안이 있으신가요?

- 📧 **이메일**: your-email@example.com
- 🐛 **버그 리포트**: [Issues](https://github.com/your-username/airline-refund-chatbot/issues)
- 💬 **디스코드**: [프로젝트 서버](https://discord.gg/your-invite) (선택사항)
- 🐦 **트위터**: [@your_handle](https://twitter.com/your_handle)

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들의 도움을 받았습니다:

- [LangChain](https://python.langchain.com/) - LLM 애플리케이션 프레임워크
- [Streamlit](https://streamlit.io/) - 웹 앱 프레임워크
- [ChromaDB](https://www.trychroma.com/) - 벡터 데이터베이스
- [OpenAI](https://openai.com/) - GPT 모델 제공

---

## 📈 향후 계획

- [ ] 실시간 항공권 가격 조회 API 연동
- [ ] 카카오톡 챗봇 버전 개발
- [ ] 모바일 앱 (React Native)
- [ ] 음성 인식 질의응답 (STT/TTS)
- [ ] 항공사 공식 API 연동
- [ ] 예약 취소 자동화
- [ ] 환불 예상 금액 계산기

---

## ⚠️ 면책 조항

본 챗봇은 **참고용**으로 제공되며, 실제 환불 및 변경 정책은 각 항공사의 공식 웹사이트나 고객센터를 통해 확인하시기 바랍니다. 

본 서비스는 정보 제공 목적이며, **법적 구속력이 없습니다**.

---

<div align="center">

### Made with ❤️ by 아몰랑환불해줘팀

**항공권 환불, 이제 쉽게!** ✈️

[![GitHub stars](https://img.shields.io/github/stars/your-username/airline-refund-chatbot?style=social)](https://github.com/your-username/airline-refund-chatbot)
[![GitHub forks](https://img.shields.io/github/forks/your-username/airline-refund-chatbot?style=social)](https://github.com/your-username/airline-refund-chatbot/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/your-username/airline-refund-chatbot?style=social)](https://github.com/your-username/airline-refund-chatbot)

[⬆ 맨 위로 가기](#-항공권-환불-상담-rag-챗봇)

</div>
