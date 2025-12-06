
import os
import glob
from pathlib import Path
import streamlit as st
import re

# 필수 패키지 로드
try:
    # from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    # from langchain.prompts import ChatPromptTemplate
    # from langchain.schema.output_parser import StrOutputParser
    # from langchain_community.document_loaders import TextLoader
    # from langchain_text_splitters import RecursiveCharacterTextSplitter
    # from langchain_community.vectorstores import Chroma
    # LangChain (수정된 버전)
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_core.prompts import ChatPromptTemplate              
    from langchain_core.output_parsers import StrOutputParser          
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
except ImportError as e:
    st.error(f"필요한 패키지를 설치해주세요: {e}")
    st.stop()

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(page_title="항공권 환불 상담 RAG 챗봇", layout="wide")
st.title("✈️ 여행 취소·환불 상담 챗봇")
st.markdown("### 🧳 아 몰랑~ 환불해줘~")

# ==========================================
# 상수 정의
# ==========================================

# 한영 동의어 매핑 (검색 개선용)
SYNONYM_DICT = {
    # 노쇼 관련
    "노쇼": ["노쇼", "No-Show", "no-show", "노 쇼", "미탑승", "예약부도"],
    "no-show": ["노쇼", "No-Show", "no-show", "미탑승", "예약부도"],

    # 환불 관련
    "환불": ["환불", "refund", "반환", "취소환불"],
    "refund": ["환불", "refund", "반환"],

    # 변경 관련
    "변경": ["변경", "change", "수정", "교환"],
    "change": ["변경", "change", "수정"],

    # 수수료 관련
    "수수료": ["수수료", "fee", "요금", "비용", "charge", "위약금", "패널티", "penalty"],
    "fee": ["수수료", "fee", "요금", "비용", "charge", "위약금", "패널티", "penalty"],
    "위약금": ["위약금", "패널티", "penalty", "수수료", "fee"],

    # 취소 관련
    "취소": ["취소", "cancel", "cancellation", "해지"],
    "cancel": ["취소", "cancel", "cancellation"],

    # 운임 종류 (이스타항공, 아시아나 등)
    "특가": ["특가", "특가운임", "프로모션", "promotion", "special"],
    "특가운임": ["특가", "특가운임", "프로모션", "special fare"],
    "할인": ["할인", "할인운임", "discount", "세일", "sale"],
    "할인운임": ["할인", "할인운임", "discount fare"],
    "일반": ["일반", "일반운임", "정상", "정상운임", "normal", "regular"],
    "일반운임": ["일반", "일반운임", "정상운임", "regular fare"],

    # 운임 등급 (제주항공, 대한항공 등)
    "베이직": ["베이직", "BASIC", "Basic", "basic"],
    "basic": ["베이직", "BASIC", "Basic"],
    "스탠다드": ["스탠다드", "STANDARD", "Standard", "standard"],
    "standard": ["스탠다드", "STANDARD", "Standard"],
    "플렉스": ["플렉스", "FLEX", "Flex", "flex", "flexible"],
    "flex": ["플렉스", "FLEX", "Flex", "flexible"],
    "세이버": ["세이버", "SAVER", "Saver", "saver"],
    "saver": ["세이버", "SAVER", "Saver"],

    # 노선 관련
    "국내선": ["국내선", "domestic", "국내"],
    "domestic": ["국내선", "domestic"],
    "국제선": ["국제선", "international", "국제", "해외", "외국"],
    "international": ["국제선", "international"],

    # 탑승수속 관련
    "탑승수속": ["탑승수속", "체크인", "check-in", "수속"],
    "체크인": ["탑승수속", "체크인", "check-in"],

    # Gate No-Show 관련
    "게이트": ["게이트", "gate", "출구장"],
    "출구장": ["게이트", "gate", "출구장"],

    # 미탑승 세분화
    "미탑승": ["미탑승", "no-show", "미승선", "불탑승"]
}


# 항공사 매핑 (파일명 → 표준명)
AIRLINE_MAPPING = {
    "대한항공": "대한항공",
    "koreanair": "대한항공",
    "korean": "대한항공",
    "제주항공": "제주항공",
    "jejuair": "제주항공",
    "jeju": "제주항공",
    "아시아나": "아시아나",
    "asiana": "아시아나",
    "진에어": "진에어",
    "jinair": "진에어",
    "jin": "진에어",
    "티웨이": "티웨이",
    "twayair": "티웨이",
    "tway": "티웨이",
    "에어서울": "에어서울",
    "airseoul": "에어서울",
    "이스타항공": "이스타항공",
    "이스타": "이스타항공",
    "eastar": "이스타항공",
}

