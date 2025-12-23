import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Analisis Pendapatan Coffeeshop",
    layout="centered"
)

# CSS CUSTOM UNTUK BACKGROUND COKLAT TUA
st.markdown("""
    <style>
    .stApp {
        background-color: #3E2723;
    }
    .stMarkdown, .stText {
        color: #EFEBE9;
    }
    h1, h2, h3 {
        color: #D7CCC8 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Analisis Pendapatan Coffeeshop")
st.write("Pencarian pendapatan minimum & maksimum menggunakan algoritma iteratif dan rekursif")

# ALGORITMA MIN MAX
def min_max_iteratif(data):
    nilai_min = data[0]
    nilai_max = data[0]

    for nilai in data:
        if nilai < nilai_min:
            nilai_min = nilai
        if nilai > nilai_max:
            nilai_max = nilai

    return nilai_min, nilai_max


def min_max_rekursif(data, bawah, atas):
    if bawah == atas:
        return data[bawah], data[bawah]

    if atas == bawah + 1:
        return min(data[bawah], data[atas]), max(data[bawah], data[atas])

    tengah = (bawah + atas) // 2
    min1, max1 = min_max_rekursif(data, bawah, tengah)
    min2, max2 = min_max_rekursif(data, tengah + 1, atas)

    return min(min1, min2), max(max1, max2)

# UPLOAD DATA
st.subheader("Upload Data Transaksi")

file_upload = st.file_uploader(
    "Upload file Excel atau csv (.xlsx, .csv)",
    type=["xlsx", "csv"]
)

if file_upload:
    # BACA & BERSIHKAN DATA
    if file_upload.name.endswith('.csv'):
        df = pd.read_csv(file_upload)
    else:
        df = pd.read_excel(file_upload)

    df = df[
        [
            "transaction_date",
            "transaction_qty",
            "unit_price",
            "product_category"
        ]
    ]

    df["revenue"] = df["transaction_qty"] * df["unit_price"]

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # DATA UNTUK ALGORITMA
    data_pendapatan = df["revenue"].tolist()
    jumlah_data = len(data_pendapatan)

    st.info(f"Total transaksi: {jumlah_data}")
    
    with st.form("parameter_form"):
        max_n = st.slider(
            "Ukuran data:",
            min_value=1000,
            max_value=jumlah_data,
            value=min(10000, jumlah_data),
            step=1000
        )
        submit = st.form_submit_button("Cari Pendapatan Min & Max")


    # JALANKAN PENCARIAN
    if submit:
        
        data_uji = data_pendapatan[:max_n]
        
        # Iteratif
        waktu_mulai = time.time()
        min_iteratif, max_iteratif = min_max_iteratif(data_uji)
        waktu_iteratif = time.time() - waktu_mulai

        # Rekursif di limit 1 jt
        if jumlah_data <= 1000000:
            waktu_mulai = time.time()
            min_rekursif, max_rekursif = min_max_rekursif(data_uji, 0, len(data_uji) - 1)
            waktu_rekursif = time.time() - waktu_mulai
        else:
            min_rekursif, max_rekursif = None, None
            waktu_rekursif = None

        # HASIL
        st.subheader("Hasil Pencarian Pendapatan")
        st.subheader(f"Jumlah Data: {max_n}")

        kolom1, kolom2 = st.columns(2)
        kolom1.metric("Pendapatan Minimum", f"$ {min_iteratif:,.0f}")
        kolom2.metric("Pendapatan Maksimum", f"$ {max_iteratif:,.0f}")

        # TABEL WAKTU EKSEKUSI
        st.subheader("Waktu Eksekusi")

        df_waktu = pd.DataFrame({
            "Metode": ["Iteratif", "Rekursif"],
            "Waktu (detik)": [waktu_iteratif, waktu_rekursif]
        })

        st.dataframe(df_waktu)

        # GRAFIK
        st.subheader("Grafik Perbandingan Waktu")

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#3E2723')
        ax.set_facecolor('#5D4037')
        
        batang = ax.bar(
            ["Iteratif", "Rekursif"],
            [
                waktu_iteratif,
                waktu_rekursif if waktu_rekursif is not None else 0
            ],
            color=['#8D6E63', '#A1887F']
        )
        
        ax.set_ylabel("Waktu (detik)", color='#EFEBE9')
        ax.set_title("Iteratif vs Rekursif", color='#EFEBE9', fontsize=14, fontweight='bold')
        ax.tick_params(colors='#EFEBE9')
        ax.spines['bottom'].set_color('#EFEBE9')
        ax.spines['top'].set_color('#EFEBE9')
        ax.spines['left'].set_color('#EFEBE9')
        ax.spines['right'].set_color('#EFEBE9')
        
        st.pyplot(fig)

        # PER KATEGORI
        st.subheader("Pendapatan Min & Max per Kategori Produk")

        hasil_kategori = (
            df.groupby("product_category")["revenue"]
            .agg(["min", "max"])
            .reset_index()
        )

        st.dataframe(hasil_kategori)

        # KESIMPULAN
        st.subheader("Kesimpulan")
        st.markdown("""
        - Pendapatan dihitung dari `transaction_qty × unit_price`
        - Algoritma **iteratif lebih cepat dan stabil**
        - Rekursif punya overhead stack → kurang cocok untuk data besar
        - Untuk analisis bisnis real-world, iteratif lebih praktis
        """)