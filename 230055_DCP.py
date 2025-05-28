# Nama Pembuat      : Fawwaz Areefa Y
# NPM Pembuat       : 230055
# Nama Program      : Dominant Color Picker
# Deskripsi Program : Program yang bisa mengambil warna domminan pada gambar yang diunggah oleh user
# Dibuat pada hari Rabu, 28 Mei 2025

import streamlit as st
from PIL import Image
import numpy as np

# Fungsi untuk menghitung jarak Euclidean antara dua titik warna
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Fungsi untuk menginisialisasi centroid secara acak dari kumpulan pixel
def initialize_centroids(pixels, k):
    indices = np.random.choice(len(pixels), k, replace=False)  # pilih indeks acak tanpa pengulangan
    return pixels[indices]

# Fungsi untuk mengelompokkan pixel berdasarkan centroid terdekat
def assign_clusters(pixels, centroids):
    clusters = [[] for _ in range(len(centroids))]  # buat list kosong untuk tiap cluster
    for pixel in pixels:
        # Hitung jarak pixel ke semua centroid
        distances = [euclidean_distance(pixel, centroid) for centroid in centroids]
        cluster_index = np.argmin(distances)  # cari centroid terdekat
        clusters[cluster_index].append(pixel)  # tambahkan pixel ke cluster tersebut
    return clusters

# Fungsi untuk memperbarui posisi centroid berdasarkan rata-rata pixel di cluster
def update_centroids(clusters, k):
    new_centroids = []
    for cluster in clusters:
        if len(cluster) == 0:
            # Jika cluster kosong, buat centroid baru secara acak
            new_centroids.append(np.random.randint(0, 256, 3))
        else:
            # Hitung rata-rata warna pixel dalam cluster
            new_centroids.append(np.mean(cluster, axis=0))
    return np.array(new_centroids)

# Fungsi utama k-means clustering manual
def kmeans_manual(pixels, k, max_iters=10):
    centroids = initialize_centroids(pixels, k)  # inisialisasi centroid
    for _ in range(max_iters):
        clusters = assign_clusters(pixels, centroids)  # assign pixel ke cluster
        new_centroids = update_centroids(clusters, k)  # update centroid
        # Jika centroid tidak berubah signifikan, hentikan iterasi
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    return centroids.astype(int)  # kembalikan centroid sebagai integer (RGB)

# Fungsi untuk konversi nilai RGB ke kode warna hex
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# UI Streamlit
st.title("🎨 Dominant Color Picker")

uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_container_width=True)
    
    n_colors = 5  # warna dominan fix 5
    
    # Resize gambar supaya proses lebih cepat dan tidak terlalu berat
    image = image.resize((150, 150))
    pixels = np.array(image).reshape(-1, 3)  # ubah gambar jadi array 2D (jumlah_pixel x 3)
    
    with st.spinner("Menghitung warna dominan..."):
        centroids = kmeans_manual(pixels, n_colors)  # dapatkan centroid warna dominan
        hex_colors = [rgb_to_hex(color) for color in centroids]  # konversi ke hex
    
    st.success("Warna dominan ditemukan!")
    
    # Tampilkan kotak warna dengan hex code di bawahnya
    cols = st.columns(n_colors)
    for i, (rgb, hex_code) in enumerate(zip(centroids, hex_colors)):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color:{hex_code};
                    width:100%;
                    height:100px;
                    border-radius:10px;
                    border: 1px solid #000;
                    ">
                </div>
                <p style="text-align:center; font-weight:bold;">{hex_code}</p>
                """,
                unsafe_allow_html=True
            )