# 📊 Retail Sales Dashboard (Streamlit)

Visualisasi interaktif data penjualan ritel berbasis **data warehouse** yang mencakup analisis performa penjualan, produk, pelanggan, lokasi, dan waktu secara real-time. Dashboard ini dibuat menggunakan **Python + Streamlit** dan dapat diakses secara online oleh manajemen perusahaan.

---

## 🚀 Live App

🔗 [Buka Dashboard di Streamlit Cloud]
[https://if5420-23524036-15062025.streamlit.app/]

---

## 📁 Struktur Dataset

Dataset1: https://github.com/amir-hojjati/Data-Analysis-Online-Retail-Transactions/blob/master/Original-Dataset/Online%20Retail.csv

Dataset2: https://www.kaggle.com/datasets/fahadrehman07/retail-transaction-dataset

Dataset3: https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset

Dashboard menggunakan data warehouse dengan skema dimensional
Loaded_Fact_Sales.csv terdiri dari join table berikut:
- **FactSales**: transaksi penjualan 
- **dimCustomer**: data pelanggan 
- **dimProduct**: produk 
- **dimLocation**: lokasi penjualan 
- **dimDate**: informasi waktu

---

## 📌 Fitur Dashboard

- ✅ KPI Cards: Total Penjualan, Produk Terlaris, Rata-rata Umur Pelanggan
- 📊 Bar Chart:
  - Penjualan per Kota dan Negara (Top 20)
  - Penjualan per Bulan
- 📆 Filter Interaktif:
  - Tahun
  - Kategori Produk
  - Lokasi (Negara)
 
Dengan bantuan OpenAI ChatGPT untuk dokumentasi & boilerplate.
