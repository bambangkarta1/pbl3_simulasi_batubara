import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="PBL 3 - Analisis Batubara",
    page_icon="⛏️",
    layout="wide"
)

# =====================================
# CUSTOM CSS — Light & Vibrant Theme
# =====================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(145deg, #f0f4ff 0%, #fff7ed 50%, #f0fdf4 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        color: #1e293b !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 50%, #db2777 100%);
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .hero-banner::before {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.07);
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        bottom: -40px; left: 40%;
        width: 160px; height: 160px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        margin: 0 0 16px 0;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .card {
        background: white;
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }

    .card-blue  { border-left: 4px solid #3b82f6; background: linear-gradient(135deg,#eff6ff 0%,white 100%); }
    .card-purple{ border-left: 4px solid #8b5cf6; background: linear-gradient(135deg,#f5f3ff 0%,white 100%); }
    .card-green { border-left: 4px solid #10b981; background: linear-gradient(135deg,#ecfdf5 0%,white 100%); }
    .card-amber { border-left: 4px solid #f59e0b; background: linear-gradient(135deg,#fffbeb 0%,white 100%); }
    .card-pink  { border-left: 4px solid #ec4899; background: linear-gradient(135deg,#fdf2f8 0%,white 100%); }

    .metric-box {
        background: white;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e40af;
        display: block;
    }

    .metric-label-text {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }

    .formula-box {
        background: #1e293b;
        border-radius: 12px;
        padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #7dd3fc;
        margin: 12px 0;
        border-left: 4px solid #3b82f6;
    }

    .tag { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    .tag-blue   { background: #dbeafe; color: #1d4ed8; }
    .tag-green  { background: #d1fae5; color: #065f46; }
    .tag-red    { background: #fee2e2; color: #991b1b; }
    .tag-amber  { background: #fef3c7; color: #92400e; }
    .tag-purple { background: #ede9fe; color: #5b21b6; }

    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        border-radius: 3px;
        margin: 24px 0 20px 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        border-radius: 12px;
        padding: 6px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
    }

    div[data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================
# DATA PT MITRABARA ADIPERDANA TBK
# =====================================

data = pd.DataFrame({
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Production": [4143080, 3591337, 3879211, 3560069, 4187315, 4015358, 3398718, 2222091, 2227170, 2112983],
    "COGS": [1892047772700, 1609109212500, 1918470991920, 2232221611560, 2377156677000,
             2112995936000, 1783567280000, 2207269456000, 2200803424000, 2037147744000],
    "HBA": [799729, 834840, 1149610, 1405232, 1090460, 843465, 1737021, 4093384, 3040000, 1937500],
    "MC": [132295, 512808, 1074648, -983107, 231006, 1536202, 534231, -360009, -1273092, 1433225]
})

INTERCEPT    = 53.99302
SLOPE        = -1.136737
CHOKE_PRICE_RP = 863888320
MC_AVG       = 283817.2
DISCOUNT_RATE = 0.05
MUC_AWAL     = 15163
T_STAR       = 114.12

PLOT_STYLE = dict(
    paper_bgcolor="white",
    plot_bgcolor="#f8fafc",
    font=dict(color="#1e293b", family="Plus Jakarta Sans"),
    margin=dict(t=55, b=40, l=55, r=20),
    legend=dict(bgcolor="white", bordercolor="#e2e8f0", borderwidth=1)
)

def styled_axes(fig):
    fig.update_xaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1", zerolinecolor="#e2e8f0")
    fig.update_yaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1", zerolinecolor="#e2e8f0")
    return fig

# =====================================
# HERO BANNER
# =====================================

st.markdown("""
<div class="hero-banner">
  <div style="position:relative;z-index:1;">
    <span class="hero-badge">⛏️ PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</span>
    <h1 class="hero-title" style="color:white!important;margin-top:14px;">
      Analisis Intertemporal Batubara
    </h1>
    <p class="hero-subtitle">
      Estimasi Fungsi Permintaan &amp; Efisiensi Dinamis — PT Mitrabara Adiperdana Tbk 2015–2024
    </p>
    <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:0.82rem;opacity:0.9;margin-top:6px;">
      <span>👤 Arif Hamdani — 10090224008</span>
      <span>👤 Bambang Karta Wijaya — 10090224020</span>
      <span>👤 Moh Bayu Mustofa — 10090224030</span>
    </div>
    <div style="margin-top:8px;font-size:0.78rem;opacity:0.7;">
      Universitas Islam Bandung &nbsp;·&nbsp; Dosen: YUHKA SUNDAYA, S.E., M.Si.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================
# TABS
# =====================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", "📈 Fungsi Permintaan",
    "🏭 Mekanisme Pasar", "⏳ Efisiensi Dinamis", "🔬 Simulasi"
])

# =====================================================================
# TAB 1 — DASHBOARD
# =====================================================================

with tab1:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Produksi", f"{data['Production'].sum():,.0f} ton", "2015–2024")
    c2.metric("Rata-rata HBA", f"Rp {data['HBA'].mean():,.0f}")
    c3.metric("Rata-rata MC", f"Rp {MC_AVG:,.0f}")
    c4.metric("T* Habis Cadangan", f"{T_STAR:.0f} tahun")

    st.markdown("### 📋 Data Historis Perusahaan")
    dd = data.copy()
    dd["COGS"]       = dd["COGS"].apply(lambda x: f"Rp {x:,.0f}")
    dd["HBA"]        = dd["HBA"].apply(lambda x: f"Rp {x:,.0f}")
    dd["MC"]         = dd["MC"].apply(lambda x: f"Rp {x:,.0f}")
    dd["Production"] = dd["Production"].apply(lambda x: f"{x:,.0f}")
    dd.columns = ["Tahun", "Produksi (ton)", "Beban Pokok", "HBA", "MC"]
    st.dataframe(dd, use_container_width=True)

    cl, cr = st.columns(2)
    with cl:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Year"], y=data["HBA"], mode="lines+markers",
                                 name="HBA", line=dict(color="#3b82f6", width=3),
                                 marker=dict(size=9, color="#1d4ed8")))
        fig.add_trace(go.Scatter(x=data["Year"], y=data["MC"], mode="lines+markers",
                                 name="MC", line=dict(color="#ec4899", width=2.5, dash="dash"),
                                 marker=dict(size=8, color="#db2777")))
        fig.update_layout(title="HBA vs Biaya Marginal (MC)", yaxis_title="Rp", **PLOT_STYLE)
        styled_axes(fig)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=data["Year"], y=data["Production"],
            marker=dict(color=data["Production"],
                        colorscale=[[0,"#bfdbfe"],[0.5,"#3b82f6"],[1,"#1e40af"]]),
            name="Produksi"
        ))
        fig2.update_layout(title="Volume Produksi (ton)", yaxis_title="Ton", **PLOT_STYLE)
        styled_axes(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# =====================================================================
# TAB 2 — FUNGSI PERMINTAAN
# =====================================================================

with tab2:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    a, b = INTERCEPT, -SLOPE
    mc = MC_AVG / 16000

    cl, cr = st.columns([1, 1])
    with cl:
        st.markdown('<div class="card card-blue"><b style="color:#1e40af;">📐 Hasil Regresi OLS (Stata)</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">P = 53.99302 − 1.136737 × Q</div>', unsafe_allow_html=True)

        s1, s2 = st.columns(2)
        s1.markdown('<div class="metric-box"><span class="metric-num">0.6330</span><span class="metric-label-text">R-squared</span></div>', unsafe_allow_html=True)
        s2.markdown('<div class="metric-box"><span class="metric-num">13.80</span><span class="metric-label-text">F-statistic</span></div>', unsafe_allow_html=True)

        st.markdown("""
<div class="card card-amber" style="margin-top:12px;">
<b>Interpretasi:</b><br>
<span class="tag tag-blue">Koef. Q = −1.137</span> Harga turun tiap tambah 1 unit Q<br><br>
<span class="tag tag-purple">Choke Price</span> 53.99302 × Rp16.000 = <b>Rp 863.888.320</b><br><br>
<span class="tag tag-green">Q maks</span> Saat P=0, Q = <b>47,50 unit</b><br><br>
<span class="tag tag-amber">Signifikansi</span> p-value Q = 0.006, konstanta = 0.001
</div>
""", unsafe_allow_html=True)

    with cr:
        q_range = np.linspace(0, 47.5, 200)
        p_range = INTERCEPT + SLOPE * q_range
        p_market = mc
        q_market = (INTERCEPT - p_market) / b

        fig_d = go.Figure()
        fig_d.add_trace(go.Scatter(
            x=[0, q_market, 0], y=[INTERCEPT, p_market, p_market],
            fill="toself", fillcolor="rgba(59,130,246,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"
        ))
        fig_d.add_trace(go.Scatter(
            x=q_range, y=p_range, mode="lines", name="Kurva Permintaan",
            line=dict(color="#1d4ed8", width=3)
        ))
        fig_d.add_hline(y=p_market, line_dash="dash", line_color="#ec4899",
                        annotation_text=f"MC ≈ {p_market:.4f}", annotation_font_color="#ec4899")
        fig_d.add_trace(go.Scatter(
            x=[q_market], y=[p_market], mode="markers",
            marker=dict(color="#1d4ed8", size=14, symbol="circle", line=dict(color="white",width=2)),
            name="Ekuilibrium"
        ))
        fig_d.update_layout(title="Kurva Permintaan & Surplus Konsumen",
                             xaxis_title="Q", yaxis_title="P", **PLOT_STYLE)
        styled_axes(fig_d)
        st.plotly_chart(fig_d, use_container_width=True)

    st.markdown("### 📊 Biaya Marginal (MC) per Tahun")
    st.markdown("""
<div class="card card-green">
Rata-rata MC = <b>Rp 283.817,2</b> — di bawah rata-rata HBA, artinya setiap tambahan produksi masih menguntungkan secara marjinal.
MC negatif beberapa tahun mengindikasikan efisiensi biaya atau anomali data laporan keuangan.
</div>
""", unsafe_allow_html=True)

    fig_mc = go.Figure()
    fig_mc.add_trace(go.Bar(
        x=data["Year"], y=data["MC"],
        marker_color=["#ef4444" if v < 0 else "#3b82f6" for v in data["MC"]],
        name="MC"
    ))
    fig_mc.add_hline(y=MC_AVG, line_dash="dot", line_color="#10b981",
                     annotation_text=f"Rata-rata MC = Rp {MC_AVG:,.0f}", annotation_font_color="#10b981")
    fig_mc.update_layout(title="Biaya Marginal (MC) 2015–2024", yaxis_title="Rp", **PLOT_STYLE)
    styled_axes(fig_mc)
    st.plotly_chart(fig_mc, use_container_width=True)

# =====================================================================
# TAB 3 — MEKANISME PASAR
# =====================================================================

with tab3:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    a_m, b_m, mc_m = INTERCEPT, -SLOPE, MC_AVG / 16000

    q_pc   = (a_m - mc_m) / b_m
    p_pc   = mc_m
    cs_pc  = 0.5 * (a_m - p_pc) * q_pc

    q_mono  = (a_m - mc_m) / (2 * b_m)
    p_mono  = a_m - b_m * q_mono
    cs_mono = 0.5 * (a_m - p_mono) * q_mono
    ps_mono = (p_mono - mc_m) * q_mono
    dwl_mono = 0.5 * (p_mono - mc_m) * (q_pc - q_mono)

    n = 3
    q_oli  = (n / (n + 1)) * (a_m - mc_m) / b_m
    p_oli  = a_m - b_m * q_oli
    cs_oli = 0.5 * (a_m - p_oli) * q_oli
    ps_oli = (p_oli - mc_m) * q_oli
    dwl_oli = 0.5 * (p_oli - mc_m) * (q_pc - q_oli)

    st.markdown("""
<div class="card card-purple">
<b>Basis Analisis:</b> P = 53.99302 − 1.136737Q &nbsp;|&nbsp; MC rata-rata = Rp 283.817,2
<br>Tiga struktur pasar: Persaingan Sempurna · Oligopoli Cournot (n=3) · Monopoli
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="card card-green">
<div style="font-size:1.1rem;font-weight:800;color:#065f46;margin-bottom:8px;">✅ Persaingan Sempurna</div>
<div class="metric-label-text">Q Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;">{q_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">P Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;">{p_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#065f46;">{cs_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Deadweight Loss</div>
<div style="font-weight:700;color:#10b981;font-size:1.2rem;">0.0000</div>
<div style="margin-top:10px;"><span class="tag tag-green">P = MC · Efisiensi Maksimal</span></div>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
<div class="card card-amber">
<div style="font-size:1.1rem;font-weight:800;color:#92400e;margin-bottom:8px;">🔶 Oligopoli Cournot (n=3)</div>
<div class="metric-label-text">Q Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;">{q_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">P Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;">{p_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#b45309;">{cs_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Deadweight Loss</div>
<div style="font-weight:700;color:#ef4444;font-size:1.2rem;">{dwl_oli:.4f}</div>
<div style="margin-top:10px;"><span class="tag tag-amber">Antara Persaingan & Monopoli</span></div>
</div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
<div class="card card-pink">
<div style="font-size:1.1rem;font-weight:800;color:#9d174d;margin-bottom:8px;">⚠️ Monopoli</div>
<div class="metric-label-text">Q Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;">{q_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">P Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;">{p_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#be185d;">{cs_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:8px;">Deadweight Loss</div>
<div style="font-weight:700;color:#ef4444;font-size:1.2rem;">{dwl_mono:.4f}</div>
<div style="margin-top:10px;"><span class="tag tag-red">MR = MC · P &gt; MC</span></div>
</div>""", unsafe_allow_html=True)

    st.markdown("### 📊 Grafik Detail Struktur Pasar")
    pasar_sel = st.selectbox("Pilih Struktur Pasar:", ["Persaingan Sempurna", "Oligopoli (Cournot)", "Monopoli"])

    if pasar_sel == "Persaingan Sempurna":
        q_eq, p_eq, cs, ps, dwl_v = q_pc, p_pc, cs_pc, 0, 0
        color_eq, color_fill = "#10b981", "rgba(16,185,129,0.15)"
        note = "P = MC → Efisiensi alokasi maksimal, DWL = 0"
    elif pasar_sel == "Monopoli":
        q_eq, p_eq, cs, ps, dwl_v = q_mono, p_mono, cs_mono, ps_mono, dwl_mono
        color_eq, color_fill = "#ec4899", "rgba(236,72,153,0.12)"
        note = "MR = MC → P > MC, timbul Deadweight Loss"
    else:
        q_eq, p_eq, cs, ps, dwl_v = q_oli, p_oli, cs_oli, ps_oli, dwl_oli
        color_eq, color_fill = "#f59e0b", "rgba(245,158,11,0.12)"
        note = "Keseimbangan Cournot (n=3) — antara persaingan & monopoli"

    q_r = np.linspace(0, a_m / b_m * 1.05, 300)

    cg, ci = st.columns([3, 2])
    with cg:
        fig_mkt = go.Figure()
        fig_mkt.add_trace(go.Scatter(
            x=[0, q_eq, 0], y=[a_m, p_eq, p_eq],
            fill="toself", fillcolor="rgba(59,130,246,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"
        ))
        if ps > 0:
            fig_mkt.add_trace(go.Scatter(
                x=[0, q_eq, q_eq, 0], y=[mc_m, mc_m, p_eq, p_eq],
                fill="toself", fillcolor=color_fill,
                line=dict(color="rgba(0,0,0,0)"), name="Surplus Produsen"
            ))
        if dwl_v > 0:
            fig_mkt.add_trace(go.Scatter(
                x=[q_eq, q_pc, q_eq], y=[p_eq, mc_m, mc_m],
                fill="toself", fillcolor="rgba(239,68,68,0.25)",
                line=dict(color="rgba(0,0,0,0)"), name="DWL"
            ))
        fig_mkt.add_trace(go.Scatter(
            x=q_r, y=a_m - b_m*q_r, mode="lines", name="Demand",
            line=dict(color="#1d4ed8", width=3)
        ))
        if pasar_sel in ["Monopoli", "Oligopoli (Cournot)"]:
            mr_r = np.linspace(0, a_m / b_m, 300)
            fig_mkt.add_trace(go.Scatter(
                x=mr_r, y=a_m - 2*b_m*mr_r, mode="lines", name="MR",
                line=dict(color="#f59e0b", width=2, dash="dot")
            ))
        fig_mkt.add_hline(y=mc_m, line_color="#6b7280", annotation_text="MC")
        fig_mkt.add_trace(go.Scatter(
            x=[q_eq], y=[p_eq], mode="markers",
            marker=dict(color=color_eq, size=16, symbol="star", line=dict(color="white",width=2)),
            name="Ekuilibrium"
        ))
        fig_mkt.update_layout(
            title=f"Grafik {pasar_sel}<br><sub>{note}</sub>",
            xaxis_title="Q", yaxis_title="P", **PLOT_STYLE
        )
        styled_axes(fig_mkt)
        st.plotly_chart(fig_mkt, use_container_width=True)

    with ci:
        st.markdown(f"""
<div class="card" style="height:100%;">
<b style="color:#1e293b;font-size:1rem;">{pasar_sel}</b>
<div style="margin-top:16px;">
  <div class="metric-label-text">Q Ekuilibrium</div>
  <div class="metric-num">{q_eq:.4f}</div>
</div>
<div style="margin-top:12px;">
  <div class="metric-label-text">P Ekuilibrium</div>
  <div class="metric-num">{p_eq:.4f}</div>
</div>
<div style="margin-top:12px;">
  <div class="metric-label-text">Surplus Konsumen</div>
  <div style="font-weight:700;color:#3b82f6;font-family:'JetBrains Mono',monospace;">{cs:.4f}</div>
</div>
<div style="margin-top:12px;">
  <div class="metric-label-text">Surplus Produsen</div>
  <div style="font-weight:700;color:#8b5cf6;font-family:'JetBrains Mono',monospace;">{ps:.4f}</div>
</div>
<div style="margin-top:12px;">
  <div class="metric-label-text">Total Surplus</div>
  <div style="font-weight:700;color:#10b981;font-family:'JetBrains Mono',monospace;">{cs+ps:.4f}</div>
</div>
<div style="margin-top:12px;">
  <div class="metric-label-text">Deadweight Loss</div>
  <div style="font-weight:700;font-family:'JetBrains Mono',monospace;color:{'#ef4444' if dwl_v>0 else '#10b981'};font-size:1.2rem;">{dwl_v:.4f}</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("### 📊 Perbandingan Tiga Struktur Pasar")
    fig_comp = make_subplots(rows=1, cols=3,
                             subplot_titles=["Q Ekuilibrium","P Ekuilibrium","Deadweight Loss"])
    labels = ["Persaingan","Oligopoli","Monopoli"]
    bc = ["#10b981","#f59e0b","#ec4899"]
    for i, vals in enumerate([[q_pc,q_oli,q_mono],[p_pc,p_oli,p_mono],[0,dwl_oli,dwl_mono]], 1):
        fig_comp.add_trace(go.Bar(x=labels, y=vals, marker_color=bc, showlegend=False), row=1, col=i)
    fig_comp.update_layout(paper_bgcolor="white", plot_bgcolor="#f8fafc",
                            font=dict(color="#1e293b"), height=340, margin=dict(t=50,b=30))
    for i in range(1,4):
        fig_comp.update_xaxes(gridcolor="#e2e8f0", row=1, col=i)
        fig_comp.update_yaxes(gridcolor="#e2e8f0", row=1, col=i)
    st.plotly_chart(fig_comp, use_container_width=True)

# =====================================================================
# TAB 4 — EFISIENSI DINAMIS
# =====================================================================

with tab4:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
<div class="card card-blue">
<b style="color:#1e40af;font-size:1rem;">📐 Parameter Model Efisiensi Dinamis</b>
<table style="width:100%;margin-top:12px;font-size:0.9rem;color:#1e293b;border-collapse:collapse;">
<tr><td style="padding:6px 0;color:#64748b;">Choke Price (a)</td><td><b>Rp 863.888.320</b></td></tr>
<tr><td style="padding:6px 0;color:#64748b;">Marginal Cost (MC)</td><td><b>Rp 283.817,2</b></td></tr>
<tr><td style="padding:6px 0;color:#64748b;">Tingkat Diskonto (r)</td><td><b>5% (0,05)</b></td></tr>
<tr><td style="padding:6px 0;color:#64748b;">MUC Awal (λ₀)</td><td><b>15.163</b></td></tr>
<tr><td style="padding:6px 0;color:#64748b;">T* Waktu Habis</td><td><b style="color:#1e40af;font-size:1.1rem;">≈ 114,12 tahun</b></td></tr>
</table>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="formula-box">T* = (1/r) × ln((a − MC) / λ₀)<br>T* = (1/0.0475) × ln((863.888.320 − 283.817,2) / 15.163)<br>T* ≈ 114,12 tahun</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="card card-amber">
<b>Interpretasi:</b>
<ul style="margin:8px 0;padding-left:18px;font-size:0.9rem;color:#1e293b;">
<li>Cadangan optimal habis dalam <b>~114 tahun</b></li>
<li>Diskonto naik → T* turun → eksploitasi dipercepat</li>
<li>MUC = opportunity cost menggunakan SDA hari ini</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with cr:
        r = DISCOUNT_RATE
        t_range = np.linspace(0, 150, 300)
        muc_t = MUC_AWAL * np.exp(r * t_range)

        fig_muc = go.Figure()
        fig_muc.add_trace(go.Scatter(
            x=t_range, y=muc_t, mode="lines", name="MUC(t) = λ₀·eʳᵗ",
            line=dict(color="#3b82f6", width=3),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"
        ))
        fig_muc.add_hline(y=CHOKE_PRICE_RP - MC_AVG, line_dash="dash", line_color="#ec4899",
                          annotation_text="Choke − MC", annotation_font_color="#ec4899")
        fig_muc.add_vline(x=T_STAR, line_dash="dot", line_color="#10b981",
                          annotation_text=f"T* = {T_STAR:.0f} thn", annotation_font_color="#10b981")
        fig_muc.update_layout(title="Pertumbuhan MUC Sepanjang Waktu",
                               xaxis_title="Tahun ke-", yaxis_title="MUC (Rp)", **PLOT_STYLE)
        styled_axes(fig_muc)
        st.plotly_chart(fig_muc, use_container_width=True)

    st.markdown("### 📉 Sensitivitas T* terhadap Tingkat Diskonto")
    r_range = np.linspace(0.01, 0.30, 100)
    t_star_range = (1 / r_range) * np.log((CHOKE_PRICE_RP - MC_AVG) / MUC_AWAL)

    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=r_range * 100, y=t_star_range, mode="lines", name="T*(r)",
        line=dict(color="#8b5cf6", width=3),
        fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"
    ))
    fig_ts.add_vline(x=5, line_dash="dot", line_color="#10b981",
                     annotation_text="r = 5%", annotation_font_color="#10b981")
    fig_ts.update_layout(title="T* vs Tingkat Diskonto",
                          xaxis_title="Tingkat Diskonto (%)", yaxis_title="T* (tahun)", **PLOT_STYLE)
    styled_axes(fig_ts)
    st.plotly_chart(fig_ts, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("MUC Saat Ini (t=0)", f"Rp {MUC_AWAL:,.0f}")
    c2.metric("MUC t=10 tahun",     f"Rp {MUC_AWAL * np.exp(DISCOUNT_RATE*10):,.0f}")
    c3.metric("MUC t=50 tahun",     f"Rp {MUC_AWAL * np.exp(DISCOUNT_RATE*50):,.0f}")

# =====================================================================
# TAB 5 — SIMULASI
# =====================================================================

with tab5:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    sim1, sim2, sim3 = st.tabs(["📉 Simulasi Harga", "🏭 Simulasi Pasar", "⏳ Simulasi T*"])

    with sim1:
        st.markdown("#### Simulasi Fungsi Permintaan")
        prod_sim = st.slider("Jumlah Produksi (juta ton)", 1.0, 6.0, 3.5, 0.1)
        p_sim = INTERCEPT + SLOPE * prod_sim
        p_sim_rp = p_sim * 16000
        c1, c2, c3 = st.columns(3)
        c1.metric("Q Input", f"{prod_sim:.1f} juta ton")
        c2.metric("P (unit skala)", f"{p_sim:.4f}")
        c3.metric("P Estimasi (Rp)", f"Rp {p_sim_rp:,.0f}")
        st.info("📌 Semakin besar produksi → harga pasar cenderung turun sesuai fungsi permintaan.")

    with sim2:
        st.markdown("#### Simulasi Struktur Pasar")
        ca, cb = st.columns(2)
        with ca:
            n_firms = st.slider("Jumlah Perusahaan (Cournot)", 1, 20, 3)
        with cb:
            mc_pct = st.slider("Perubahan MC (%)", -50, 100, 0)

        mc_adj = (MC_AVG / 16000) * (1 + mc_pct / 100)
        a_s, b_s = INTERCEPT, -SLOPE
        q_s = (a_s - mc_adj) / (2 * b_s) if n_firms == 1 else (n_firms/(n_firms+1))*(a_s-mc_adj)/b_s
        p_s = a_s - b_s * q_s
        label = "Monopoli" if n_firms == 1 else f"Cournot (n={n_firms})"
        q_pc_s = (a_s - mc_adj) / b_s
        cs_s   = 0.5 * (a_s - p_s) * q_s
        ps_s   = (p_s - mc_adj) * q_s
        dwl_s  = 0.5 * (p_s - mc_adj) * (q_pc_s - q_s) if p_s > mc_adj else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Q* ({label})", f"{q_s:.3f}")
        c2.metric("P* Ekuilibrium", f"{p_s:.4f}")
        c3.metric("Total Surplus", f"{cs_s+ps_s:.4f}")
        c4.metric("DWL", f"{dwl_s:.4f}")

        q_r2 = np.linspace(0, a_s/b_s*1.05, 300)
        fig_s2 = go.Figure()
        fig_s2.add_trace(go.Scatter(x=q_r2, y=a_s-b_s*q_r2, mode="lines",
                                    name="Demand", line=dict(color="#1d4ed8", width=2.5)))
        if n_firms == 1:
            mr_r2 = np.linspace(0, a_s/(2*b_s)*1.1, 300)
            fig_s2.add_trace(go.Scatter(x=mr_r2, y=a_s-2*b_s*mr_r2, mode="lines",
                                        name="MR", line=dict(color="#f59e0b", width=2, dash="dot")))
        fig_s2.add_hline(y=mc_adj, line_color="#6b7280", annotation_text="MC")
        fig_s2.add_trace(go.Scatter(x=[q_s], y=[p_s], mode="markers",
                                    marker=dict(color="#8b5cf6", size=14, symbol="star",
                                                line=dict(color="white",width=2)), name="Ekuilibrium"))
        fig_s2.update_layout(title=f"Simulasi {label}", xaxis_title="Q", yaxis_title="P", **PLOT_STYLE)
        styled_axes(fig_s2)
        st.plotly_chart(fig_s2, use_container_width=True)

    with sim3:
        st.markdown("#### Simulasi Waktu Habis Cadangan (T*)")
        ca, cb = st.columns(2)
        with ca:
            r_sim   = st.slider("Tingkat Diskonto (%)", 1, 30, 5) / 100
            muc0_sim = st.slider("MUC Awal (λ₀)", 5000, 100000, 15163, 1000)
        with cb:
            mc_sim_rp = st.slider("Marginal Cost (Rp)", 100000, 1000000, int(MC_AVG), 10000)
            cp_sim    = st.slider("Choke Price (juta Rp)", 500, 2000, 864, 10) * 1_000_000

        if cp_sim > mc_sim_rp and muc0_sim > 0:
            t_sim = (1 / r_sim) * np.log((cp_sim - mc_sim_rp) / muc0_sim)
            st.metric("T* Simulasi", f"{t_sim:.2f} tahun", delta=f"{t_sim - T_STAR:.2f} vs baseline")
            st.success(f"✅ Cadangan habis dalam **{t_sim:.1f} tahun** dengan parameter tersebut.")
        else:
            st.error("⚠️ Parameter tidak valid: Choke Price harus lebih besar dari MC dan MUC₀ > 0")

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.8rem;padding:16px 0;">
  PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp;
  Universitas Islam Bandung &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)