# Meta Supervisor
[![Deployed](https://github.com/FinAgent-Lab/fin-agent/actions/workflows/simple-deploy.yml/badge.svg)](https://github.com/FinAgent-Lab/fin-agent/actions/workflows/simple-deploy.yml)

## 목차

1. [프로젝트 소개](#1-프로젝트-소개)
2. [주요 기능](#2-주요-기능)
3. [기술 스택](#3-기술-스택)
4. [프로젝트 구조](#4-프로젝트-구조)
5. [설치 및 실행 방법](#5-설치-및-실행-방법)
6. [API 사용 예시](#6-api-사용-예시)
7. [문제 해결](#7-문제-해결-troubleshooting)
8. [배포](#8-배포)
9. [향후 계획](#9-향후-계획)

## 1. 프로젝트 소개

**Meta Supervisor**는 자연어(한국어)로 된 금융 관련 요청을 이해하고, 이를 분석하여 여러 전문 백엔드 API(예: 트레이딩 전략 API, 시장 분석 API)로 작업을 분기하고 오케스트레이션하는 지능형 에이전트입니다.

사용자가 "삼성전자 주가 분석해줘" 와 같은 간단한 명령을 내리면, Meta Supervisor는 의도를 파악하고 적절한 백엔드에 요청을 전달하여 그 결과를 사용자에게 제공하는 것을 목표로 합니다.

## 2. 주요 기능

- **🤖 자연어 이해 (NLU):** `konlpy`를 활용한 한국어 문장 의도(Intent) 및 핵심 개체(Entity) 분석
- **🔀 지능형 요청 라우팅:** LangGraph 기반 워크플로우를 통한 동적 서비스 라우팅
- **⚡ 고성능 비동기 서버:** FastAPI와 Uvicorn 기반의 비동기 처리로 높은 처리량 보장
- **🔌 확장 가능한 서비스 구조:** `httpx`를 활용한 외부 API 연동 및 새로운 서비스 쉬운 추가
- **🛡️ 견고한 예외 처리:** 서비스 장애 시에도 안정적인 운영 및 일관된 오류 응답 제공
- **📊 종합 모니터링:** 헬스체크, 로깅 미들웨어를 통한 서비스 상태 실시간 모니터링
- **🐳 컨테이너 지원:** Docker 및 Docker Compose를 통한 간편한 배포 및 확장

## 3. 기술 스택

- **언어:** Python 3.10+
- **웹 프레임워크:** FastAPI
- **패키지 관리:** uv (고성능 Python 패키지 관리자)
- **자연어 처리:** Konlpy
- **HTTP 클라이언트:** HTTPX
- **데이터 유효성 검사:** Pydantic
- **AI 프레임워크:** LangChain, LangGraph
- **LLM API:** OpenAI GPT
- **컨테이너화:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## 4. 프로젝트 구조

```
.
├── .venv/                   # 가상 환경 (uv로 관리)
├── src/
│   └── meta_supervisor/
│       ├── __init__.py
│       ├── config.py        # 환경 변수 및 설정
│       ├── dependencies.py  # FastAPI 의존성 주입
│       ├── main.py          # FastAPI 앱 진입점
│       ├── schemas.py       # Pydantic 데이터 모델
│       ├── simple_logging.py # 로깅 미들웨어
│       ├── routers/         # API 라우터 (엔드포인트)
│       │   ├── __init__.py
│       │   └── api.py
│       ├── services/        # 핵심 비즈니스 로직
│       │   ├── __init__.py
│       │   ├── agent_service.py      # 에이전트 서비스
│       │   ├── market_analysis_service.py # 시장 분석 서비스
│       │   ├── nlu_service.py        # 자연어 처리 서비스
│       │   ├── routing_service.py    # 요청 라우팅 서비스
│       │   └── trading_service.py    # 트레이딩 서비스
│       └── tools/           # LangGraph 도구
│           ├── __init__.py
│           ├── base_tool.py
│           ├── market_analysis_tool.py
│           └── trading_tool.py
├── tests/                   # 테스트 파일
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_endpoints.py
│   ├── test_basic.py
│   └── test_logging_middleware.py
├── .env.template           # 환경 변수 템플릿
├── docker-compose.prod.yaml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml          # 프로젝트 설정 및 의존성 (uv 관리)
├── run.sh                  # 서버 실행 스크립트
├── uv.lock                 # uv 의존성 잠금 파일
└── README.md
```

## 5. 설치 및 실행 방법

### 5.1. 사전 요구사항

- **Python 3.10 이상** (권장: 3.12+)
- **uv 패키지 관리자**: 빠르고 안정적인 Python 패키지 관리자
- **Java 11 이상 (JDK)**: `konlpy` 라이브러리 실행에 필수. `JAVA_HOME` 환경 변수 설정 필요

### 5.2. 설치 과정

1. **저장소 복제:**
   ```bash
   git clone https://github.com/FinAgent-Lab/fin-agent.git
   cd fin-agent
   ```

2. **uv 패키지 관리자 설치 (필요한 경우):**
   ```bash
   pip install uv
   ```

3. **의존성 설치 및 가상환경 생성:**
   ```bash
   # 프로덕션 의존성만 설치
   uv sync --no-dev
   
   # 또는 개발 의존성 포함하여 설치
   uv sync
   ```

### 5.3. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

```bash
# .env.template 파일을 복사하여 시작
cp .env.template .env
```

**.env 파일 예시:**
```env
# 필수 환경 변수
OPENAI_API_KEY=your_openai_api_key_here

# 선택적 환경 변수 (기본값 사용 가능)
OPENAI_BASE_URL=https://api.openai.com/v1
MAIN_LLM_MODEL=gpt-4o-mini
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1

# 서버 설정
ENVIRONMENT=development
```

### 5.4. 서버 실행

다음 중 한 가지 방법으로 서버를 실행할 수 있습니다:

**방법 1: 실행 스크립트 사용 (권장)**
```bash
chmod +x run.sh
./run.sh
```

**방법 2: uv를 통한 직접 실행**
```bash
uv run uvicorn src.meta_supervisor.main:app --host 0.0.0.0 --port 8000 --reload
```

**방법 3: 프로덕션 환경**
```bash
uv run uvicorn src.meta_supervisor.main:app --host 0.0.0.0 --port 8000 --workers 4
```

서버가 정상적으로 실행되면 `http://localhost:8000` 에서 접근할 수 있습니다.

- **API 문서 (Swagger):** http://localhost:8000/docs
- **API 문서 (ReDoc):** http://localhost:8000/redoc
- **헬스체크:** http://localhost:8000/health

## 5.5. 개발 환경 설정

개발을 위한 추가 설정:

```bash
# 개발 의존성 포함 설치
uv sync

# 코드 포맷팅 (Black)
uv run black .

# 코드 린팅 (Ruff)  
uv run ruff check .

# 테스트 실행
uv run pytest -v

# 테스트 커버리지 확인
uv run pytest --cov=src --cov-report=html
```

## 6. API 사용 예시

## 6. API 사용 예시

### 6.1. 헬스체크 엔드포인트

```bash
# 기본 헬스체크
curl http://localhost:8000/health

# 상세 정보 포함
curl http://localhost:8000/health | jq '.'
```

**응답 예시:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "Meta Supervisor",
  "version": "0.1.0",
  "environment": "development",
  "checks": {
    "environment": {
      "status": "healthy",
      "missing": []
    },
    "market_analysis_service": {
      "status": "healthy",
      "available": true
    }
  }
}
```

### 6.2. 통합 쿼리 처리 엔드포인트

자연어 쿼리를 `/api/query` 엔드포인트로 전송할 수 있습니다.

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "삼성전자 005930 주가 분석해줘",
    "model": "gpt-4o-mini",
    "temperature": 0.2
  }'
```

**성공 응답 예시:**
```json
{
  "success": true,
  "data": {
    "answer": "삼성전자(005930) 주가 분석 결과입니다...",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "processing_time": 2.5
  },
  "error_code": null,
  "error_message": null
}
```

### 6.3. 외부 API 연동

#### 6.3.1. 마켓 분석 API 연동 포맷

**외부 마켓 분석 API 요청 포맷:**
```python
class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = "gpt-4o-mini"  # 환경변수 MAIN_LLM_MODEL 기본값
    temperature: Optional[float] = 0.2
```

**외부 마켓 분석 API 응답 포맷:**
```python
class QueryResponse(BaseModel):
    answer: str
    timestamp: str
```

Meta Supervisor의 `MarketAnalysisService`가 위 포맷으로 외부 마켓 분석 API와 통신합니다.

#### 6.3.2. 에러 응답 (백엔드 서비스 미연결 시)

외부 백엔드 서비스에 연결할 수 없는 경우의 응답:

```json
{
  "success": false,
  "data": null,
  "error_code": "INTERNAL_SERVER_ERROR",
  "error_message": "All connection attempts failed"
}
```

#### 6.3.3. API 문서 확인

서버 실행 후 다음 URL에서 상세한 API 문서를 확인할 수 있습니다:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 7. 문제 해결 (Troubleshooting)

### 7.1. 일반적인 문제

#### Java 관련 오류 (konlpy 사용 시)
```bash
# 문제: Java가 설치되지 않았거나 JAVA_HOME이 설정되지 않음
# 해결: Java 11+ 설치 및 환경변수 설정
export JAVA_HOME=/path/to/your/java
export PATH=$JAVA_HOME/bin:$PATH
```

#### 환경 변수 관련 오류
```bash
# 문제: OpenAI API 키가 설정되지 않음
# 해결: .env 파일 확인 및 API 키 설정
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

#### 포트 충돌 문제
```bash
# 문제: 8000 포트가 이미 사용 중
# 해결: 다른 포트 사용
uv run uvicorn src.meta_supervisor.main:app --host 0.0.0.0 --port 8001
```

### 7.2. 로그 확인

```bash
# Docker 컨테이너 로그 확인
docker compose -f docker-compose.prod.yaml logs -f

# 서비스별 로그 확인
docker compose -f docker-compose.prod.yaml logs -f meta-supervisor
```

### 7.3. 개발 모드 디버깅

```bash
# 디버그 모드로 서버 실행
PYTHONPATH=src python -m meta_supervisor.main

# 또는 상세 로깅과 함께
PYTHONPATH=src python -m uvicorn meta_supervisor.main:app --reload --log-level debug
```

## 8. 배포

### 8.1. Docker를 이용한 배포

프로젝트는 멀티 스테이지 Docker 빌드를 사용하여 최적화된 컨테이너를 제공합니다.

#### 8.1.1. 환경 변수 설정

배포 전에 다음 환경 변수들을 설정해야 합니다:

**필수 환경 변수:**
```bash
OPENAI_API_KEY=your_openai_api_key
```

**선택적 환경 변수 (기본값 제공):**
```bash
ENVIRONMENT=production
OPENAI_BASE_URL=https://api.openai.com/v1
MAIN_LLM_MODEL=gpt-4o-mini
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1
APISERVER_PORT_EXTERNAL=8000
```

#### 8.1.2. Docker Compose를 이용한 배포

```bash
# 1. 환경 변수 파일 생성
cat > .env << EOF
ENVIRONMENT=production
APISERVER_PORT_EXTERNAL=8000
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
MAIN_LLM_MODEL=gpt-4o-mini
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1
EOF

# 2. 서비스 빌드 및 시작
docker compose -f docker-compose.prod.yaml up -d

# 3. 서비스 상태 확인
docker compose -f docker-compose.prod.yaml ps

# 4. 로그 확인
docker compose -f docker-compose.prod.yaml logs -f
```

#### 8.1.3. 헬스체크

서비스가 정상적으로 실행되고 있는지 확인:

```bash
# 기본 상태 확인
curl http://localhost:8000/health

# 상세 헬스체크 정보 확인
curl http://localhost:8000/health | jq '.'
```

### 8.2. GitHub Actions를 이용한 자동 배포

프로젝트는 GitHub Actions를 통한 자동 배포를 지원합니다.

#### 8.2.1. GitHub Secrets 설정

다음 Secret을 GitHub 저장소에 설정해주세요:

| Secret 이름 | 설명 | 필수 여부 |
|-------------|------|-----------|
| `OPENAI_API_KEY` | OpenAI API 키 | 필수 |

#### 8.2.2. GitHub Variables 설정 (선택사항)

다음 Variables를 설정할 수 있습니다:

| Variable 이름 | 기본값 | 설명 |
|---------------|--------|------|
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI API 기본 URL |
| `MAIN_LLM_MODEL` | `gpt-4o-mini` | 사용할 LLM 모델 |
| `TRADING_STRATEGY_API_BASE_URL` | `http://trading-strategy-team/api/v1` | 트레이딩 전략 API URL |
| `MARKET_ANALYSIS_API_BASE_URL` | `http://market-analysis-team/api/v1` | 시장 분석 API URL |

#### 8.2.3. 배포 트리거

자동 배포는 다음 경우에 실행됩니다:

- **자동 트리거:** `main`, `develop`, `dev` 브랜치에 push
- **수동 트리거:** GitHub Actions 페이지에서 "Simple Deploy to Self-Hosted Runner" 워크플로우 수동 실행

#### 8.2.4. 배포 상태 확인

README 상단의 배포 상태 배지를 통해 최신 배포 상태를 확인할 수 있습니다:
[![Deployed](https://github.com/FinAgent-Lab/fin-agent/actions/workflows/simple-deploy.yml/badge.svg)](https://github.com/FinAgent-Lab/fin-agent/actions/workflows/simple-deploy.yml)

## 9. 향후 계획

### 9.1. 단기 계획
- [ ] 실제 백엔드 API 명세에 맞춰 서비스 통신 로직 구체화
- [ ] **사용자 요청에서 주식 종목코드(스톡 넘버) 추출 기능 고도화**
- [ ] 에러 처리 및 재시도 로직 강화
- [ ] API 응답 시간 최적화

### 9.2. 중기 계획  
- [ ] 사용자 인증 및 세션 관리 시스템 구축
- [ ] 요청 히스토리 및 결과 캐싱 기능
- [ ] 다중 LLM 모델 지원 및 모델 선택 최적화
- [ ] 실시간 시장 데이터 스트리밍 지원

### 9.3. 장기 계획
- [ ] 고급 비즈니스 로직 및 워크플로우 엔진 구축
- [ ] 종합적인 로깅, 모니터링 및 알람 시스템
- [ ] 멀티테넌시 지원 및 사용자별 개인화
- [ ] 모바일 앱 및 웹 프론트엔드 개발
