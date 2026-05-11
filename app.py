import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="PBL 3 - Analisis Batubara",
    page_icon="⛏️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
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
        content: ""; position: absolute; top: -60px; right: -60px;
        width: 220px; height: 220px; border-radius: 50%;
        background: rgba(255,255,255,0.07);
    }
    .hero-banner::after {
        content: ""; position: absolute; bottom: -40px; left: 40%;
        width: 160px; height: 160px; border-radius: 50%;
        background: rgba(255,255,255,0.05);
    }
    .hero-title { font-size: 2rem; font-weight: 800; margin: 0 0 6px 0; letter-spacing: -0.02em; }
    .hero-subtitle { font-size: 0.95rem; opacity: 0.85; margin: 0 0 16px 0; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px; padding: 4px 14px;
        font-size: 0.8rem; font-weight: 600; letter-spacing: 0.04em;
    }
    .dev-credit-box {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 14px; padding: 14px 20px; margin-top: 16px;
        font-size: 0.85rem; line-height: 1.8; color: rgba(255,255,255,0.95);
    }
    .card {
        background: white; border-radius: 16px; padding: 20px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    .card-blue   { border-left: 4px solid #3b82f6; background: linear-gradient(135deg,#eff6ff 0%,white 100%); }
    .card-purple { border-left: 4px solid #8b5cf6; background: linear-gradient(135deg,#f5f3ff 0%,white 100%); }
    .card-green  { border-left: 4px solid #10b981; background: linear-gradient(135deg,#ecfdf5 0%,white 100%); }
    .card-amber  { border-left: 4px solid #f59e0b; background: linear-gradient(135deg,#fffbeb 0%,white 100%); }
    .card-pink   { border-left: 4px solid #ec4899; background: linear-gradient(135deg,#fdf2f8 0%,white 100%); }
    .card-red    { border-left: 4px solid #ef4444; background: linear-gradient(135deg,#fff1f2 0%,white 100%); }

    /* ── ANALISIS ILMIAH BOX ── */
    .analisis-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 14px; padding: 20px 24px; margin: 16px 0 8px 0;
        border-left: 4px solid #38bdf8;
        color: #cbd5e1; font-size: 0.875rem; line-height: 1.9;
    }
    .analisis-box b, .analisis-box strong { color: #7dd3fc; }
    .ab-label {
        display: inline-block; border-radius: 6px; padding: 2px 10px;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.05em;
        margin: 0 4px 10px 0;
    }
    .ab-finding  { background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); }
    .ab-critical { background: rgba(251,113,133,0.15); color: #fb7185; border: 1px solid rgba(251,113,133,0.3); }
    .ab-implic   { background: rgba(52,211,153,0.15);  color: #34d399; border: 1px solid rgba(52,211,153,0.3); }

    /* ── POLICY CARDS ── */
    .policy-section-title {
        font-size: 0.8rem; font-weight: 800; letter-spacing: 0.08em;
        text-transform: uppercase; color: #64748b; margin: 20px 0 10px 0;
    }
    .pcard {
        border-radius: 16px; padding: 22px 24px; margin-bottom: 14px;
        position: relative; overflow: hidden;
    }
    .pcard::before {
        content: attr(data-num);
        position: absolute; top: 6px; right: 18px;
        font-size: 3rem; font-weight: 900; opacity: 0.08;
        font-family: 'JetBrains Mono', monospace; line-height: 1;
        color: white;
    }
    .pcard-gov  { background: linear-gradient(135deg,#0c4a6e,#0369a1); color: #e0f2fe; border-left: 5px solid #38bdf8; }
    .pcard-corp { background: linear-gradient(135deg,#14532d,#15803d); color: #dcfce7; border-left: 5px solid #4ade80; }
    .pcard-crit { background: linear-gradient(135deg,#3b0764,#6d28d9); color: #ede9fe; border-left: 5px solid #a78bfa; }
    .pcard-title { font-size: 1rem; font-weight: 800; margin-bottom: 10px; }
    .pcard-body { font-size: 0.86rem; line-height: 1.78; opacity: 0.93; }
    .ptag {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 0.71rem; font-weight: 700; margin: 6px 3px 0 0;
        letter-spacing: 0.04em;
    }
    .pt-blue   { background: rgba(56,189,248,0.2);  color: #7dd3fc; }
    .pt-green  { background: rgba(74,222,128,0.2);  color: #4ade80; }
    .pt-red    { background: rgba(251,113,133,0.2); color: #fb7185; }
    .pt-amber  { background: rgba(251,191,36,0.2);  color: #fbbf24; }
    .pt-purple { background: rgba(167,139,250,0.2); color: #a78bfa; }

    /* ── FRAMEWORK BANNER ── */
    .fw-banner {
        background: linear-gradient(135deg,#0f172a,#1e293b);
        border-radius: 16px; padding: 22px 26px; margin-bottom: 20px;
        border-left: 5px solid #f59e0b;
    }
    .fw-banner-title { color: #f1f5f9; font-size: 1rem; font-weight: 800; margin-bottom: 6px; }
    .fw-banner-body  { color: #94a3b8; font-size: 0.87rem; line-height: 1.8; }

    /* ── MISC ── */
    .sim-panel {
        background: linear-gradient(135deg,#f0f9ff,#e0f2fe);
        border: 2px solid #0ea5e9; border-radius: 16px; padding: 18px 22px; margin: 12px 0 18px 0;
    }
    .sim-panel-green {
        background: linear-gradient(135deg,#f0fdf4,#dcfce7);
        border: 2px solid #22c55e; border-radius: 16px; padding: 18px 22px; margin: 12px 0 18px 0;
    }
    .sim-panel-purple {
        background: linear-gradient(135deg,#faf5ff,#ede9fe);
        border: 2px solid #a855f7; border-radius: 16px; padding: 18px 22px; margin: 12px 0 18px 0;
    }
    .sim-panel-amber {
        background: linear-gradient(135deg,#fffbeb,#fef3c7);
        border: 2px solid #f59e0b; border-radius: 16px; padding: 18px 22px; margin: 12px 0 18px 0;
    }
    .sim-badge {
        display: inline-block; background: #0ea5e9; color: white;
        border-radius: 8px; padding: 3px 12px;
        font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 10px;
    }
    .result-pill {
        display: inline-block; background: white; border: 1.5px solid #e2e8f0;
        border-radius: 10px; padding: 8px 16px; margin: 4px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 600; color: #1e293b;
    }
    .result-pill-blue  { border-color: #3b82f6; color: #1d4ed8; background: #eff6ff; }
    .result-pill-green { border-color: #10b981; color: #065f46; background: #ecfdf5; }
    .result-pill-red   { border-color: #ef4444; color: #991b1b; background: #fef2f2; }
    .result-pill-amber { border-color: #f59e0b; color: #92400e; background: #fffbeb; }
    .metric-box {
        background: white; border-radius: 14px; padding: 18px 20px;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;
    }
    .metric-num {
        font-family: 'JetBrains Mono', monospace; font-size: 1.5rem;
        font-weight: 700; color: #1e40af; display: block;
    }
    .metric-label-text {
        font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;
    }
    .formula-box {
        background: #1e293b; border-radius: 12px; padding: 16px 20px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: #7dd3fc;
        margin: 12px 0; border-left: 4px solid #3b82f6;
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
        border-radius: 3px; margin: 24px 0 20px 0;
    }
    .market-card { border-radius: 16px; padding: 22px; border: 1px solid #e2e8f0; margin-bottom: 16px; }
    .market-pc   { background: linear-gradient(135deg,#ecfdf5,#d1fae5); border-left: 5px solid #10b981; }
    .market-oli  { background: linear-gradient(135deg,#fffbeb,#fef3c7); border-left: 5px solid #f59e0b; }
    .market-mono { background: linear-gradient(135deg,#fdf2f8,#fce7f3); border-left: 5px solid #ec4899; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: white; border-radius: 12px; padding: 6px; border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; color: #64748b; font-weight: 600; font-size: 0.85rem; padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        color: #1e40af !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important; font-size: 0.8rem !important;
        text-transform: uppercase; letter-spacing: 0.04em;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA & KONSTANTA
# ─────────────────────────────────────────────
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
    paper_bgcolor="white", plot_bgcolor="#f8fafc",
    font=dict(color="#1e293b", family="Plus Jakarta Sans"),
    margin=dict(t=55, b=40, l=55, r=20),
    legend=dict(bgcolor="white", bordercolor="#e2e8f0", borderwidth=1)
)

def styled_axes(fig):
    fig.update_xaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1", zerolinecolor="#e2e8f0")
    fig.update_yaxes(gridcolor="#e2e8f0", linecolor="#cbd5e1", zerolinecolor="#e2e8f0")
    return fig

def analisis_box(html_content):
    """Renders dark scientific analysis box."""
    st.markdown(f'<div class="analisis-box">{html_content}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div style="position:relative;z-index:1;display:flex;align-items:flex-start;gap:24px;">
    <div style="flex-shrink:0;display:flex;align-items:center;justify-content:center;">
      <img src="data:image/jpeg;base64,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dSDbtYuIe11FvxXdtTa8elBjqLoO9sk4744D3hvY549De/dvBT0U1v0tyJ2o/ET9zcgvNuq3/cazQO66iiDHkMqptx+Mcdg5rCNm7gnc9gkdADQGtAAA2AHgg9a2Wy3WW3U1os9BT0VDRxNgp6anjEccUbRs1rWjsAA7AAvaREBERAREQEREBERAREQEREBERAREQEREBERB6zbdb2V77qygp21skTYH1IiaJXRgkhhftuWgkkDfbcleyiIC9C/WCx5RaKrH8ktFHdLZXRmGppKuFssMzD3tcxwIIXvogi24uuiDpazy3POFuZtNN500+JVk20bvE+STO9qfRG87ehw7lFrlOKZLhF+rMXzCw11mu9vkMVTRVsDoponDwLXDf5+4q0mtWaxcMOhuvVZabnqhgNBdrhZKqKppKzl6ucdW8O6p727F8R22Mbt2kb9iDSXRfaZasafcNtBX6p5Rdqv74XNr7NZq6QvFpoC38W1vN5zTIDz8m+zQW7AHddgLxjjjijbFExrGMAa1rRsAB3ABeSAiIgIiIMS1e9yfNfk7cvq0irCKz3q97k+a/J25fVpFWEQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQFlWk/up4b8oLd9ZjWKrKtJ/dTw35QW76zGgs/IiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICItScV+ssGgXD7mepxeBWW23PitzT7+tm/FwD/O5pPqBQZpiWp2nWe1VwocLzeyXqqtNTJR11PRVscstNNG4teyRgPM0hwI7R4LJ1VvtGZZbj+QffZYMludsvPXOqPL6OqfDP1hPMXc7CDuT2ntXZ+hnS68Rmmvk9q1IiodRLPHs1zq7/Z7g1vqqGDZx/bY4+tBOCi5K0M6Trha1o8nttblT8Jvk2zfufkXLAxzz4MqATE753NPqXV9JV0tfTR1lDUxVFPM0PjlieHse09xDh2EfEg/siIgIiICIiAiIgIiIMS1e9yfNfk7cvq0irCKz3q97k+a/J25fVpFWEQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQFlWk/up4b8oLd9ZjWKrKtJ/dTw35QW76zGgs/IiICIiAiIgIiICIv5zzwUsL6ipmZFFGC573uDWtHpJPYAg/oi5u1i6QzhR0W6+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jTmuY6klp7XTvknt73EclS6RxLpQ3bZzQB2EkDcAEJENK+EPht0VutPf9NdI7HaLvStcyG4hj5qpgc0tdtLK5zhuCQdj3ErcCx3DtQ8E1CsdPkmD5faL5bKpgkiqqGrZKwg+nY9h9R2I8VgGt/FroFw/WSouuoWoVrjq4mF0Npo52VFfUuHcxkLCXDf0u2aPEhBw/wBOBkVubjGluJ9aw18lfcLjyb+c2Fscce/xFzv+Urh7o+Meq8k4ydLaOkic/wAlvQuEhA9rHBG+VxP+T/VY/wAWnEvk3FVrBX6k32nNDQsYKKz23n5hRUTCSxhPcXkkucfFzj4ALufoaOG+5MuN74lslt74aTyeSyY51jduuc4jymdu/vQGiMHxJkHgglbREQEREEX/AEm/AXqFqvq3juqWhWHyXa4ZQBbb/BC5kbIZ4m/iquRziGtaYxyOcT3xt8XLcfR+dH9k/CbcLhneZajmtvl8t4oquy21v/R8beYPaXveOaWRpB2IDQOZ3fuu3UQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERByrxkcAWJ8YV7s2SXzUS947X2GhfQ0rKaninpy1zy8ucx2zuYnYdjh2ALVPCF0YV54X+IGl1Zr9TLZk1roLdV01LC23yU1SyeZoYHkFzm7BheO/fchSAIgL8JDQXOOwA3JX6vwgEbFBWd4jMyfqFr3qFmjpOdt2yS4VEbv/AAuvcGf8oapXuhdwv7i8OuSZlLHtJkmSyMY7b20VNCxg+bnfIuuM34ZeHrUdsgzbRnEbo+XfmmktUTJiT49YwB+/r3WRaY6WYBo1h9NgOmeOQ2OwUckssFFFLJI1j5Hl7zzSOc47ucT2ns7hsEGVoiICIiAiIg0ZxgcK2KcWWlU+D3mdtvvNC81liuvJzOo6rl284d5jePNe30bEdoCgY1y4bNY+HXJJ8c1RwyttwY8tp7gyMyUVY0HsfDMByuB9HY4eICstL07rZ7TfaKS23u10lwpJRs+nqoGyxuHra4EFBVtorrdLaHC3XKqpQ/23UzOZzfHse1e1Y8dyjMboy245Y7ne7hUO2bBR00lRM9x/VaCSrIcvC1w2TVhuEug+BuqCeYvNgpu/4uTZZxj2G4hiMHkuKYraLNDtt1dvoYqdu3xMaEEPXCT0TGpeoF3ocv4h6OfEMVie2Y2hzwLncAO3kc0b+TsPiXeft3NHeJi8ZxmwYbj9vxTFrTTWy0WqnZS0dHTMDI4YmjZrWgL6aICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiD//2Q=="
           alt="Logo UNISBA"
           style="width:110px;height:110px;object-fit:contain;
                  background:white;border-radius:50%;padding:8px;
                  box-shadow:0 4px 20px rgba(0,0,0,0.25);" />
    </div>
    <div style="flex:1;">
      <span class="hero-badge">⛏️ PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</span>
      <h1 class="hero-title" style="color:white!important;margin-top:10px;">Analisis Intertemporal Batubara</h1>
      <p class="hero-subtitle">Estimasi Fungsi Permintaan &amp; Efisiensi Dinamis — PT Mitrabara Adiperdana Tbk 2015–2024</p>
      <div class="dev-credit-box">
        <b>Dikembangkan oleh:</b><br>
        &nbsp;• Arif Hamdani (10090224008)<br>
        &nbsp;• Bambang Karta Wijaya (10090224025)<br>
        &nbsp;• Moh Bayu Mustofa (10090224030)<br><br>
        Pada mata kuliah <b>Ekonomi Sumber Daya Alam dan Lingkungan</b>
        &nbsp;·&nbsp; Di bawah bimbingan <b>Yuhka Sundaya, S.E., M.Si.</b><br>
        <span style="font-size:0.8rem;opacity:0.75;">Universitas Islam Bandung · Fakultas Ekonomi dan Bisnis · 2026</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", "📈 Fungsi Permintaan", "🏭 Mekanisme Pasar",
    "⏳ Efisiensi Dinamis", "🔬 Simulasi", "📋 Laporan"
])

# =====================================================================
# TAB 1 — DASHBOARD
# =====================================================================
with tab1:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Produksi", f"{data['Production'].sum():,.0f} ton", "2015–2024")
    c2.metric("Rata-rata HBA",  f"Rp {data['HBA'].mean():,.0f}")
    c3.metric("Rata-rata MC",   f"Rp {MC_AVG:,.0f}")
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
            fill="toself", fillcolor="rgba(59,130,246,0.12)", line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"))
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
    st.markdown('<div class="card card-green">Rata-rata MC = <b>Rp 283.817,2</b> — di bawah rata-rata HBA, artinya setiap tambahan produksi masih menguntungkan secara marjinal.</div>', unsafe_allow_html=True)
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
    with col_s1: mc_pct_tab3  = st.slider("Perubahan MC (%)", -50, 150, 0, key="mc_pct_tab3")
    with col_s2: n_firms_tab3 = st.slider("Jumlah perusahaan oligopoli (n)", 2, 20, 3, key="n_firms_tab3")
    with col_s3: cp_mult_tab3 = st.slider("Choke Price multiplier (×)", 0.5, 2.0, 1.0, 0.05, key="cp_mult_tab3")

    a_m = INTERCEPT; b_m = -SLOPE
    mc_adj = (MC_AVG / 16000) * (1 + mc_pct_tab3 / 100)
    q_pc   = max(0, (a_m - mc_adj) / b_m); p_pc = mc_adj; cs_pc = 0.5*(a_m-p_pc)*q_pc
    q_mono = max(0, (a_m - mc_adj) / (2*b_m)); p_mono = a_m - b_m*q_mono
    cs_mono = 0.5*(a_m-p_mono)*q_mono; ps_mono = max(0,(p_mono-mc_adj)*q_mono)
    dwl_mono = max(0, 0.5*(p_mono-mc_adj)*(q_pc-q_mono))
    n_eff = n_firms_tab3
    q_oli = max(0,(n_eff/(n_eff+1))*(a_m-mc_adj)/b_m); p_oli = a_m-b_m*q_oli
    cs_oli = 0.5*(a_m-p_oli)*q_oli; ps_oli = max(0,(p_oli-mc_adj)*q_oli)
    dwl_oli = max(0, 0.5*(p_oli-mc_adj)*(q_pc-q_oli))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="market-card market-pc">
<div style="font-size:1.1rem;font-weight:800;color:#065f46;margin-bottom:12px;">✅ Persaingan Sempurna</div>
<div class="metric-label-text">Q* Ekuilibrium</div><div class="metric-num" style="color:#065f46;font-size:1.6rem;">{q_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div><div class="metric-num" style="color:#065f46;font-size:1.6rem;">{p_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div><div style="font-weight:700;color:#065f46;">{cs_pc:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div><div style="font-weight:800;color:#10b981;font-size:1.3rem;">0.0000 ✓</div>
<div style="margin-top:12px;"><span class="tag tag-green">P = MC · Efisiensi Maksimal</span></div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="market-card market-oli">
<div style="font-size:1.1rem;font-weight:800;color:#92400e;margin-bottom:12px;">🔶 Oligopoli Cournot (n={n_eff})</div>
<div class="metric-label-text">Q* Ekuilibrium</div><div class="metric-num" style="color:#b45309;font-size:1.6rem;">{q_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div><div class="metric-num" style="color:#b45309;font-size:1.6rem;">{p_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div><div style="font-weight:700;color:#b45309;">{cs_oli:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div><div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_oli:.4f} ⚠</div>
<div style="margin-top:12px;"><span class="tag tag-amber">Antara Persaingan & Monopoli</span></div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
<div class="market-card market-mono">
<div style="font-size:1.1rem;font-weight:800;color:#9d174d;margin-bottom:12px;">⚠️ Monopoli</div>
<div class="metric-label-text">Q* Ekuilibrium</div><div class="metric-num" style="color:#be185d;font-size:1.6rem;">{q_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">P* Ekuilibrium</div><div class="metric-num" style="color:#be185d;font-size:1.6rem;">{p_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Surplus Konsumen</div><div style="font-weight:700;color:#be185d;">{cs_mono:.4f}</div>
<div class="metric-label-text" style="margin-top:10px;">Deadweight Loss</div><div style="font-weight:800;color:#ef4444;font-size:1.3rem;">{dwl_mono:.4f} ⛔</div>
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
            marker=dict(color=color_eq, size=16, symbol="star", line=dict(color="white", width=2)), name="Ekuilibrium"))
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
    r_range_d = np.linspace(0.01, 0.30, 100)
    t_star_range = (1/r_range_d) * np.log((CHOKE_PRICE_RP-MC_AVG)/MUC_AWAL)
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=r_range_d*100, y=t_star_range, mode="lines", name="T*(r)",
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
        p_sim_val = INTERCEPT + SLOPE * prod_sim; p_sim_rp = p_sim_val * 16000
        c1, c2, c3 = st.columns(3)
        c1.metric("Q Input", f"{prod_sim:.1f} juta ton")
        c2.metric("P (unit skala)", f"{p_sim_val:.4f}")
        c3.metric("P Estimasi (Rp)", f"Rp {p_sim_rp:,.0f}")
        st.info("📌 Semakin besar produksi → harga pasar cenderung turun sesuai fungsi permintaan.")
        q_anim = np.linspace(0, 47.5, 200)
        p_anim = INTERCEPT + SLOPE * q_anim
        fig_anim = go.Figure()
        fig_anim.add_trace(go.Scatter(x=q_anim, y=p_anim, mode="lines", name="Kurva Permintaan",
            line=dict(color="#1d4ed8", width=3)))
        fig_anim.add_trace(go.Scatter(x=[prod_sim], y=[p_sim_val], mode="markers",
            marker=dict(color="#ec4899", size=16, symbol="circle", line=dict(color="white", width=2)),
            name=f"Q={prod_sim:.1f}"))
        fig_anim.add_annotation(x=prod_sim, y=p_sim_val, text=f"  Q={prod_sim:.1f}, P={p_sim_val:.3f}",
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
            marker=dict(color="#8b5cf6", size=14, symbol="star", line=dict(color="white", width=2)), name="Ekuilibrium"))
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
            muc_sim = muc0_sim * np.exp(r_sim * t_sim_range)
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
# TAB 6 — LAPORAN
# =====================================================================
with tab6:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

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
      Bambang Karta Wijaya (10090224025) &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
      <b>Dosen Pembimbing:</b> Yuhka Sundaya, S.E., M.Si.<br>
      <span style="font-size:0.78rem;opacity:0.75;">
        Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan &nbsp;·&nbsp;
        Universitas Islam Bandung &nbsp;·&nbsp; Fakultas Ekonomi dan Bisnis &nbsp;·&nbsp; 2026
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

    # ── BAB I ──
    st.markdown("""
<div style="margin-top:28px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#1e40af,#3b82f6);color:white;border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB I</div>
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
1. <b>Bagaimana dinamika perubahan harga dan teknologi memengaruhi pergeseran status cadangan (<i>resource</i> ke <i>reserve</i>)?</b><br><br>
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

    # ── BAB II ──
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#5b21b6,#8b5cf6);color:white;border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB II</div>
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

    # ── BAB III ──
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#92400e,#f59e0b);color:white;border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB III</div>
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

        analisis_box("""
<span class="ab-label ab-finding">📊 ANALISIS DATA</span>
<span class="ab-label ab-critical">⚠️ CATATAN KRITIS</span><br><br>
Data historis MBAP 2015–2024 memperlihatkan dua anomali struktural yang signifikan dari perspektif
ekonomi sumber daya alam. <b>Pertama</b>, nilai MC negatif pada tahun 2018 (−Rp 983.107), 2022
(−Rp 360.009), dan 2023 (−Rp 1.273.092) secara teknis tidak dapat diinterpretasikan sebagai biaya
marjinal sejati dalam kerangka neoklasik standar. Nilai negatif ini merupakan <i>artifact</i> dari
metode <i>incremental cost</i> berbasis selisih COGS dan volume produksi, bukan cerminan kondisi biaya
produksi aktual.<br><br>
<b>Implikasi kritis metodologis:</b> Penggunaan pendekatan COGS differencing tidak mampu memisahkan
<i>fixed cost</i> dari <i>variable cost</i>, sehingga fluktuasi besar pada COGS yang tidak proporsional
dengan perubahan volume akan menghasilkan MC yang distortif. Pendekatan <i>stochastic frontier analysis</i>
(SFA) atau metode <i>activity-based costing</i> (ABC) lebih disarankan untuk estimasi MC yang akurat pada
industri tambang. Penggunaan rata-rata MC tunggal (Rp 283.817/ton) sebagai konstanta model Hotelling
perlu diperlakukan dengan reservasi epistemologis yang serius.
""")

    # ── BAB IV ──
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#065f46,#10b981);color:white;border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB IV</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">HASIL DAN PEMBAHASAN</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)

    # 4.1 — FUNGSI PERMINTAAN
    with st.expander("4.1  Estimasi Fungsi Permintaan & Simulasi Kurva", expanded=True):
        st.markdown("""
<div class="card card-green">
<b>Hasil Regresi OLS:</b> P̂ = 53,993 − 1,137·Q &nbsp;|&nbsp; R² = 0,633 &nbsp;|&nbsp; F = 13,80 &nbsp;|&nbsp; p-value Q = 0,006
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sim-panel"><span class="sim-badge">🎛️ SIMULASI KURVA PERMINTAAN</span>', unsafe_allow_html=True)
        st.markdown("Ubah parameter di bawah — kurva dan titik ekuilibrium akan bergerak secara real-time.")
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

        lap_mc    = (MC_AVG / 16000) * (lap_mc_pct / 100)
        lap_q_max = lap_intercept / lap_slope_abs
        lap_q_eq  = max(0, (lap_intercept - lap_mc) / lap_slope_abs)
        lap_p_eq  = lap_mc
        lap_cs    = 0.5 * (lap_intercept - lap_p_eq) * lap_q_eq
        lap_q_orig = (INTERCEPT - MC_AVG/16000) / abs(SLOPE)

        q_sim_l = np.linspace(0, lap_q_max * 1.05, 300)
        p_sim_l = lap_intercept + (-lap_slope_abs) * q_sim_l
        q_orig_l = np.linspace(0, INTERCEPT / abs(SLOPE) * 1.05, 300)
        p_orig_l = INTERCEPT + SLOPE * q_orig_l

        fig_lap1 = go.Figure()
        fig_lap1.add_trace(go.Scatter(x=q_orig_l, y=p_orig_l, mode="lines", name="Kurva Baseline",
            line=dict(color="#94a3b8", width=2, dash="dot"), opacity=0.6))
        if lap_q_eq > 0:
            fig_lap1.add_trace(go.Scatter(x=[0, lap_q_eq, 0], y=[lap_intercept, lap_p_eq, lap_p_eq],
                fill="toself", fillcolor="rgba(59,130,246,0.15)", line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen"))
        fig_lap1.add_trace(go.Scatter(x=q_sim_l, y=p_sim_l, mode="lines", name="Kurva Simulasi",
            line=dict(color="#1d4ed8", width=3)))
        fig_lap1.add_hline(y=lap_mc, line_dash="dash", line_color="#ec4899",
                           annotation_text=f"MC = {lap_mc:.3f}", annotation_font_color="#ec4899")
        if lap_q_eq > 0:
            fig_lap1.add_trace(go.Scatter(x=[lap_q_eq], y=[lap_p_eq], mode="markers",
                marker=dict(color="#1d4ed8", size=16, symbol="circle", line=dict(color="white", width=3)),
                name=f"Ekuilibrium (Q={lap_q_eq:.2f})"))
        fig_lap1.add_annotation(x=0, y=lap_intercept, text=f"Choke P = {lap_intercept:.1f}",
            showarrow=False, xanchor="left", font=dict(color="#1d4ed8", size=11))
        fig_lap1.update_layout(
            title=f"Kurva Permintaan Interaktif — P = {lap_intercept:.2f} − {lap_slope_abs:.3f}·Q",
            xaxis_title="Q (Kuantitas)", yaxis_title="P (Harga Skala)", **PLOT_STYLE, height=420)
        styled_axes(fig_lap1)
        st.plotly_chart(fig_lap1, use_container_width=True)

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.markdown(f'<div class="result-pill result-pill-blue">Q* = {lap_q_eq:.3f}</div>', unsafe_allow_html=True)
        col_r2.markdown(f'<div class="result-pill result-pill-green">P* = {lap_p_eq:.4f}</div>', unsafe_allow_html=True)
        col_r3.markdown(f'<div class="result-pill result-pill-blue">CS = {lap_cs:.4f}</div>', unsafe_allow_html=True)
        col_r4.markdown(f'<div class="result-pill result-pill-amber">Q maks = {lap_q_max:.2f}</div>', unsafe_allow_html=True)

        pergeseran = lap_q_eq - lap_q_orig
        arah = "↑ naik" if pergeseran > 0 else "↓ turun"
        st.markdown(f"""
<div class="card card-amber" style="margin-top:8px;padding:12px 18px;">
📌 <b>Interpretasi Pergeseran:</b> Dibanding baseline, titik ekuilibrium bergeser
<span style="color:{'#065f46' if pergeseran>0 else '#991b1b'};font-weight:700;">{arah} sebesar {abs(pergeseran):.3f} unit Q</span>.
{'Kurva lebih datar → permintaan lebih elastis.' if lap_slope_abs < abs(SLOPE) else
 'Kurva lebih curam → permintaan lebih inelastis.' if lap_slope_abs > abs(SLOPE) else
 'Kemiringan sama dengan baseline.'}
</div>
""", unsafe_allow_html=True)

        # ── Analisis Ilmiah 4.1 ──
        analisis_box("""
<span class="ab-label ab-finding">📐 TEMUAN STATISTIK</span>
<span class="ab-label ab-critical">⚠️ LIMITASI MODEL</span>
<span class="ab-label ab-implic">✅ IMPLIKASI KEBIJAKAN</span><br><br>
<b>Temuan Statistik:</b> Estimasi OLS menghasilkan koefisien kemiringan (b = −1,137) yang secara
statistik signifikan pada taraf kepercayaan 99% (p = 0,006). Nilai R² sebesar 0,633 mengindikasikan
bahwa sekitar 63,3% variasi harga dapat dijelaskan oleh variasi kuantitas produksi — angka yang
tergolong moderat dalam analisis <i>time-series</i> komoditas berdurasi pendek (n = 10). Statistik
F sebesar 13,80 mengonfirmasi bahwa model secara keseluruhan signifikan.<br><br>
<b>Limitasi Model yang Wajib Dikritisi:</b> Regresi OLS sederhana dua-variabel mengandung risiko
<i>omitted variable bias</i> (OVB) yang substansial. Variabel harga energi substitusi, kurs IDR/USD,
pertumbuhan ekonomi mitra dagang, serta volatilitas kebijakan ekspor tidak dimasukkan sebagai kontrol.
Lebih jauh, terdapat potensi endogenitas antara P dan Q — harga mempengaruhi keputusan produksi,
dan sebaliknya — yang membuat estimator OLS tidak konsisten. Pendekatan <i>two-stage least squares</i>
(2SLS) atau <i>vector autoregression</i> (VAR) dengan variabel instrumen yang valid akan menghasilkan
estimasi yang lebih andal secara kausal.<br><br>
<b>Implikasi Kebijakan:</b> <i>Choke price</i> Rp 863,9 juta/ton merepresentasikan batas valuasi
teoritis yang dapat digunakan sebagai acuan dalam penetapan <i>resource rent tax</i> progresif dan
sebagai tolok ukur penilaian cadangan dalam kerangka JORC atau NI 43-101.
""")

        regresi_df = pd.DataFrame({
            "Variabel": ["Q (Kuantitas Produksi)", "Konstanta (_cons)"],
            "Koefisien": [-1.136737, 53.99302],
            "Std. Error": [0.306004, 10.48285],
            "t-statistik": [-3.71, 5.15],
            "P>|t|": [0.006, 0.001],
        })
        st.dataframe(regresi_df, use_container_width=True)

    # 4.2 — SPEKTRUM CADANGAN
    with st.expander("4.2  Analisis Pergeseran Spektrum Cadangan"):
        st.markdown('<div class="sim-panel-green"><span class="sim-badge" style="background:#22c55e;">🎛️ SIMULASI SPEKTRUM CADANGAN</span>', unsafe_allow_html=True)
        st.markdown("Geser harga dan biaya untuk melihat berapa banyak tahun masuk kategori Reserve vs Resource.")
        sg1, sg2 = st.columns(2)
        with sg1:
            hba_mult = st.slider("Skenario Harga HBA (× dari aktual)", 0.3, 2.5, 1.0, 0.05,
                                 key="spec_hba", help="1.0 = harga aktual; <1 = harga turun; >1 = harga naik")
        with sg2:
            mc_level = st.slider("Skenario MC (Rp/ton)", 50000, 2000000, int(MC_AVG), 50000,
                                 key="spec_mc", help="Ubah biaya marjinal untuk melihat dampak ke status cadangan")
        st.markdown('</div>', unsafe_allow_html=True)

        status_data = data.copy()
        status_data["HBA_sim"]     = status_data["HBA"] * hba_mult
        status_data["Margin_sim"]  = status_data["HBA_sim"] - mc_level
        status_data["Status"]      = status_data["Margin_sim"].apply(lambda x: "✅ Reserve" if x > 0 else "⚠️ Resource")
        status_data["Margin_awal"] = status_data["HBA"] - MC_AVG
        n_reserve  = (status_data["Status"] == "✅ Reserve").sum()
        n_resource = (status_data["Status"] == "⚠️ Resource").sum()

        sm1, sm2, sm3 = st.columns(3)
        sm1.metric("Tahun sebagai Reserve",  f"{n_reserve} / 10")
        sm2.metric("Tahun sebagai Resource", f"{n_resource} / 10")
        sm3.metric("MC Skenario", f"Rp {mc_level:,.0f}")

        colors_bar = ["#10b981" if v > 0 else "#ef4444" for v in status_data["Margin_sim"]]
        fig_spec = go.Figure()
        fig_spec.add_trace(go.Bar(x=status_data["Year"], y=status_data["Margin_sim"],
            marker_color=colors_bar, name="Margin Simulasi",
            text=[f"{'✅' if v>0 else '⚠️'} Rp {v:,.0f}" for v in status_data["Margin_sim"]],
            textposition="outside"))
        fig_spec.add_trace(go.Scatter(x=status_data["Year"], y=status_data["Margin_awal"],
            mode="lines+markers", name="Margin Baseline",
            line=dict(color="#94a3b8", width=2, dash="dot"), marker=dict(size=7)))
        fig_spec.add_hline(y=0, line_color="#1e293b", line_width=2)
        fig_spec.update_layout(
            title=f"Margin (HBA×{hba_mult:.2f} − MC Rp {mc_level:,.0f}) per Tahun",
            xaxis_title="Tahun", yaxis_title="Margin (Rp/ton)", **PLOT_STYLE, height=400)
        styled_axes(fig_spec)
        st.plotly_chart(fig_spec, use_container_width=True)

        # ── Analisis Ilmiah 4.2 ──
        analisis_box(f"""
<span class="ab-label ab-finding">🔬 ANALISIS McKELVEY</span>
<span class="ab-label ab-critical">⚠️ KRITIK DINAMIS</span>
<span class="ab-label ab-implic">✅ IMPLIKASI STRATEGIS</span><br><br>
<b>Analisis Spektrum Cadangan (McKelvey Box):</b> Pada skenario baseline (HBA aktual, MC rata-rata
Rp 283.817/ton), seluruh 10 tahun observasi menunjukkan margin positif, mengindikasikan bahwa
cadangan MBAP secara konsisten berada di <b>Kuadran I McKelvey</b> (Reserve — teridentifikasi dan
layak ekonomi). Namun kepositifan margin ini bersifat sangat sensitif terhadap perubahan harga:
penurunan HBA sebesar 60–70% dari level aktual sudah cukup untuk mendorong sejumlah tahun observasi
masuk ke kategori <b>Conditional Resource</b> (Kuadran II).<br><br>
<b>Kritik Dinamis:</b> Grafik margin mengekspos <i>price dependency</i> yang ekstrem dalam
klasifikasi cadangan MBAP. Lonjakan margin pada 2022 (HBA >Rp 4 juta/ton) mencerminkan fenomena
<i>windfall rent</i> — keuntungan yang tidak mencerminkan peningkatan produktivitas riil, melainkan
semata guncangan sisi penawaran global. Mengandalkan harga spot tahunan untuk mengklasifikasikan
cadangan adalah pendekatan yang <i>procyclical</i>: menciptakan ilusi kelimpahan saat boom dan
kepanikan alokasi saat koreksi.<br><br>
<b>Implikasi Strategis:</b> Perusahaan dan regulator perlu mengadopsi <i>price band</i> konservatif
dalam perencanaan cadangan — misalnya menggunakan rata-rata HBA 5 tahun (<i>rolling average</i>)
sebagai basis klasifikasi, bukan harga spot tahunan. Pendekatan ini sejalan dengan praktik terbaik
standar pelaporan JORC (Australia) dan NI 43-101 (Kanada) yang mensyaratkan penggunaan harga
<i>long-run equilibrium</i> dalam penentuan status cadangan.
""")

        st.dataframe(status_data[["Year","HBA","HBA_sim","Margin_sim","Status"]].rename(
            columns={"Year":"Tahun","HBA":"HBA Aktual","HBA_sim":"HBA Simulasi",
                     "Margin_sim":"Margin (Rp/ton)","Status":"Status Cadangan"}),
            use_container_width=True)

    # 4.3 — HOTELLING
    with st.expander("4.3  Evaluasi Efisiensi Intertemporal (Uji Hotelling)"):
        st.markdown('<div class="sim-panel-purple"><span class="sim-badge" style="background:#a855f7;">🎛️ SIMULASI JALUR HOTELLING</span>', unsafe_allow_html=True)
        st.markdown("Ubah parameter untuk melihat bagaimana jalur MUC bergerak dan T* berubah.")
        sh1, sh2, sh3 = st.columns(3)
        with sh1: hot_r    = st.slider("Tingkat Diskonto r (%)", 1, 25, 5, 1, key="hot_r") / 100
        with sh2: hot_muc0 = st.slider("MUC Awal λ₀ (Rp)", 1000, 100000, 15163, 1000, key="hot_muc0")
        with sh3: hot_cp_mc = st.slider("Choke − MC (juta Rp)", 100, 2000, int((CHOKE_PRICE_RP-MC_AVG)/1e6), 10,
                                         key="hot_cpmc") * 1_000_000
        st.markdown('</div>', unsafe_allow_html=True)

        if hot_muc0 > 0 and hot_cp_mc > 0:
            hot_t_star = (1 / hot_r) * np.log(hot_cp_mc / hot_muc0)
            t_max_plot = max(200, hot_t_star * 1.4)
            t_hot = np.linspace(0, t_max_plot, 500)
            muc_hot = hot_muc0 * np.exp(hot_r * t_hot)
            hba_mc_actual = data["HBA"] - MC_AVG
            t_actual = data["Year"] - data["Year"].min()

            hm1, hm2, hm3 = st.columns(3)
            hm1.metric("T* Simulasi", f"{hot_t_star:.1f} tahun", delta=f"{hot_t_star - T_STAR:+.1f} vs baseline")
            hm2.metric("Tahun Cadangan Habis", f"~{2025 + int(hot_t_star)}")
            hm3.metric("MUC pada T*", f"Rp {hot_muc0 * np.exp(hot_r * hot_t_star):,.0f}")

            fig_hot = go.Figure()
            fig_hot.add_trace(go.Scatter(x=t_hot, y=muc_hot, mode="lines",
                name=f"MUC(t) = {hot_muc0:,}·e^({hot_r:.2f}t)",
                line=dict(color="#8b5cf6", width=3), fill="tozeroy", fillcolor="rgba(139,92,246,0.08)"))
            muc_base = MUC_AWAL * np.exp(DISCOUNT_RATE * t_hot)
            fig_hot.add_trace(go.Scatter(x=t_hot, y=muc_base, mode="lines",
                name="MUC Baseline (r=5%, λ₀=15.163)",
                line=dict(color="#94a3b8", width=2, dash="dot"), opacity=0.7))
            fig_hot.add_hline(y=hot_cp_mc, line_dash="dash", line_color="#ec4899",
                              annotation_text=f"Choke−MC = Rp {hot_cp_mc/1e6:.0f}jt", annotation_font_color="#ec4899")
            fig_hot.add_vline(x=hot_t_star, line_dash="dot", line_color="#10b981",
                              annotation_text=f"T* = {hot_t_star:.1f} thn", annotation_font_color="#10b981")
            fig_hot.add_vline(x=T_STAR, line_dash="dot", line_color="#94a3b8",
                              annotation_text=f"T* baseline = {T_STAR:.0f}",
                              annotation_font_color="#94a3b8", annotation_position="bottom right")
            fig_hot.add_trace(go.Scatter(x=t_actual, y=hba_mc_actual, mode="markers+lines",
                name="HBA − MC Aktual", marker=dict(color="#f59e0b", size=10, symbol="diamond"),
                line=dict(color="#f59e0b", width=1.5, dash="dash")))
            fig_hot.update_layout(
                title=f"Jalur MUC Hotelling — T* = {hot_t_star:.1f} tahun (r={hot_r*100:.0f}%)",
                xaxis_title="Tahun ke-", yaxis_title="MUC / Harga Bersih (Rp)", **PLOT_STYLE, height=440)
            styled_axes(fig_hot)
            st.plotly_chart(fig_hot, use_container_width=True)

            # ── Analisis Ilmiah 4.3 ──
            analisis_box(f"""
<span class="ab-label ab-finding">📉 EVALUASI HOTELLING RULE</span>
<span class="ab-label ab-critical">⚠️ DEVIASI EMPIRIS</span>
<span class="ab-label ab-implic">✅ REKOMENDASI ALOKASI</span><br><br>
<b>Evaluasi Kepatuhan terhadap Aturan Hotelling:</b> Jalur MUC teoritis pada r = {hot_r*100:.0f}%
menghasilkan T* = {hot_t_star:.1f} tahun. Perbandingan antara jalur MUC teoritis dengan data aktual
HBA − MC (titik berlian kuning) mengungkap <b>deviasi yang substansial dan tidak acak</b>: data
aktual memperlihatkan lonjakan dramatis pada 2021–2022 yang jauh melampaui jalur eksponensial
Hotelling, sebelum terkoreksi tajam pada 2023–2024. Pola ini tidak konsisten dengan asumsi
<i>rational intertemporal optimization</i> yang menjadi fondasi model.<br><br>
<b>Deviasi Empiris dan Akarnya:</b> Penyimpangan ini mengkonfirmasi temuan empiris luas dalam
literatur bahwa <i>Hotelling Rule</i> sulit diverifikasi karena pasar energi nyata dipengaruhi
faktor di luar model: guncangan geopolitik, perilaku kartel, ekspektasi teknologi substitusi, dan
<i>policy uncertainty</i>. Studi Halvorsen &amp; Smith (1991) serta Miller &amp; Upton (1985) telah
mendokumentasikan kegagalan empiris Hotelling Rule pada berbagai komoditas mineral. Secara khusus
untuk batubara, ancaman <i>stranded asset</i> akibat transisi energi global menambahkan dimensi
risiko yang sepenuhnya absen dari formulasi Hotelling orisinal.<br><br>
<b>Rekomendasi Alokasi:</b> T* = {hot_t_star:.1f} tahun harus diperlakukan sebagai <b>batas atas
normatif</b>, bukan proyeksi deterministik. Perencanaan operasional sebaiknya menggunakan
<i>scenario planning</i> tiga jalur: optimistis (r = 3%), baseline (r = 5%), dan konservatif
(r = 8–10%) untuk mempertimbangkan kisaran T* yang lebih realistis dalam konteks akselerasi
transisi energi global pasca-COP28.
""")

            r_vals_s = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
            sens_df = pd.DataFrame({
                "r": [f"{int(r*100)}%" for r in r_vals_s],
                "T* (tahun)": [f"{(1/r)*np.log(hot_cp_mc/hot_muc0):.1f}" for r in r_vals_s],
                "Habis ~Tahun": [f"~{2025+int((1/r)*np.log(hot_cp_mc/hot_muc0))}" for r in r_vals_s],
                "MUC t=10": [f"Rp {hot_muc0*np.exp(r*10):,.0f}" for r in r_vals_s]
            })
            st.markdown("**Tabel Sensitivitas T\* terhadap berbagai r:**")
            st.dataframe(sens_df, use_container_width=True)

            analisis_box("""
<span class="ab-label ab-finding">📊 ANALISIS SENSITIVITAS INTERTEMPORAL</span><br><br>
<b>Interpretasi Tabel Sensitivitas:</b> Tabel di atas mengungkap relasi <i>inverse non-linear</i>
antara tingkat diskonto (r) dan T*. Kenaikan r dari 3% ke 10% memotong T* secara dramatis —
mencerminkan bagaimana preferensi jangka pendek yang lebih tinggi secara sistematis mentransfer
kekayaan alam dari generasi mendatang ke generasi saat ini. Ini bukan sekadar kalkulasi teknis-finansial,
melainkan mengandung <b>dimensi etis intergenerasi yang fundamental</b>.<br><br>
Penggunaan <i>market discount rate</i> (5–8%) secara implisit menyatakan bahwa kesejahteraan generasi
mendatang bernilai lebih rendah secara eksponensial dibanding generasi saat ini — suatu posisi yang
dapat diperdebatkan secara moral dalam kerangka teori keadilan Rawlsian. Stern (2006) berargumen
bahwa <i>social discount rate</i> yang etis mendekati 1,4%, yang jika diterapkan di sini akan
memperpanjang T* secara signifikan dan mereduksi intensitas eksploitasi optimal saat ini.
""")

    # 4.4 — GREEN PARADOX
    with st.expander("4.4  Analisis Distorsi Pasar dan Green Paradox"):
        st.markdown('<div class="sim-panel-amber"><span class="sim-badge" style="background:#f59e0b;color:#1e293b;">🎛️ SIMULASI GREEN PARADOX</span>', unsafe_allow_html=True)
        st.markdown("Simulasikan dampak pengumuman pajak karbon terhadap keputusan produksi perusahaan.")
        gp1, gp2, gp3 = st.columns(3)
        with gp1:
            gp_tax_rp = st.slider("Besaran Pajak Karbon (Rp/ton)", 0, 1000000, 300000, 25000,
                                  key="gp_tax", help="Pajak yang direncanakan berlaku di masa depan")
        with gp2:
            gp_t_announce = st.slider("Tahun Pajak Berlaku (tahun ke-)", 1, 20, 5, 1,
                                      key="gp_ta", help="Berapa tahun dari sekarang pajak mulai berlaku")
        with gp3:
            gp_accel = st.slider("Percepatan Produksi Sblm Pajak (%)", 0, 100, 30, 5,
                                 key="gp_acc", help="Berapa % produksi dipercepat sebelum pajak berlaku")
        st.markdown('</div>', unsafe_allow_html=True)

        baseline_prod = data["Production"].mean()
        years_future  = list(range(2025, 2045))
        prod_baseline = [baseline_prod] * len(years_future)
        prod_accel = []; emisi_baseline = []; emisi_accel = []
        for i, yr in enumerate(years_future):
            t_rel = yr - 2025
            if t_rel < gp_t_announce:
                p = baseline_prod * (1 + gp_accel/100)
            else:
                sisa_rasio = max(0, 1 - (gp_accel/100) * (gp_t_announce / max(1, 20-gp_t_announce)))
                p = baseline_prod * sisa_rasio * max(0.3, 1 - (gp_tax_rp / 2000000))
            prod_accel.append(p)
            emisi_baseline.append(baseline_prod * 2.5 / 1e9)
            emisi_accel.append(p * 2.5 / 1e9)

        total_emisi_baseline = sum(emisi_baseline)
        total_emisi_accel    = sum(emisi_accel)
        delta_emisi = total_emisi_accel - total_emisi_baseline
        gpm1, gpm2, gpm3 = st.columns(3)
        gpm1.metric("Total Emisi Baseline", f"{total_emisi_baseline:.2f} Gt CO₂")
        gpm2.metric("Total Emisi + Green Paradox", f"{total_emisi_accel:.2f} Gt CO₂",
                    delta=f"+{delta_emisi:.2f} Gt" if delta_emisi > 0 else f"{delta_emisi:.2f} Gt")
        gpm3.metric("Produksi Puncak (sblm pajak)", f"{max(prod_accel)/1e6:.2f} juta ton")

        fig_gp = make_subplots(rows=1, cols=2, subplot_titles=["Volume Produksi (ton)", "Emisi CO₂ Kumulatif (Gt)"])
        fig_gp.add_trace(go.Scatter(x=years_future, y=prod_baseline, mode="lines",
            name="Baseline", line=dict(color="#3b82f6", width=2.5, dash="dot")), row=1, col=1)
        colors_gp = ["#ef4444" if yr < 2025 + gp_t_announce else "#10b981" for yr in years_future]
        fig_gp.add_trace(go.Bar(x=years_future, y=prod_accel, name="Dengan Green Paradox",
            marker_color=colors_gp, opacity=0.85), row=1, col=1)
        fig_gp.add_vline(x=2025 + gp_t_announce - 0.5, line_dash="dash", line_color="#f59e0b",
                         annotation_text=f"Pajak berlaku {2025+gp_t_announce}",
                         annotation_font_color="#f59e0b", row=1, col=1)
        emisi_cum_base  = np.cumsum(emisi_baseline)
        emisi_cum_accel = np.cumsum(emisi_accel)
        fig_gp.add_trace(go.Scatter(x=years_future, y=emisi_cum_base, mode="lines",
            name="Emisi Baseline", line=dict(color="#3b82f6", width=2.5)), row=1, col=2)
        fig_gp.add_trace(go.Scatter(x=years_future, y=emisi_cum_accel, mode="lines",
            name="Emisi + Paradox", line=dict(color="#ef4444", width=2.5),
            fill="tonexty", fillcolor="rgba(239,68,68,0.1)"), row=1, col=2)
        fig_gp.update_layout(paper_bgcolor="white", plot_bgcolor="#f8fafc",
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

        # ── Analisis Ilmiah 4.4 ──
        analisis_box(f"""
<span class="ab-label ab-finding">🌍 MEKANISME GREEN PARADOX</span>
<span class="ab-label ab-critical">⚠️ CRITIQUE OF POLICY DESIGN</span>
<span class="ab-label ab-implic">✅ SOLUSI BERBASIS BUKTI</span><br><br>
<b>Mekanisme Formal Green Paradox (Sinn, 2008):</b> Fenomena ini berakar dari rasionalitas
intertemporal produsen sumber daya tak terbarukan. Ketika pemerintah mengumumkan pajak karbon
yang baru berlaku pada tahun ke-{gp_t_announce}, produsen menghadapi pilihan: menjual sekarang
pada harga bersih (P − MC) atau menunggu dengan beban pajak tambahan. Nilai sekarang dari penjualan
masa depan turun sebesar nilai pajak yang didiskontokan — mendorong pergeseran kurva penawaran ke
kanan dan akselerasi produksi pra-pajak. Simulasi mengkonfirmasi kelebihan emisi kumulatif
<b>{abs(delta_emisi):.2f} Gt CO₂</b> sebagai akibat mekanisme ini.<br><br>
<b>Kritik Desain Kebijakan:</b> Hasil simulasi menyoroti kegagalan fundamental pendekatan karbon
yang bersifat <i>pre-announced</i> dengan <i>long implementation lag</i>. Semakin jauh horison
implementasi pajak, semakin besar insentif akselerasi, dan semakin lebar <i>paradox gap</i> antara
tujuan dan <i>outcome</i> kebijakan. Pajak yang lebih besar (Rp {gp_tax_rp:,}/ton) justru
memperbesar intensitas paradoks jika tidak diimbangi <i>immediate binding constraint</i> terhadap
produksi saat ini — sebuah dilema kebijakan yang secara konseptual belum terpecahkan dalam
literatur iklim internasional.<br><br>
<b>Solusi Berbasis Bukti:</b> Tiga pendekatan empiris telah terbukti memitigasi Green Paradox:
(1) <b>Pajak karbon berlaku segera dengan kenaikan bertahap (<i>escalating carbon price</i>)</b> —
menghilangkan insentif akselerasi karena setiap ton yang dijual hari ini sudah menanggung biaya
karbon; (2) <b>Kuota produksi absolut berbasis anggaran karbon</b> — memutus hubungan antara
ekspektasi harga dan keputusan produksi; (3) <b>Moratorium ekspansi konsesi baru</b> — membatasi
<i>supply side</i> struktural tanpa menciptakan insentif akselerasi. Kombinasi instrumen ini dikenal
sebagai <i>supply-side climate policy</i> (Lazarus &amp; van Asselt, 2018).
""")

    # ── BAB V ──
    st.markdown("""
<div style="margin-top:32px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
    <div style="background:linear-gradient(135deg,#991b1b,#ef4444);color:white;border-radius:10px;padding:6px 16px;font-weight:800;font-size:1rem;">BAB V</div>
    <h3 style="margin:0;color:#1e293b;font-size:1.25rem;">KESIMPULAN DAN REKOMENDASI</h3>
  </div>
  <div class="section-divider" style="margin:8px 0 18px 0;"></div>
</div>
""", unsafe_allow_html=True)

    with st.expander("5.1  Kesimpulan", expanded=True):
        st.markdown("""
<div class="card card-red">

**1. Fungsi Permintaan: Kekuatan Sekaligus Keterbatasan Epistemologis**

Estimasi OLS menghasilkan P = 53,993 − 1,137Q (R² = 0,633, F = 13,80) — secara statistik memadai,
namun tidak mencukupi untuk menangkap kompleksitas struktural pasar batubara global. Absennya
variabel instrumen dan potensi endogenitas P–Q menjadi catatan metodologis yang tidak dapat diabaikan.
*Choke Price* Rp 863,9 juta/ton adalah referensi valuasi yang berguna, dengan catatan ia bersifat
*model-dependent* dan bukan harga pasar yang dapat diobservasi secara langsung.

**2. Dinamika MC: Indikator yang Menyesatkan Jika Dibaca Mentah**

Rata-rata MC Rp 283.817/ton menyembunyikan volatilitas ekstrem, termasuk nilai negatif pada 2018,
2022, dan 2023 — *artifact* metodologis dari pendekatan COGS differencing yang tidak mampu
memisahkan biaya tetap dari biaya variabel. Penggunaannya sebagai konstanta tunggal dalam model
Hotelling perlu diperlakukan dengan reservasi ilmiah yang serius.

**3. T* = 114 Tahun: Optimisme yang Harus Dikalibrasi Ulang**

T* ≈ 114 tahun pada r = 5% adalah *upper bound* normatif, bukan jaminan keberlanjutan. Pada r yang
lebih realistis untuk pasar berkembang (8–10%), T* menyusut ke kisaran 60–70 tahun. Lebih kritis:
T* sama sekali tidak memperhitungkan risiko *stranded assets* akibat akselerasi transisi energi
global yang dapat mengobsoleskan permintaan batubara jauh sebelum cadangan habis secara fisik.

**4. Green Paradox: Ancaman Sistematik yang Diabaikan Pembuat Kebijakan**

Simulasi mengkonfirmasi bahwa kebijakan karbon dengan *implementation lag* panjang bersifat
kontraproduktif dalam jangka pendek. Kegagalan desain kebijakan ini bukan teori abstrak —
ia terdokumentasi secara empiris di berbagai negara produsen yang mengumumkan moratorium atau
pajak karbon dengan horison jauh.

</div>
""", unsafe_allow_html=True)

    with st.expander("5.2  Rekomendasi Strategis — Cetak Biru Transformasi"):

        st.markdown("""
<div class="fw-banner">
  <div class="fw-banner-title">🧭 KERANGKA KEBIJAKAN: "EXTRACT SMART, TRANSITION FASTER"</div>
  <div class="fw-banner-body">
    Rekomendasi berikut dirancang sebagai <b style="color:#f1f5f9;">cetak biru transformasi sistemik</b>
    yang mengakui ketegangan inheren antara profitabilitas jangka pendek, keberlanjutan intertemporal,
    dan tanggung jawab lingkungan lintas generasi. Setiap rekomendasi dirancang dengan logika kausalitas
    yang jelas — bukan sekadar anjuran normatif yang mengawang tanpa mekanisme implementasi.
  </div>
</div>
""", unsafe_allow_html=True)

        # GOV
        st.markdown('<div class="policy-section-title">🏛️ UNTUK PEMERINTAH REPUBLIK INDONESIA</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="pcard pcard-gov" data-num="R1">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">⚡ R1 — Pajak Karbon Dinamis Berbasis HBA (<i>Price-Linked Carbon Tax</i>)</div>
    <div class="pcard-body">
      Bukan sekadar pajak karbon flat — melainkan tarif yang <b>berfluktuasi proporsional terhadap HBA</b>:
      saat HBA tinggi (booming), tarif naik otomatis menangkap windfall rent; saat HBA rendah, tarif turun
      melindungi industri dari kebangkrutan. Formula: <i>τ(t) = τ_base × (HBA_t / HBA_rolling_avg)</i>.
      Mekanisme ini secara struktural mengeliminasi insentif windfall extraction sekaligus bersifat
      <i>countercyclical</i> — justru kebalikan dari pajak flat yang terlalu ringan saat boom
      dan terlalu berat saat bust.<br><br>
      <b>Mengapa lebih baik dari status quo?</b> Indonesia telah memiliki pajak karbon Rp 30.000/ton CO₂
      sejak 2022 — namun nilainya terlalu kecil (sekitar $2/ton vs rekomendasi IMF $75/ton) dan bersifat
      flat sehingga gagal menangkap ekonomi rente yang terbukti sangat besar pada 2021–2022.
    </div>
    <div>
      <span class="ptag pt-blue">Instrumen Fiskal Inovatif</span>
      <span class="ptag pt-red">Prioritas Segera</span>
      <span class="ptag pt-amber">Implementasi 2026–2027</span>
    </div>
  </div>
</div>

<div class="pcard pcard-gov" data-num="R2">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">🔒 R2 — Kuota Produksi Nasional Berbasis Anggaran Karbon (<i>Carbon Budget Quota</i>)</div>
    <div class="pcard-body">
      Indonesia harus menetapkan <b>batas produksi batubara nasional</b> yang secara eksplisit
      terintegrasi dengan komitmen NDC Paris Agreement. Bukan moratorium tiba-tiba yang memicu Green
      Paradox, melainkan <b>penurunan kuota bertahap 3–5% per tahun</b> mulai 2027 yang terencana,
      transparan, dan mengikat secara hukum melalui revisi UU Minerba.<br><br>
      <b>Kritik terhadap status quo:</b> Tidak adanya <i>ceiling</i> produksi nasional adalah lubang
      kebijakan terbesar Indonesia dalam tata kelola SDA batubara. Membiarkan keputusan produksi
      sepenuhnya pada mekanisme pasar adalah kegagalan menginternalisasi biaya generasi mendatang —
      suatu bentuk subsidi implisit yang dibebankan kepada anak cucu.
    </div>
    <div>
      <span class="ptag pt-blue">Regulasi Sisi Penawaran</span>
      <span class="ptag pt-red">Kritis-Sistemik</span>
      <span class="ptag pt-amber">2027–2035 Fase I</span>
    </div>
  </div>
</div>

<div class="pcard pcard-gov" data-num="R3">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">💰 R3 — Dana Transformasi Generasi (<i>Sovereign Transition Fund</i>) — Model Norwegian GPF</div>
    <div class="pcard-body">
      Setiap sen <i>windfall rent</i> dari HBA di atas US$120/ton wajib masuk ke
      <b>Dana Transformasi Generasi (DTG)</b> — dana abadi berstruktur <i>sovereign wealth fund</i>
      yang secara konstitusional diamanatkan untuk: (1) investasi infrastruktur EBT, (2) beasiswa
      riset energi bersih, (3) jaring pengaman sosial bagi 1,2 juta pekerja tambang yang akan
      terdampak transisi energi.<br><br>
      <b>Realitas yang memprihatinkan:</b> Windfall HBA 2021–2022 menghasilkan keuntungan luar biasa
      bagi industri, namun sebagian besar mengalir ke dividen pemegang saham dan ekspansi kapasitas —
      bukan ke investasi transisi. Tanpa mekanisme institusional yang mengikat, siklus ini akan
      berulang selamanya. Model Norwegia membuktikan batubara/minyak bisa menjadi fondasi kemakmuran
      lintas generasi — jika dikelola dengan disiplin fiskal yang ketat.
    </div>
    <div>
      <span class="ptag pt-blue">Fiskal Intergenerasi</span>
      <span class="ptag pt-green">Model Terbukti (Norwegia)</span>
      <span class="ptag pt-amber">Legislasi 2026</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # CORP
        st.markdown('<div class="policy-section-title">🏢 UNTUK PT MITRABARA ADIPERDANA TBK</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="pcard pcard-corp" data-num="R4">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">🌱 R4 — Strategi "Coal-to-Clean": Diversifikasi Portofolio Menuju Perusahaan Energi</div>
    <div class="pcard-body">
      MBAP harus secara eksplisit mendefinisikan ulang identitas korporasinya dari "perusahaan
      pertambangan batubara" menjadi <b>"perusahaan energi yang sedang bertransisi"</b>. Langkah
      konkret: alokasi minimum 15% CAPEX tahunan ke proyek energi terbarukan (PLTS, PLTBm dari
      limbah tambang), pengembangan fasilitas gasifikasi batubara untuk pasar domestik, dan
      investasi dalam teknologi CCUS (<i>carbon capture, utilization and storage</i>).<br><br>
      <b>Mengapa urgen?</b> Dengan T* = 114 tahun, MBAP memiliki <i>runway</i> yang cukup untuk
      transisi gradual — tetapi hanya jika dimulai sekarang. Setiap tahun keterlambatan mempersingkat
      jendela transisi yang tersedia dan meningkatkan risiko <i>stranded asset</i> ketika permintaan
      batubara global mulai kontraksi struktural pasca-2030.
    </div>
    <div>
      <span class="ptag pt-green">Transformasi Bisnis</span>
      <span class="ptag pt-blue">Diversifikasi Portofolio</span>
      <span class="ptag pt-amber">Horizon 2030</span>
    </div>
  </div>
</div>

<div class="pcard pcard-corp" data-num="R5">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">📐 R5 — Rencanakan pada <i>Social Discount Rate</i> (r = 2–3%), Bukan <i>Market Rate</i></div>
    <div class="pcard-body">
      Perencanaan cadangan internal MBAP saat ini mungkin menggunakan <i>weighted average cost of
      capital</i> (WACC) sebagai diskonto — umumnya 10–15% untuk sektor tambang Indonesia. Pada
      tingkat ini, T* menyusut ke kisaran 50–60 tahun, menciptakan tekanan implisit untuk
      mempercepat ekstraksi. <b>Mengadopsi <i>social discount rate</i> 2–3% untuk perencanaan
      cadangan jangka panjang</b> akan memperpanjang T* secara signifikan, mengurangi intensitas
      ekstraksi optimal, dan memposisikan perusahaan sebagai operator yang bertanggung jawab
      secara intergenerasi — sebuah keunggulan kompetitif nyata dalam era investor ESG.<br><br>
      <b>Argumen bisnis:</b> Investor institusional global (BlackRock, Vanguard) semakin
      mensyaratkan perencanaan berbasis <i>social discount rate</i> dalam penilaian ESG.
      MBAP yang pertama mengadopsi ini di industri batubara Indonesia akan memperoleh
      <i>first-mover advantage</i> dalam akses modal ESG.
    </div>
    <div>
      <span class="ptag pt-green">ESG Leadership</span>
      <span class="ptag pt-blue">Perencanaan Strategis</span>
      <span class="ptag pt-purple">Keunggulan Kompetitif</span>
    </div>
  </div>
</div>

<div class="pcard pcard-corp" data-num="R6">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">📊 R6 — Transparansi Radikal: Integrasikan Shadow Price Karbon ke Laporan Keuangan</div>
    <div class="pcard-body">
      MBAP harus menjadi pelopor dengan mengintegrasikan <b><i>shadow carbon price</i></b>
      (bayangan harga karbon: US$50–75/ton CO₂ sesuai rekomendasi IMF) secara eksplisit ke
      dalam laporan keuangan tahunan — memperlihatkan berapa nilai "utang karbon" yang belum
      dibayar kepada atmosfer dan generasi mendatang. Selain itu, publikasikan <b><i>reserve
      life index</i></b> yang dihitung pada tiga skenario diskonto (3%, 5%, 8%) untuk
      memberikan gambaran jujur tentang kelangkaan relatif cadangan.<br><br>
      <b>Mengapa penting?</b> Tanpa transparansi ini, laporan keuangan MBAP secara sistematis
      <i>overvalue</i> aset cadangan karena tidak mencerminkan biaya eksternalitas karbon.
      Ini bukan hanya masalah etika — ini adalah risiko regulasi dan litigasi yang nyata
      seiring implementasi TCFD (<i>Task Force on Climate-related Financial Disclosures</i>)
      menjadi wajib di bursa saham global.
    </div>
    <div>
      <span class="ptag pt-green">Pelaporan ESG</span>
      <span class="ptag pt-blue">TCFD Compliance</span>
      <span class="ptag pt-red">Mitigasi Risiko Regulasi</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # CRITICAL
        st.markdown('<div class="policy-section-title">🔴 REKOMENDASI KRITIS — HAL YANG TIDAK BOLEH DILAKUKAN</div>', unsafe_allow_html=True)

        st.markdown("""
<div class="pcard pcard-crit" data-num="X">
  <div style="position:relative;z-index:1;">
    <div class="pcard-title">🚫 Anti-Rekomendasi: Jebakan Kebijakan yang Harus Dihindari</div>
    <div class="pcard-body">
      Analisis ini juga mengidentifikasi tiga <b>anti-pola kebijakan</b> yang secara intuitif
      tampak masuk akal namun terbukti kontraproduktif secara ilmiah:<br><br>
      <b>(1) Moratorium ekspor tiba-tiba</b> — seperti yang dilakukan Januari 2022, justru menciptakan
      panik pasar, lonjakan HBA global, dan insentif kuat bagi produsen untuk mempercepat ekstraksi
      segera setelah moratorium dicabut. Kebijakan sisi penawaran harus <i>gradual dan predictable</i>,
      bukan kejutan.<br><br>
      <b>(2) Subsidi energi terbarukan tanpa disertai penghapusan subsidi batubara</b> — menciptakan
      persaingan yang tidak setara dan memperlambat transisi. Subsidi EBT hanya efektif jika
      <i>level playing field</i> dipulihkan dengan menghilangkan subsidi implisit dan eksternalitas
      yang tidak diinternalisasi oleh sektor batubara.<br><br>
      <b>(3) Penetapan HBA domestik di bawah harga internasional (DMO 25%)</b> — secara paradoks
      menstimulasi konsumsi domestik yang berlebihan dan menghambat efisiensi energi, berlawanan
      dengan tujuan transisi energi. Subsidi energi fosil adalah bentuk paling regresif dari
      transfer kekayaan dari generasi mendatang ke konsumen saat ini.
    </div>
    <div>
      <span class="ptag pt-purple">Analisis Kritis</span>
      <span class="ptag pt-red">Peringatan Kebijakan</span>
      <span class="ptag pt-amber">Berbasis Bukti Empiris</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── DAFTAR PUSTAKA ──
    with st.expander("Daftar Pustaka"):
        st.markdown("""
<div class="card card-blue" style="font-size:0.88rem;line-height:2.0;">

**Buku & Artikel Ilmiah:**
- Hotelling, H. (1931). *The Economics of Exhaustible Resources*. Journal of Political Economy, 39(2), 137–175.
- Sinn, H.W. (2008). *Public Policies against Global Warming: A Supply Side Approach*. International Tax and Public Finance, 15(4), 360–394.
- Santayana, G. (1896). *The Sense of Beauty*. Charles Scribner's Sons.
- Tietenberg, T. & Lewis, L. (2018). *Environmental and Natural Resource Economics* (11th ed.). Routledge.
- Field, B.C. & Field, M.K. (2016). *Environmental Economics: An Introduction* (7th ed.). McGraw-Hill.
- Stern, N. (2006). *The Economics of Climate Change: The Stern Review*. Cambridge University Press.
- Halvorsen, R. & Smith, T.R. (1991). A test of the theory of exhaustible resources. *The Quarterly Journal of Economics*, 106(1), 123–140.
- Lazarus, M. & van Asselt, H. (2018). Fossil fuel supply and climate policy. *Climatic Change*, 150(1), 1–13.

**Data & Laporan:**
- PT Mitrabara Adiperdana Tbk. (2015–2024). *Laporan Tahunan*. IDX: MBAP.
- Kementerian ESDM RI. (2015–2024). *Harga Batubara Acuan (HBA) Bulanan*.
- Bank Indonesia. (2024). *Laporan Kebijakan Moneter*.
- IEA. (2023). *Coal 2023 — Analysis and Forecast to 2026*.
- IPCC. (2022). *Sixth Assessment Report (AR6) — WG III: Mitigation of Climate Change*.
- IMF. (2023). *Fiscal Policies for a Livable Planet*. Fiscal Monitor.

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:linear-gradient(135deg,#1e293b,#334155);border-radius:16px;
            padding:20px 28px;margin-top:28px;text-align:center;color:#94a3b8;font-size:0.82rem;line-height:2;">
  <b style="color:#e2e8f0;font-size:0.95rem;">PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</b><br>
  Arif Hamdani (10090224008) &nbsp;·&nbsp; Bambang Karta Wijaya (10090224025) &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
  Dosen Pembimbing: <b style="color:#cbd5e1;">Yuhka Sundaya, S.E., M.Si.</b>
  &nbsp;·&nbsp; Universitas Islam Bandung &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.82rem;padding:16px 0;line-height:1.9;">
  <b style="color:#64748b;">PBL 3 — Ekonomi Sumber Daya Alam dan Lingkungan</b><br>
  Dikembangkan oleh: Arif Hamdani (10090224008) &nbsp;·&nbsp;
  Bambang Karta Wijaya (10090224025) &nbsp;·&nbsp; Moh Bayu Mustofa (10090224030)<br>
  Di bawah bimbingan <b style="color:#64748b;">Yuhka Sundaya, S.E., M.Si.</b>
  &nbsp;·&nbsp; Universitas Islam Bandung &nbsp;·&nbsp; Kelompok 6 &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)