# 항공사 키워드 (질문에서 추출용)
AIRLINE_KEYWORDS = {
    "대한항공": ["대한항공", "대한", "koreanair", "korean air", "kal"],
    "제주항공": ["제주항공", "제주", "jejuair", "jeju air"],
    "아시아나": ["아시아나", "asiana"],
    "진에어": ["진에어", "진 에어", "jinair", "jin air", "진"],
    "티웨이": ["티웨이", "티웨이항공", "twayair", "tway", "tway air"],
    "에어서울": ["에어서울", "airseoul", "air seoul"],
    "이스타항공": ["이스타", "이스타항공", "eastar", "eastar jet"],
}

# RAG 라우팅 키워드 (대폭 확장)
RAG_KEYWORDS = [
    # === 환불/취소 관련 ===
    "환불", "불환", "반환", "돌려", "돌려받", "리펀", "refund",
    "취소", "캔슬", "cancel", "cancellation", "해지", "철회",
    "부분환불", "전액환불", "일부환불",

    # === 변경 관련 ===
    "변경", "수정", "교환", "바꾸", "바꿔", "change", "modify", "modification",
    "일정변경", "날짜변경", "시간변경", "편명변경", "경로변경",
    "재발권", "리이슈", "reissue",

    # === 수수료 관련 ===
    "수수료", "fee", "charge", "비용", "요금", "가격", "금액",
    "위약금", "패널티", "penalty", "벌금",
    "변경수수료", "환불수수료", "취소수수료", "재발권수수료",
    "무료", "공짜", "꽁짜", "꽁자", "꽁자", "free", "면제",

    # === 항공권/티켓 관련 ===
    "항공권", "티켓", "ticket", "표", "비행기표", "항공", "항공편",
    "편명", "좌석", "seat", "booking", "예약",

    # === 운임 등급 ===
    "운임", "fare", "등급", "클래스", "class",

    # 기본 운임 등급 (제주항공, 대한항공 등)
    "flex", "flexible", "플렉스", "플렉시블",
    "standard", "스탠다드",
    "saver", "세이버", "save",
    "basic", "베이직", "베이식",

    # 이스타항공/아시아나 운임 종류
    "특가", "특가운임", "프로모션", "promotion", "special",
    "할인", "할인운임", "discount", "세일",
    "일반", "일반운임", "정상", "정상운임", "regular", "normal",

    # 좌석 등급
    "premium", "프리미엄", "비즈", "biz", "business",
    "이코노미", "economy", "일반석", "비즈니스석", "일등석", "퍼스트",

    # === 노선 구분 ===
    "국내선", "국내", "domestic", "도메스틱",
    "국제선", "국제", "international", "인터내셔널", "해외", "외국"
    "단거리", "중거리", "장거리", "short", "medium", "long",

    # === 노쇼 관련 ===
    "노쇼", "no-show", "noshow", "미탑승", "미승선", "불탑승",
    "미취소", "미출현", "불출석", "예약부도",
    "게이트", "gate", "출구장", "탑승구",
    "탑승수속", "체크인", "check-in", "수속",

    # === 기간/시간 관련 ===
    "기간", "기한", "유효", "유효기간", "validity", "만료",
    "출발", "출발일", "출발전", "출발후", "departure",
    "당일", "오늘", "며칠", "몇일", "며칠전", "일전", "전",
    "이전", "이후", "before", "after",
    "91일", "90일", "60일", "15일", "14일", "4일", "3일",

    # === 규정/정책 관련 ===
    "규정", "정책", "policy", "약관", "조건", "규칙", "rule",
    "가능", "불가", "가능한", "안되", "되나", "할수있", "할수없",

    # === 항공사명 ===
    "대한항공", "아시아나", "제주항공", "진에어", "티웨이",
    "korean", "koreanair", "asiana", "jeju", "jejuair", "jin", "jinair", "tway",

    # === 질문 키워드 ===
    "언제", "when", "얼마", "how much", "어디", "where",
    "무엇", "what", "왜", "why",
    "가능해", "되나요", "인가요", "한가요", "나요",
]

