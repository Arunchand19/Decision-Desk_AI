import json

from pydantic import BaseModel, Field, ValidationError

from .config import get_settings
from .retrieval import retriever
from .schemas import Action


class DecisionOutput(BaseModel):
    action: Action
    confidence: float = Field(ge=0, le=1)
    reason: str = Field(min_length=1)
    sources: list[str] = Field(min_length=1)


def _fallback(ticket: str, context: list[dict[str, str | float]]) -> DecisionOutput:
    text = ticket.lower()
    sources = list(dict.fromkeys(str(item["source"]) for item in context)) or ["No matching policy"]
    missing_photos = "photo" not in text and "picture" not in text or any(phrase in text for phrase in ("no photo", "no picture", "not taken", "have not taken", "not sent"))
    if ("damaged" in text or "broken" in text) and missing_photos:
        return DecisionOutput(action=Action.REQUEST_PHOTOS, confidence=0.91, reason="The damaged-goods policy requires photographs of the package and item before a refund or replacement is promised.", sources=sources)
    if "wrong item" in text or "incorrect item" in text:
        return DecisionOutput(action=Action.REQUEST_ORDER_DETAILS, confidence=0.82, reason="The wrong-item policy requires the order number and a photograph of the received item before arranging a replacement.", sources=sources)
    if "cancel" in text and "shipped" not in text:
        return DecisionOutput(action=Action.REQUEST_ORDER_DETAILS, confidence=0.79, reason="The cancellation policy requires the order number and shipping status before cancellation can be confirmed.", sources=sources)
    if "return" in text or "refund" in text:
        return DecisionOutput(action=Action.REQUEST_ORDER_DETAILS, confidence=0.72, reason="The returns and refunds policies require the order number and item condition before eligibility can be decided.", sources=sources)
    if not context or float(context[0]["score"]) == 0:
        return DecisionOutput(action=Action.NEEDS_MORE_INFORMATION, confidence=0.45, reason="The policy documents do not contain enough evidence to decide this ticket.", sources=sources)
    return DecisionOutput(action=Action.NEEDS_MORE_INFORMATION, confidence=0.58, reason="The available policy context suggests a support workflow, but the ticket lacks enough specific facts for a reliable decision.", sources=sources)


def decide(ticket: str) -> DecisionOutput:
    context = retriever.retrieve(ticket)
    settings = get_settings()
    if not settings.gemini_api_key:
        return _fallback(ticket, context)
    prompt = """You are a support policy decision assistant. Use only the supplied policy context. Never invent policy. If facts are insufficient, choose NEEDS_MORE_INFORMATION. Return JSON with action, confidence (0 to 1), reason, and sources.\n\nTicket:\n%s\n\nPolicy context:\n%s""" % (ticket, json.dumps(context, ensure_ascii=False))
    try:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt, config={"response_mime_type": "application/json"})
        result = DecisionOutput.model_validate_json(response.text)
        allowed_sources = {str(item["source"]) for item in context}
        if not set(result.sources).issubset(allowed_sources):
            raise ValueError("Model returned a source outside retrieved context")
        return result
    except (ValidationError, ValueError, json.JSONDecodeError, Exception):
        return _fallback(ticket, context)
