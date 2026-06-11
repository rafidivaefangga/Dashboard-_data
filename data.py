import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================

# CONFIG

# =====================================

st.set_page_config(
page_title="Flexible Data Dashboard",
page_icon="📊",
layout="wide"
)

st.title("📊 Flexible Data Dashboard")
st.markdown("Upload CSV dan analisis data secara interaktif")

# =====================================

# UPLOAD FILE

# =====================================

uploaded_file = st.file_uploader(
"Upload file CSV",
type=["csv"]
)

if uploaded_file is not None:

```
# Load data
df = pd.read_csv(
    uploaded_file,
    encoding="latin1",
    on_bad_lines="skip"
)

df.columns = df.columns.str.strip()

# =====================================
# PREVIEW
# =====================================
st.subheader("📄 Preview Data")
st.dataframe(df.head())

# =====================================
# PILIH KOLOM
# =====================================
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) == 0:
    st.error("Tidak ada kolom numerik pada dataset")
    st.stop()

all_cols = df.columns.tolist()

st.sidebar.header("⚙️ Pengaturan")

sales_col = st.sidebar.selectbox(
    "Kolom Numerik",
    numeric_cols
)

category_col = st.sidebar.selectbox(
    "Kolom Kategori",
    all_cols
)

product_col = st.sidebar.selectbox(
    "Kolom Produk",
    all_cols
)

# =====================================
# FILTER
# =====================================
st.sidebar.subheader("🎯 Filter")

selected_category = st.sidebar.multiselect(
    "Pilih Kategori",
    options=df[category_col].dropna().unique(),
    default=df[category_col].dropna().unique()
)

df_filtered = df[
    df[category_col].isin(selected_category)
]

# =====================================
# KPI
# =====================================
total_sales = df_filtered[sales_col].sum()
avg_sales = df_filtered[sales_col].mean()
count_data = len(df_filtered)

st.subheader("📈 Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total",
    f"{total_sales:,.2f}"
)

col2.metric(
    "📊 Rata-rata",
    f"{avg_sales:,.2f}"
)

col3.metric(
    "📦 Jumlah Data",
    count_data
)

# =====================================
# SALES BY CATEGORY
# =====================================
category_sales = (
    df_filtered.groupby(category_col)[sales_col]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

col_left, col_right = st.columns(2)

with col_left:

    st.subheader("📊 Sales by Category")

    fig_bar = px.bar(
        category_sales,
        x=category_col,
        y=sales_col,
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with col_right:

    st.subheader("🥧 Distribusi Category")

    fig_pie = px.pie(
        category_sales,
        names=category_col,
        values=sales_col
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# =====================================
# TOP PRODUK
# =====================================
st.subheader("🏆 Top 10 Produk")

top_products = (
    df_filtered.groupby(product_col)[sales_col]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(
    top_products,
    use_container_width=True
)

# =====================================
# STATISTIK
# =====================================
st.subheader("📈 Statistik Deskriptif")

st.dataframe(
    df_filtered.describe(),
    use_container_width=True
)

# =====================================
# DATA FILTER
# =====================================
st.subheader("📋 Data Setelah Filter")

st.dataframe(
    df_filtered,
    use_container_width=True
)

# =====================================
# DOWNLOAD
# =====================================
csv = df_filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Data Filter",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
```

else:

```
st.info(
    "👆 Upload file CSV untuk mulai analisis"
)
```
