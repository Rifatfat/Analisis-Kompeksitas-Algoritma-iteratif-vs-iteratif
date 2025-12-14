import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Benchmark Algoritma Min/Max", layout="centered")
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

# SETTING UJI
st.subheader("Konfigurasi Pengujian")
max_n = st.slider("Ukuran data maksimum", 100, 10000, 5000, step=100)
step = st.selectbox("Kenaikan ukuran data", [100, 500, 1000])
repeat = st.slider("Jumlah pengulangan", 1, 10, 3)

sizes = list(range(step, max_n + 1, step))

# JALANKAN BENCHMARK
if st.button("Jalankan Benchmark"):
    iter_times = []
    rec_times = []

    for n in sizes:
        data = [random.randint(50_000, 5_000_000) for _ in range(n)]

        # Iteratif
        total_iter = 0
        for _ in range(repeat):
            start = time.time()
            min_max_iteratif(data)
            total_iter += time.time() - start
        iter_times.append(total_iter / repeat)

        # Rekursif (dibatasi)
        if n <= 2000:
            total_rec = 0
            for _ in range(repeat):
                start = time.time()
                min_max_rekursif(data, 0, n - 1)
                total_rec += time.time() - start
            rec_times.append(total_rec / repeat)
        else:
            rec_times.append(None)

    # TABEL HASIL
    st.subheader("Tabel Hasil Uji")
    df = pd.DataFrame({
        "Jumlah Data (n)": sizes,
        "Iteratif (detik)": iter_times,
        "Rekursif (detik)": rec_times
    })
    st.dataframe(df)

    # GRAFIK
    st.subheader("Grafik Perbandingan Waktu")
    fig = plt.figure()
    plt.plot(sizes, iter_times, marker='o', label='Iteratif')
    plt.plot(sizes, rec_times, marker='o', label='Rekursif')
    plt.xlabel("Jumlah Data (n)")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.title("Iteratif vs Rekursif")
    plt.legend()
    st.pyplot(fig)

    # KESIMPULAN
    st.subheader("Kesimpulan")
    st.markdown("""
    - Algoritma iteratif konsisten lebih cepat.
    - Algoritma rekursif memiliki overhead stack.
    - Untuk dataset besar, pendekatan iteratif lebih efisien secara praktis.
    """)
