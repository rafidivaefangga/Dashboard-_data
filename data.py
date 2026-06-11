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
    import plotly.express as px
    
    st.subheader("📊 Sales by Category")
    
    category_sales = (
        df_filtered.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    
    fig_bar = px.bar(
        category_sales,
        x=sales_col,
        y=category_col,
        orientation='h',
        title="Top 10 Category Sales",
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

    # =========================
    # PIE CHART (FIXED 🔥)
    # =========================
    st.subheader("🥧 Distribusi Data")
    
    category_sales_full = (
        df_filtered.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    
    # Top 5 + Others
    top_n = 5
    top_data = category_sales_full.head(top_n)
    
    others_value = category_sales_full[sales_col].iloc[top_n:].sum()
    
    if others_value > 0:
        top_data.loc[len(top_data)] = ["Others", others_value]
    
    fig_pie = px.pie(
        top_data,
        names=category_col,
        values=sales_col,
        title="Top Categories Distribution",
    )
    
    fig_pie.update_traces(textinfo='percent+label')
    
    st.plotly_chart(fig_pie, use_container_width=True)

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
