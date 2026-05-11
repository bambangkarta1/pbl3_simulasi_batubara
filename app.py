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
# CUSTOM CSS
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
 
    .main .block-container { padding-top: 2rem; }
 
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
 
    .dev-credit-box {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 14px;
        padding: 14px 20px;
        margin-top: 16px;
        font-size: 0.85rem;
        line-height: 1.8;
        color: rgba(255,255,255,0.95);
    }
 
    .card {
        background: white;
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
 
    .card-blue   { border-left: 4px solid #3b82f6; background: linear-gradient(135deg,#eff6ff 0%,white 100%); }
    .card-purple { border-left: 4px solid #8b5cf6; background: linear-gradient(135deg,#f5f3ff 0%,white 100%); }
    .card-green  { border-left: 4px solid #10b981; background: linear-gradient(135deg,#ecfdf5 0%,white 100%); }
    .card-amber  { border-left: 4px solid #f59e0b; background: linear-gradient(135deg,#fffbeb 0%,white 100%); }
    .card-pink   { border-left: 4px solid #ec4899; background: linear-gradient(135deg,#fdf2f8 0%,white 100%); }
 
    .sim-panel {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 2px solid #0ea5e9;
        border-radius: 16px;
        padding: 18px 22px;
        margin: 12px 0 18px 0;
    }
 
    .sim-panel-green {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 2px solid #22c55e;
        border-radius: 16px;
        padding: 18px 22px;
        margin: 12px 0 18px 0;
    }
 
    .sim-panel-purple {
        background: linear-gradient(135deg, #faf5ff, #ede9fe);
        border: 2px solid #a855f7;
        border-radius: 16px;
        padding: 18px 22px;
        margin: 12px 0 18px 0;
    }
 
    .sim-panel-amber {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 18px 22px;
        margin: 12px 0 18px 0;
    }
 
    .sim-badge {
        display: inline-block;
        background: #0ea5e9;
        color: white;
        border-radius: 8px;
        padding: 3px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
 
    .result-pill {
        display: inline-block;
        background: white;
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        padding: 8px 16px;
        margin: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 600;
        color: #1e293b;
    }
 
    .result-pill-blue  { border-color: #3b82f6; color: #1d4ed8; background: #eff6ff; }
    .result-pill-green { border-color: #10b981; color: #065f46; background: #ecfdf5; }
    .result-pill-red   { border-color: #ef4444; color: #991b1b; background: #fef2f2; }
    .result-pill-amber { border-color: #f59e0b; color: #92400e; background: #fffbeb; }
 
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
 
    .market-card {
        border-radius: 16px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
 
    .market-pc   { background: linear-gradient(135deg,#ecfdf5,#d1fae5); border-left: 5px solid #10b981; }
    .market-oli  { background: linear-gradient(135deg,#fffbeb,#fef3c7); border-left: 5px solid #f59e0b; }
    .market-mono { background: linear-gradient(135deg,#fdf2f8,#fce7f3); border-left: 5px solid #ec4899; }
 
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
 
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
 
# =====================================
# DATA & KONSTANTA
# =====================================
 
data = pd.DataFrame({
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Production": [4143080, 3591337, 3879211, 3560069, 4187315, 4015358, 3398718, 2222091, 2227170, 2112983],
    "COGS": [1892047772700, 1609109212500, 1918470991920, 2232221611560, 2377156677000,
             2112995936000, 1783567280000, 2207269456000, 2200803424000, 2037147744000],
    "HBA": [799729, 834840, 1149610, 1405232, 1090460, 843465, 1737021, 4093384, 3040000, 1937500],
    "MC":  [132295, 512808, 1074648, -983107, 231006, 1536202, 534231, -360009, -1273092, 1433225]
})
 
INTERCEPT      = 53.99302
SLOPE          = -1.136737
CHOKE_PRICE_RP = 863888320
MC_AVG         = 283817.2
DISCOUNT_RATE  = 0.05
MUC_AWAL       = 15163
T_STAR         = 114.12
 
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
    <h1 class="hero-title" style="color:white!important;margin-top:10px;">
      Analisis Intertemporal Batubara
    </h1>
    <p class="hero-subtitle">
      Estimasi Fungsi Permintaan &amp; Efisiensi Dinamis — PT Mitrabara Adiperdana Tbk 2015–2024
    </p>
    <div class="dev-credit-box">
      <b>Dikembangkan oleh:</b><br>
      &nbsp;• Arif Hamdani (10090224008)<br>
      &nbsp;• Bambang Karta Wijaya (10090224020)<br>
      &nbsp;• Moh Bayu Mustofa (10090224030)<br><br>
      Pada mata kuliah <b>Ekonomi Sumber Daya Alam dan Lingkungan</b>
      &nbsp;·&nbsp; Di bawah bimbingan <b>Yuhka Sundaya, S.E., M.Si.</b><br>
      <span style="font-size:0.8rem;opacity:0.75;">Universitas Islam Bandung · Fakultas Ekonomi dan Bisnis · 2025</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
 
# =====================================
# TABS
# =====================================
 
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "📈 Fungsi Permintaan",
    "🏭 Mekanisme Pasar",
    "⏳ Efisiensi Dinamis",
    "🔬 Simulasi",
    "📋 Laporan"
])
 
# =====================================================================
# TAB 1 — DASHBOARD
# =====================================================================
 
with tab1:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
 
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Produksi",    f"{data['Production'].sum():,.0f} ton", "2015–2024")
    c2.metric("Rata-rata HBA",     f"Rp {data['HBA'].mean():,.0f}")
    c3.metric("Rata-rata MC",      f"Rp {MC_AVG:,.0f}")
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
            name="HBA", line=dict(color="#3b82f6", width=3), marker=dict(size=9, color="#1d4ed8")))
        fig.add_trace(go.Scatter(x=data["Year"], y=data["MC"], mode="lines+markers",
            name="MC", line=dict(color="#ec4899", width=2.5, dash="dash"), marker=dict(size=8, color="#db2777")))
        fig.update_layout(title="HBA vs Biaya Marginal (MC)", yaxis_title="Rp", **PLOT_STYLE)
        styled_axes(fig); st.plotly_chart(fig, use_container_width=True)
 
    with cr:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=data["Year"], y=data["Production"],
            marker=dict(color=data["Production"], colorscale=[[0,"#bfdbfe"],[0.5,"#3b82f6"],[1,"#1e40af"]]),
            name="Produksi"))
        fig2.update_layout(title="Volume Produksi (ton)", yaxis_title="Ton", **PLOT_STYLE)
        styled_axes(fig2); st.plotly_chart(fig2, use_container_width=True)
 
    st.markdown("### 💰 Beban Pokok Penjualan (COGS) per Tahun")
    fig_cogs = go.Figure()
    fig_cogs.add_trace(go.Bar(x=data["Year"], y=data["COGS"],
        marker=dict(color=data["COGS"], colorscale=[[0,"#c4b5fd"],[0.5,"#8b5cf6"],[1,"#4c1d95"]]), name="COGS"))
    fig_cogs.update_layout(title="Beban Pokok Penjualan 2015–2024", yaxis_title="Rp", **PLOT_STYLE)
    styled_axes(fig_cogs); st.plotly_chart(fig_cogs, use_container_width=True)
 
# =====================================================================
# TAB 2 — FUNGSI PERMINTAAN
# =====================================================================
 
with tab2:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
 
    a_d, b_d = INTERCEPT, -SLOPE
    mc_d = MC_AVG / 16000
 
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
        p_market = mc_d
        q_market = (INTERCEPT - p_market) / b_d
 
        fig_d = go.Figure()
        fig_d.add_trace(go.Scatter(x=[0, q_market, 0], y=[INTERCEPT, p_market, p_market],
            fill="toself", fillcolor="rgba(59,130,246,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"))
        fig_d.add_trace(go.Scatter(x=q_range, y=p_range, mode="lines", name="Kurva Permintaan",
            line=dict(color="#1d4ed8", width=3)))
        fig_d.add_hline(y=p_market, line_dash="dash", line_color="#ec4899",
                        annotation_text=f"MC ≈ {p_market:.4f}", annotation_font_color="#ec4899")
        fig_d.add_trace(go.Scatter(x=[q_market], y=[p_market], mode="markers",
            marker=dict(color="#1d4ed8", size=14, symbol="circle", line=dict(color="white", width=2)),
            name="Ekuilibrium"))
        fig_d.update_layout(title="Kurva Permintaan & Surplus Konsumen",
                            xaxis_title="Q", yaxis_title="P", **PLOT_STYLE)
        styled_axes(fig_d); st.plotly_chart(fig_d, use_container_width=True)
 
    st.markdown("### 📊 Biaya Marginal (MC) per Tahun")
    st.markdown("""
<div class="card card-green">
Rata-rata MC = <b>Rp 283.817,2</b> — di bawah rata-rata HBA, artinya setiap tambahan produksi masih menguntungkan secara marjinal.
</div>
""", unsafe_allow_html=True)
 
    fig_mc = go.Figure()
    fig_mc.add_trace(go.Bar(x=data["Year"], y=data["MC"],
        marker_color=["#ef4444" if v < 0 else "#3b82f6" for v in data["MC"]], name="MC"))
    fig_mc.add_hline(y=MC_AVG, line_dash="dot", line_color="#10b981",
                     annotation_text=f"Rata-rata MC = Rp {MC_AVG:,.0f}", annotation_font_color="#10b981")
    fig_mc.update_layout(title="Biaya Marginal (MC) 2015–2024", yaxis_title="Rp", **PLOT_STYLE)
    styled_axes(fig_mc); st.plotly_chart(fig_mc, use_container_width=True)
 
# =====================================================================
# TAB 3 — MEKANISME PASAR
# =====================================================================
 
with tab3:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
 
    st.markdown("""
<div class="card card-purple">
<b>Basis Analisis:</b> P = 53.99302 − 1.136737Q &nbsp;|&nbsp; MC rata-rata = Rp 283.817,2
<br>Tiga struktur pasar: Persaingan Sempurna · Oligopoli Cournot (n=3) · Monopoli
</div>
""", unsafe_allow_html=True)
 
    st.markdown("### ⚙️ Simulasi Parameter Pasar")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1: mc_pct_tab3 = st.slider("Perubahan MC (%)", -50, 150, 0, key="mc_pct_tab3")
    with col_s2: n_firms_tab3 = st.slider("Jumlah perusahaan oligopoli (n)", 2, 20, 3, key="n_firms_tab3")
    with col_s3: cp_mult_tab3 = st.slider("Choke Price multiplier (×)", 0.5, 2.0, 1.0, 0.05, key="cp_mult_tab3")
 
    a_m  = INTERCEPT
    b_m  = -SLOPE
    mc_adj = (MC_AVG / 16000) * (1 + mc_pct_tab3 / 100)
 
    q_pc    = max(0, (a_m - mc_adj) / b_m);  p_pc  = mc_adj;  cs_pc = 0.5*(a_m-p_pc)*q_pc
    q_mono  = max(0, (a_m - mc_adj) / (2*b_m)); p_mono = a_m - b_m*q_mono
    cs_mono = 0.5*(a_m-p_mono)*q_mono; ps_mono = max(0,(p_mono-mc_adj)*q_mono)
    dwl_mono = max(0, 0.5*(p_mono-mc_adj)*(q_pc-q_mono))
    n_eff   = n_firms_tab3
    q_oli   = max(0,(n_eff/(n_eff+1))*(a_m-mc_adj)/b_m); p_oli = a_m-b_m*q_oli
    cs_oli  = 0.5*(a_m-p_oli)*q_oli; ps_oli = max(0,(p_oli-mc_adj)*q_oli)
    dwl_oli = max(0, 0.5*(p_oli-mc_adj)*(q_pc-q_oli))
 
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="market-card market-pc">
<div style="font-size:1.1rem;font-weight:800;color:#065f46;margin-bottom:12px;">✅ Persaingan Sempurna</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;font-size:1.6rem;">{q_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;font-size:1.6rem;">{p_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#065f46;">{cs_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#10b981;font-size:1.3rem;">0.0000 ✓</div>
<div style="margin-top:12px;"><span class="tag tag-green">P = MC · Efisiensi Maksimal</span></div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="market-card market-oli">
<div style="font-size:1.1rem;font-weight:800;color:#92400e;margin-bottom:12px;">🔶 Oligopoli Cournot (n={n_eff})</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;font-size:1.6rem;">{q_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;font-size:1.6rem;">{p_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#b45309;">{cs_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_oli:.4f} ⚠</div>
<div style="margin-top:12px;"><span class="tag tag-amber">Antara Persaingan & Monopoli</span></div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
<div class="market-card market-mono">
<div style="font-size:1.1rem;font-weight:800;color:#9d174d;margin-bottom:12px;">⚠️ Monopoli</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;font-size:1.6rem;">{q_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;font-size:1.6rem;">{p_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#be185d;">{cs_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_mono:.4f} ⛔</div>
<div style="margin-top:12px;"><span class="tag tag-red">MR = MC · P > MC</span></div>
</div>""", unsafe_allow_html=True)
 
    st.markdown("### 📊 Grafik Detail Struktur Pasar")
    pasar_sel = st.selectbox("Pilih Struktur Pasar:", ["Persaingan Sempurna", "Oligopoli (Cournot)", "Monopoli"])
 
    if pasar_sel == "Persaingan Sempurna":
        q_eq, p_eq, cs, ps, dwl_v = q_pc, p_pc, cs_pc, 0, 0
        color_eq = "#10b981"; note = "P = MC → Efisiensi alokasi maksimal, DWL = 0"
    elif pasar_sel == "Monopoli":
        q_eq, p_eq, cs, ps, dwl_v = q_mono, p_mono, cs_mono, ps_mono, dwl_mono
        color_eq = "#ec4899"; note = "MR = MC → P > MC, timbul Deadweight Loss"
    else:
        q_eq, p_eq, cs, ps, dwl_v = q_oli, p_oli, cs_oli, ps_oli, dwl_oli
        color_eq = "#f59e0b"; note = f"Keseimbangan Cournot (n={n_eff}) — antara persaingan & monopoli"
 
    q_r = np.linspace(0, a_m / b_m * 1.05, 300)
    cg, ci = st.columns([3, 2])
    with cg:
        fig_mkt = go.Figure()
        fig_mkt.add_trace(go.Scatter(x=[0, q_eq, 0], y=[a_m, p_eq, p_eq],
            fill="toself", fillcolor="rgba(59,130,246,0.12)", line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"))
        if ps > 0:
            fig_mkt.add_trace(go.Scatter(x=[0, q_eq, q_eq, 0], y=[mc_adj, mc_adj, p_eq, p_eq],
                fill="toself", fillcolor="rgba(245,158,11,0.15)", line=dict(color="rgba(0,0,0,0)"), name="Surplus Produsen"))
        if dwl_v > 0:
            fig_mkt.add_trace(go.Scatter(x=[q_eq, q_pc, q_eq], y=[p_eq, mc_adj, mc_adj],
                fill="toself", fillcolor="rgba(239,68,68,0.25)", line=dict(color="rgba(0,0,0,0)"), name="DWL"))
        fig_mkt.add_trace(go.Scatter(x=q_r, y=a_m-b_m*q_r, mode="lines", name="Demand",
            line=dict(color="#1d4ed8", width=3)))
        if pasar_sel in ["Monopoli", "Oligopoli (Cournot)"]:
            mr_r = np.linspace(0, a_m/b_m, 300)
            fig_mkt.add_trace(go.Scatter(x=mr_r, y=a_m-2*b_m*mr_r, mode="lines", name="MR",
                line=dict(color="#f59e0b", width=2, dash="dot")))
        fig_mkt.add_hline(y=mc_adj, line_color="#6b7280", annotation_text="MC")
        fig_mkt.add_trace(go.Scatter(x=[q_eq], y=[p_eq], mode="markers",
            marker=dict(color=color_eq, size=16, symbol="star", line=dict(color="white", width=2)),
            name="Ekuilibrium"))
        fig_mkt.update_layout(title=f"Grafik {pasar_sel}<br><sub>{note}</sub>",
                              xaxis_title="Q", yaxis_title="P", **PLOT_STYLE)
        styled_axes(fig_mkt); st.plotly_chart(fig_mkt, use_container_width=True)
 
    with ci:
        st.markdown(f"""
<div class="card">
<b style="color:#1e293b;font-size:1rem;">{pasar_sel}</b>
<div style="margin-top:16px;"><div class="metric-label-text">Q Ekuilibrium</div><div class="metric-num">{q_eq:.4f}</div></div>
<div style="margin-top:12px;"><div class="metric-label-text">P Ekuilibrium</div><div class="metric-num">{p_eq:.4f}</div></div>
<div style="margin-top:12px;"><div class="metric-label-text">Surplus Konsumen</div>
<div style="font-weight:700;color:#3b82f6;font-family:'JetBrains Mono',monospace;">{cs:.4f}</div></div>
<div style="margin-top:12px;"><div class="metric-label-text">Surplus Produsen</div>
<div style="font-weight:700;color:#8b5cf6;font-family:'JetBrains Mono',monospace;">{ps:.4f}</div></div>
<div style="margin-top:12px;"><div class="metric-label-text">Total Surplus</div>
<div style="font-weight:700;color:#10b981;font-family:'JetBrains Mono',monospace;">{cs+ps:.4f}</div></div>
<div style="margin-top:12px;"><div class="metric-label-text">Deadweight Loss</div>
<div style="font-weight:700;font-family:'JetBrains Mono',monospace;color:{'#ef4444' if dwl_v>0 else '#10b981'};font-size:1.2rem;">{dwl_v:.4f}</div></div>
</div>""", unsafe_allow_html=True)
 
    st.markdown("### 📊 Perbandingan Tiga Struktur Pasar")
    fig_comp = make_subplots(rows=1, cols=3, subplot_titles=["Q Ekuilibrium", "P Ekuilibrium", "Deadweight Loss"])
    labels = ["Persaingan", "Oligopoli", "Monopoli"]; bc = ["#10b981", "#f59e0b", "#ec4899"]
    for i, vals in enumerate([[q_pc,q_oli,q_mono],[p_pc,p_oli,p_mono],[0,dwl_oli,dwl_mono]], 1):
        fig_comp.add_trace(go.Bar(x=labels, y=vals, marker_color=bc, showlegend=False), row=1, col=i)
    fig_comp.update_layout(paper_bgcolor="white", plot_bgcolor="#f8fafc",
                           font=dict(color="#1e293b"), height=340, margin=dict(t=50, b=30))
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
        st.markdown('<div class="formula-box">T* = (1/r) × ln((a − MC) / λ₀)<br>T* ≈ 114,12 tahun</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="card card-amber">
<b>Interpretasi:</b>
<ul style="margin:8px 0;padding-left:18px;font-size:0.9rem;">
<li>Cadangan optimal habis dalam <b>~114 tahun</b></li>
<li>Diskonto naik → T* turun → eksploitasi dipercepat</li>
<li>MUC = opportunity cost menggunakan SDA hari ini</li>
</ul>
</div>
""", unsafe_allow_html=True)
 
    with cr:
        t_range = np.linspace(0, 150, 300)
        muc_t   = MUC_AWAL * np.exp(DISCOUNT_RATE * t_range)
        fig_muc = go.Figure()
        fig_muc.add_trace(go.Scatter(x=t_range, y=muc_t, mode="lines", name="MUC(t) = λ₀·eʳᵗ",
            line=dict(color="#3b82f6", width=3), fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"))
        fig_muc.add_hline(y=CHOKE_PRICE_RP-MC_AVG, line_dash="dash", line_color="#ec4899",
                          annotation_text="Choke − MC", annotation_font_color="#ec4899")
        fig_muc.add_vline(x=T_STAR, line_dash="dot", line_color="#10b981",
                          annotation_text=f"T* = {T_STAR:.0f} thn", annotation_font_color="#10b981")
        fig_muc.update_layout(title="Pertumbuhan MUC Sepanjang Waktu",
                              xaxis_title="Tahun ke-", yaxis_title="MUC (Rp)", **PLOT_STYLE)
        styled_axes(fig_muc); st.plotly_chart(fig_muc, use_container_width=True)
 
    st.markdown("### 📉 Sensitivitas T* terhadap Tingkat Diskonto")
    r_range = np.linspace(0.01, 0.30, 100)
    t_star_range = (1/r_range) * np.log((CHOKE_PRICE_RP-MC_AVG)/MUC_AWAL)
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=r_range*100, y=t_star_range, mode="lines", name="T*(r)",
        line=dict(color="#8b5cf6", width=3), fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"))
    fig_ts.add_vline(x=5, line_dash="dot", line_color="#10b981",
                    annotation_text="r = 5%", annotation_font_color="#10b981")
    fig_ts.update_layout(title="T* vs Tingkat Diskonto",
                         xaxis_title="Tingkat Diskonto (%)", yaxis_title="T* (tahun)", **PLOT_STYLE)
    styled_axes(fig_ts); st.plotly_chart(fig_ts, use_container_width=True)
 
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
        p_sim    = INTERCEPT + SLOPE * prod_sim; p_sim_rp = p_sim * 16000
        c1, c2, c3 = st.columns(3)
        c1.metric("Q Input", f"{prod_sim:.1f} juta ton")
        c2.metric("P (unit skala)", f"{p_sim:.4f}")
        c3.metric("P Estimasi (Rp)", f"Rp {p_sim_rp:,.0f}")
        st.info("📌 Semakin besar produksi → harga pasar cenderung turun sesuai fungsi permintaan.")
        q_anim = np.linspace(0, 47.5, 200); p_anim = INTERCEPT + SLOPE * q_anim
        fig_anim = go.Figure()
        fig_anim.add_trace(go.Scatter(x=q_anim, y=p_anim, mode="lines", name="Kurva Permintaan",
            line=dict(color="#1d4ed8", width=3)))
        fig_anim.add_trace(go.Scatter(x=[prod_sim], y=[p_sim], mode="markers",
            marker=dict(color="#ec4899", size=16, symbol="circle", line=dict(color="white", width=2)),
            name=f"Q={prod_sim:.1f}"))
        fig_anim.add_annotation(x=prod_sim, y=p_sim, text=f"  Q={prod_sim:.1f}, P={p_sim:.3f}",
            showarrow=True, arrowhead=2, arrowcolor="#ec4899", font=dict(color="#ec4899", size=12))
        fig_anim.update_layout(title="Posisi Produksi pada Kurva Permintaan",
                               xaxis_title="Q (juta ton)", yaxis_title="P (skala)", **PLOT_STYLE)
        styled_axes(fig_anim); st.plotly_chart(fig_anim, use_container_width=True)
 
    with sim2:
        st.markdown("#### Simulasi Struktur Pasar")
        ca, cb = st.columns(2)
        with ca: n_firms = st.slider("Jumlah Perusahaan (Cournot)", 1, 20, 3)
        with cb: mc_pct_s2 = st.slider("Perubahan MC (%)", -50, 100, 0, key="sim2_mc")
        mc_adj_s2 = (MC_AVG/16000)*(1+mc_pct_s2/100); a_s, b_s = INTERCEPT, -SLOPE
        if n_firms == 1:
            q_s = max(0,(a_s-mc_adj_s2)/(2*b_s)); label = "Monopoli"
        else:
            q_s = max(0,(n_firms/(n_firms+1))*(a_s-mc_adj_s2)/b_s); label = f"Cournot (n={n_firms})"
        p_s = a_s-b_s*q_s; q_pc_s = max(0,(a_s-mc_adj_s2)/b_s)
        cs_s = 0.5*(a_s-p_s)*q_s; ps_s = max(0,(p_s-mc_adj_s2)*q_s)
        dwl_s = max(0, 0.5*(p_s-mc_adj_s2)*(q_pc_s-q_s))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Q* ({label})", f"{q_s:.3f}"); c2.metric("P* Ekuilibrium", f"{p_s:.4f}")
        c3.metric("Total Surplus", f"{cs_s+ps_s:.4f}"); c4.metric("DWL", f"{dwl_s:.4f}")
        q_r2 = np.linspace(0, a_s/b_s*1.05, 300)
        fig_s2 = go.Figure()
        fig_s2.add_trace(go.Scatter(x=q_r2, y=a_s-b_s*q_r2, mode="lines", name="Demand",
            line=dict(color="#1d4ed8", width=2.5)))
        if n_firms == 1:
            mr_r2 = np.linspace(0, a_s/(2*b_s)*1.1, 300)
            fig_s2.add_trace(go.Scatter(x=mr_r2, y=a_s-2*b_s*mr_r2, mode="lines", name="MR",
                line=dict(color="#f59e0b", width=2, dash="dot")))
        fig_s2.add_hline(y=mc_adj_s2, line_color="#6b7280", annotation_text="MC")
        fig_s2.add_trace(go.Scatter(x=[q_s], y=[p_s], mode="markers",
            marker=dict(color="#8b5cf6", size=14, symbol="star", line=dict(color="white", width=2)),
            name="Ekuilibrium"))
        fig_s2.update_layout(title=f"Simulasi {label}", xaxis_title="Q", yaxis_title="P", **PLOT_STYLE)
        styled_axes(fig_s2); st.plotly_chart(fig_s2, use_container_width=True)
 
    with sim3:
        st.markdown("#### Simulasi Waktu Habis Cadangan (T*)")
        ca, cb = st.columns(2)
        with ca:
            r_sim    = st.slider("Tingkat Diskonto (%)", 1, 30, 5) / 100
            muc0_sim = st.slider("MUC Awal (λ₀)", 5000, 100000, 15163, 1000)
        with cb:
            mc_sim_rp = st.slider("Marginal Cost (Rp)", 100000, 1000000, int(MC_AVG), 10000)
            cp_sim    = st.slider("Choke Price (juta Rp)", 500, 2000, 864, 10) * 1_000_000
        if cp_sim > mc_sim_rp and muc0_sim > 0:
            t_sim = (1/r_sim)*np.log((cp_sim-mc_sim_rp)/muc0_sim)
            delta = t_sim - T_STAR
            st.metric("T* Simulasi", f"{t_sim:.2f} tahun", delta=f"{delta:+.2f} vs baseline")
            st.success(f"✅ Cadangan habis dalam **{t_sim:.1f} tahun**")
            t_sim_range = np.linspace(0, max(150, t_sim*1.2), 300)
            muc_sim     = muc0_sim * np.exp(r_sim * t_sim_range)
            fig_sim3 = go.Figure()
            fig_sim3.add_trace(go.Scatter(x=t_sim_range, y=muc_sim, mode="lines", name="MUC(t)",
                line=dict(color="#8b5cf6", width=3), fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"))
            fig_sim3.add_hline(y=cp_sim-mc_sim_rp, line_dash="dash", line_color="#ec4899",
                               annotation_text="Choke − MC", annotation_font_color="#ec4899")
            fig_sim3.add_vline(x=t_sim, line_dash="dot", line_color="#10b981",
                               annotation_text=f"T* = {t_sim:.1f} thn", annotation_font_color="#10b981")
            fig_sim3.update_layout(title=f"Pertumbuhan MUC — T* = {t_sim:.1f} tahun",
                                   xaxis_title="Tahun ke-", yaxis_title="MUC (Rp)", **PLOT_STYLE)
            styled_axes(fig_sim3); st.plotly_chart(fig_sim3, use_container_width=True)
        else:
            st.error("⚠️ Parameter tidak valid: Choke Price harus lebih besar dari MC dan MUC₀ > 0")
 
# =====================================================================
# TAB 6 — LAPORAN (dengan Simulasi Kurva Interaktif)
# =====================================================================
 
with tab6:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
 
    # ── HEADER LAPORAN ──────────────────────────────────────────────────
    st.markdown("""
<div class="hero-banner" style="background:linear-gradient(135deg,#1e3a5f 0%,#1e40af 50%,#2563eb 100%);padding:28px 36px;">
  <div style="position:relative;z-index:1;">
    <span class="hero-badge">📋 Laporan Proyek Berbasis Pembelajaran (PBL) 3</span>
    <h2 class="hero-title" style="color:white!important;margin-top:10px;font-size:1.5rem;">
      Analisis Intertemporal dan Dinamika Alokasi Sumber Daya <i>Depletable</i>
    </h2>
    <p class="hero-subtitle">PT Mitrabara Adiperdana Tbk · Periode 2015–2024</p>
    <div class="dev-credit-box" style="margin-top:12px;">
      <b>Disusun oleh:</b> Arif Hamdani (10090224008) &nbsp;·&nbsp;
      Bambang Karta Wijaya (10090224020) &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
      <b>Dosen Pembimbing:</b> Yuhka Sundaya, S.E., M.Si.<br>
      <span style="font-size:0.78rem;opacity:0.75;">
        Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan &nbsp;·&nbsp;
        Universitas Islam Bandung &nbsp;·&nbsp; Fakultas Ekonomi dan Bisnis &nbsp;·&nbsp; 2025
      </span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
 
    st.markdown("""
<div class="card" style="display:flex;gap:10px;flex-wrap:wrap;padding:14px 18px;">
  <span class="tag tag-blue">BAB I · Pendahuluan</span>
  <span class="tag tag-purple">BAB II · Tinjauan Pustaka</span>
  <span class="tag tag-amber">BAB III · Metodologi</span>
  <span class="tag tag-green">BAB IV · Hasil & Pembahasan</span>
  <span class="tag tag-red">BAB V · Kesimpulan & Rekomendasi</span>
</div>
""", unsafe_allow_html=True)
 
    # =========================================================
    # BAB I
    # =========================================================
    st.markdown("""
<div style="margin-top:28px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#1e40af,#3b82f6);color:white;
                border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB I</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">PENDAHULUAN</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)
 
    with st.expander("1.1  Latar Belakang", expanded=True):
        st.markdown("""
<div class="card card-blue">
Batubara merupakan salah satu komoditas energi fosil yang memiliki peran strategis dalam perekonomian
Indonesia, baik sebagai sumber energi domestik maupun komoditas ekspor unggulan. Dalam perspektif
ekonomi sumber daya alam, batubara tergolong sebagai <b>sumber daya tak terbarukan (<i>depletable
resource</i>)</b> — setiap ton yang diekstraksi hari ini akan mengurangi cadangan yang tersedia untuk
generasi mendatang secara permanen.<br><br>
Pendekatan filosofis George Santayana dalam <i>The Sense of Beauty</i> mengingatkan bahwa <b>nilai</b> sebuah
komoditas bukan semata-mata ditentukan oleh kandungan fisiknya, melainkan oleh preferensi, ekspektasi,
dan cara manusia mempersepsikan kegunaan sumber daya tersebut lintas waktu.<br><br>
PT Mitrabara Adiperdana Tbk (MBAP) mengoperasikan konsesi tambang di Kalimantan Utara dengan fokus pada
batubara kalori menengah-tinggi. Selama 2015–2024, perusahaan menghadapi dinamika HBA yang sangat
fluktuatif — dari US$50/ton (2016) hingga >US$250/ton (2022).
</div>
""", unsafe_allow_html=True)
 
    with st.expander("1.2  Rumusan Masalah"):
        st.markdown("""
<div class="card card-purple">
1. <b>Bagaimana dinamika perubahan harga dan teknologi memengaruhi pergeseran status cadangan
   (<i>resource</i> ke <i>reserve</i>)?</b><br><br>
2. <b>Apakah jalur ekstraksi aktual 2015–2024 memenuhi kondisi efisiensi intertemporal (Aturan Hotelling)?</b><br><br>
3. <b>Bagaimana potensi <i>Green Paradox</i> dapat terjadi akibat rencana kebijakan lingkungan?</b>
</div>
""", unsafe_allow_html=True)
 
    with st.expander("1.3  Tujuan Penelitian"):
        st.markdown("""
<div class="card card-green">
1. Mengestimasi fungsi permintaan batubara via regresi OLS (2015–2024).<br>
2. Menurunkan biaya marginal (MC) dari laporan keuangan riil MBAP.<br>
3. Menghitung dan mengevaluasi T* berdasarkan model Hotelling dengan diskonto kontinyu.<br>
4. Menemukan pola alokasi optimal antara profitabilitas jangka pendek dan keberlanjutan.<br>
5. Menganalisis potensi <i>Green Paradox</i> dalam konteks transisi energi Indonesia.
</div>
""", unsafe_allow_html=True)
 
    # =========================================================
    # BAB II
    # =========================================================
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#5b21b6,#8b5cf6);color:white;
                border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB II</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">TINJAUAN PUSTAKA DAN LANDASAN TEORITIS</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)
 
    with st.expander("2.1  Konsep Nilai dan Ekspektasi Waktu (Perspektif Santayana)", expanded=True):
        st.markdown("""
<div class="card card-purple">
Filsuf George Santayana berpendapat bahwa <b>nilai tidak bersifat intrinsik pada objek</b>, melainkan
muncul dari interaksi antara objek dengan subjek berdasarkan preferensi dan kebutuhan. Dalam ekonomi
SDA, harga batubara bukan semata cermin kandungan kalori, melainkan <b>cermin ekspektasi kolektif pasar</b>
terhadap ketersediaan energi masa depan, kemajuan teknologi substitusi, dan risiko regulasi.<br><br>
Lonjakan HBA hingga >US$300/ton pada 2022 mencerminkan ekspektasi terhadap kelangkaan energi pasca-pandemi
dan krisis geopolitik — bukan perubahan mendasar biaya ekstraksi.
</div>
""", unsafe_allow_html=True)
 
    with st.expander("2.2  Taksonomi Cadangan (McKelvey Box)"):
        st.markdown("""
<div class="card card-blue">
 
| Kuadran | Nama | Deskripsi |
|---------|------|-----------|
| I | **Reserves** | Teridentifikasi + layak ekonomi → siap diproduksi |
| II | **Conditional Resources** | Teridentifikasi + tidak layak saat ini |
| III | **Hypothetical Resources** | Belum teridentifikasi + diperkirakan layak |
| IV | **Speculative Resources** | Belum teridentifikasi + sangat tidak pasti |
 
Batas Kuadran I dan II bersifat **dinamis** — bergeser seiring perubahan harga dan teknologi.
</div>
""", unsafe_allow_html=True)
 
    with st.expander("2.3  Model Alokasi Intertemporal dan Aturan Hotelling"):
        st.markdown(r"""
<div class="card card-amber">
 
**Aturan Hotelling** (1931): harga bersih harus tumbuh dengan laju *r*:
 
$$\frac{dP}{dt} = r \cdot P \quad \Rightarrow \quad \lambda(t) = \lambda_0 \cdot e^{rt}$$
 
**Waktu habis cadangan:**
 
$$T^* = \frac{1}{r} \ln\left(\frac{a - MC}{\lambda_0}\right) \approx 114{,}12 \text{ tahun}$$
 
</div>
""", unsafe_allow_html=True)
 
    with st.expander("2.4  Eksternalitas Lingkungan dan Green Paradox"):
        st.markdown("""
<div class="card card-pink">
<b>Green Paradox</b> (Sinn, 2008): pengumuman kebijakan lingkungan di masa depan justru
<b>mempercepat ekstraksi saat ini</b>. Produsen rasional menjual sebelum pajak berlaku →
emisi jangka pendek meningkat berlawanan dengan tujuan kebijakan.<br><br>
Solusi: kebijakan harus <b>bertahap dan kredibel</b>, bukan diumumkan mendadak dengan horizon jauh.
</div>
""", unsafe_allow_html=True)
 
    # =========================================================
    # BAB III
    # =========================================================
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#92400e,#f59e0b);color:white;
                border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB III</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">METODOLOGI PENELITIAN</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)
 
    with st.expander("3.1  Jenis dan Sumber Data", expanded=True):
        st.markdown("""
<div class="card card-amber">
 
| Jenis Data | Sumber | Periode |
|------------|--------|---------|
| Volume Produksi (ton) | Laporan Tahunan MBAP (IDX) | 2015–2024 |
| COGS (Rp) | Laporan Keuangan Audited | 2015–2024 |
| HBA | Kementerian ESDM RI | 2015–2024 |
| Tingkat Bunga (r) | Bank Indonesia | 2024 |
 
MC = (COGS_t − COGS_{t-1}) / (Q_t − Q_{t-1}) · P_model = HBA / 16.000
</div>
""", unsafe_allow_html=True)
 
    with st.expander("3.2  Tahapan Analisis"):
        st.markdown("""
<div class="card card-blue">
 
**Tahap 1** — Estimasi OLS: P = a + bQ + ε (Stata)
 
**Tahap 2** — Simulasi Spektrum Cadangan: Reserve layak jika P − MC > 0
 
**Tahap 3** — Proyeksi Hotelling: λ(t) = λ₀·eʳᵗ vs data aktual (HBA − MC)
 
**Tahap 4** — Skenario Green Paradox: dampak pengumuman pajak karbon terhadap produksi
</div>
""", unsafe_allow_html=True)
 
    with st.expander("3.3  Data Historis PT Mitrabara Adiperdana Tbk"):
        mc_table = data[["Year","Production","COGS","HBA","MC"]].copy()
        mc_table.columns = ["Tahun","Produksi (ton)","COGS (Rp)","HBA (Rp/ton)","MC (Rp/ton)"]
        st.dataframe(mc_table, use_container_width=True)
 
    # =========================================================
    # BAB IV — dengan 4 Simulasi Kurva Interaktif
    # =========================================================
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#065f46,#10b981);color:white;
                border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB IV</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">HASIL DAN PEMBAHASAN</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)
 
    # ------------------------------------------------------------------
    # 4.1 — SIMULASI KURVA PERMINTAAN INTERAKTIF
    # ------------------------------------------------------------------
    with st.expander("4.1  Estimasi Fungsi Permintaan & Simulasi Kurva", expanded=True):
        st.markdown("""
<div class="card card-green">
<b>Hasil Regresi OLS:</b> P̂ = 53,993 − 1,137·Q &nbsp;|&nbsp; R² = 0,633 &nbsp;|&nbsp; F = 13,80 &nbsp;|&nbsp; p-value Q = 0,006
</div>
""", unsafe_allow_html=True)
 
        # Panel simulasi kurva permintaan
        st.markdown('<div class="sim-panel"><span class="sim-badge">🎛️ SIMULASI KURVA PERMINTAAN</span>', unsafe_allow_html=True)
        st.markdown("Ubah parameter di bawah — kurva dan titik ekuilibrium akan bergerak secara real-time.", unsafe_allow_html=True)
 
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            lap_intercept = st.slider("Choke Price / Konstanta (a)", 20.0, 90.0, float(INTERCEPT), 0.5,
                                      key="lap_a", help="Pergeser ini menggeser kurva permintaan naik/turun")
        with sc2:
            lap_slope_abs = st.slider("Kemiringan Kurva |b|", 0.3, 3.0, abs(SLOPE), 0.05,
                                      key="lap_b", help="Makin besar → kurva makin curam (inelastis)")
        with sc3:
            lap_mc_pct = st.slider("Biaya Marginal MC (% dari baseline)", 10, 300, 100, 5,
                                   key="lap_mc", help="100% = MC baseline Rp 283.817")
        st.markdown('</div>', unsafe_allow_html=True)
 
        # Kalkulasi dinamis
        lap_b   = -lap_slope_abs
        lap_mc  = (MC_AVG / 16000) * (lap_mc_pct / 100)
        lap_q_max = lap_intercept / lap_slope_abs
        lap_q_eq  = max(0, (lap_intercept - lap_mc) / lap_slope_abs)
        lap_p_eq  = lap_mc
        lap_cs    = 0.5 * (lap_intercept - lap_p_eq) * lap_q_eq
        lap_q_orig = (INTERCEPT - MC_AVG/16000) / abs(SLOPE)
 
        q_sim = np.linspace(0, lap_q_max * 1.05, 300)
        p_sim_line = lap_intercept + lap_b * q_sim
 
        # Kurva asli (baseline)
        q_orig = np.linspace(0, INTERCEPT / abs(SLOPE) * 1.05, 300)
        p_orig_line = INTERCEPT + SLOPE * q_orig
 
        fig_lap1 = go.Figure()
 
        # Kurva baseline (abu-abu transparan)
        fig_lap1.add_trace(go.Scatter(x=q_orig, y=p_orig_line, mode="lines", name="Kurva Baseline",
            line=dict(color="#94a3b8", width=2, dash="dot"),
            opacity=0.6))
 
        # Surplus konsumen
        if lap_q_eq > 0:
            fig_lap1.add_trace(go.Scatter(
                x=[0, lap_q_eq, 0], y=[lap_intercept, lap_p_eq, lap_p_eq],
                fill="toself", fillcolor="rgba(59,130,246,0.15)",
                line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"))
 
        # Kurva simulasi
        fig_lap1.add_trace(go.Scatter(x=q_sim, y=p_sim_line, mode="lines", name="Kurva Simulasi",
            line=dict(color="#1d4ed8", width=3)))
 
        # Garis MC
        fig_lap1.add_hline(y=lap_mc, line_dash="dash", line_color="#ec4899",
                           annotation_text=f"MC = {lap_mc:.3f}", annotation_font_color="#ec4899")
 
        # Titik ekuilibrium
        if lap_q_eq > 0:
            fig_lap1.add_trace(go.Scatter(x=[lap_q_eq], y=[lap_p_eq], mode="markers",
                marker=dict(color="#1d4ed8", size=16, symbol="circle", line=dict(color="white", width=3)),
                name=f"Ekuilibrium (Q={lap_q_eq:.2f})"))
 
        # Anotasi choke price
        fig_lap1.add_annotation(x=0, y=lap_intercept, text=f"Choke P = {lap_intercept:.1f}",
            showarrow=False, xanchor="left", font=dict(color="#1d4ed8", size=11))
 
        fig_lap1.update_layout(
            title=f"Kurva Permintaan Interaktif — P = {lap_intercept:.2f} − {lap_slope_abs:.3f}·Q",
            xaxis_title="Q (Kuantitas)", yaxis_title="P (Harga Skala)", **PLOT_STYLE,
            height=420)
        styled_axes(fig_lap1)
        st.plotly_chart(fig_lap1, use_container_width=True)
 
        # Hasil metrik dinamis
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.markdown(f'<div class="result-pill result-pill-blue">Q* = {lap_q_eq:.3f}</div>', unsafe_allow_html=True)
        col_r2.markdown(f'<div class="result-pill result-pill-green">P* = {lap_p_eq:.4f}</div>', unsafe_allow_html=True)
        col_r3.markdown(f'<div class="result-pill result-pill-blue">CS = {lap_cs:.4f}</div>', unsafe_allow_html=True)
        col_r4.markdown(f'<div class="result-pill result-pill-amber">Q maks = {lap_q_max:.2f}</div>', unsafe_allow_html=True)
 
        pergeseran = lap_q_eq - lap_q_orig
        arah = "↑ naik" if pergeseran > 0 else "↓ turun"
        warna = "green" if pergeseran > 0 else "red"
        st.markdown(f"""
<div class="card card-amber" style="margin-top:8px;padding:12px 18px;">
📌 <b>Interpretasi Pergeseran:</b> Dibanding baseline, titik ekuilibrium bergeser
<span style="color:{'#065f46' if pergeseran>0 else '#991b1b'};font-weight:700;">
{arah} sebesar {abs(pergeseran):.3f} unit Q</span>.
{'Kurva lebih datar → permintaan lebih elastis.' if lap_slope_abs < abs(SLOPE) else
 'Kurva lebih curam → permintaan lebih inelastis.' if lap_slope_abs > abs(SLOPE) else
 'Kemiringan sama dengan baseline.'}
</div>
""", unsafe_allow_html=True)
 
        # Tabel regresi
        regresi_df = pd.DataFrame({
            "Variabel": ["Q (Kuantitas Produksi)", "Konstanta (_cons)"],
            "Koefisien": [-1.136737, 53.99302],
            "Std. Error": [0.306004, 10.48285],
            "t-statistik": [-3.71, 5.15],
            "P>|t|": [0.006, 0.001],
        })
        st.dataframe(regresi_df, use_container_width=True)
 
    # ------------------------------------------------------------------
    # 4.2 — SIMULASI PERGESERAN SPEKTRUM CADANGAN
    # ------------------------------------------------------------------
    with st.expander("4.2  Analisis Pergeseran Spektrum Cadangan"):
 
        st.markdown('<div class="sim-panel-green"><span class="sim-badge" style="background:#22c55e;">🎛️ SIMULASI SPEKTRUM CADANGAN</span>', unsafe_allow_html=True)
        st.markdown("Geser harga dan biaya untuk melihat berapa banyak tahun masuk kategori Reserve vs Resource.", unsafe_allow_html=True)
 
        sg1, sg2 = st.columns(2)
        with sg1:
            hba_mult = st.slider("Skenario Harga HBA (× dari aktual)", 0.3, 2.5, 1.0, 0.05,
                                 key="spec_hba", help="1.0 = harga aktual; <1 = harga turun; >1 = harga naik")
        with sg2:
            mc_level = st.slider("Skenario MC (Rp/ton)", 50000, 2000000, int(MC_AVG), 50000,
                                 key="spec_mc", help="Ubah biaya marjinal untuk melihat dampak ke status cadangan")
        st.markdown('</div>', unsafe_allow_html=True)
 
        status_data = data.copy()
        status_data["HBA_sim"]    = status_data["HBA"] * hba_mult
        status_data["Margin_sim"] = status_data["HBA_sim"] - mc_level
        status_data["Status"]     = status_data["Margin_sim"].apply(
            lambda x: "✅ Reserve" if x > 0 else "⚠️ Resource")
        status_data["Margin_awal"] = status_data["HBA"] - MC_AVG
 
        n_reserve  = (status_data["Status"] == "✅ Reserve").sum()
        n_resource = (status_data["Status"] == "⚠️ Resource").sum()
 
        sm1, sm2, sm3 = st.columns(3)
        sm1.metric("Tahun sebagai Reserve",  f"{n_reserve} / 10")
        sm2.metric("Tahun sebagai Resource", f"{n_resource} / 10")
        sm3.metric("MC Skenario", f"Rp {mc_level:,.0f}")
 
        # Grafik batang margin
        colors_bar = ["#10b981" if v > 0 else "#ef4444" for v in status_data["Margin_sim"]]
        fig_spec = go.Figure()
        fig_spec.add_trace(go.Bar(
            x=status_data["Year"], y=status_data["Margin_sim"],
            marker_color=colors_bar, name="Margin Simulasi (HBA_sim − MC_sim)",
            text=[f"{'✅' if v>0 else '⚠️'} Rp {v:,.0f}" for v in status_data["Margin_sim"]],
            textposition="outside"))
        # Margin baseline
        fig_spec.add_trace(go.Scatter(
            x=status_data["Year"], y=status_data["Margin_awal"], mode="lines+markers",
            name="Margin Baseline", line=dict(color="#94a3b8", width=2, dash="dot"),
            marker=dict(size=7)))
        fig_spec.add_hline(y=0, line_color="#1e293b", line_width=2)
        fig_spec.update_layout(
            title=f"Margin (HBA×{hba_mult:.2f} − MC Rp {mc_level:,.0f}) per Tahun",
            xaxis_title="Tahun", yaxis_title="Margin (Rp/ton)", **PLOT_STYLE, height=400)
        styled_axes(fig_spec)
        st.plotly_chart(fig_spec, use_container_width=True)
 
        st.dataframe(status_data[["Year","HBA","HBA_sim","Margin_sim","Status"]].rename(
            columns={"Year":"Tahun","HBA":"HBA Aktual","HBA_sim":"HBA Simulasi",
                     "Margin_sim":"Margin (Rp/ton)","Status":"Status Cadangan"}),
            use_container_width=True)
 
    # ------------------------------------------------------------------
    # 4.3 — SIMULASI UJI HOTELLING INTERAKTIF
    # ------------------------------------------------------------------
    with st.expander("4.3  Evaluasi Efisiensi Intertemporal (Uji Hotelling)"):
 
        st.markdown('<div class="sim-panel-purple"><span class="sim-badge" style="background:#a855f7;">🎛️ SIMULASI JALUR HOTELLING</span>', unsafe_allow_html=True)
        st.markdown("Ubah parameter untuk melihat bagaimana jalur MUC bergerak dan T* berubah.", unsafe_allow_html=True)
 
        sh1, sh2, sh3 = st.columns(3)
        with sh1:
            hot_r     = st.slider("Tingkat Diskonto r (%)", 1, 25, 5, 1, key="hot_r") / 100
        with sh2:
            hot_muc0  = st.slider("MUC Awal λ₀ (Rp)", 1000, 100000, 15163, 1000, key="hot_muc0")
        with sh3:
            hot_cp_mc = st.slider("Choke − MC (juta Rp)", 100, 2000, int((CHOKE_PRICE_RP-MC_AVG)/1e6), 10,
                                  key="hot_cpmc") * 1_000_000
        st.markdown('</div>', unsafe_allow_html=True)
 
        if hot_muc0 > 0 and hot_cp_mc > 0:
            hot_t_star = (1 / hot_r) * np.log(hot_cp_mc / hot_muc0)
            t_max_plot = max(200, hot_t_star * 1.4)
            t_hot = np.linspace(0, t_max_plot, 500)
            muc_hot = hot_muc0 * np.exp(hot_r * t_hot)
 
            # Data aktual HBA - MC
            hba_mc_actual = data["HBA"] - MC_AVG
            t_actual      = data["Year"] - data["Year"].min()
 
            hm1, hm2, hm3 = st.columns(3)
            hm1.metric("T* Simulasi", f"{hot_t_star:.1f} tahun",
                       delta=f"{hot_t_star - T_STAR:+.1f} vs baseline")
            hm2.metric("Tahun Cadangan Habis", f"~{2025 + int(hot_t_star)}")
            hm3.metric("MUC pada T*", f"Rp {hot_muc0 * np.exp(hot_r * hot_t_star):,.0f}")
 
            fig_hot = go.Figure()
            # Area MUC
            fig_hot.add_trace(go.Scatter(x=t_hot, y=muc_hot, mode="lines",
                name=f"MUC(t) = {hot_muc0:,}·e^({hot_r:.2f}t)",
                line=dict(color="#8b5cf6", width=3),
                fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"))
 
            # Kurva baseline (abu-abu)
            muc_base = MUC_AWAL * np.exp(DISCOUNT_RATE * t_hot)
            fig_hot.add_trace(go.Scatter(x=t_hot, y=muc_base, mode="lines",
                name="MUC Baseline (r=5%, λ₀=15.163)",
                line=dict(color="#94a3b8", width=2, dash="dot"), opacity=0.7))
 
            # Garis Choke-MC
            fig_hot.add_hline(y=hot_cp_mc, line_dash="dash", line_color="#ec4899",
                              annotation_text=f"Choke−MC = Rp {hot_cp_mc/1e6:.0f}jt",
                              annotation_font_color="#ec4899")
 
            # Garis T*
            fig_hot.add_vline(x=hot_t_star, line_dash="dot", line_color="#10b981",
                              annotation_text=f"T* = {hot_t_star:.1f} thn",
                              annotation_font_color="#10b981")
            # T* baseline
            fig_hot.add_vline(x=T_STAR, line_dash="dot", line_color="#94a3b8",
                              annotation_text=f"T* baseline = {T_STAR:.0f}",
                              annotation_font_color="#94a3b8", annotation_position="bottom right")
 
            # Data aktual
            fig_hot.add_trace(go.Scatter(x=t_actual, y=hba_mc_actual, mode="markers+lines",
                name="HBA − MC Aktual", marker=dict(color="#f59e0b", size=10, symbol="diamond"),
                line=dict(color="#f59e0b", width=1.5, dash="dash")))
 
            fig_hot.update_layout(
                title=f"Jalur MUC Hotelling — T* = {hot_t_star:.1f} tahun (r={hot_r*100:.0f}%)",
                xaxis_title="Tahun ke-", yaxis_title="MUC / Harga Bersih (Rp)",
                **PLOT_STYLE, height=440)
            styled_axes(fig_hot)
            st.plotly_chart(fig_hot, use_container_width=True)
 
            st.markdown(f"""
<div class="card card-amber">
💡 <b>Interpretasi:</b> Pada r = {hot_r*100:.0f}% dan λ₀ = Rp {hot_muc0:,},
cadangan optimal habis dalam <b>{hot_t_star:.1f} tahun</b> (~tahun {2025+int(hot_t_star)}).
Data aktual HBA−MC (titik kuning) {'<b>berada di atas jalur Hotelling</b> → indikasi underpricing relatif atau ekspektasi rente tinggi' if hba_mc_actual.mean() > hot_muc0 * np.exp(hot_r * 5) else '<b>mendekati jalur Hotelling</b> → ekstraksi mendekati kondisi efisien'}.
</div>
""", unsafe_allow_html=True)
 
            # Tabel sensitivitas
            r_vals = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
            t_vals = [(1/r)*np.log(hot_cp_mc/hot_muc0) for r in r_vals]
            sens_df = pd.DataFrame({
                "r": [f"{int(r*100)}%"   for r in r_vals],
                "T* (tahun)": [f"{t:.1f}" for t in t_vals],
                "Habis ~Tahun": [f"~{2025+int(t)}" for t in t_vals],
                "MUC t=10": [f"Rp {hot_muc0*np.exp(r*10):,.0f}" for r in r_vals]
            })
            st.markdown("**Tabel Sensitivitas T\* terhadap berbagai r (dengan λ₀ dan Choke−MC dari slider):**")
            st.dataframe(sens_df, use_container_width=True)
 
    # ------------------------------------------------------------------
    # 4.4 — SIMULASI GREEN PARADOX INTERAKTIF
    # ------------------------------------------------------------------
    with st.expander("4.4  Analisis Distorsi Pasar dan Green Paradox"):
 
        st.markdown('<div class="sim-panel-amber"><span class="sim-badge" style="background:#f59e0b;color:#1e293b;">🎛️ SIMULASI GREEN PARADOX</span>', unsafe_allow_html=True)
        st.markdown("Simulasikan dampak pengumuman pajak karbon terhadap keputusan produksi perusahaan.", unsafe_allow_html=True)
 
        gp1, gp2, gp3 = st.columns(3)
        with gp1:
            gp_tax_rp   = st.slider("Besaran Pajak Karbon (Rp/ton)", 0, 1000000, 300000, 25000,
                                    key="gp_tax", help="Pajak yang direncanakan berlaku di masa depan")
        with gp2:
            gp_t_announce = st.slider("Tahun Pajak Berlaku (tahun ke-)", 1, 20, 5, 1,
                                      key="gp_ta", help="Berapa tahun dari sekarang pajak mulai berlaku")
        with gp3:
            gp_accel = st.slider("Percepatan Produksi Sblm Pajak (%)", 0, 100, 30, 5,
                                 key="gp_acc", help="Berapa % produksi dipercepat sebelum pajak berlaku")
        st.markdown('</div>', unsafe_allow_html=True)
 
        # Baseline produksi
        baseline_prod = data["Production"].mean()
        years_future  = list(range(2025, 2045))
        prod_baseline = [baseline_prod] * len(years_future)
        prod_accel    = []
        emisi_baseline = []
        emisi_accel    = []
 
        for i, yr in enumerate(years_future):
            t_rel = yr - 2025
            if t_rel < gp_t_announce:
                # Sebelum pajak → produksi dipercepat
                p = baseline_prod * (1 + gp_accel/100)
            else:
                # Setelah pajak → produksi turun (cadangan terkuras + efek pajak)
                sisa_rasio = max(0, 1 - (gp_accel/100) * (gp_t_announce / max(1, 20-gp_t_announce)))
                p = baseline_prod * sisa_rasio * max(0.3, 1 - (gp_tax_rp / 2000000))
            prod_accel.append(p)
            emisi_baseline.append(baseline_prod * 2.5 / 1e9)   # ton CO2 (faktor konversi sederhana)
            emisi_accel.append(p * 2.5 / 1e9)
 
        gpm1, gpm2, gpm3 = st.columns(3)
        total_emisi_baseline = sum(emisi_baseline)
        total_emisi_accel    = sum(emisi_accel)
        delta_emisi = total_emisi_accel - total_emisi_baseline
        gpm1.metric("Total Emisi Baseline", f"{total_emisi_baseline:.2f} Gt CO₂")
        gpm2.metric("Total Emisi + Green Paradox", f"{total_emisi_accel:.2f} Gt CO₂",
                    delta=f"+{delta_emisi:.2f} Gt" if delta_emisi > 0 else f"{delta_emisi:.2f} Gt")
        gpm3.metric("Produksi Puncak (sblm pajak)",
                    f"{max(prod_accel)/1e6:.2f} juta ton")
 
        fig_gp = make_subplots(rows=1, cols=2,
                               subplot_titles=["Volume Produksi (ton)", "Emisi CO₂ Kumulatif (Gt)"])
 
        # Produksi
        fig_gp.add_trace(go.Scatter(x=years_future, y=prod_baseline, mode="lines",
            name="Baseline", line=dict(color="#3b82f6", width=2.5, dash="dot")), row=1, col=1)
        colors_gp = ["#ef4444" if yr < 2025 + gp_t_announce else "#10b981" for yr in years_future]
        fig_gp.add_trace(go.Bar(x=years_future, y=prod_accel, name="Dengan Green Paradox",
            marker_color=colors_gp, opacity=0.85), row=1, col=1)
        fig_gp.add_vline(x=2025 + gp_t_announce - 0.5, line_dash="dash", line_color="#f59e0b",
                         annotation_text=f"Pajak berlaku {2025+gp_t_announce}",
                         annotation_font_color="#f59e0b", row=1, col=1)
 
        # Emisi kumulatif
        emisi_cum_base  = np.cumsum(emisi_baseline)
        emisi_cum_accel = np.cumsum(emisi_accel)
        fig_gp.add_trace(go.Scatter(x=years_future, y=emisi_cum_base, mode="lines",
            name="Emisi Baseline", line=dict(color="#3b82f6", width=2.5)), row=1, col=2)
        fig_gp.add_trace(go.Scatter(x=years_future, y=emisi_cum_accel, mode="lines",
            name="Emisi + Paradox", line=dict(color="#ef4444", width=2.5),
            fill="tonexty", fillcolor="rgba(239,68,68,0.1)"), row=1, col=2)
 
        fig_gp.update_layout(
            paper_bgcolor="white", plot_bgcolor="#f8fafc",
            font=dict(color="#1e293b", family="Plus Jakarta Sans"),
            height=400, margin=dict(t=55, b=40, l=55, r=20),
            legend=dict(bgcolor="white", bordercolor="#e2e8f0", borderwidth=1))
        fig_gp.update_xaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1")
        fig_gp.update_yaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1")
        st.plotly_chart(fig_gp, use_container_width=True)
 
        paradoks_pct = (delta_emisi / total_emisi_baseline * 100) if total_emisi_baseline > 0 else 0
        st.markdown(f"""
<div class="card card-pink" style="margin-top:8px;">
⚠️ <b>Green Paradox Terdeteksi:</b> Pengumuman pajak Rp {gp_tax_rp:,}/ton yang berlaku
{gp_t_announce} tahun ke depan memicu percepatan produksi {gp_accel}% selama periode pra-pajak.
Akibatnya emisi kumulatif 2025–2044 <b>{'naik' if delta_emisi>0 else 'turun'} {abs(paradoks_pct):.1f}%</b>
dibanding skenario tanpa akselerasi — {'paradoks langsung bertentangan dengan tujuan kebijakan!' if delta_emisi>0 else 'kebijakan berhasil mitigasi paradoks.'}
</div>
""", unsafe_allow_html=True)
 
    # =========================================================
    # BAB V
    # =========================================================
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#991b1b,#ef4444);color:white;
                border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB V</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">KESIMPULAN DAN REKOMENDASI (STRATEGIC POLICY)</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)
 
    with st.expander("5.1  Kesimpulan", expanded=True):
        st.markdown("""
<div class="card" style="border-left:4px solid #ef4444;background:linear-gradient(135deg,#fff1f2,white);">
 
**1. Fungsi Permintaan dan Dinamika Harga**
Estimasi OLS: P = 53,993 − 1,137Q (R² = 0,633). Choke Price = Rp 863.888.320/ton.
Fluktuasi HBA tidak sepenuhnya mengikuti jalur Hotelling — guncangan eksternal mendominasi jangka pendek.
 
**2. Efisiensi Alokasi Sumber Daya**
MC rata-rata (Rp 283.817/ton) < HBA rata-rata → produksi efisien secara marjinal.
T* ≈ 114 tahun → potensi keberlanjutan panjang pada r = 5%.
 
**3. Negosiasi Nilai Lintas Waktu (Perspektif Santayana)**
Persepsi dan ekspektasi — bukan hanya biaya-manfaat terukur — membentuk pola alokasi aktual.
Lonjakan 2022 mencerminkan ekspektasi "kelangkaan energi", bukan perubahan biaya fundamental.
 
**4. Risiko Green Paradox**
Kebijakan lingkungan yang tidak kredibel/tiba-tiba berpotensi memicu race to extract —
meningkatkan emisi jangka pendek berlawanan dengan tujuan kebijakan.
 
</div>
""", unsafe_allow_html=True)
 
    with st.expander("5.2  Rekomendasi / Kebijakan Solutif"):
        st.markdown("""
<div class="card" style="border-left:4px solid #ef4444;background:linear-gradient(135deg,#fff1f2,white);">
 
**Untuk Pemerintah:**
 
**R1 — Pajak Karbon Bertahap & Transparan**
Mulai Rp 30.000/ton CO₂ (2025), naik Rp 10.000/tahun → mengurangi insentif race to extract.
 
**R2 — Cap-and-Trade Nasional**
Kuota produksi nasional + sistem perdagangan izin → eliminasi struktural insentif akselerasi.
 
**R3 — Windfall Tax Selektif**
Saat HBA > US$150/ton, pajak windfall 20–30% untuk mendanai transisi energi.
 
**Untuk PT Mitrabara Adiperdana Tbk:**
 
**R4 — Diversifikasi ke Hilir dan EBT**
Investasi dari windfall 2021–2022 ke gasifikasi batubara, energi surya/PLTA.
 
**R5 — Rencanakan pada Social Discount Rate (~3%)**
Perpanjang T* → jaga nilai cadangan untuk generasi mendatang + pertahankan license to operate.
 
**R6 — Transparansi ESG & Shadow Price Karbon**
Integrasikan shadow price karbon ke laporan keberlanjutan untuk investor ESG.
 
</div>
""", unsafe_allow_html=True)
 
    # ── DAFTAR PUSTAKA ──────────────────────────────────────────────────
    with st.expander("Daftar Pustaka"):
        st.markdown("""
<div class="card card-blue" style="font-size:0.88rem;line-height:2.0;">
 
**Buku & Artikel Ilmiah:**
- Hotelling, H. (1931). *The Economics of Exhaustible Resources*. Journal of Political Economy, 39(2), 137–175.
- Sinn, H.W. (2008). *Public Policies against Global Warming: A Supply Side Approach*. International Tax and Public Finance, 15(4), 360–394.
- Santayana, G. (1896). *The Sense of Beauty*. Charles Scribner's Sons.
- Tietenberg, T. & Lewis, L. (2018). *Environmental and Natural Resource Economics* (11th ed.). Routledge.
- Field, B.C. & Field, M.K. (2016). *Environmental Economics: An Introduction* (7th ed.). McGraw-Hill.
 
**Data & Laporan:**
- PT Mitrabara Adiperdana Tbk. (2015–2024). *Laporan Tahunan*. IDX: MBAP.
- Kementerian ESDM RI. (2015–2024). *Harga Batubara Acuan (HBA) Bulanan*.
- Bank Indonesia. (2024). *Laporan Kebijakan Moneter*.
- IEA. (2023). *Coal 2023 — Analysis and Forecast to 2026*.
- IPCC. (2022). *Sixth Assessment Report (AR6) — WG III: Mitigation of Climate Change*.
 
</div>
""", unsafe_allow_html=True)
 
    # ── FOOTER ─────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#1e293b,#334155);border-radius:16px;
            padding:20px 28px;margin-top:28px;text-align:center;color:#94a3b8;
            font-size:0.82rem;line-height:2;">
  <b style="color:#e2e8f0;font-size:0.95rem;">PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</b><br>
  Arif Hamdani (10090224008) &nbsp;·&nbsp; Bambang Karta Wijaya (10090224020)
  &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
  Dosen Pembimbing: <b style="color:#cbd5e1;">Yuhka Sundaya, S.E., M.Si.</b>
  &nbsp;·&nbsp; Universitas Islam Bandung &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
 
# =====================================
# FOOTER GLOBAL
# =====================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#94a3b8;font-size:0.82rem;padding:16px 0;line-height:1.9;">
  <b style="color:#64748b;">PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</b><br>
  Dikembangkan oleh: Arif Hamdani (10090224008) &nbsp;·&nbsp;
  Bambang Karta Wijaya (10090224020) &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
  Di bawah bimbingan <b style="color:#64748b;">Yuhka Sundaya, S.E., M.Si.</b>
  &nbsp;·&nbsp; Universitas Islam Bandung &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)