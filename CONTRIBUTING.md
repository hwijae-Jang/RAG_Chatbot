# 기여 가이드 (Contributing Guide)

항공권 환불 상담 RAG 챗봇 프로젝트에 기여해주셔서 감사합니다! 🎉

## 🤝 기여 방법

### 1. 이슈 생성

버그를 발견하거나 새로운 기능을 제안하고 싶다면:

1. [Issues](https://github.com/your-username/airline-refund-chatbot/issues)로 이동
2. 기존 이슈를 먼저 검색하여 중복 확인
3. 새 이슈 생성 시 템플릿 선택:
   - 🐛 Bug Report (버그 리포트)
   - ✨ Feature Request (기능 제안)
   - 📝 Documentation (문서 개선)

### 2. Pull Request 제출

#### Step 1: Fork & Clone

```bash
# 1. GitHub에서 저장소 Fork
# 2. 로컬에 Clone
git clone https://github.com/YOUR-USERNAME/airline-refund-chatbot.git
cd airline-refund-chatbot
```

#### Step 2: 브랜치 생성

```bash
# 기능 추가
git checkout -b feature/amazing-feature

# 버그 수정
git checkout -b fix/bug-description

# 문서 개선
git checkout -b docs/update-readme
```

#### Step 3: 개발 환경 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 개발용 추가 패키지 (선택)
pip install pytest black flake8
```

#### Step 4: 변경사항 작성

- 코드 스타일 가이드를 따라주세요 (PEP 8)
- 주석을 명확하게 작성해주세요
- 기능 추가 시 테스트 코드도 함께 작성해주세요

#### Step 5: 커밋

```bash
git add .
git commit -m "feat: Add amazing feature"

# 커밋 메시지 컨벤션
# feat: 새로운 기능
# fix: 버그 수정
# docs: 문서 수정
# style: 코드 포맷팅
# refactor: 코드 리팩토링
# test: 테스트 코드
# chore: 빌드 및 설정
```

#### Step 6: Push & PR

```bash
git push origin feature/amazing-feature
```

GitHub에서 Pull Request를 생성하고 다음을 포함해주세요:
- 변경사항 설명
- 관련 이슈 번호 (#123)
- 테스트 결과 (해당하는 경우)

## 📋 코드 스타일 가이드

### Python 코드

```python
# Good ✅
def calculate_refund_fee(fare_type: str, days_before: int) -> int:
    """
    환불 수수료를 계산합니다.
    
    Args:
        fare_type: 운임 종류 (FLEX, STANDARD, BASIC)
        days_before: 출발일까지 남은 일수
    
    Returns:
        환불 수수료 (원)
    """
    if fare_type == "FLEX":
        return 0
    elif fare_type == "STANDARD":
        if days_before >= 91:
            return 3000
        return 10000
    return -1  # 환불 불가

# Bad ❌
def calc(t,d):
    if t=="FLEX":return 0
    elif t=="STANDARD":
        if d>=91:return 3000
        return 10000
    return -1
```

### 문서화

```python
# Good ✅
def expand_query_with_synonyms(query: str) -> str:
    """
    검색 쿼리에 동의어를 추가하여 확장합니다.
    
    예시:
        >>> expand_query_with_synonyms("노쇼 수수료")
        "노쇼 No-Show 미탑승 수수료 fee 위약금"
    
    Args:
        query: 원본 검색 쿼리
    
    Returns:
        동의어가 추가된 확장 쿼리
    """
    # 구현...
```

## 🧪 테스트

새로운 기능을 추가할 때는 테스트 코드를 함께 작성해주세요:

```python
# tests/test_utils.py
import pytest
from app import expand_query_with_synonyms

def test_expand_query_with_synonyms():
    """동의어 확장 테스트"""
    query = "노쇼 수수료"
    expanded = expand_query_with_synonyms(query)
    
    assert "노쇼" in expanded
    assert "No-Show" in expanded
    assert "수수료" in expanded
    assert "fee" in expanded

def test_extract_airline_from_query():
    """항공사 추출 테스트"""
    from app import extract_airline_from_query
    
    airlines = extract_airline_from_query("제주항공 환불 규정")
    assert "제주항공" in airlines
    
    airlines = extract_airline_from_query("koreanair refund policy")
    assert "대한항공" in airlines
```

테스트 실행:
```bash
pytest tests/
```

## 📝 기여 아이디어

### 🆕 새로운 항공사 추가

1. `data/` 폴더에 규정 문서 추가
2. `AIRLINE_MAPPING` 및 `AIRLINE_KEYWORDS` 업데이트
3. 테스트 케이스 작성
4. README.md 업데이트

### 🌍 다국어 지원

1. `locales/` 폴더 구조 설계
2. 번역 파일 작성 (en.json, ja.json 등)
3. i18n 라이브러리 통합

### 📊 대시보드 추가

1. Streamlit 메트릭 위젯 활용
2. 질문 빈도 분석
3. 항공사별 통계

### 🎨 UI/UX 개선

1. 커스텀 CSS 스타일링
2. 애니메이션 효과
3. 다크모드 지원

## ⚡ 우선순위 높은 작업

현재 다음 기능들이 우선적으로 필요합니다:

- [ ] 단위 테스트 코드 작성
- [ ] 에러 핸들링 개선
- [ ] 로깅 시스템 추가
- [ ] 성능 최적화 (캐싱)
- [ ] 다국어 지원 (영어, 일본어)

## 🔍 코드 리뷰 체크리스트

PR 제출 전에 확인해주세요:

- [ ] 코드가 PEP 8 스타일 가이드를 따릅니다
- [ ] 모든 함수에 docstring이 있습니다
- [ ] 테스트 코드가 작성되었습니다 (해당하는 경우)
- [ ] README.md가 업데이트되었습니다 (해당하는 경우)
- [ ] 변경사항이 기존 기능을 손상시키지 않습니다
- [ ] 커밋 메시지가 명확합니다

## 📧 문의

기여 과정에서 질문이 있다면:

- GitHub Issues에 질문 남기기
- 이메일: hwijae35@naver.com

## 🎁 기여자 명단

프로젝트에 기여해주신 모든 분들께 감사드립니다!

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- 여기에 기여자 목록이 자동으로 추가됩니다 -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

다시 한번 기여해주셔서 감사합니다! 🙏
