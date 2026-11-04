# تحليل مبيعات Superstore

مشروع تدريبي بـ Python لتحليل بيانات متجر Superstore: استكشاف البيانات، تنظيفها، قياس المبيعات والربح، ثم إنشاء رسوم توضح المنتجات والشهور والفئات.

## مصدر البيانات

حمّلي `Sample - Superstore.csv` من [صفحة Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) وضعيه في مجلد `data/` داخل المشروع. وافقي على شروط Kaggle إن ظهرت. لا يتضمن هذا التسليم نسخة من بيانات Kaggle؛ يتم إنشاء CSV المنظف والرسوم بعد التشغيل.

## التشغيل

```bash
python -m pip install -r requirements.txt
```

ضعي الملف هنا: `data/Sample - Superstore.csv`، ثم شغلي التحليل:

```bash
python analysis.py
```

أو افتحي `notebooks/superstore_sales_analysis.ipynb` في Jupyter وشغلي الخلايا بالترتيب. إذا كنتِ تستخدمين Jupyter محليًا، ثبتي الاعتماديات أعلاه أولًا.

## نواتج التشغيل

- `results/superstore_cleaned.csv`: بيانات بعد حذف الصفوف المكررة وغير الصالحة، وضبط الأنواع وإضافة الشهر والسنة.
- `results/charts/01_top_products.png`: أكثر 10 منتجات حسب مجموع الوحدات المباعة.
- `results/charts/02_monthly_sales.png`: اتجاه المبيعات شهريًا.
- `results/charts/03_category_share.png`: حصة كل فئة من المبيعات.
- `results/charts/04_profit_by_category.png`: الربح الإجمالي حسب الفئة.

يُبقي التنظيف قيم Sales السالبة لأنها قد تمثل مرتجعات أو تسويات؛ ويتخلص من الصفوف التي تفتقد التاريخ أو المبيعات أو الكمية، ومن الكميات غير الموجبة. القيم الناقصة في حقول التصنيف/المنتج/العميل توسم بـ «غير محدد». تُحفظ النتائج الرقمية الدقيقة في CSV، بينما تُنسق الأرقام للعرض عند الحاجة.

## أسئلة التحليل

1. كم صفًا وعمودًا في المصدر؟ ما أنواع البيانات والقيم الناقصة والتكرارات؟
2. ما إجمالي المبيعات والربح؟ ما المنتجات والفئات الأعلى أداءً؟
3. كيف تتغير المبيعات من شهر إلى آخر؟ من العملاء الأعلى مساهمة في المبيعات؟

## هيكل المجلد

```text
Superstore_Sales_Analysis/
├── analysis.py
├── requirements.txt
├── README.md
├── data/                 # ملف Kaggle يوضع هنا
├── notebooks/
│   └── superstore_sales_analysis.ipynb
└── results/              # ينشأ CSV والرسوم هنا عند التشغيل
```

## المصدر

Superstore Dataset على Kaggle: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
