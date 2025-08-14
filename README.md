# video-agent# 🎬 Video Agent (Azure)

Agent تعليمي بسيط يفهرس فيديوهات عبر **Azure AI Video Indexer** ويولد **ملخّص/Highlights/FAQs** عبر **Azure OpenAI**.

## ✨ المزايا
- رفع/فهرسة فيديوهات بالرابط (URL)
- سحب Insights/Transcript
- تلخيص عربي منسّق إلى Markdown

## 🧱 المتطلبات
- Python 3.11+
- حساب Azure وخدمات:
  - Azure AI Video Indexer (Account ID, Location, API Key)
  - Azure OpenAI (Endpoint, Key, Deployment)
  - (اختياري) Azure Blob Storage (Connection String)
- تفعيل GitHub Actions (اختياري)

## ⚙️ الإعداد
1) انسخ القيم إلى ملف `.env` (من `.env.example`):