# ==========================================
# 유틸리티 함수
# ==========================================

def expand_query_with_synonyms(query: str) -> str:
    """
    검색 쿼리에 동의어를 추가하여 확장
    예: "노쇼 수수료" → "노쇼 No-Show 미탑승 수수료 fee 위약금"
    """
    expanded_terms = []
    words = query.split()

    for word in words:
        word_lower = word.lower()
        # 원본 단어 추가
        expanded_terms.append(word)

        # 동의어 사전에서 찾기
        if word_lower in SYNONYM_DICT:
            synonyms = SYNONYM_DICT[word_lower]
            for syn in synonyms:
                if syn.lower() != word_lower:
                    expanded_terms.append(syn)

    # 중복 제거 후 반환
    return " ".join(dict.fromkeys(expanded_terms))


def extract_airline_name(filepath: str) -> str:
    """파일명에서 항공사명을 정확하게 추출"""
    filename = Path(filepath).stem.lower()

    for key, value in AIRLINE_MAPPING.items():
        if key.lower() in filename:
            return value

    # 매핑에 없으면 파일명 그대로 사용
    return Path(filepath).stem


def extract_airline_from_query(q: str) -> list:
    """질문에서 항공사명 추출"""
    airlines = []
    q_lower = q.lower()

    for airline, keywords in AIRLINE_KEYWORDS.items():
        if any(kw in q_lower for kw in keywords):
            airlines.append(airline)

    return airlines


def route_to_rag(q: str) -> bool:
    """질문이 RAG가 필요한지 판단"""
    q_lower = q.lower()
    return any(kw.lower() in q_lower for kw in RAG_KEYWORDS)


def get_history_text(n_turns=6):
    """최근 n_turns 개의 대화만 반환"""
    hist = st.session_state["history"][-n_turns:]
    lines = []
    for role, content in hist:
        prefix = "사용자" if role == "user" else "어시스턴트"
        lines.append(f"{prefix}: {content}")
    return "\n".join(lines) if lines else "대화이력 없음"


# ==========================================
# 사이드바 설정
# ==========================================
with st.sidebar:
    st.header("📚 사이드바 옵션")
    k = st.slider("검색 개수 k", 1, 10, 5, help="RAG 검색시 가져올 문서 수")
    similarity_threshold = st.slider(
        "유사도 임계값",
        0.0, 1.0, 0.3, 0.05,
        help="이 값 이상의 유사도를 가진 문서만 사용"
    )

    show_sources = st.checkbox("근거(소스)표시", value=True)
    show_debug = st.checkbox("디버그 정보 표시", value=False)

    st.divider()

    # ==========================================
    # 필터 검색 UI (신규 추가)
    # ==========================================
    st.header("🔍 필터 검색")
    st.markdown("원하는 조건을 선택하고 검색 버튼을 눌러주세요")

    filter_airline = st.selectbox(
        "항공사",
        ["선택안함", "대한항공", "제주항공", "진에어", "아시아나", "티웨이", "에어서울"],
        help="항공사를 선택하세요"
    )

    filter_route = st.selectbox(
        "노선",
        ["선택안함", "국제선", "국내선"],
        help="국제선 또는 국내선을 선택하세요"
    )

    filter_seat = st.selectbox(
        "좌석 등급",
        ["선택안함", "일반석", "비즈니스석", "프리미엄이코노미"],
        help="좌석 등급을 선택하세요"
    )

    filter_regulation = st.selectbox(
        "규정 종류",
        ["선택안함", "환불", "변경", "노쇼", "취소"],
        help="알고 싶은 규정을 선택하세요"
    )

    # 필터 검색 버튼
    if st.button("🔍 필터로 검색", type="primary", use_container_width=True, key="filter_search_btn"):
        # 필터 값 수집
        filter_parts = []
        if filter_airline != "선택안함":
            filter_parts.append(filter_airline)
        if filter_route != "선택안함":
            filter_parts.append(filter_route)
        if filter_seat != "선택안함":
            filter_parts.append(filter_seat)
        if filter_regulation != "선택안함":
            filter_parts.append(filter_regulation)

        if filter_parts:
            # 필터를 자연어 쿼리로 변환
            filter_query = " ".join(filter_parts)
            # 세션에 저장하여 메인 로직에서 처리
            st.session_state["filter_query"] = filter_query
            st.session_state["filter_display"] = " > ".join(filter_parts)
            st.rerun()
        else:
            st.warning("⚠️ 최소 하나 이상의 필터를 선택해주세요")

    st.divider()

    st.header("❓ 예시 질문")
    example_questions = [
        "제주항공 국제선 변경 수수료는 얼마인가요?",
        "대한항공 국제선 환불 수수료는 얼마인가요?",
        "진에어 국제선 노쇼 위약금은?",
        "아시아나 국제선 탑승수속 후 미탑승 위약금",
        "대한항공 일반석 환불 수수료",
    ]
    for q_example in example_questions:
        if st.button(q_example, key=q_example, use_container_width=True):
            st.session_state["example_query"] = q_example

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("새로운 대화 시작", use_container_width=True):
        st.session_state.pop("messages", None)
        st.session_state.pop("history", None)
        st.session_state.pop("filter_query", None)
        st.session_state.pop("filter_display", None)
        st.cache_resource.clear()
        st.rerun()
    if c2.button("메모리 초기화", use_container_width=True):
        st.session_state.pop("history", None)
        st.success("메모리가 초기화되었습니다.")

