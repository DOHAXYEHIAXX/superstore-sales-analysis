"""Reusable cleaning, analysis, and chart generation for Superstore sales."""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
RAW_FILE = DATA_DIR / "Sample - Superstore.csv"
OUTPUT_FILE = RESULTS_DIR / "superstore_cleaned.csv"
CHART_DIR = RESULTS_DIR / "charts"


def load_and_clean(path=RAW_FILE):
    """Load the CSV, standardize headers and data types, and remove invalid or duplicate rows."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}\n"
            "Download the CSV from Kaggle and place it in the data folder "
            "with the name 'Sample - Superstore.csv'."
        )

    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    required = {
        "Order Date",
        "Sales",
        "Quantity",
        "Category",
        "Product Name",
        "Customer ID",
    }
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Required columns are missing: {sorted(missing)}")

    rows_before_cleaning = len(df)
    df = df.drop_duplicates().copy()

    for column in ["Order Date", "Ship Date"]:
        if column in df:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    for column in ["Sales", "Quantity", "Discount", "Profit"]:
        if column in df:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Keep missing customer, category, and product labels explicit.
    # Rows missing core dates or measures cannot be used in the analysis.
    df["Category"] = df["Category"].fillna("Unspecified")
    df["Product Name"] = df["Product Name"].fillna("Unspecified")
    df["Customer ID"] = df["Customer ID"].fillna("Unspecified")

    df = df.dropna(subset=["Order Date", "Sales", "Quantity"])

    # Quantity must be positive. Negative sales are retained because they may
    # represent legitimate returns or adjustments.
    df = df[df["Quantity"] > 0].copy()

    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Order Year"] = df["Order Date"].dt.year.astype("int64")
    df["Order Month"] = df["Order Date"].dt.month.astype("int64")

    # This count includes rows excluded by all cleaning rules.
    df.attrs["removed_rows"] = rows_before_cleaning - len(df)

    return df


def summarize(df):
    """Create summary tables for monthly sales, categories, products, and customers."""
    sales_by_month = (
        df.groupby("Year-Month", as_index=False)["Sales"]
        .sum()
    )

    sales_by_category = (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    top_products = (
        df.groupby("Product Name", as_index=False)
        .agg(
            Units_Sold=("Quantity", "sum"),
            Sales=("Sales", "sum"),
        )
        .sort_values(["Units_Sold", "Sales"], ascending=False)
        .head(10)
    )

    if "Order ID" in df:
        top_customers = (
            df.groupby("Customer ID", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Orders=("Order ID", "nunique"),
            )
        )
    else:
        top_customers = (
            df.groupby("Customer ID", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Orders=("Sales", "size"),
            )
        )

    top_customers = top_customers.sort_values(
        "Sales", ascending=False
    ).head(10)

    return sales_by_month, sales_by_category, top_products, top_customers


def make_charts(df, out_dir=CHART_DIR):
    """Create and save charts for products, monthly sales, categories, and profit."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid", palette="deep")
    monthly, categories, products, _ = summarize(df)

    # Top 10 products by units sold
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(
        data=products.sort_values("Units_Sold"),
        x="Units_Sold",
        y="Product Name",
        ax=ax,
        color="#3b82a0",
    )
    ax.set(
        title="Top 10 Products by Units Sold",
        xlabel="Units Sold",
        ylabel="Product",
    )
    fig.tight_layout()
    fig.savefig(out_dir / "01_top_products.png", dpi=160)
    plt.close(fig)

    # Monthly sales trend
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=monthly,
        x="Year-Month",
        y="Sales",
        marker="o",
        ax=ax,
        color="#e07a3f",
    )
    ax.set(
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($)",
    )
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(out_dir / "02_monthly_sales.png", dpi=160)
    plt.close(fig)

    # Sales share by category
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        categories["Sales"],
        labels=categories["Category"],
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
    )
    ax.set_title("Sales Share by Category")
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(out_dir / "03_category_share.png", dpi=160)
    plt.close(fig)

    # Optional fourth chart: profit by category
    if "Profit" in df:
        profit = (
            df.groupby("Category", as_index=False)["Profit"]
            .sum()
            .sort_values("Profit")
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=profit,
            x="Profit",
            y="Category",
            ax=ax,
            color="#65a765",
        )
        ax.set(
            title="Profit by Category",
            xlabel="Profit ($)",
            ylabel="Category",
        )
        fig.tight_layout()
        fig.savefig(out_dir / "04_profit_by_category.png", dpi=160)
        plt.close(fig)


def run(path=RAW_FILE):
    """Run the full cleaning and analysis workflow."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_clean(path)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    make_charts(df)

    monthly, categories, products, customers = summarize(df)

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "total_sales": float(df["Sales"].sum()),
        "total_profit": (
            float(df["Profit"].sum()) if "Profit" in df else None
        ),
        "date_min": str(df["Order Date"].min().date()),
        "date_max": str(df["Order Date"].max().date()),
        "top_product_by_units": (
            products.iloc[0]["Product Name"] if len(products) else None
        ),
        "top_category_by_sales": (
            categories.iloc[0]["Category"] if len(categories) else None
        ),
        "top_customer_by_sales": (
            customers.iloc[0]["Customer ID"] if len(customers) else None
        ),
        "monthly_sales": monthly.to_dict(orient="records"),
    }

    print("Analysis complete.\n")

    for key, value in report.items():
        print(f"{key}: {value}")

    print(f"\nCleaned CSV: {OUTPUT_FILE}")
    print(f"Charts: {CHART_DIR}")

    return df, report


if __name__ == "__main__":
    run()
