# 🔒 보안 가이드 (SECURITY.md)

## ⚠️ 중요한 보안 주의사항

이 프로젝트를 사용할 때 반드시 지켜야 할 보안 규칙입니다.

---

## 🔑 API 키 보안

### ❌ 절대 하지 말아야 할 것

```python
# 🚫 나쁜 예: 코드에 API 키 직접 입력
os.environ["OPENAI_API_KEY"] = "sk-proj-abc123..."  # 위험!
```

**위험:**
- GitHub에 업로드 시 API 키가 공개됨
- 악의적 사용자가 키를 탈취하여 과금 발생
- OpenAI 계정이 정지될 수 있음

### ✅ 올바른 방법

#### 방법 1: `.env` 파일 사용 (로컬 환경)

```bash
# .env 파일
OPENAI_API_KEY=sk-proj-your-key-here
```

```python
# Python 코드
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 자동 로드
api_key = os.getenv("OPENAI_API_KEY")
```

**중요:** `.env` 파일을 `.gitignore`에 추가하세요!

```bash
# .gitignore
.env
.env.local
```

#### 방법 2: `getpass` 사용 (Google Colab/Jupyter)

```python
from getpass import getpass
import os

# 사용자 입력 (입력 내용이 화면에 표시되지 않음)
api_key = getpass("OpenAI API 키를 입력하세요: ")
os.environ["OPENAI_API_KEY"] = api_key
```

#### 방법 3: 환경 변수 직접 설정 (배포 환경)

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-proj-your-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-proj-your-key-here"
```

---

## 🔍 GitHub에 업로드하기 전 체크리스트

### 필수 확인사항

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는가?
- [ ] 코드에 API 키가 직접 입력되어 있지 않은가?
- [ ] `chroma_db/` 폴더가 `.gitignore`에 포함되어 있는가?
- [ ] 개인정보가 포함된 로그 파일이 없는가?
- [ ] Jupyter Notebook에 출력된 API 키가 없는가?

### Git 히스토리에서 API 키 제거

실수로 API 키를 커밋했다면:

```bash
# BFG Repo-Cleaner 사용 (권장)
brew install bfg  # macOS
apt-get install bfg  # Ubuntu

# API 키가 포함된 파일 제거
bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 또는 git-filter-repo 사용
pip install git-filter-repo
git filter-repo --invert-paths --path .env
```

**중요:** 이미 공개된 API 키는 즉시 폐기하고 새로 발급받으세요!

---

## 🛡️ API 키 관리 Best Practices

### 1. 키 로테이션

- 정기적으로 API 키를 교체하세요 (권장: 3개월마다)
- OpenAI 대시보드에서 사용하지 않는 키는 삭제하세요

### 2. 사용량 모니터링

- [OpenAI Usage Dashboard](https://platform.openai.com/usage)에서 일일 사용량 확인
- 예상치 못한 사용량 급증 시 즉시 키 폐기

### 3. 비용 제한 설정

```python
# OpenAI 대시보드에서 설정
# Settings → Billing → Usage limits
# 월간 사용 한도 설정 (예: $10)
```

### 4. 키별 권한 제한

- API 키마다 사용 범위를 제한하세요
- 필요한 모델과 엔드포인트만 허용

---

## 🚨 API 키 유출 시 대응

### 즉시 수행할 작업

1. **OpenAI 대시보드에서 키 폐기**
   - https://platform.openai.com/api-keys
   - "Revoke" 버튼 클릭

2. **새로운 키 발급**
   - 새 키를 안전하게 저장
   - 프로젝트에 새 키 적용

3. **GitHub 저장소 정리**
   - 유출된 키가 포함된 커밋 삭제
   - 히스토리 재작성

4. **청구 확인**
   - 비정상적인 사용량 확인
   - 필요 시 OpenAI 고객지원 문의

### 자동 스캔 도구

```bash
# git-secrets 설치 (API 키 커밋 방지)
brew install git-secrets

# 프로젝트에 설정
git secrets --install
git secrets --register-aws
git secrets --add 'sk-[a-zA-Z0-9]{48}'
```

---

## 📝 Google Colab 사용 시 주의사항

### 1. 노트북 공유 전 확인

```python
# ❌ 나쁜 예: 출력에 API 키 노출
print(f"API Key: {os.environ['OPENAI_API_KEY']}")

# ✅ 좋은 예: 일부만 표시
api_key = os.environ['OPENAI_API_KEY']
print(f"API Key: {api_key[:10]}***")
```

### 2. 노트북 셀 출력 정리

노트북을 공유하기 전:
- `Edit → Clear all outputs` 실행
- API 키가 출력된 셀이 없는지 확인

### 3. Colab Secrets 사용 (권장)

```python
from google.colab import userdata

# Colab Secrets에 저장된 값 사용
api_key = userdata.get('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = api_key
```

Secrets 설정: 🔑 아이콘 → Add new secret

---

## 🔐 추가 보안 권장사항

### 1. HTTPS 사용

- ngrok은 기본적으로 HTTPS를 사용합니다 (`bind_tls=True`)
- 로컬 개발 시에도 가능하면 HTTPS 사용

### 2. 입력 검증

```python
# 사용자 입력을 검증하여 인젝션 공격 방지
def sanitize_input(user_input: str) -> str:
    # SQL 인젝션, XSS 등 방지
    forbidden_patterns = ["<script", "javascript:", "SELECT", "DROP"]
    for pattern in forbidden_patterns:
        if pattern.lower() in user_input.lower():
            raise ValueError("Invalid input detected")
    return user_input
```

### 3. 로깅 보안

```python
# ❌ 나쁜 예: 민감한 정보 로깅
logger.info(f"User query: {query}, API Key: {api_key}")

# ✅ 좋은 예: 민감한 정보 제외
logger.info(f"User query: {query}")
```

---

## 📧 보안 이슈 리포트

보안 취약점을 발견하셨나요?

**공개적으로 이슈를 올리지 마세요!**

대신 다음 이메일로 비공개로 연락해주세요:
- **이메일**: security@your-project.com
- **PGP 키**: (선택사항)

24시간 이내에 답변드리겠습니다.

---

## 📚 참고 자료

- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**마지막 업데이트**: 2024년 1월

보안은 모두의 책임입니다. 안전한 개발 환경을 만들어갑시다! 🔒
