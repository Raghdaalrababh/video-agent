from __future__ import annotations
from typing import Any
from openai import OpenAI
from .config import settings

# إنشاء عميل Azure OpenAI
# ملاحظة: لازم تكوني ماغي القيم في .env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
if not (settings.aoai_endpoint and settings.aoai_key and settings.aoai_deployment):
    raise ValueError("Missing Azure OpenAI configuration in .env")

client = OpenAI(
    api_key=settings.aoai_key,
    base_url=f"{settings.aoai_endpoint}/openai/deployments/{settings.aoai_deployment}",
)

SYSTEM_PROMPT = (
    "You are a precise video analysis assistant. "
    "Given a transcript or JSON text, produce:\n"
    "1) ملخص موجز (5-8 سطور)\n"
    "2) Highlights (٥ نقاط)\n"
    "3) أسئلة وأجوبة سريعة (٣-٥)\n"
    "الإخراج يكون Markdown عربي واضح."
)

def summarize_from_transcript(transcript_text: str) -> str:
    """
    يستقبل نص طويل (تفريغ/JSON كنص) ويرجع Markdown مُلخّص.
    نقتطع النص إذا كان أطول من اللازم لتجنب تجاوز حدود السياق.
    """
    # قصّ بسيط للاحتياط (قيمي حسب نشر موديلك)
    snippet = transcript_text if len(transcript_text) <= 12000 else transcript_text[:12000]

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": snippet},
    ]
    # model هنا هو اسم الـ deployment في Azure (مثلاً gpt-4o-mini)
    res = client.chat.completions.create(messages=messages, model=settings.aoai_deployment)
    return res.choices[0].message.content or ""
