# Meta Supervisor

## 1. 프로젝트 소개

**Meta Supervisor**는 자연어(한국어)로 된 금융 관련 요청을 이해하고, 이를 분석하여 여러 전문 백엔드 API(예: 트레이딩 전략 API, 시장 분석 API)로 작업을 분기하고 오케스트레이션하는 지능형 에이전트입니다.

사용자가 "삼성전자 주가 분석해줘" 와 같은 간단한 명령을 내리면, Meta Supervisor는 의도를 파악하고 적절한 백엔드에 요청을 전달하여 그 결과를 사용자에게 제공하는 것을 목표로 합니다.

## 2. 주요 기능

- **자연어 이해 (NLU):** `konlpy`를 사용하여 한국어 문장의 의도(Intent)와 핵심 개체(Entity)를 분석합니다.
- **지능형 요청 라우팅:** 분석된 의도에 따라 가장 적절한 백엔드 서비스로 요청을 동적으로 라우팅합니다.
- **비동기 API 서버:** `FastAPI`와 `Uvicorn`을 기반으로 한 고성능 비동기 서버로 구축되었습니다.
- **확장 가능한 클라이언트 구조:** `httpx`를 사용하여 새로운 백엔드 API를 쉽게 추가하고 연동할 수 있는 구조를 갖추고 있습니다.
- **견고한 예외 처리:** 서비스의 어떤 단계에서 오류가 발생하더라도 서버가 중단되지 않고, 일관된 형식의 오류를 반환합니다.

## 3. 기술 스택

- **언어:** Python 3.12+
- **웹 프레임워크:** FastAPI
- **패키지 관리:** uv
- **자연어 처리:** Konlpy
- **HTTP 클라이언트:** HTTPX
- **데이터 유효성 검사:** Pydantic

## 4. 프로젝트 구조

```
.
├── .venv/
├── src/
│   └── meta_supervisor/
│       ├── __init__.py
│       ├── clients/         # 외부 API 클라이언트
│       │   ├── __init__.py
│       │   ├── base_client.py
│       │   ├── market_client.py
│       │   └── trading_client.py
│       ├── routers/         # API 라우터 (엔드포인트)
│       │   ├── __init__.py
│       │   └── api.py
│       ├── schemas.py       # Pydantic 데이터 모델
│       ├── services/        # 핵심 비즈니스 로직
│       │   ├── __init__.py
│       │   ├── nlu_service.py
│       │   └── routing_service.py
│       ├── config.py        # 환경 변수 및 설정
│       └── main.py          # FastAPI 앱 진입점
├── pyproject.toml
├── requirements.txt
├── run.sh                   # 서버 실행 스크립트
└── README.md
```

## 5. 설치 및 실행 방법

### 5.1. 사전 요구사항

- Python 3.12 이상
- `uv` 패키지 관리자 (`pip install uv`)
- **Java 11 이상 (JDK):** `konlpy` 라이브러리 실행에 필수입니다. `JAVA_HOME` 환경 변수가 올바르게 설정되어 있어야 합니다.

### 5.2. 설치 과정

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/FinAgent-Lab/fin-agent
    cd fin-agent
    ```

2.  **의존성 패키지 설치:**
    ```bash
    uv pip install -r requirements.txt
    ```

### 5.3. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 백엔드 API 서버의 URL을 설정합니다.

```.env
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1
```

### 5.4. 서버 실행

아래의 셸 스크립트를 실행하여 FastAPI 서버를 시작합니다.

```bash
bash run.sh
```

서버가 정상적으로 실행되면 `http://0.0.0.0:8000` 에서 실행됩니다.

## 6. API 사용 예시

### 6.1. 통합 쿼리 처리 엔드포인트

`curl`을 사용하여 `/api/query` 엔드포인트에 자연어 쿼리를 전송할 수 있습니다.

```bash
curl -X POST "http://localhost:8000/api/query" \
-H "Content-Type: application/json" \
-d '{"query": "삼성전자 005930 주가 분석"}'
```

### 6.2. 외부 API 연동

#### 마켓 분석 API 연동 포맷

**외부 마켓 분석 API 요청 포맷:**
```python
class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = os.getenv("MAIN_LLM_MODEL", "gpt-4o-mini")
    temperature: Optional[float] = 0.2
```

**외부 마켓 분석 API 응답 포맷:**
```python
class QueryResponse(BaseModel):
    answer: str
    timestamp: str
```

Meta Supervisor의 `MarketAnalysisService`가 위 포맷으로 외부 마켓 분석 API와 직접 통신합니다.

#### 예상 응답 (백엔드 서버가 없을 경우)

```json
{
  "success": false,
  "data": null,
  "error_code": "INTERNAL_SERVER_ERROR",
  "error_message": "All connection attempts failed"
}
```

## 7. 배포

### 7.1. Docker를 이용한 배포

프로젝트는 Docker를 사용하여 컨테이너화되어 있습니다.

#### 환경 변수 설정

배포 전에 다음 환경 변수들을 설정해야 합니다:

```bash
# 필수 환경 변수
OPENAI_API_KEY=your_openai_api_key

# 선택적 환경 변수 (기본값 사용 가능)
ENVIRONMENT=production
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1
MAIN_LLM_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

#### Docker Compose를 이용한 배포

```bash
# 환경 변수 파일 생성
cat > .env << EOF
ENVIRONMENT=production
APISERVER_PORT_EXTERNAL=8000
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
MAIN_LLM_MODEL=gpt-4o-mini
TRADING_STRATEGY_API_BASE_URL=http://trading-strategy-team/api/v1
MARKET_ANALYSIS_API_BASE_URL=http://market-analysis-team/api/v1
EOF

# 서비스 빌드 및 시작
docker compose -f docker-compose.prod.yaml up -d

# 서비스 상태 확인
docker compose -f docker-compose.prod.yaml ps

# 로그 확인
docker compose -f docker-compose.prod.yaml logs -f
```

#### 헬스체크

서비스가 정상적으로 실행되고 있는지 확인:

```bash
curl http://localhost:8000/health
```

### 7.2. GitHub Actions를 이용한 자동 배포

프로젝트는 GitHub Actions를 통한 자동 배포를 지원합니다.

#### GitHub Secrets 설정

다음 Secrets를 GitHub 저장소에 설정해주세요:

- `OPENAI_API_KEY`: OpenAI API 키 (필수)

#### GitHub Variables 설정 (선택사항)

다음 Variables를 설정할 수 있습니다:

- `OPENAI_BASE_URL`: OpenAI API 기본 URL (기본값: https://api.openai.com/v1)
- `MAIN_LLM_MODEL`: 사용할 LLM 모델 (기본값: gpt-4o-mini)
- `TRADING_STRATEGY_API_BASE_URL`: 트레이딩 전략 API URL
- `MARKET_ANALYSIS_API_BASE_URL`: 시장 분석 API URL

#### 배포 트리거

- `main`, `develop`, `dev` 브랜치에 푸시하거나
- GitHub Actions 페이지에서 수동으로 "Simple Deploy to Self-Hosted Runner" 워크플로우 실행

## 8. 향후 계획

- 실제 백엔드 API 명세에 맞춰 `clients` 모듈의 요청/응답 로직 구체화
- 사용자 인증 및 세션 관리 기능 추가
- 비즈니스 로직 및 워크플로우 고도화
- 로깅 및 모니터링 시스템 구축
- **fin-agent에서 사용자 요청에 담긴 스톡 넘버를 확인할 수 있는 기능 추가**