# Nama Pembuat      : Fawwaz Areefa Y
# NPM Pembuat       : 230055
# Nama Program      : Dominant Color Picker
# Deskripsi Program : Program yang bisa mengambil warna domminan pada gambar yang diunggah oleh user
# Dibuat pada hari Rabu, 28 Mei 2025

import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Hitung jarak Euclidean antara dua warna
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Clustering manual untuk mencari warna dominan
def manual_color_clustering(image, n_colors=5, max_iter=10):
    image = image.resize((150, 150))  # Resize untuk percepat proses
    pixels = np.array(image).reshape(-1, 3).astype(float)

    # Pilih centroid awal secara acak dari piksel
    np.random.seed(42)
    centroids = pixels[np.random.choice(len(pixels), n_colors, replace=False)]

    for _ in range(max_iter):
        # Kelompokkan piksel ke centroid terdekat
        labels = []
        for pixel in pixels:
            distances = [euclidean_distance(pixel, centroid) for centroid in centroids]
            labels.append(np.argmin(distances))
        labels = np.array(labels)

        # Update centroid sebagai rata-rata dari setiap grup
        new_centroids = []
        for i in range(n_colors):
            cluster_pixels = pixels[labels == i]
            if len(cluster_pixels) > 0:
                new_centroids.append(np.mean(cluster_pixels, axis=0))
            else:
                # Jika cluster kosong, inisialisasi ulang secara acak
                new_centroids.append(pixels[np.random.choice(len(pixels))])
        centroids = np.array(new_centroids)

    # Konversi ke integer & hex
    final_colors = centroids.astype(int)
    hex_colors = ['#%02x%02x%02x' % tuple(color) for color in final_colors]

    return final_colors, hex_colors

# Tampilkan palet warna di bawah gambar
def show_palette(colors, hex_colors):
    fig, ax = plt.subplots(figsize=(max(len(colors), 5), 2))
    for i, (color, hex_code) in enumerate(zip(colors, hex_colors)):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=np.array(color)/255))
        ax.text(i + 0.5, -0.2, hex_code, ha='center', va='top', fontsize=10)
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(fig)

# Streamlit UI
st.title("🎨 Dominant Color Picker")
st.write("Upload gambar dan dapatkan 5 warna dominan.")

uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar yang diupload', use_container_width=True)

    with st.spinner("Mengambil warna dominan..."):
        colors, hex_colors = manual_color_clustering(image, n_colors=5)
        st.success("Berhasil! 🎉")
        show_palette(colors, hex_colors)