# ==========================================
# 세션 초기화
# ==========================================
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []
if "example_query" not in st.session_state:
    st.session_state["example_query"] = None

# ==========================================
# OpenAI API 키 확인
# ==========================================
if "OPENAI_API_KEY" not in os.environ:
    st.warning("⚠️ OpenAI API 키를 설정해주세요!")
    api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API 키가 설정되었습니다!")
        st.rerun()
    else:
        st.stop()

# ==========================================
# LLM 및 프롬프트 구성
# ==========================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# RAG 프롬프트 (개선 - 표 형식 출력 강화)
rag_prompt = ChatPromptTemplate.from_template(
    """
너는 항공권 환불 및 변경을 도와주는 친절한 한국어 상담 챗봇이야.
아래 항공사 정책 문서를 참고해서 질문에 정확하고 친절하게 답변해줘.

⚠️ 중요: 사용자의 질문을 정확히 이해하고, 가장 관련성 높은 규정을 찾아서 답변해줘.
- "탑승수속 후 미탑승" ≠ "Gate No-Show" (출구장 입장 후)
- "미취소 후 미탑승" ≠ "탑승수속 후 미탑승"
각 상황에 맞는 정확한 규정을 제시해줘.

최근 대화:
{history}

참고 정책 문서:
{context}

사용자 질문: {q}

📋 **답변 형식 규칙 (매우 중요!)**:

🚫 **절대 금지 사항**:
- title:, airline:, language:, note: 같은 메타데이터 절대 출력 금지
- 원본 MD 문서를 그대로 복사 붙여넣기 금지
- 문서 원문의 title, note, language 등 메타 정보 출력 금지

✅ **필수 출력 형식**:

**1️⃣ 제목 (## 형식)**
```
## [항공사명] [좌석등급] [규정종류] ([노선] 기준)
예: ## 대한항공 일반석 환불 수수료 (한국 출발 국제선 기준)
```

**2️⃣ 표 형식 데이터 (Markdown 표로 완전히 변환)**
- 문서에 표가 있으면 **반드시 깔끔한 Markdown 표로 재구성**
- 단거리/중거리/장거리가 있으면 **각각 ### 소제목과 별도 표로 출력**
- 모든 행과 열을 **완전히** 포함 (생략 절대 금지)

**표 출력 예시**:
```markdown
### 단거리 일반석
| 출발 기준 | FLEX (B,M) | Standard (S,H,E,K,L,U,Q,T) | Saver (L,U,Q,T) |
|---|---:|---:|---:|
| 91일 이상 | 무료 | 무료 | 무료 |
| 90~61일 | 30,000원 | 30,000원 | 60,000원 |
| 60~31일 | 50,000원 | 50,000원 | 80,000원 |
| 30~15일 | 60,000원 | 60,000원 | 100,000원 |
| 14~4일 | 70,000원 | 70,000원 | 전액 환불 불가 |
| 3일~출발 | 80,000원 | 80,000원 | 전액 환불 불가 |

### 중거리 일반석
| 출발 기준 | FLEX | Standard | Saver |
|---|---:|---:|---:|
| 91일 이상 | 무료 | 무료 | 무료 |
| 90~61일 | 40,000원 | 40,000원 | 80,000원 |
...

### 장거리 일반석
| 출발 기준 | FLEX (B,M,W) | Standard | Saver |
|---|---:|---:|---:|
| 91일 이상 | 무료 | 무료 | - |
...
```

**3️⃣ 주요 사항 정리 (핵심 포인트 3-5개)**
```markdown
**주요 사항**:
- 91일 이상 전 취소 시 FLEX/Standard는 무료 환불
- Saver 운임은 출발 14일 전부터 전액 환불 불가
- 장거리 노선은 Saver 운임이 없음
- 출발일에 가까울수록 환불 수수료가 증가
```

**4️⃣ 안내 문구 (필수)**
```markdown
⚠️ 정확한 정보는 해당 항공사 공식 웹사이트를 확인해주세요.
```

⚠️ **체크리스트 (모두 만족해야 함)**:
- [ ] 메타데이터(title, note, language, airline) 완전히 제거됨?
- [ ] 표가 완전한 Markdown 형식으로 변환됨?
- [ ] 단거리/중거리/장거리 각각 별도 표로 출력됨?
- [ ] 모든 운임 등급(FLEX, Standard, Saver 등) 포함됨?
- [ ] 모든 기간(91일 이상, 90~61일 등) 포함됨?
- [ ] 주요 사항이 정리됨?
- [ ] 안내 문구가 포함됨?

답변:
"""
)
rag_chain = rag_prompt | llm | StrOutputParser()

