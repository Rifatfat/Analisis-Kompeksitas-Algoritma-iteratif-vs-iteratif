import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# ================================
# KONFIGURASI HALAMAN
# ================================
st.set_page_config(
    page_title="Benchmark Algoritma Min/Max",
    layout="centered"
)

st.title("Benchmark Iteratif vs Rekursif")
st.write("Perbandingan waktu eksekusi algoritma pencarian minimum & maksimum")

# ================================
# ALGORITMA
# ================================
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

# ================================
# INPUT DATA CSV
# ================================
st.subheader("Input Data CSV")

uploaded_file = st.file_uploader(
    "Upload file CSV (berisi data numerik)",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("Silakan upload file CSV terlebih dahulu")
    st.stop()

df = pd.read_csv(uploaded_file)

st.write("Preview Data:")
st.dataframe(df.head())

# Pilih kolom
column = st.selectbox("Pilih kolom data", df.columns)

# Ambil data numerik
data = df[column].dropna().astype(int).tolist()

if len(data) < 2:
    st.error("Data harus memiliki minimal 2 baris")
    st.stop()

st.success(f"Total data: {len(data)}")

# ================================
# KONFIGURASI BENCHMARK
# ================================
st.subheader("Konfigurasi Pengujian")

max_n = st.slider(
    "Ukuran data maksimum",
    min_value=2,
    max_value=len(data),
    value=min(5000, len(data)),
    step=100
)

step = st.selectbox(
    "Kenaikan ukuran data",
    [100, 500, 1000]
)

repeat = st.slider(
    "Jumlah pengulangan",
    1, 10, 3
)

sizes = list(range(step, max_n + 1, step))

# ================================
# JALANKAN BENCHMARK
# ================================
if st.button("Jalankan Benchmark"):
    iter_times = []
    rec_times = []

    for n in sizes:
        subset_data = data[:n]

        # Iteratif
        total_iter = 0
        for _ in range(repeat):
            start = time.perf_counter()
            min_max_iteratif(subset_data)
            total_iter += time.perf_counter() - start
        iter_times.append(total_iter / repeat)

        # Rekursif (dibatasi)
        if n <= 10000:
            total_rec = 0
            for _ in range(repeat):
                start = time.perf_counter()
                min_max_rekursif(subset_data, 0, n - 1)
                total_rec += time.perf_counter() - start
            rec_times.append(total_rec / repeat)
        else:
            rec_times.append(None)

    # ================================
    # TABEL HASIL
    # ================================
    st.subheader("Tabel Hasil Uji")

    df_result = pd.DataFrame({
        "Jumlah Data (n)": sizes,
        "Iteratif (detik)": iter_times,
        "Rekursif (detik)": rec_times
    })

    st.dataframe(df_result)

    # ================================
    # GRAFIK
    # ================================
    st.subheader("Grafik Perbandingan Waktu")

    fig = plt.figure()
    plt.plot(sizes, iter_times, marker="o", label="Iteratif")
    plt.plot(sizes, rec_times, marker="o", label="Rekursif")
    plt.xlabel("Jumlah Data (n)")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.title("Benchmark Iteratif vs Rekursif")
    plt.legend()
    st.pyplot(fig)

    # ================================
    # KESIMPULAN
    # ================================
    st.subheader("Kesimpulan")
    st.markdown("""
    - Algoritma **iteratif** konsisten lebih cepat.
    - Algoritma **rekursif** memiliki overhead pemanggilan fungsi.
    - Untuk dataset besar, pendekatan iteratif lebih efisien secara praktis.
    """)
