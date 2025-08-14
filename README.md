# 🎬 Video Agent — Azure AI Educational Project

مشروع تعليمي يهدف إلى توضيح كيفية بناء Agent للتعامل مع الفيديوهات باستخدام خدمات **Microsoft Azure**.  
يقوم المشروع بفهرسة الفيديوهات، استخراج النصوص والـ Insights، ثم تلخيصها باللغة العربية.

---

## ✨ المزايا الرئيسية
- **فهرسة الفيديوهات** باستخدام [Azure AI Video Indexer](https://learn.microsoft.com/en-us/azure/azure-video-indexer/).
- **تلخيص المحتوى** وإنتاج النقاط البارزة (Highlights) والأسئلة الشائعة (FAQs) باستخدام [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/).
- تصميم هيكلي احترافي مع دعم أوامر CLI.
- **CI/CD** عبر GitHub Actions لاختبارات الكود وفحص الجودة.

---

## 🧱 المتطلبات
- Python 3.11+
- حساب Azure يحتوي على:
  - Azure AI Video Indexer
  - Azure OpenAI
  -Azure Blob Storage
