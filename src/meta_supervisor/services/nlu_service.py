from konlpy.tag import Okt
import re
from .. import schemas

INTENT_KEYWORDS = {
    "market_analysis": ["분석", "시세", "주가", "차트", "전망"],
    "strategy_creation": ["전략", "만들", "생성", "개발"],
    "backtest": ["백테스트", "과거", "검증"],
    "strategy_execution": ["실행", "매매", "주문", "시작", "적용"],
}


def preprocess_and_tokenize(text: str) -> list[str]:
    """
    Preprocesses and tokenizes Korean text.
    - Removes special characters
    - Extracts nouns and verbs (lemmatized)
    """
    okt = Okt()  # Create instance locally
    # 1. Remove special characters and hangul jamo
    processed_text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", text)
    # 2. Tokenize and lemmatize
    tokens = okt.pos(processed_text, norm=True, stem=True)
    # 3. Extract meaningful parts of speech (nouns, verbs)
    meaningful_tokens = [word for word, pos in tokens if pos in ["Noun", "Verb"]]
    return meaningful_tokens


def classify_intent(tokens: list[str]) -> str:
    """
    Classifies the user's intent based on keywords in tokens.
    """
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in tokens for keyword in keywords):
            return intent
    return "unknown"


def extract_entities(text: str) -> dict:
    """
    Extracts entities like stock codes from the text.
    """
    entities = {}
    # Extract stock code (6-digit number)
    stock_code_match = re.search(r"(\d{6})", text)
    if stock_code_match:
        entities["stock_code"] = stock_code_match.group(1)
    return entities


def analyze(text: str) -> schemas.IntentAnalysisResult:
    """
    Analyzes the user's natural language query.
    """
    tokens = preprocess_and_tokenize(text)
    intent = classify_intent(tokens)
    entities = extract_entities(text)
    return schemas.IntentAnalysisResult(intent=intent, entities=entities)
