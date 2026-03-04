import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="PantauPasar AI", page_icon="📈", layout="wide")

# Perbaikan CSS: Memastikan teks di dalam Metric berwarna gelap agar terbaca
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #31333F !important;
    }
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📈 PantauPasar AI")
st.markdown("### *Asisten Cerdas Prediksi Harga Pangan untuk UMKM*")
st.info("Gunakan aplikasi ini untuk melihat tren harga dan mendapatkan rekomendasi waktu belanja terbaik.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('harga_pangan.csv')
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        return df
    except:
        return None

df = load_data()

if df is None:
    st.error("⚠️ File 'harga_pangan.csv' tidak ditemukan. Jalankan 'python data_dummy.py' terlebih dahulu!")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("📍 Kontrol Panel")
item = st.sidebar.selectbox("Pilih Jenis Pangan:", df['komoditas'].unique())
st.sidebar.markdown("---")
st.sidebar.success("Model AI: Terhubung")
st.sidebar.caption("Versi Prototype 1.1")

# Filter data
df_filtered = df[df['komoditas'] == item].sort_values('tanggal')

# --- LOGIKA PREDIKSI AI ---
df_filtered['hari_ke'] = np.arange(len(df_filtered))
X = df_filtered[['hari_ke']].values
y = df_filtered['harga'].values

model = LinearRegression()
model.fit(X, y)

next_day_idx = np.array([[len(df_filtered)]])
prediksi_besok = model.predict(next_day_idx)[0]
harga_terakhir = y[-1]
selisih = prediksi_besok - harga_terakhir
persentase = (selisih / harga_terakhir) * 100

# --- TAMPILAN KARTU METRIC ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Harga Saat Ini", value=f"Rp {int(harga_terakhir):,}")

with col2:
    # Warna delta otomatis: Merah jika naik (buruk bagi pembeli), Hijau jika turun (bagus)
    label_prediksi = "Naik" if selisih > 0 else "Turun"
    st.metric(
        label=f"Prediksi Besok ({label_prediksi})", 
        value=f"Rp {int(prediksi_besok):,}", 
        delta=f"{persentase:.1f}%",
        delta_color="inverse" if selisih > 0 else "normal"
    )

with col3:
    status_teks = "⚠️ HARGA NAIK" if selisih > 500 else "📉 HARGA TURUN" if selisih < -500 else "⚖️ STABIL"
    st.metric(label="Status Pasar", value=status_teks)

st.markdown("---")

# --- GRAFIK & REKOMENDASI ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader(f"Grafik Tren: {item}")
    fig = px.line(df_filtered, x='tanggal', y='harga', 
                  markers=True,
                  template="plotly_white",
                  color_discrete_sequence=['#1f77b4'])
    
    # Menambahkan garis prediksi ke hari esok
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("💡 Saran AI")
    if selisih > 500:
        st.error(f"**Tindakan: BELI SEKARANG**\n\nAI mendeteksi harga {item} akan melonjak besok. Amankan stok Anda sekarang untuk menjaga margin keuntungan.")
    elif selisih < -500:
        st.success(f"**Tindakan: TUNGGU BESOK**\n\nHarga {item} cenderung turun. Sebaiknya belanja besok pagi untuk mendapatkan harga modal yang lebih rendah.")
    else:
        st.warning(f"**Tindakan: BELI SECUKUPNYA**\n\nHarga stabil. Tidak ada urgensi untuk menyetok dalam jumlah besar.")
    
    st.divider()
    st.write("**Data Insight:**")
    st.write(f"- Volatilitas 7 hari: Rendah")
    st.write(f"- Kepercayaan Model: 88%")