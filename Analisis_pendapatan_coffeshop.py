import streamlit as st #
import pandas as pd
import time
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Analisis Pendapatan Coffeeshop",
    layout="centered"
)

st.title(" Analisis Pendapatan Coffeeshop")
st.write("Pencarian pendapatan minimum & maksimum menggunakan algoritma iteratif dan rekursif")

# ALGORITMA MIN MAX
def min_max_iteratif(data):
    min_val = data[0]
    max_val = data[0]

    for x in data:
        if x < min_val:
            min_val = x
        if x > max_val:
            max_val = x

    return min_val, max_val


def min_max_rekursif(data, low, high):
    if low == high:
        return data[low], data[low]

    if high == low + 1:
        return min(data[low], data[high]), max(data[low], data[high])

    mid = (low + high) // 2
    min1, max1 = min_max_rekursif(data, low, mid)
    min2, max2 = min_max_rekursif(data, mid + 1, high)

    return min(min1, min2), max(max1, max2)

# UPLOAD DATA
st.subheader(" Upload Data Transaksi")

uploaded_file = st.file_uploader(
    "Upload file Excel atau cvs (.xlsx, .cvs)",
    type=["xlsx", "cvs"]
)

if uploaded_file:
    # BACA & BERSIHKAN DATA
    df = pd.read_excel(uploaded_file)

    df = df[
        [
            "transaction_date",
            "transaction_qty",
            "unit_price",
            "product_category"
        ]
    ]

    df["revenue"] = df["transaction_qty"] * df["unit_price"]

    st.subheader(" Preview Data")
    st.dataframe(df.head())

    # DATA UNTUK ALGORITMA
    revenues = df["revenue"].tolist()
    n = len(revenues)

    st.info(f"Total transaksi: {n}")

    # JALANKAN PENCARIAN
    if st.button(" Cari Pendapatan Min & Max"):
        # Iteratif
        start = time.time()
        min_iter, max_iter = min_max_iteratif(revenues)
        time_iter = time.time() - start

        # Rekursif di limit 1 jt
        if n <= 1000000:
            start = time.time()
            min_rec, max_rec = min_max_rekursif(revenues, 0, n - 1)
            time_rec = time.time() - start
        else:
            min_rec, max_rec = None, None
            time_rec = None

        # HASIL
        st.subheader(" Hasil Pencarian Pendapatan")

        col1, col2 = st.columns(2)
        col1.metric("Pendapatan Minimum", f"$ {min_iter:,.0f}")
        col2.metric("Pendapatan Maksimum", f"$ {max_iter:,.0f}")

        # TABEL WAKTU EKSEKUSI
        st.subheader(" Waktu Eksekusi")

        time_df = pd.DataFrame({
            "Metode": ["Iteratif", "Rekursif"],
            "Waktu (detik)": [time_iter, time_rec]
        })

        st.dataframe(time_df)

        # GRAFIK
        st.subheader(" Grafik Perbandingan Waktu")

        fig = plt.figure()
        plt.bar(
            ["Iteratif", "Rekursif"],
            [
                time_iter,
                time_rec if time_rec is not None else 0
            ]
        )
        plt.ylabel("Waktu (detik)")
        plt.title("Iteratif vs Rekursif")
        st.pyplot(fig)

        # BONUS: PER KATEGORI
        st.subheader(" Pendapatan Min & Max per Kategori Produk")

        category_result = (
            df.groupby("product_category")["revenue"]
            .agg(["min", "max"])
            .reset_index()
        )

        st.dataframe(category_result)

        # KESIMPULAN
        st.subheader(" Kesimpulan")
        st.markdown("""
        - Pendapatan dihitung dari `transaction_qty × unit_price`
        - Algoritma **iteratif lebih cepat dan stabil**
        - Rekursif punya overhead stack → kurang cocok untuk data besar
        - Untuk analisis bisnis real-world, iteratif lebih praktis
        """)
