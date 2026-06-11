import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔥 Flexible Data Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload file CSV kamu", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file, encoding='latin1', on_bad_lines='skip')

    # Rapihin kolom
    df.columns = df.columns.str.strip()

    st.subheader("📄 Preview Data")
    st.write(df.head())

    # Pilih kolom
    numeric_cols = df.select_dtypes(include='number').columns
    all_cols = df.columns

    sales_col = st.selectbox("Pilih kolom angka (Sales)", numeric_cols)
    category_col = st.selectbox("Pilih kolom kategori", all_cols)
    product_col = st.selectbox("Pilih kolom produk", all_cols)

    # =========================
    # FILTER
    # =========================
    st.subheader("🎯 Filter Data")

    selected_category = st.multiselect(
        "Pilih kategori (opsional)",
        options=df[category_col].unique(),
        default=df[category_col].unique()
    )

    df_filtered = df[df[category_col].isin(selected_category)]

    # =========================
    # METRIC
    # =========================
    st.subheader("📊 Ringkasan")

    total_sales = df_filtered[sales_col].sum()
    avg_sales = df_filtered[sales_col].mean()
    count_data = df_filtered.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", f"{total_sales:,.2f}")
    col2.metric("Rata-rata", f"{avg_sales:,.2f}")
    col3.metric("Jumlah Data", count_data)

    # =========================
    # BAR CHART
    # =========================
    st.subheader("📊 Sales by Category")

    category_sales = (
        df_filtered.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig1, ax1 = plt.subplots()
    category_sales.plot(kind='barh', ax=ax1)

    ax1.set_xlabel("Sales")
    ax1.set_ylabel(category_col)

    st.pyplot(fig1)

    # =========================
    # PIE CHART (FIXED 🔥)
    # =========================
    st.subheader("🥧 Distribusi Data")

    category_sales_full = (
        df_filtered.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    # Top 5 + Others
    top_n = 5
    top_data = category_sales_full.head(top_n)
    others = category_sales_full.iloc[top_n:].sum()

    if others > 0:
        top_data["Others"] = others

    fig2, ax2 = plt.subplots()

    ax2.pie(
        top_data,
        labels=None,  # biar ga numpuk
        autopct='%1.1f%%',
        startangle=90
    )

    ax2.legend(top_data.index, loc="best")
    ax2.set_title("Top Categories Distribution")
    ax2.axis('equal')

    st.pyplot(fig2)

    # =========================
    # TOP 5
    # =========================
    st.subheader("🏆 Top 5 Data")

    top_products = (
        df_filtered.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.write(top_products)

    # =========================
    # DOWNLOAD
    # =========================
    st.subheader("⬇️ Download Data")

    csv = df_filtered.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download data hasil filter",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

else:
    st.info("Upload file CSV")
