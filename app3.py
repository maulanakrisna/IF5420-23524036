import streamlit as st
import pandas as pd
import plotly.express as px
# from config import get_connection

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load data
# engine = get_connection()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('loaded_fact_sales.csv')
    return df

df = load_data()

# Handle missing values
df['Gender'] = df['Gender'].fillna('Unknown')
df['Country'] = df['Country'].fillna('Unknown')
df['ProductCategory'] = df['ProductCategory'].fillna('Unknown')

# Sidebar Filter
st.sidebar.title("📌 Filter Data Interaktif")

# Filter Tahun
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(df['Year'].dropna().unique()))

# Filter Bulan
# selected_month = st.sidebar.selectbox("Pilih Bulan", sorted(df['Month'].dropna().unique()))

# Filter Kategori Produk
selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    df['ProductCategory'].dropna().unique(),
    default=df['ProductCategory'].dropna().unique()
)

# Filter Lokasi: Negara
selected_country = st.sidebar.multiselect(
    "Pilih Negara",
    df['Country'].dropna().unique(),
    default=df['Country'].dropna().unique()
)

# Filter Segment Pelanggan (berdasarkan Usia)
# Kita bisa buat kolom segment usia
# bins = [0, 18, 25, 35, 50, 65, 100]
# labels = ['<18', '18-25', '26-35', '36-50', '51-65', '65+']
# df['AgeSegment'] = pd.cut(df['Age'], bins=bins, labels=labels)

# selected_segment = st.sidebar.multiselect(
#     "Pilih Segment Usia Pelanggan",
#     df['AgeSegment'].dropna().unique(),
#     default=df['AgeSegment'].dropna().unique()
# )

# # Sidebar filter
# st.sidebar.title("📌 Filter Data")
# selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(df['Year'].dropna().unique()))
# selected_country = st.sidebar.multiselect("Pilih Negara", df['Country'].dropna().unique(), default=df['Country'].dropna().unique())
# selected_category = st.sidebar.multiselect("Pilih Kategori Produk", df['ProductCategory'].dropna().unique(), default=df['ProductCategory'].dropna().unique())

# Filter data sesuai input dari slicer
filtered_df = df[
    (df['Year'] == selected_year) &
    (df['ProductCategory'].isin(selected_category)) &
    (df['Country'].isin(selected_country))
]

# # Filter data
# filtered_df = df[
#     (df['Year'] == selected_year) &
#     (df['Country'].isin(selected_country)) &
#     (df['ProductCategory'].isin(selected_category))
# ]

# Judul dashboard
st.title(f"📊 Dashboard Penjualan Ritel - Tahun {selected_year}")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penjualan", f"${filtered_df['TotalAmount'].sum():,.2f}")
col2.metric("Jumlah Transaksi", f"{filtered_df.shape[0]:,}")
col3.metric("Total Produk Terjual", f"{filtered_df['Quantity'].sum():,.0f}")
# Cari kategori produk terlaris
if not filtered_df.empty:
    top_category = filtered_df.groupby('ProductCategory')['TotalAmount'].sum().idxmax()
    top_category_value = filtered_df.groupby('ProductCategory')['TotalAmount'].sum().max()
    col4.metric("Kategori Terlaris", top_category, f"${top_category_value:,.2f}")
else:
    col4.metric("Kategori Terlaris", "Data tidak tersedia", "")

# Penjualan per Bulan
monthly_sales = filtered_df.groupby('Month')['TotalAmount'].sum().reset_index()
fig1 = px.bar(monthly_sales, x='Month', y='TotalAmount', title='📅 Penjualan per Bulan')
st.plotly_chart(fig1, use_container_width=True)

# Top Kategori Produk
top_cat = filtered_df.groupby('ProductCategory')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
fig2 = px.pie(top_cat, names='ProductCategory', values='TotalAmount', title='🏷️ Distribusi Penjualan per Kategori')
st.plotly_chart(fig2, use_container_width=True)

# Top 10 Produk berdasarkan Total Penjualan
top_products = filtered_df.groupby('ProductCategory')['TotalAmount'].sum().sort_values(ascending=False).head(10).reset_index()
# (opsional: join dengan nama produk jika punya dimProduct)

