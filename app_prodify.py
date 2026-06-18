import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.optimize import linprog

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

st.set_page_config(
    page_title="PRODIFY",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 PRODIFY")
st.subheader("Prediksi dan Optimasi Produktivitas Harian Mahasiswa")

# ==================================================
# LOAD DATA
# ==================================================

data = pd.read_csv("prodify_dummy_data.csv")

X = data[
    [
        "jam_tidur",
        "jam_fokus",
        "distraksi_hp",
        "olahraga",
        "kafein",
        "mood",
        "deadline",
    ]
]

y = data["skor_produktivitas"]

model = LinearRegression()
model.fit(X, y)

# ==================================================
# SIDEBAR INPUT
# ==================================================

st.sidebar.header("📝 Input Aktivitas Harian")

jam_tidur = st.sidebar.slider(
    "Jam Tidur",
    0.0,
    12.0,
    7.0
)

jam_fokus = st.sidebar.slider(
    "Jam Fokus",
    0.0,
    12.0,
    4.0
)

distraksi_hp = st.sidebar.slider(
    "Distraksi HP",
    0.0,
    10.0,
    2.0
)

olahraga = st.sidebar.slider(
    "Olahraga",
    0.0,
    3.0,
    1.0
)

kafein = st.sidebar.slider(
    "Konsumsi Kafein",
    0,
    5,
    1
)

mood = st.sidebar.slider(
    "Mood",
    1,
    10,
    7
)

deadline = st.sidebar.selectbox(
    "Ada Deadline?",
    ["Tidak", "Ya"]
)

deadline_num = 1 if deadline == "Ya" else 0

# ==================================================
# PREDIKSI
# ==================================================

pred = model.predict(
    [[
        jam_tidur,
        jam_fokus,
        distraksi_hp,
        olahraga,
        kafein,
        mood,
        deadline_num
    ]]
)[0]

pred = max(0, min(100, pred))

# ==================================================
# METRIC
# ==================================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Produktivitas",
        f"{pred:.1f}/100"
    )

with c2:
    st.metric(
        "Jam Fokus",
        f"{jam_fokus:.1f} jam"
    )

with c3:
    st.metric(
        "Mood",
        f"{mood}/10"
    )

# ==================================================
# STATUS PRODUKTIVITAS
# ==================================================

st.subheader("📊 Status Produktivitas")

if pred >= 85:
    st.success(
        "🔥 Produktivitas Anda sangat tinggi."
    )

elif pred >= 70:
    st.success(
        "✅ Produktivitas Anda berada pada kategori baik."
    )

elif pred >= 55:
    st.warning(
        "⚠️ Produktivitas Anda cukup baik namun masih dapat ditingkatkan."
    )

else:
    st.error(
        "🚨 Produktivitas Anda masih rendah dan perlu perhatian."
    )

# ==================================================
# RINGKASAN
# ==================================================

st.subheader("📋 Ringkasan Hari Ini")

if pred >= 80:
    st.write(
        """
        Pola aktivitas Anda secara umum sudah mendukung
        produktivitas yang optimal. Pertahankan kebiasaan
        baik yang sudah dilakukan.
        """
    )

elif pred >= 60:
    st.write(
        """
        Produktivitas Anda cukup baik, namun masih terdapat
        beberapa faktor yang dapat diperbaiki agar hasilnya
        lebih optimal.
        """
    )

else:
    st.write(
        """
        Beberapa kebiasaan harian masih menghambat produktivitas.
        Fokus utama yang perlu diperhatikan adalah manajemen waktu,
        kualitas istirahat, dan pengurangan distraksi.
        """
    )

# ==================================================
# FAKTOR UTAMA
# ==================================================

st.subheader("🔍 Faktor yang Terdeteksi")

if jam_tidur < 6:
    st.info(
        "😴 Durasi tidur berada di bawah rekomendasi sehingga dapat menurunkan konsentrasi."
    )

if distraksi_hp > 4:
    st.info(
        "📱 Distraksi HP cukup tinggi dan berpotensi mengurangi efektivitas belajar."
    )

if mood < 5:
    st.info(
        "😊 Mood yang rendah dapat mempengaruhi motivasi dan fokus."
    )

if olahraga < 0.5:
    st.info(
        "🏃 Aktivitas fisik masih rendah dan dapat mempengaruhi energi harian."
    )

if jam_fokus >= 6:
    st.success(
        "🎯 Jam fokus yang tinggi menjadi faktor utama yang mendukung produktivitas."
    )

# ==================================================
# OPTIMASI WAKTU
# ==================================================

st.subheader("⚡ Rekomendasi Pembagian Waktu")

if pred >= 80:
    fokus_target = 5
    hiburan_max = 2

elif pred >= 60:
    fokus_target = 6
    hiburan_max = 1.5

else:
    fokus_target = 7
    hiburan_max = 1

c = [-5, -1, -2, 3]

A_eq = [[1, 1, 1, 1]]
b_eq = [10]

A_ub = [
    [1, 0, 0, 0],
    [0, 0, 0, 1]
]

b_ub = [
    fokus_target,
    hiburan_max
]

bounds = [
    (0, None),
    (1, None),
    (0.5, 2),
    (0, None)
]

res = linprog(
    c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds
)

if res.success:

    fokus, istirahat, olahraga_opt, hiburan = res.x

    a, b, c, d = st.columns(4)

    a.metric(
        "Fokus",
        f"{fokus:.1f} jam"
    )

    b.metric(
        "Istirahat",
        f"{istirahat:.1f} jam"
    )

    c.metric(
        "Olahraga",
        f"{olahraga_opt:.1f} jam"
    )

    d.metric(
        "Hiburan",
        f"{hiburan:.1f} jam"
    )

# ==================================================
# REKOMENDASI
# ==================================================

st.subheader("🎯 Rekomendasi Hari Ini")

rekomendasi = []

if jam_tidur < 6:
    rekomendasi.append(
        "Tambahkan durasi tidur menjadi 7–8 jam."
    )

if distraksi_hp > 4:
    rekomendasi.append(
        "Kurangi penggunaan HP saat jam belajar."
    )

if olahraga < 0.5:
    rekomendasi.append(
        "Luangkan minimal 30 menit untuk olahraga ringan."
    )

if mood < 5:
    rekomendasi.append(
        "Sisihkan waktu untuk relaksasi dan menjaga suasana hati."
    )

if jam_fokus < 4:
    rekomendasi.append(
        "Tambahkan sesi fokus belajar secara bertahap."
    )

if len(rekomendasi) == 0:
    st.success(
        "Pertahankan pola aktivitas saat ini karena sudah cukup mendukung produktivitas."
    )
else:
    for item in rekomendasi:
        st.write(f"• {item}")

# ==================================================
# POTENSI PENINGKATAN
# ==================================================

st.subheader("📈 Potensi Peningkatan")

st.write(
    """
    Berdasarkan pola aktivitas yang dimasukkan,
    peningkatan kualitas tidur, pengurangan distraksi digital,
    dan konsistensi waktu fokus berpotensi meningkatkan
    produktivitas harian secara lebih optimal.
    """
)

# ==================================================
# VISUALISASI
# ==================================================

st.subheader("📊 Hubungan Jam Fokus dan Produktivitas")

st.scatter_chart(
    data,
    x="jam_fokus",
    y="skor_produktivitas"
)

# ==================================================
# DATA
# ==================================================

with st.expander("Lihat Data Dummy"):
    st.dataframe(data)