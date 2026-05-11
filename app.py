import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Analisis Intertemporal Batubara",
    page_icon="⛏️",
    layout="wide"
)

# =====================================
# HEADER
# =====================================

st.title("Analisis Intertemporal Sumber Daya Batubara")

st.subheader(
    "PBL 3 - Ekonomi Sumber Daya Alam dan Lingkungan"
)

# =====================================
# IDENTITAS
# =====================================

with st.container():

    st.markdown("""
### Kelompok 6

**Arif Hamdani** — 10090224008

**Bambang Karta Wijaya** — 10090224020

**Moh Bayu Mustofa** — 10090224030

---

### Universitas
Universitas Islam Bandung

### Dosen Pengampu
YUHKA SUNDAYA, S.E., M.Si.
""")

# =====================================
# LOAD DATA
# =====================================

data = pd.read_csv(
    "data/coal_data.csv"
)

# =====================================
# DASHBOARD METRIC
# =====================================

st.header("Dashboard Perusahaan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Produksi",
    f"{data['Production'].sum():,.0f} Ton"
)

col2.metric(
    "Rata-rata HBA",
    f"Rp {data['HBA'].mean():,.0f}"
)

col3.metric(
    "Rata-rata MC",
    f"Rp {data['MC'].mean():,.0f}"
)

# =====================================
# DATAFRAME
# =====================================

st.subheader("Data Perusahaan")

st.dataframe(
    data,
    use_container_width=True
)

# =====================================
# SIMULASI HARGA
# =====================================

st.header("Simulasi Harga Batubara")

selected_year = st.selectbox(
    "Pilih Tahun",
    data["Year"]
)

production = st.slider(
    "Jumlah Produksi",
    1000000,
    5000000,
    3000000,
    step=100000
)

price = 53.99302 - (
    1.136737 * (production / 100000)
)

st.metric(
    "Harga Simulasi",
    f"{price:.2f}"
)

st.info(
    "Semakin besar produksi, harga cenderung turun."
)

# =====================================
# SIMULASI DISKONTO
# =====================================

st.header("Efisiensi Dinamis")

discount_rate = st.slider(
    "Tingkat Diskonto (%)",
    1,
    30,
    5
)

muc = (
    data["HBA"].mean() -
    data["MC"].mean()
)

future_value = muc * (
    (1 + discount_rate / 100) ** 10
)

col4, col5 = st.columns(2)

col4.metric(
    "Marginal User Cost",
    f"Rp {muc:,.0f}"
)

col5.metric(
    "Future Scarcity Value",
    f"Rp {future_value:,.0f}"
)

# =====================================
# SIMULASI DATA EKONOMI
# =====================================

st.header("Simulasi Data Ekonomi")

# Slider perubahan HBA
hba_change = st.slider(
    "Perubahan Harga HBA (%)",
    -50,
    100,
    0
)

# Slider perubahan produksi
production_change = st.slider(
    "Perubahan Produksi (%)",
    -50,
    100,
    0
)

# Slider perubahan MC
mc_change = st.slider(
    "Perubahan MC (%)",
    -50,
    100,
    0
)

# =====================================
# COPY DATA
# =====================================

sim_data = data.copy()

# =====================================
# SIMULASI PERUBAHAN
# =====================================

sim_data["HBA"] = (
    sim_data["HBA"] *
    (1 + hba_change / 100)
)

sim_data["Production"] = (
    sim_data["Production"] *
    (1 + production_change / 100)
)

sim_data["MC"] = (
    sim_data["MC"] *
    (1 + mc_change / 100)
)

# =====================================
# DATA HASIL SIMULASI
# =====================================

st.subheader("Data Setelah Simulasi")

st.dataframe(
    sim_data,
    use_container_width=True
)

# =====================================
# GRAFIK HBA
# =====================================

st.subheader("Grafik Harga Batubara")

fig_hba = px.line(
    sim_data,
    x="Year",
    y="HBA",
    markers=True
)

st.plotly_chart(
    fig_hba,
    use_container_width=True
)

# =====================================
# GRAFIK PRODUKSI
# =====================================

st.subheader("Grafik Produksi")

fig_prod = px.bar(
    sim_data,
    x="Year",
    y="Production"
)

st.plotly_chart(
    fig_prod,
    use_container_width=True
)

# =====================================
# GRAFIK MC
# =====================================

st.subheader("Grafik Marginal Cost")

fig_mc = px.line(
    sim_data,
    x="Year",
    y="MC",
    markers=True
)

st.plotly_chart(
    fig_mc,
    use_container_width=True
)

# =====================================
# SCATTER PLOT
# =====================================

st.subheader("Hubungan Produksi dan Harga")

import plotly.graph_objects as go

fig_scatter = go.Figure()

for year in sim_data["Year"].unique():
    df_year = sim_data[sim_data["Year"] == year]
    fig_scatter.add_trace(go.Scatter(
        x=df_year["Production"],
        y=df_year["HBA"],
        mode="markers",
        name=str(year),
        marker=dict(
            size=df_year["MC"] / df_year["MC"].max() * 30 + 5
        )
    ))

fig_scatter.update_layout(
    xaxis_title="Production",
    yaxis_title="HBA"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)