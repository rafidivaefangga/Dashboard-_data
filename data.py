import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="🔥 Data Dashboard",
    layout="wide"
)

st.title("🔥 Flexible Data Dashboard")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload file CSV kamu", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, encoding='latin1', on_bad_lines='skip')
    df.columns = df.columns.str.strip()

    st.subheader("📄 Preview Data")
    st.dataframe(df.head(), use_container_width=True)

    # =========================
    # VALIDASI KOLOM
    # =========================
    numeric_cols = df.select_dtypes(include='number').columns
    all_cols = df.columns

    if len(numeric_cols) == 0:
        st.error("❌ Tidak ada kolom numerik di data")
        st.stop()

    # =========================
    # PILIH KOLOM
    # =========================
    sales_col = st.selectbox("Pilih kolom angka (Sales)", numeric_cols)
    category_col = st.selectbox("Pilih kolom kategori", all_cols)
    product_col = st.selectbox("Pilih kolom produk", all_cols)

    # =========================
    # CLEANING
    # =========================
    df = df.dropna(subset=[sales_col])

    # =========================
    # FILTER
    # =========================
    st.subheader("🎯 Filter Data")

    selected_category = st.multiselect(
        "Pilih kategori",
        options=df[category_col].dropna().unique(),
        default=df[category_col].dropna().unique()
    )

    df_filtered = df[df[category_col].isin(selected_category)]

    if df_filtered.empty:
        st.warning("⚠️ Data kosong setelah filter")
        st.stop()

    # =========================
    # METRICS
    # =========================
    st.subheader("📊 Ringkasan")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", f"{df_filtered[sales_col].sum():,.2f}")
    col2.metric("Rata-rata", f"{df_filtered[sales_col].mean():,.2f}")
    col3.metric("Jumlah Data", df_filtered.shape[0])

    # =========================
    # BAR CHART (FIX)
    # =========================
    st.subheader("📊 Sales by Category")

    category_sales = (
        df_filtered.groupby(category_col, as_index=False)[sales_col]
        .sum()
        .sort_values(by=sales_col, ascending=False)
        .head(10)
    )

    fig_bar = px.bar(
        category_sales,
        x=sales_col,
        y=category_col,
        orientation='h',
        title="Top 10 Category Sales",
        text=sales_col
    )

    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_bar, use_container_width=True)

    # =========================
    # PIE CHART (FIX TOTAL)
    # =========================
    st.subheader("🥧 Distribusi Data")

    category_sales_full = (
        df_filtered.groupby(category_col, as_index=False)[sales_col]
        .sum()
        .sort_values(by=sales_col, ascending=False)
    )

    top_n = 5
    top_data = category_sales_full.head(top_n).copy()

    others = category_sales_full[sales_col].iloc[top_n:].sum()

    if others > 0:
        others_row = pd.DataFrame({
            category_col: ["Others"],
            sales_col: [others]
        })
        top_data = pd.concat([top_data, others_row], ignore_index=True)

    fig_pie = px.pie(
        top_data,
        names=category_col,
        values=sales_col,
        title="Top Categories Distribution",
        hole=0.4  # donut biar modern
    )

    fig_pie.update_traces(textinfo='percent+label')

    st.plotly_chart(fig_pie, use_container_width=True)

    # =========================
    # TOP 5 PRODUCT (FIX)
    # =========================
    st.subheader("🏆 Top 5 Data")

    top_products = (
        df_filtered.groupby(product_col, as_index=False)[sales_col]
        .sum()
        .sort_values(by=sales_col, ascending=False)
        .head(5)
    )

    st.dataframe(top_products, use_container_width=True)

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
    st.info("Upload file CSV untuk mulai")
