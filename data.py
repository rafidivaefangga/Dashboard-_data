import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔥 Flexible Data Dashboard")

# Upload file
uploaded_file = st.file_uploader("Penjualan_mobil.csv", type=["csv"])

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

    # FILTER
    st.subheader("🎯 Filter Data")
    selected_category = st.multiselect(
        "Pilih kategori (opsional)",
        options=df[category_col].unique(),
        default=df[category_col].unique()
    )

    df_filtered = df[df[category_col].isin(selected_category)]

    # METRIC
    st.subheader("📊 Ringkasan")
    total_sales = df_filtered[sales_col].sum()
    avg_sales = df_filtered[sales_col].mean()
    count_data = df_filtered.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", f"{total_sales:,.2f}")
    col2.metric("Rata-rata", f"{avg_sales:,.2f}")
    col3.metric("Jumlah Data", count_data)

    # BAR CHART
    st.subheader("📊 Sales by Category")
    category_sales = df_filtered.groupby(category_col)[sales_col].sum()

    fig1, ax1 = plt.subplots()
    category_sales.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    # PIE CHART
    st.subheader("🥧 Distribusi Data")
    fig2, ax2 = plt.subplots()
    category_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel('')
    st.pyplot(fig2)

    # TOP 5
    st.subheader("🏆 Top 5 Data")
    top_products = (
        df_filtered.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.write(top_products)

    # DOWNLOAD
    st.subheader("⬇️ Download Data")
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data hasil filter",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

else:
    st.info("Upload file CSV dulu bro 🚀")