fig5 = px.bar(top_products, x='TotalAmount', y='ProductCategory', orientation='h',
              title='🏆 Top 10 Produk berdasarkan Penjualan',
              labels={'ProductCategory': 'ID Produk', 'TotalAmount': 'Total Penjualan ($)'})
st.plotly_chart(fig5, use_container_width=True)

# Distribusi berdasarkan Gender
gender_sales = filtered_df.groupby('Gender')['TotalAmount'].sum().reset_index()
fig3 = px.bar(gender_sales, x='Gender', y='TotalAmount', title='👤 Penjualan berdasarkan Gender')
st.plotly_chart(fig3, use_container_width=True)

# Penjualan per Kota (City)
if 'City' in filtered_df.columns and filtered_df['City'].notna().any():
    city_sales = filtered_df.groupby('City')['TotalAmount'].sum().sort_values(ascending=False).head(20).reset_index()
    fig6 = px.bar(city_sales, x='City', y='TotalAmount',
                  title='🏙️ Top 20 Penjualan per Kota',
                  labels={'TotalAmount': 'Total Penjualan ($)'})
    st.plotly_chart(fig6, use_container_width=True)

# Penjualan per Negara (Country)
if 'Country' in filtered_df.columns and filtered_df['Country'].notna().any():
    country_sales = filtered_df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False).head(20).reset_index()
    fig7 = px.bar(country_sales, x='Country', y='TotalAmount',
                  title='🌍 Top 20 Penjualan per Negara',
                  labels={'TotalAmount': 'Total Penjualan ($)'})
    st.plotly_chart(fig7, use_container_width=True)

# Agregasi penjualan per negara
country_sales_map = (
    filtered_df.groupby('Country')['TotalAmount']
    .sum()
    .reset_index()
)

# Visualisasi peta dunia (Choropleth)
fig_world = px.choropleth(
    country_sales_map,
    locations='Country',
    locationmode='country names',
    color='TotalAmount',
    color_continuous_scale='Blues',
    title='🌍 Penjualan per Negara (World Map)',
    labels={'TotalAmount': 'Total Penjualan ($)'}
)
st.plotly_chart(fig_world, use_container_width=True)

# Agregasi penjualan per State (misal hanya untuk US)
usa_df = filtered_df[filtered_df['Country'] == 'United States']

# Penjualan per State (State)
if 'State' in usa_df.columns and usa_df['State'].notna().any():
    state_sales = usa_df.groupby('State')['TotalAmount'].sum().sort_values(ascending=False).head(20).reset_index()
    fig6 = px.bar(state_sales, x='State', y='TotalAmount',
                  title='🏙️ Top 20 Penjualan per State',
                  labels={'TotalAmount': 'Total Penjualan ($)'})
    st.plotly_chart(fig6, use_container_width=True)

if 'State' in usa_df.columns and usa_df['State'].notna().any():
    state_sales = (
        usa_df.groupby('State')['TotalAmount']
        .sum()
        .reset_index()
    )

    fig_state = px.choropleth(
        state_sales,
        locations='State',
        locationmode='USA-states',
        color='TotalAmount',
        scope='usa',
        color_continuous_scale='YlGnBu',
        title='🌍 Penjualan per Negara Bagian (USA)',
        labels={'TotalAmount': 'Total Penjualan ($)'}
    )
    st.plotly_chart(fig_state, use_container_width=True)

# # Penjualan per Negara
# country_sales = filtered_df.groupby('Country')['TotalAmount'].sum().reset_index()
# fig4 = px.bar(country_sales, x='Country', y='TotalAmount', title='🌍 Penjualan per Negara')
# st.plotly_chart(fig4, use_container_width=True)

# filtered_df['Region'] = filtered_df['City'].fillna('') + ", " + filtered_df['Country'].fillna('')
# region_sales = filtered_df.groupby('Region')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
# fig_region = px.bar(region_sales, x='Region', y='TotalAmount', title='📍 Penjualan per Region')
# st.plotly_chart(fig_region, use_container_width=True)