# 일반 대화 프롬프트
base_prompt = ChatPromptTemplate.from_template(
    """
너는 항공권 환불 및 변경을 도와주는 친절한 한국어 상담 챗봇이야.
항공권 환불/취소와 관련 없는 질문이면 정중히 안내하고, 환불 관련 질문을 유도해줘.

최근 대화:
{history}

사용자: {q}

답변:
"""
)
base_chain = base_prompt | llm | StrOutputParser()

# ==========================================
# 벡터 DB 초기화
# ==========================================
@st.cache_resource
def initialize_vectordb():
    """MD 파일들을 로드하고 벡터 DB를 생성"""

    # 파일 패턴
    patterns = [
        # "/content/data/airlines_md/*.md",
        # "./data/airlines_md/*.md",
        "data/airlines_md/*.md",
    ]

    seen = set()
    loader_files = []

    for pat in patterns:
        for fp in glob.glob(pat, recursive=True):
            if fp.endswith(".md") and fp not in seen and Path(fp).is_file():
                seen.add(fp)
                loader_files.append(fp)

    # 로드 결과 표시
    st.caption(f"📄 로드된 MD 파일 수: {len(loader_files)}")
    if loader_files:
        with st.expander("📂 로드된 파일 목록", expanded=True):
            for fp in loader_files:
                airline = extract_airline_name(fp)
                st.text(f"{airline}: {fp}")

    if not loader_files:
        st.error("❌ MD 파일을 찾지 못했습니다.")
        st.info("""
        💡 **해결 방법:**
        - 코랩: `/content/data/airlines_md/` 폴더에 MD 파일 업로드
        - 로컬: `./data/airlines_md/` 폴더에 MD 파일 저장
        """)
        st.stop()

    # 문서 로딩
    all_docs = []
    airline_set = set()

    for fp in loader_files:
        try:
            docs = TextLoader(fp, encoding="utf-8").load()
        except Exception as e:
            st.warning(f"⚠️ 로드 실패: {fp} ({e})")
            continue

        airline_tag = extract_airline_name(fp)
        airline_set.add(airline_tag)

        for d in docs:
            if not d.page_content or not d.page_content.strip():
                continue
            d.metadata["airline"] = airline_tag
            d.metadata["source_path"] = fp
            d.metadata["filename"] = Path(fp).name
            all_docs.append(d)

    if not all_docs:
        st.error("❌ 문서를 로드했지만 내용이 비어 있습니다.")
        st.stop()

    # 청크 분할 (표 보존을 위해 크기 증가)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # 표를 포함하도록 크기 증가
        chunk_overlap=400,  # 오버랩 증가
        separators=[
            "\n\n## ",
            "\n\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )
    chunks = splitter.split_documents(all_docs)

    if not chunks:
        st.error("❌ 청크 분할 결과가 비었습니다.")
        st.stop()

    # 임베딩 및 벡터 DB 생성
    emb = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma.from_documents(chunks, emb)

    st.success(f"✅ 인덱싱 완료: 문서 {len(all_docs)}건, 청크 {len(chunks)}건")

    # 항공사 목록 저장
    st.session_state["available_airlines"] = sorted(list(airline_set))

    return db

# 벡터 DB 초기화
db = initialize_vectordb()

# 항공사 정보 표시
if "available_airlines" in st.session_state:
    with st.sidebar:
        st.info(f"🏢 사용 가능한 항공사: {', '.join(st.session_state['available_airlines'])}")

# ==========================================
# RAG 답변 생성 (최적화 버전)
# ==========================================
def refund_rag(q, k_override=None, threshold=None):
    """
    RAG를 사용한 답변 생성 (최적화)
    - 한영 동의어 확장 지원
    - 항공사 필터링 강화
    - 표 데이터 최적화
    - 명확한 에러 처리
    """
    kk = k_override if k_override is not None else k
    th = threshold if threshold is not None else similarity_threshold

    try:
        # 1️⃣ 질문 분석
        query_airlines = extract_airline_from_query(q)
        expanded_query = expand_query_with_synonyms(q)

        # 2️⃣ 검색 쿼리 구성 (항공사명 가중치 증가)
        if query_airlines:
            # 항공사명을 2번 반복하여 가중치 증가
            search_query = f"{' '.join(query_airlines)} {' '.join(query_airlines)} {expanded_query}"
        else:
            search_query = expanded_query

        # 3️⃣ 검색 개수 동적 조정
        is_table_query = any(kw in q for kw in ["수수료", "위약금", "요금", "비용", "환불", "변경", "취소"])
        search_k = kk * 3 if is_table_query else kk * 2

        # 4️⃣ 디버그 정보 출력
        if show_debug:
            st.info(f"🔍 원본 쿼리: `{q}`")
            st.info(f"🔍 확장된 쿼리: `{expanded_query}`")
            st.info(f"🏢 감지된 항공사: {', '.join(query_airlines) if query_airlines else '없음'}")
            st.info(f"📊 검색 개수: {search_k} (표 데이터: {'예' if is_table_query else '아니오'})")

        # 5️⃣ 벡터 DB 검색
        all_results = db.similarity_search_with_relevance_scores(search_query, k=search_k)

        # 6️⃣ 항공사 필터링 (명시된 경우 강제 적용)
        if query_airlines:
            filtered_results = []
            for d, score in all_results:
                doc_airline = d.metadata.get('airline', '')
                if any(qa in doc_airline for qa in query_airlines):
                    # 항공사 지정 시 임계값 완화 (20% 낮춤)
                    relaxed_threshold = th * 0.8
                    if score >= relaxed_threshold:
                        filtered_results.append((d, score))

            # 필터링 결과 확인
            if not filtered_results:
                missing_airlines = ', '.join(query_airlines)
                error_msg = f"""
❌ **{missing_airlines}** 항공사의 관련 규정을 찾을 수 없습니다.

**확인 사항:**
1. 로드된 항공사 목록을 확인해주세요 (사이드바 참조)
2. 항공사명 표기를 확인해주세요:
   - "진에어" / "JIN AIR"
   - "아시아나" / "ASIANA"
   - "대한항공" / "KOREAN AIR"

**해결 방법:**
- 유사도 임계값을 낮춰보세요 (현재: {th:.2f} → 권장: 0.2~0.3)
- 항공사명을 생략하고 검색해보세요 (예: "국제선 노쇼 위약금")
- 디버그 모드를 켜서 전체 검색 결과를 확인해보세요
"""
                if show_debug:
                    st.warning("🔍 전체 검색 결과 (필터링 전):")
                    for i, (d, score) in enumerate(all_results[:10], 1):
                        airline = d.metadata.get('airline', '알 수 없음')
                        st.write(f"[{i}] **{airline}** - 유사도: {score:.3f}")

                return error_msg, []

            results = filtered_results[:kk]
        else:
            # 항공사 미지정 시 일반 임계값 적용
            results = [(d, score) for d, score in all_results if score >= th]
            results = results[:kk]

        # 7️⃣ 최종 결과 검증
        if not results:
            fallback_msg = f"""
관련 규정을 찾지 못했습니다. 😥

**시도한 검색어:** `{expanded_query}`

**가능한 원인:**
- 유사도 임계값({th:.2f})이 너무 높습니다
- 질문이 너무 추상적이거나 문서에 없는 내용입니다

**해결 방법:**
1. 유사도 임계값을 **0.2~0.3**으로 낮춰보세요
2. 질문을 더 구체적으로 작성해보세요
   - 좋은 예: "제주항공 국제선 BASIC 운임 출발 3일 전 변경 수수료"
3. 항공사명을 명확히 해주세요
"""
            return fallback_msg, []

        # 8️⃣ 컨텍스트 구성 (중복 제거)
        context_parts = []
        seen_content = set()

        for d, score in results:
            content = d.page_content
            if content in seen_content:
                continue
            seen_content.add(content)

            airline = d.metadata.get('airline', '알 수 없음')
            context_parts.append(f"[{airline} 규정 | 유사도: {score:.2f}]\n{content}")

        context = "\n\n" + "="*50 + "\n\n".join(context_parts)
        history_text = get_history_text()

        # 9️⃣ LLM 호출
        answer = rag_chain.invoke({
            "history": history_text,
            "context": context,
            "q": q
        })

        # 🔟 소스 정보 생성
        sources = []
        for d, score in results:
            airline = d.metadata.get('airline', '알 수 없음')
            filename = d.metadata.get('filename', '알 수 없음')
            preview = d.page_content[:300].replace('\n', ' ')
            sources.append({
                "airline": airline,
                "filename": filename,
                "score": score,
                "content": preview,
                "full_content": d.page_content
            })

        return answer, sources

    except Exception as e:
        error_msg = f"❌ RAG 처리 중 오류 발생: {str(e)}"
        st.error(error_msg)
        import traceback
        if show_debug:
            st.error(f"상세 오류:\n```\n{traceback.format_exc()}\n```")
        return error_msg, []

# ==========================================
# 채팅 UI
# ==========================================
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ==========================================
# 필터 검색 처리 (신규 추가)
# ==========================================
if st.session_state.get("filter_query"):
    filter_query = st.session_state.pop("filter_query")
    filter_display = st.session_state.pop("filter_display")

    # 사용자 메시지로 필터 정보 표시
    user_message = f"**현재 적용된 필터**: {filter_display}"
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state["messages"].append({"role": "user", "content": user_message})
    st.session_state["history"].append(("user", user_message))

    # RAG로 검색하여 LLM 답변 생성
    with st.chat_message("assistant"):
        try:
            with st.spinner("🔍 필터 조건에 맞는 규정을 검색 중..."):
                ans, sources = refund_rag(filter_query, k_override=k)

            st.markdown(ans)
            st.success("✅ 항공권 환불 규정을 기반으로 답변되었습니다.")

            # 디버그 정보
            if show_debug and sources:
                with st.expander("🐛 디버그 정보", expanded=False):
                    st.write(f"필터 쿼리: {filter_query}")
                    st.write(f"검색된 청크 수: {len(sources)}")
                    st.write(f"유사도 임계값: {similarity_threshold}")
                    for i, src in enumerate(sources, 1):
                        st.write(f"**[{i}] {src['airline']}** ({src['filename']}) - 유사도: {src['score']:.3f}")

            # 참고 근거
            if show_sources and sources:
                with st.expander("🔍 참고 근거 문서 보기", expanded=False):
                    for i, src in enumerate(sources, 1):
                        st.markdown(f"### 📋 [{i}] {src['airline']} (유사도: {src['score']:.2f})")
                        st.markdown(f"**파일**: `{src['filename']}`")
                        st.markdown(f"```\n{src['content'][:500]}...\n```")

                        if st.checkbox(f"전체 내용 보기 [{i}]", key=f"full_filter_{i}"):
                            st.text_area(
                                "전체 내용",
                                src['full_content'],
                                height=300,
                                key=f"full_filter_text_{i}"
                            )
                        st.markdown("---")

        except Exception as e:
            error_message = f"❌ 필터 검색 중 오류가 발생했습니다: {str(e)}"
            st.error(error_message)
            ans = error_message

    # 메시지 저장
    st.session_state["messages"].append({"role": "assistant", "content": ans})
    st.session_state["history"].append(("assistant", ans))

# ==========================================
# 일반 채팅 입력 처리
# ==========================================
# 입력 처리
user_input = None
if st.session_state.get("example_query"):
    user_input = st.session_state["example_query"]
    st.session_state["example_query"] = None
else:
    user_input = st.chat_input("항공권 환불/변경에 대해 질문해주세요 (예: '진에어 노쇼 위약금은?')")

if user_input:
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["history"].append(("user", user_input))

    # 히스토리 길이 제한
    if len(st.session_state["history"]) > 20:
        st.session_state["history"] = st.session_state["history"][-20:]

    # RAG 라우팅
    use_rag = route_to_rag(user_input)

    # 어시스턴트 응답
    with st.chat_message("assistant"):
        try:
            if use_rag:
                # RAG 답변
                with st.spinner("🔍 관련 정보를 검색하는 중..."):
                    ans, sources = refund_rag(user_input, k_override=k)

                st.markdown(ans)
                st.success("✅ 항공권 환불 규정을 기반으로 답변되었습니다.")

                # 디버그 정보
                if show_debug and sources:
                    with st.expander("🐛 디버그 정보", expanded=False):
                        st.write(f"검색된 청크 수: {len(sources)}")
                        st.write(f"유사도 임계값: {similarity_threshold}")
                        detected_airlines = extract_airline_from_query(user_input)
                        if detected_airlines:
                            st.write(f"감지된 항공사: {', '.join(detected_airlines)}")
                        for i, src in enumerate(sources, 1):
                            st.write(f"**[{i}] {src['airline']}** ({src['filename']}) - 유사도: {src['score']:.3f}")

                # 참고 근거
                if show_sources and sources:
                    with st.expander("🔍 참고 근거 문서 보기", expanded=False):
                        for i, src in enumerate(sources, 1):
                            st.markdown(f"### 📋 [{i}] {src['airline']} (유사도: {src['score']:.2f})")
                            st.markdown(f"**파일**: `{src['filename']}`")
                            st.markdown(f"```\n{src['content']}...\n```")

                            if st.checkbox(f"전체 내용 보기 [{i}]", key=f"full_{i}"):
                                st.text_area(
                                    "전체 내용",
                                    src['full_content'],
                                    height=300,
                                    key=f"full_text_{i}"
                                )
                            st.markdown("---")
            else:
                # 일반 대화
                history_text = get_history_text()
                with st.spinner("💬 답변 생성 중..."):
                    ans = base_chain.invoke({"history": history_text, "q": user_input})

                st.markdown(ans)
                st.info("💬 일반 대화로 답변되었습니다. 환불/취소 관련 질문은 자동으로 규정을 검색합니다.")

        except Exception as e:
            error_message = f"❌ 답변 생성 중 오류가 발생했습니다: {str(e)}"
            st.error(error_message)
            ans = error_message

    # 메시지 저장
    st.session_state["messages"].append({"role": "assistant", "content": ans})
    st.session_state["history"].append(("assistant", ans))

# ==========================================
# 하단 안내 및 푸터
# ==========================================
st.markdown("---")
st.caption("⚠️ 본 챗봇은 참고용이며, 정확한 정보는 항공사 공식 웹사이트 또는 고객센터를 통해 확인해주세요.")

with st.expander("ℹ️ 사용 가이드", expanded=False):
    st.markdown("""
    ### 💡 사용 팁

    1. **항공사명을 명확히 명시하세요**
       - ❌ "변경 수수료는?"
       - ✅ "제주항공 국제선 변경 수수료는?"

    2. **구체적으로 질문하세요**
       - ❌ "환불 되나요?"
       - ✅ "제주항공 BASIC 운임 출발 5일 전 변경 수수료는?"

    3. **유사도 임계값 조정**
       - 답변이 없다면 임계값을 **0.2~0.3**으로 낮춰보세요

    4. **근거 문서 확인**
       - "근거(소스)표시" 옵션으로 참고 규정 확인 가능

    5. **디버그 모드 활용**
       - 검색 과정을 상세히 확인하고 싶을 때 활성화

    6. **한영 혼용 검색 지원**
       - "노쇼" → "No-Show"로 자동 확장
       - "환불" → "refund"로 자동 확장
    """)
