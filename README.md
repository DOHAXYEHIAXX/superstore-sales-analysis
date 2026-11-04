# Superstore Sales Analysis

A Python project for exploring and analyzing Superstore sales data. It covers data quality checks, cleaning, sales and profit analysis, product and customer performance, and monthly trends.

## Dataset

Download `Sample - Superstore.csv` from the [Kaggle dataset page](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place it in the `data/` directory.

## Requirements

- Python 3.9 or later
- pandas
- numpy
- matplotlib
- seaborn
- Jupyter Notebook

Install the Python packages with:

```bash
python -m pip install -r requirements.txt
```

## Run the analysis

Run the script from the project directory:

```bash
python analysis.py
```

Alternatively, open `notebooks/superstore_sales_analysis.ipynb` in Jupyter and run the cells in order.

## Project structure

```text
.
├── analysis.py
├── data/
│   └── Sample - Superstore.csv
├── notebooks/
│   └── superstore_sales_analysis.ipynb
├── results/
│   ├── charts/
│   └── superstore_cleaned.csv
├── README.md
└── requirements.txt
```

## Data cleaning

The analysis removes exact duplicate rows, converts date and numeric columns to appropriate types, and excludes records missing an order date, sales value, or quantity. Rows with non-positive quantities are excluded. Negative sales are retained because they may represent returns or adjustments. Missing category, product, and customer labels are marked as `Unspecified`.

## Outputs

The project writes a cleaned CSV file and charts showing the top products by units sold, monthly sales, sales share by category, and profit by category.
