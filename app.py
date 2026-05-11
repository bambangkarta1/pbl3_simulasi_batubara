import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

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

    .animated-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        font-weight: 700;
        transition: all 0.3s ease;
    }

    footer {visibility: hidden;}

    .unisba-logo-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 12px;
    }

    .sim-result-box {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        margin-top: 12px;
    }

    .highlight-green { color: #065f46; font-weight: 700; }
    .highlight-red   { color: #991b1b; font-weight: 700; }
    .highlight-amber { color: #92400e; font-weight: 700; }
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

INTERCEPT         = 53.99302
SLOPE             = -1.136737
CHOKE_PRICE_RP    = 863888320
MC_AVG            = 283817.2
DISCOUNT_RATE     = 0.05
MUC_AWAL          = 15163
T_STAR            = 114.12

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
# UNISBA LOGO (SVG inline)
# =====================================

UNISBA_LOGO_B64 = "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"

# =====================================
# HERO BANNER
# =====================================

st.markdown(f"""
<div class="hero-banner">
  <div style="position:relative;z-index:1;">
    <div class="unisba-logo-wrap">
      <img src="data:image/png;base64,{UNISBA_LOGO_B64}" style="width:72px;height:72px;border-radius:50%;object-fit:cover;background:white;" alt="Logo Universitas Islam Bandung">
      <div>
        <span class="hero-badge">⛏️ PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</span>
        <h1 class="hero-title" style="color:white!important;margin-top:10px;">
          Analisis Intertemporal Batubara
        </h1>
        <p class="hero-subtitle">
          Estimasi Fungsi Permintaan &amp; Efisiensi Dinamis — PT Mitrabara Adiperdana Tbk 2015–2024
        </p>
      </div>
    </div>
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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Fungsi Permintaan",
    "🏭 Mekanisme Pasar",
    "⏳ Efisiensi Dinamis",
    "🔬 Simulasi"
])

# =====================================================================
# TAB 1 — DASHBOARD
# =====================================================================

with tab1:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Produksi",      f"{data['Production'].sum():,.0f} ton", "2015–2024")
    c2.metric("Rata-rata HBA",       f"Rp {data['HBA'].mean():,.0f}")
    c3.metric("Rata-rata MC",        f"Rp {MC_AVG:,.0f}")
    c4.metric("T* Habis Cadangan",   f"{T_STAR:.0f} tahun")

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
        fig.add_trace(go.Scatter(
            x=data["Year"], y=data["HBA"], mode="lines+markers",
            name="HBA", line=dict(color="#3b82f6", width=3),
            marker=dict(size=9, color="#1d4ed8")
        ))
        fig.add_trace(go.Scatter(
            x=data["Year"], y=data["MC"], mode="lines+markers",
            name="MC", line=dict(color="#ec4899", width=2.5, dash="dash"),
            marker=dict(size=8, color="#db2777")
        ))
        fig.update_layout(title="HBA vs Biaya Marginal (MC)", yaxis_title="Rp", **PLOT_STYLE)
        styled_axes(fig)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=data["Year"], y=data["Production"],
            marker=dict(
                color=data["Production"],
                colorscale=[[0,"#bfdbfe"],[0.5,"#3b82f6"],[1,"#1e40af"]]
            ),
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
            marker=dict(color="#1d4ed8", size=14, symbol="circle", line=dict(color="white", width=2)),
            name="Ekuilibrium"
        ))
        fig_d.update_layout(
            title="Kurva Permintaan & Surplus Konsumen",
            xaxis_title="Q", yaxis_title="P", **PLOT_STYLE
        )
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
                     annotation_text=f"Rata-rata MC = Rp {MC_AVG:,.0f}",
                     annotation_font_color="#10b981")
    fig_mc.update_layout(title="Biaya Marginal (MC) 2015–2024", yaxis_title="Rp", **PLOT_STYLE)
    styled_axes(fig_mc)
    st.plotly_chart(fig_mc, use_container_width=True)

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

    # ── SIMULASI PARAMETER ──────────────────────────────────────────
    st.markdown("### ⚙️ Simulasi Parameter Pasar")
    st.markdown("""
<div class="card card-blue" style="margin-bottom:8px;">
<b>Geser parameter di bawah</b> untuk melihat perubahan keseimbangan pasar secara real-time pada ketiga struktur pasar.
</div>
""", unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        mc_pct_tab3 = st.slider(
            "Perubahan MC (%)", -50, 150, 0,
            help="Menggeser biaya marginal relatif dari baseline Rp 283.817,2",
            key="mc_pct_tab3"
        )
    with col_s2:
        n_firms_tab3 = st.slider(
            "Jumlah perusahaan oligopoli (n)", 2, 20, 3,
            key="n_firms_tab3"
        )
    with col_s3:
        cp_mult_tab3 = st.slider(
            "Choke Price multiplier (×)", 0.5, 2.0, 1.0, 0.05,
            help="Mengubah skala choke price dari baseline",
            key="cp_mult_tab3"
        )

    a_m = INTERCEPT
    b_m = -SLOPE
    mc_adj = (MC_AVG / 16000) * (1 + mc_pct_tab3 / 100)

    # --- Persaingan Sempurna ---
    q_pc   = max(0, (a_m - mc_adj) / b_m)
    p_pc   = mc_adj
    cs_pc  = 0.5 * (a_m - p_pc) * q_pc

    # --- Monopoli ---
    q_mono  = max(0, (a_m - mc_adj) / (2 * b_m))
    p_mono  = a_m - b_m * q_mono
    cs_mono = 0.5 * (a_m - p_mono) * q_mono
    ps_mono = max(0, (p_mono - mc_adj) * q_mono)
    dwl_mono = max(0, 0.5 * (p_mono - mc_adj) * (q_pc - q_mono))

    # --- Oligopoli Cournot ---
    n_eff  = n_firms_tab3
    q_oli  = max(0, (n_eff / (n_eff + 1)) * (a_m - mc_adj) / b_m)
    p_oli  = a_m - b_m * q_oli
    cs_oli = 0.5 * (a_m - p_oli) * q_oli
    ps_oli = max(0, (p_oli - mc_adj) * q_oli)
    dwl_oli = max(0, 0.5 * (p_oli - mc_adj) * (q_pc - q_oli))

    # ── KARTU HASIL ────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
<div class="market-card market-pc">
<div style="font-size:1.1rem;font-weight:800;color:#065f46;margin-bottom:12px;">
  ✅ Persaingan Sempurna
</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;font-size:1.6rem;">{q_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#065f46;font-size:1.6rem;">{p_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#065f46;font-size:1.1rem;">{cs_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Produsen</div>
<div style="font-weight:700;color:#065f46;font-size:1.1rem;">0.0000</div>
<div class="metric-label-text" style="margin-top:10px;">Total Surplus</div>
<div style="font-weight:700;color:#065f46;font-size:1.1rem;">{cs_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#10b981;font-size:1.3rem;">0.0000 ✓</div>
<div style="margin-top:12px;"><span class="tag tag-green">P = MC · Efisiensi Maksimal</span></div>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
<div class="market-card market-oli">
<div style="font-size:1.1rem;font-weight:800;color:#92400e;margin-bottom:12px;">
  🔶 Oligopoli Cournot (n={n_eff})
</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;font-size:1.6rem;">{q_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#b45309;font-size:1.6rem;">{p_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#b45309;font-size:1.1rem;">{cs_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Produsen</div>
<div style="font-weight:700;color:#b45309;font-size:1.1rem;">{ps_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Total Surplus</div>
<div style="font-weight:700;color:#b45309;font-size:1.1rem;">{cs_oli+ps_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_oli:.4f} ⚠</div>
<div style="margin-top:12px;"><span class="tag tag-amber">Antara Persaingan & Monopoli</span></div>
</div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
<div class="market-card market-mono">
<div style="font-size:1.1rem;font-weight:800;color:#9d174d;margin-bottom:12px;">
  ⚠️ Monopoli
</div>
<div class="metric-label-text">Q* Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;font-size:1.6rem;">{q_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div>
<div class="metric-num" style="color:#be185d;font-size:1.6rem;">{p_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div>
<div style="font-weight:700;color:#be185d;font-size:1.1rem;">{cs_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Produsen</div>
<div style="font-weight:700;color:#be185d;font-size:1.1rem;">{ps_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Total Surplus</div>
<div style="font-weight:700;color:#be185d;font-size:1.1rem;">{cs_mono+ps_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div>
<div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_mono:.4f} ⛔</div>
<div style="margin-top:12px;"><span class="tag tag-red">MR = MC · P &gt; MC</span></div>
</div>""", unsafe_allow_html=True)

    # ── GRAFIK DETAIL PER PASAR ─────────────────────────────────────
    st.markdown("### 📊 Grafik Detail Struktur Pasar")
    pasar_sel = st.selectbox(
        "Pilih Struktur Pasar:",
        ["Persaingan Sempurna", "Oligopoli (Cournot)", "Monopoli"]
    )

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
        note = f"Keseimbangan Cournot (n={n_eff}) — antara persaingan & monopoli"

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
                x=[0, q_eq, q_eq, 0], y=[mc_adj, mc_adj, p_eq, p_eq],
                fill="toself", fillcolor=color_fill,
                line=dict(color="rgba(0,0,0,0)"), name="Surplus Produsen"
            ))
        if dwl_v > 0:
            fig_mkt.add_trace(go.Scatter(
                x=[q_eq, q_pc, q_eq], y=[p_eq, mc_adj, mc_adj],
                fill="toself", fillcolor="rgba(239,68,68,0.25)",
                line=dict(color="rgba(0,0,0,0)"), name="DWL"
            ))
        fig_mkt.add_trace(go.Scatter(
            x=q_r, y=a_m - b_m * q_r, mode="lines", name="Demand",
            line=dict(color="#1d4ed8", width=3)
        ))
        if pasar_sel in ["Monopoli", "Oligopoli (Cournot)"]:
            mr_r = np.linspace(0, a_m / b_m, 300)
            fig_mkt.add_trace(go.Scatter(
                x=mr_r, y=a_m - 2 * b_m * mr_r, mode="lines", name="MR",
                line=dict(color="#f59e0b", width=2, dash="dot")
            ))
        fig_mkt.add_hline(y=mc_adj, line_color="#6b7280", annotation_text="MC")
        fig_mkt.add_trace(go.Scatter(
            x=[q_eq], y=[p_eq], mode="markers",
            marker=dict(color=color_eq, size=16, symbol="star", line=dict(color="white", width=2)),
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

    # ── GRAFIK PERBANDINGAN ─────────────────────────────────────────
    st.markdown("### 📊 Perbandingan Tiga Struktur Pasar")
    fig_comp = make_subplots(
        rows=1, cols=3,
        subplot_titles=["Q Ekuilibrium", "P Ekuilibrium", "Deadweight Loss"]
    )
    labels = ["Persaingan", "Oligopoli", "Monopoli"]
    bc = ["#10b981", "#f59e0b", "#ec4899"]
    for i, vals in enumerate([[q_pc, q_oli, q_mono], [p_pc, p_oli, p_mono], [0, dwl_oli, dwl_mono]], 1):
        fig_comp.add_trace(go.Bar(x=labels, y=vals, marker_color=bc, showlegend=False), row=1, col=i)
    fig_comp.update_layout(
        paper_bgcolor="white", plot_bgcolor="#f8fafc",
        font=dict(color="#1e293b"), height=340, margin=dict(t=50, b=30)
    )
    for i in range(1, 4):
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
        st.markdown(
            '<div class="formula-box">'
            'T* = (1/r) × ln((a − MC) / λ₀)<br>'
            'T* = (1/0.05) × ln((863.888.320 − 283.817,2) / 15.163)<br>'
            'T* ≈ 114,12 tahun'
            '</div>',
            unsafe_allow_html=True
        )
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
        r_t4 = DISCOUNT_RATE
        t_range = np.linspace(0, 150, 300)
        muc_t = MUC_AWAL * np.exp(r_t4 * t_range)

        fig_muc = go.Figure()
        fig_muc.add_trace(go.Scatter(
            x=t_range, y=muc_t, mode="lines", name="MUC(t) = λ₀·eʳᵗ",
            line=dict(color="#3b82f6", width=3),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"
        ))
        fig_muc.add_hline(
            y=CHOKE_PRICE_RP - MC_AVG, line_dash="dash", line_color="#ec4899",
            annotation_text="Choke − MC", annotation_font_color="#ec4899"
        )
        fig_muc.add_vline(
            x=T_STAR, line_dash="dot", line_color="#10b981",
            annotation_text=f"T* = {T_STAR:.0f} thn", annotation_font_color="#10b981"
        )
        fig_muc.update_layout(
            title="Pertumbuhan MUC Sepanjang Waktu",
            xaxis_title="Tahun ke-", yaxis_title="MUC (Rp)", **PLOT_STYLE
        )
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
    fig_ts.add_vline(
        x=5, line_dash="dot", line_color="#10b981",
        annotation_text="r = 5%", annotation_font_color="#10b981"
    )
    fig_ts.update_layout(
        title="T* vs Tingkat Diskonto",
        xaxis_title="Tingkat Diskonto (%)", yaxis_title="T* (tahun)", **PLOT_STYLE
    )
    styled_axes(fig_ts)
    st.plotly_chart(fig_ts, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("MUC Saat Ini (t=0)", f"Rp {MUC_AWAL:,.0f}")
    c2.metric("MUC t=10 tahun",     f"Rp {MUC_AWAL * np.exp(DISCOUNT_RATE * 10):,.0f}")
    c3.metric("MUC t=50 tahun",     f"Rp {MUC_AWAL * np.exp(DISCOUNT_RATE * 50):,.0f}")

# =====================================================================
# TAB 5 — SIMULASI
# =====================================================================

with tab5:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    sim1, sim2, sim3 = st.tabs(["📉 Simulasi Harga", "🏭 Simulasi Pasar", "⏳ Simulasi T*"])

    # ── SIM 1 ──────────────────────────────────────────────────────
    with sim1:
        st.markdown("#### Simulasi Fungsi Permintaan")
        prod_sim = st.slider("Jumlah Produksi (juta ton)", 1.0, 6.0, 3.5, 0.1)
        p_sim    = INTERCEPT + SLOPE * prod_sim
        p_sim_rp = p_sim * 16000
        c1, c2, c3 = st.columns(3)
        c1.metric("Q Input",         f"{prod_sim:.1f} juta ton")
        c2.metric("P (unit skala)",  f"{p_sim:.4f}")
        c3.metric("P Estimasi (Rp)", f"Rp {p_sim_rp:,.0f}")
        st.info("📌 Semakin besar produksi → harga pasar cenderung turun sesuai fungsi permintaan.")

        # Grafik animasi: plot bergerak sesuai slider
        q_anim = np.linspace(0, 47.5, 200)
        p_anim = INTERCEPT + SLOPE * q_anim
        fig_anim = go.Figure()
        fig_anim.add_trace(go.Scatter(
            x=q_anim, y=p_anim, mode="lines", name="Kurva Permintaan",
            line=dict(color="#1d4ed8", width=3)
        ))
        fig_anim.add_trace(go.Scatter(
            x=[prod_sim], y=[p_sim], mode="markers",
            marker=dict(color="#ec4899", size=16, symbol="circle",
                        line=dict(color="white", width=2)),
            name=f"Q={prod_sim:.1f}"
        ))
        fig_anim.add_annotation(
            x=prod_sim, y=p_sim,
            text=f"  Q={prod_sim:.1f}, P={p_sim:.3f}",
            showarrow=True, arrowhead=2, arrowcolor="#ec4899",
            font=dict(color="#ec4899", size=12)
        )
        fig_anim.update_layout(
            title="Posisi Produksi pada Kurva Permintaan",
            xaxis_title="Q (juta ton)", yaxis_title="P (skala)", **PLOT_STYLE
        )
        styled_axes(fig_anim)
        st.plotly_chart(fig_anim, use_container_width=True)

    # ── SIM 2 ──────────────────────────────────────────────────────
    with sim2:
        st.markdown("#### Simulasi Struktur Pasar")
        ca, cb = st.columns(2)
        with ca:
            n_firms = st.slider("Jumlah Perusahaan (Cournot)", 1, 20, 3)
        with cb:
            mc_pct_s2 = st.slider("Perubahan MC (%)", -50, 100, 0)

        mc_adj_s2 = (MC_AVG / 16000) * (1 + mc_pct_s2 / 100)
        a_s, b_s  = INTERCEPT, -SLOPE

        if n_firms == 1:
            q_s = max(0, (a_s - mc_adj_s2) / (2 * b_s))
            label = "Monopoli"
        else:
            q_s = max(0, (n_firms / (n_firms + 1)) * (a_s - mc_adj_s2) / b_s)
            label = f"Cournot (n={n_firms})"

        p_s     = a_s - b_s * q_s
        q_pc_s  = max(0, (a_s - mc_adj_s2) / b_s)
        cs_s    = 0.5 * (a_s - p_s) * q_s
        ps_s    = max(0, (p_s - mc_adj_s2) * q_s)
        dwl_s   = max(0, 0.5 * (p_s - mc_adj_s2) * (q_pc_s - q_s))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Q* ({label})", f"{q_s:.3f}")
        c2.metric("P* Ekuilibrium", f"{p_s:.4f}")
        c3.metric("Total Surplus", f"{cs_s + ps_s:.4f}")
        c4.metric("DWL", f"{dwl_s:.4f}")

        q_r2 = np.linspace(0, a_s / b_s * 1.05, 300)
        fig_s2 = go.Figure()
        fig_s2.add_trace(go.Scatter(
            x=q_r2, y=a_s - b_s * q_r2, mode="lines",
            name="Demand", line=dict(color="#1d4ed8", width=2.5)
        ))
        if n_firms == 1:
            mr_r2 = np.linspace(0, a_s / (2 * b_s) * 1.1, 300)
            fig_s2.add_trace(go.Scatter(
                x=mr_r2, y=a_s - 2 * b_s * mr_r2, mode="lines",
                name="MR", line=dict(color="#f59e0b", width=2, dash="dot")
            ))
        fig_s2.add_hline(y=mc_adj_s2, line_color="#6b7280", annotation_text="MC")
        fig_s2.add_trace(go.Scatter(
            x=[q_s], y=[p_s], mode="markers",
            marker=dict(color="#8b5cf6", size=14, symbol="star",
                        line=dict(color="white", width=2)),
            name="Ekuilibrium"
        ))
        fig_s2.update_layout(
            title=f"Simulasi {label}",
            xaxis_title="Q", yaxis_title="P", **PLOT_STYLE
        )
        styled_axes(fig_s2)
        st.plotly_chart(fig_s2, use_container_width=True)

    # ── SIM 3 ──────────────────────────────────────────────────────
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
            t_sim = (1 / r_sim) * np.log((cp_sim - mc_sim_rp) / muc0_sim)
            delta = t_sim - T_STAR
            st.metric(
                "T* Simulasi",
                f"{t_sim:.2f} tahun",
                delta=f"{delta:+.2f} vs baseline"
            )
            st.success(f"✅ Cadangan habis dalam **{t_sim:.1f} tahun** dengan parameter tersebut.")

            t_sim_range = np.linspace(0, max(150, t_sim * 1.2), 300)
            muc_sim     = muc0_sim * np.exp(r_sim * t_sim_range)

            fig_sim3 = go.Figure()
            fig_sim3.add_trace(go.Scatter(
                x=t_sim_range, y=muc_sim, mode="lines", name="MUC(t)",
                line=dict(color="#8b5cf6", width=3),
                fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"
            ))
            fig_sim3.add_hline(
                y=cp_sim - mc_sim_rp, line_dash="dash", line_color="#ec4899",
                annotation_text="Choke − MC", annotation_font_color="#ec4899"
            )
            fig_sim3.add_vline(
                x=t_sim, line_dash="dot", line_color="#10b981",
                annotation_text=f"T* = {t_sim:.1f} thn", annotation_font_color="#10b981"
            )
            fig_sim3.update_layout(
                title=f"Pertumbuhan MUC — T* = {t_sim:.1f} tahun",
                xaxis_title="Tahun ke-", yaxis_title="MUC (Rp)", **PLOT_STYLE
            )
            styled_axes(fig_sim3)
            st.plotly_chart(fig_sim3, use_container_width=True)
        else:
            st.error("⚠️ Parameter tidak valid: Choke Price harus lebih besar dari MC dan MUC₀ > 0")

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#94a3b8;font-size:0.82rem;padding:16px 0;line-height:1.9;">
  <b style="color:#64748b;">PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</b><br>
  Dikembangkan oleh: Arif Hamdani (10090224008) &nbsp;·&nbsp;
  Bambang Karta Wijaya (10090224020) &nbsp;·&nbsp;
  Moh Bayu Mustofa (10090224030)<br>
  Di bawah bimbingan <b style="color:#64748b;">Yuhka Sundaya, S.E., M.Si.</b>
  &nbsp;·&nbsp; Universitas Islam Bandung &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)