import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Analisis Batubara — MBAP",
    page_icon="⛏️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f8f9fa; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.page-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    color: white;
}
.page-header h1 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: white !important;
    margin: 0 0 6px 0 !important;
}
.page-header p {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.65);
    margin: 0;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1a1a2e;
    border-left: 4px solid #185FA5;
    padding-left: 12px;
    margin: 32px 0 14px 0;
}
.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6c757d;
    margin: 18px 0 10px 0;
}

.metric-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.metric-card .num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 600;
    display: block;
    margin-bottom: 2px;
}
.metric-card .lbl {
    font-size: 0.72rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.num-blue   { color: #185FA5; }
.num-green  { color: #3B6D11; }
.num-amber  { color: #854F0B; }
.num-red    { color: #A32D2D; }
.num-purple { color: #3C3489; }

.market-card {
    background: white;
    border-radius: 10px;
    padding: 16px;
    border-left: 3px solid #e9ecef;
    border-top: 1px solid #e9ecef;
    border-right: 1px solid #e9ecef;
    border-bottom: 1px solid #e9ecef;
    margin-bottom: 12px;
}
.market-card.pc     { border-left-color: #1D9E75; }
.market-card.oli    { border-left-color: #BA7517; }
.market-card.mono   { border-left-color: #A32D2D; }
.mc-name { font-size: 0.88rem; font-weight: 600; color: #1a1a2e; margin-bottom: 10px; }
.mc-row  { display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 6px; }
.mc-lbl  { color: #6c757d; }
.mc-val  { font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #1a1a2e; }
.badge   { display: inline-block; font-size: 0.7rem; padding: 2px 9px; border-radius: 20px; margin-top: 8px; font-weight: 500; }
.badge-g { background: #EAF3DE; color: #3B6D11; }
.badge-y { background: #FAEEDA; color: #854F0B; }
.badge-r { background: #FCEBEB; color: #A32D2D; }

.insight-box {
    background: white;
    border: 1px solid #e9ecef;
    border-left: 3px solid #185FA5;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #495057;
    line-height: 1.75;
    margin: 12px 0;
}
.theory-box {
    background: #f0f4ff;
    border: 1px solid #c7d4f5;
    border-left: 3px solid #3C3489;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #2d3561;
    line-height: 1.75;
    margin: 12px 0;
}
.warn-box {
    background: #FAEEDA;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #854F0B;
    line-height: 1.75;
    margin: 12px 0;
}
.danger-box {
    background: #FCEBEB;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #A32D2D;
    line-height: 1.75;
    margin: 12px 0;
}
.success-box {
    background: #EAF3DE;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #3B6D11;
    line-height: 1.75;
    margin: 12px 0;
}

div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
}
.divider-section {
    border: none;
    border-top: 2px dashed #dee2e6;
    margin: 36px 0 24px 0;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
A        = 53.99302
B        = 1.136737
MC_BASE  = 283817.2
HBA_BASE = 1.9375e6
CP_BASE  = 863888320.0
MUC0_BASE = 15163.0
R_BASE   = 0.05
T_STAR_BASE = 114.12

# ─── DATA HISTORIS ──────────────────────────────────────────────────────────────
data = pd.DataFrame({
    "Year":       [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Production": [4143080, 3591337, 3879211, 3560069, 4187315,
                   4015358, 3398718, 2222091, 2227170, 2112983],
    "COGS":       [1892047772700, 1609109212500, 1918470991920, 2232221611560,
                   2377156677000, 2112995936000, 1783567280000, 2207269456000,
                   2200803424000, 2037147744000],
    "HBA":        [799729, 834840, 1149610, 1405232, 1090460,
                   843465, 1737021, 4093384, 3040000, 1937500],
    "MC":         [132295, 512808, 1074648, -983107, 231006,
                   1536202, 534231, -360009, -1273092, 1433225],
})

PLOT_STYLE = dict(
    paper_bgcolor="white",
    plot_bgcolor="#f8f9fb",
    font=dict(color="#1a1a2e", family="Inter, sans-serif"),
    margin=dict(t=40, b=36, l=50, r=20),
    legend=dict(bgcolor="white", bordercolor="#e9ecef", borderwidth=1, font=dict(size=11)),
)

def ax(fig):
    fig.update_xaxes(gridcolor="#edf2f7", linecolor="#dee2e6", zerolinecolor="#dee2e6")
    fig.update_yaxes(gridcolor="#edf2f7", linecolor="#dee2e6", zerolinecolor="#dee2e6")
    return fig

def calc_market(hba_m, mc_m, n):
    mc_u = mc_m / hba_m * A if hba_m > 0 else A * 0.9
    mc_u = min(mc_u, A * 0.99)
    q_pc   = max(0.0, (A - mc_u) / B)
    p_pc   = mc_u
    q_mono = max(0.0, (A - mc_u) / (2 * B))
    p_mono = A - B * q_mono
    q_oli  = max(0.0, (n / (n + 1)) * (A - mc_u) / B)
    p_oli  = A - B * q_oli
    cs_pc   = 0.5 * (A - p_pc)   * q_pc
    cs_mono = 0.5 * (A - p_mono) * q_mono
    ps_mono = max(0.0, (p_mono - mc_u) * q_mono)
    dwl_mono= max(0.0, 0.5 * (p_mono - mc_u) * (q_pc - q_mono))
    cs_oli  = 0.5 * (A - p_oli)  * q_oli
    ps_oli  = max(0.0, (p_oli - mc_u)  * q_oli)
    dwl_oli = max(0.0, 0.5 * (p_oli - mc_u)  * (q_pc - q_oli))
    return dict(
        q_pc=q_pc, p_pc=p_pc, cs_pc=cs_pc,
        q_mono=q_mono, p_mono=p_mono, cs_mono=cs_mono, ps_mono=ps_mono, dwl_mono=dwl_mono,
        q_oli=q_oli, p_oli=p_oli, cs_oli=cs_oli, ps_oli=ps_oli, dwl_oli=dwl_oli,
        mc_u=mc_u,
    )

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div style="display:flex;align-items:center;gap:20px;">
    <img src="data:image/jpeg;base64,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" style="height:80px;width:80px;object-fit:contain;border-radius:8px;background:white;padding:4px;" />
    <div style="flex:1;">
      <div style="font-size:0.72rem;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Universitas Islam Bandung · Fakultas Ekonomi &amp; Bisnis</div>
      <h1 style="font-size:1.1rem !important;font-weight:700 !important;color:white !important;margin:0 0 4px 0 !important;line-height:1.3 !important;">⛏️ Analisis Intertemporal Batubara</h1>
      <div style="font-size:0.80rem;color:rgba(255,255,255,0.80);margin-bottom:6px;">PT Mitrabara Adiperdana Tbk (MBAP) — Dinamika Alokasi Sumber Daya <em>Depletable</em></div>
      <div style="display:flex;flex-wrap:wrap;gap:16px;font-size:0.75rem;color:rgba(255,255,255,0.65);border-top:1px solid rgba(255,255,255,0.15);padding-top:8px;margin-top:2px;">
        <span>📚 <strong style="color:rgba(255,255,255,0.85);">Mata Kuliah:</strong> Ekonomi Sumber Daya Alam &amp; Lingkungan</span>
        <span>👨‍🏫 <strong style="color:rgba(255,255,255,0.85);">Dosen Pengampu:</strong> Yuhka Sundaya, S.E., M.Si.</span>
        <span>👥 <strong style="color:rgba(255,255,255,0.85);">Kelompok:</strong> 
Arif Hamdani (10090224008) · 
Bambang Karta Wijaya (10090224025) · 
Moh Bayu Mustofa (10090224030)
</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# BAGIAN 1 — DASHBOARD DATA HISTORIS
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Bagian 1: Dashboard Data Historis (2015–2024)</div>', unsafe_allow_html=True)

st.markdown("""<div class="theory-box">
    📖 <strong>Latar Belakang:</strong> PT Mitrabara Adiperdana Tbk (MBAP) adalah perusahaan
    pertambangan batubara yang terdaftar di Bursa Efek Indonesia. Batubara sebagai sumber daya
    <em>depletable</em> memiliki nilai yang dipengaruhi oleh preferensi pasar dan kebutuhan energi manusia —
    sesuai perspektif <em>The Sense of Beauty</em> (Santayana): nilai muncul karena kebutuhan dan preferensi.
    Data historis 2015–2024 berikut menjadi dasar analisis intertemporal dan uji Aturan Hotelling.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Ringkasan data historis 2015–2024</div>', unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.markdown(f"""<div class="metric-card">
        <span class="num num-blue">{data['Production'].sum()/1e6:.2f} jt</span>
        <span class="lbl">Total Produksi (ton)</span>
    </div>""", unsafe_allow_html=True)
with d2:
    st.markdown(f"""<div class="metric-card">
        <span class="num num-amber">Rp {data['HBA'].mean()/1e6:.2f} jt</span>
        <span class="lbl">Rata-rata HBA (Rp/ton)</span>
    </div>""", unsafe_allow_html=True)
with d3:
    st.markdown(f"""<div class="metric-card">
        <span class="num num-green">Rp {MC_BASE/1e3:.0f} rb</span>
        <span class="lbl">Rata-rata MC (Rp/ton)</span>
    </div>""", unsafe_allow_html=True)
with d4:
    st.markdown(f"""<div class="metric-card">
        <span class="num num-purple">{T_STAR_BASE:.0f} thn</span>
        <span class="lbl">T* Habis Cadangan</span>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Data historis PT Mitrabara Adiperdana Tbk</div>', unsafe_allow_html=True)
dd = data.copy()
dd["COGS_fmt"]       = dd["COGS"].apply(lambda x: f"Rp {x:,.0f}")
dd["HBA_fmt"]        = dd["HBA"].apply(lambda x: f"Rp {x:,.0f}")
dd["MC_fmt"]         = dd["MC"].apply(lambda x: f"Rp {x:,.0f}")
dd["Production_fmt"] = dd["Production"].apply(lambda x: f"{x:,.0f}")
dd_disp = dd[["Year","Production_fmt","COGS_fmt","HBA_fmt","MC_fmt"]].copy()
dd_disp.columns = ["Tahun", "Produksi (ton)", "Beban Pokok (Rp)", "HBA (Rp/ton)", "MC (Rp/ton)"]
st.dataframe(dd_disp, use_container_width=True, hide_index=True)

st.markdown('<div class="section-label">Grafik HBA vs Biaya Marginal (MC)</div>', unsafe_allow_html=True)
cl, cr = st.columns(2)
with cl:
    fig_hba = go.Figure()
    fig_hba.add_trace(go.Scatter(
        x=data["Year"], y=data["HBA"], mode="lines+markers", name="HBA",
        line=dict(color="#185FA5", width=2.5),
        marker=dict(size=8, color="#185FA5", line=dict(color="white", width=2))
    ))
    fig_hba.add_trace(go.Scatter(
        x=data["Year"], y=data["MC"], mode="lines+markers", name="MC",
        line=dict(color="#ec4899", width=2, dash="dash"),
        marker=dict(size=7, color="#ec4899", line=dict(color="white", width=2))
    ))
    fig_hba.add_hline(y=MC_BASE, line_dash="dot", line_color="#10b981",
                       annotation_text=f"Rata-rata MC = Rp {MC_BASE:,.0f}",
                       annotation_font_color="#10b981", annotation_position="bottom right")
    fig_hba.update_layout(
        title="HBA vs Biaya Marginal (MC) 2015–2024",
        xaxis_title="Tahun", yaxis_title="Rp/ton",
        height=350, **PLOT_STYLE
    )
    ax(fig_hba)
    st.plotly_chart(fig_hba, use_container_width=True)

with cr:
    colors_prod = [
        f"rgba(24,95,165,{0.4 + 0.6 * (v - data['Production'].min()) / (data['Production'].max() - data['Production'].min())})"
        for v in data["Production"]
    ]
    fig_prod = go.Figure()
    fig_prod.add_trace(go.Bar(
        x=data["Year"], y=data["Production"],
        marker_color=colors_prod, marker_line_width=0,
        name="Produksi", text=[f"{v/1e6:.2f}jt" for v in data["Production"]],
        textposition="outside", textfont=dict(size=10)
    ))
    fig_prod.update_layout(
        title="Volume Produksi (ton) 2015–2024",
        xaxis_title="Tahun", yaxis_title="Ton",
        height=350, **PLOT_STYLE
    )
    ax(fig_prod)
    st.plotly_chart(fig_prod, use_container_width=True)

st.markdown("""<div class="insight-box">
    💡 <strong>Analisis HBA & Produksi:</strong>
    HBA (Harga Batubara Acuan) mencapai puncaknya pada 2022 (Rp 4,09 jt/ton) didorong oleh krisis
    energi global pasca-pandemi dan konflik Rusia-Ukraina. Lonjakan harga ini menjadi sinyal pasar
    bahwa batubara MBAP bergerak dari status <em>resource</em> ke <em>reserve</em> yang lebih luas —
    artinya volume yang layak diekstraksi secara ekonomis meningkat. Namun produksi justru turun signifikan
    sejak 2021, menunjukkan adanya kendala kapasitas operasional dan mungkin juga keputusan strategis
    intertemporal untuk tidak menguras cadangan saat harga tinggi. Rata-rata MC Rp 283.817/ton
    jauh di bawah HBA rata-rata Rp 1,94 jt/ton, mengindikasikan margin keuntungan yang substantial.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Beban Pokok Penjualan (COGS)</div>', unsafe_allow_html=True)
colors_cogs = [
    f"rgba(83,74,183,{0.35 + 0.65 * (v - data['COGS'].min()) / (data['COGS'].max() - data['COGS'].min())})"
    for v in data["COGS"]
]
fig_cogs = go.Figure()
fig_cogs.add_trace(go.Bar(
    x=data["Year"], y=data["COGS"],
    marker_color=colors_cogs, marker_line_width=0,
    name="COGS",
    text=[f"Rp {v/1e12:.2f}T" for v in data["COGS"]],
    textposition="outside", textfont=dict(size=10)
))
fig_cogs.update_layout(
    title="Beban Pokok Penjualan (COGS) 2015–2024",
    xaxis_title="Tahun", yaxis_title="Rp",
    height=320, **PLOT_STYLE
)
ax(fig_cogs)
st.plotly_chart(fig_cogs, use_container_width=True)

st.markdown("""<div class="insight-box">
    💡 <strong>Analisis COGS:</strong>
    COGS merupakan proksi biaya total ekstraksi yang digunakan dalam perhitungan biaya marginal (MC).
    COGS tertinggi terjadi pada 2019 (Rp 2,38 T) dan tetap tinggi pada 2022–2024 meski volume produksi
    turun drastis sejak 2022. Hal ini mengindikasikan <strong>biaya tetap yang besar</strong> dalam industri
    pertambangan — biaya infrastruktur, alat berat, dan tenaga kerja tidak dapat diturunkan proporsional
    dengan penurunan produksi. Fenomena ini relevan dengan Taksonomi Cadangan (<em>McKelvey Box</em>):
    ketika biaya akses meningkat relatif terhadap harga, sebagian cadangan bisa berpindah dari
    <em>reserve</em> kembali ke <em>resource</em> yang tidak layak secara ekonomis.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Biaya Marginal (MC) per tahun</div>', unsafe_allow_html=True)
mc_colors = ["rgba(226,75,74,0.75)" if v < 0 else "rgba(24,95,165,0.7)" for v in data["MC"]]
fig_mc = go.Figure()
fig_mc.add_trace(go.Bar(
    x=data["Year"], y=data["MC"],
    marker_color=mc_colors, marker_line_width=0,
    name="MC",
    text=[f"Rp {v:,.0f}" for v in data["MC"]],
    textposition="outside", textfont=dict(size=9)
))
fig_mc.add_hline(y=MC_BASE, line_dash="dot", line_color="#10b981",
                  annotation_text=f"Rata-rata MC = Rp {MC_BASE:,.0f}",
                  annotation_font_color="#10b981", annotation_position="bottom right")
fig_mc.add_hline(y=0, line_color="#1a1a2e", line_width=1.5)
fig_mc.update_layout(
    title="Biaya Marginal (MC) 2015–2024 — Merah = Negatif (artefak metodologi)",
    xaxis_title="Tahun", yaxis_title="Rp/ton",
    height=320, **PLOT_STYLE
)
ax(fig_mc)
st.plotly_chart(fig_mc, use_container_width=True)

st.markdown("""<div class="insight-box">
   💡 <strong>Catatan MC Negatif — Keterbatasan Metodologi:</strong>
    Nilai MC negatif pada 2018, 2022, dan 2023 merupakan <em>artefak metodologi</em> dari pendekatan
    <em>incremental COGS</em> — bukan cerminan biaya aktual yang negatif secara ekonomi.
    MC dihitung sebagai ΔCOGS/ΔProduksi; ketika COGS dan volume keduanya turun dalam periode berbeda,
    hasilnya bisa negatif. Dalam teori ekonomi sumber daya, MC tidak bisa negatif karena selalu ada
    biaya nyata untuk mengekstraksi satu ton tambahan. Oleh karena itu, <strong>rata-rata MC Rp 283.817/ton</strong>
    digunakan sebagai konstanta yang lebih representatif dalam seluruh model analisis ini.
    Ini sesuai metodologi simulasi pada Bab III: menggunakan data rata-rata yang stabil untuk proyeksi.
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# BAGIAN 2 — ANALISIS STRUKTUR PASAR
# ══════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏭 Bagian 2: Analisis Struktur Pasar</div>', unsafe_allow_html=True)

st.markdown("""<div class="theory-box">
   📖 <strong>Landasan Teoritis:</strong>
    Struktur pasar menentukan bagaimana harga dan kuantitas produksi ditetapkan, yang pada gilirannya
    memengaruhi kecepatan deplesi cadangan. Tiga struktur yang dianalisis:
    (1) <strong>Persaingan Sempurna</strong>: P = MC, efisien statik namun deplesi tercepat;
    (2) <strong>Oligopoli Cournot</strong>: n perusahaan bersaing kuantitas, hasil di antara keduanya;
    (3) <strong>Monopoli</strong>: MR = MC, harga di atas MC, produksi tertekan — secara paradoks
    memperlambat deplesi cadangan namun menciptakan kerugian kesejahteraan (<em>deadweight loss</em>).
    Gunakan slider di bawah untuk mensimulasikan berbagai skenario.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Parameter model struktur pasar</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    hba_m = st.slider("Harga pasar / HBA (juta Rp/ton)", 0.5, 5.0, 1.94, 0.05,
                      help="HBA aktual 2024 ≈ Rp 1,94 jt/ton")
with c2:
    mc_m  = st.slider("Biaya marginal MC (juta Rp/ton)", 0.1, 2.5, 0.28, 0.05,
                      help="Rata-rata MC 2015–2024 ≈ Rp 0,28 jt/ton")
with c3:
    stok  = st.slider("Stok cadangan (juta ton)", 10, 200, 60, 5,
                      help="Perkiraan cadangan tersisa perusahaan")
with c4:
    n_firms = st.slider("Perusahaan oligopoli (n)", 2, 20, 3, 1,
                        help="Jumlah perusahaan dalam model Cournot")

m = calc_market(hba_m, mc_m, n_firms)
life_pc   = stok / m["q_pc"]   if m["q_pc"]   > 0 else float("inf")
life_mono = stok / m["q_mono"] if m["q_mono"] > 0 else float("inf")
life_oli  = stok / m["q_oli"]  if m["q_oli"]  > 0 else float("inf")

st.markdown('<div class="section-label">Perbandingan tiga struktur pasar</div>', unsafe_allow_html=True)
col_pc, col_oli, col_mono = st.columns(3)

with col_pc:
    st.markdown(f"""
<div class="market-card pc">
  <div class="mc-name">✅ Persaingan Sempurna</div>
  <div class="mc-row"><span class="mc-lbl">Q* produksi</span><span class="mc-val">{m['q_pc']:.3f} unit</span></div>
  <div class="mc-row"><span class="mc-lbl">P* harga</span><span class="mc-val">{m['p_pc']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Surplus konsumen</span><span class="mc-val">{m['cs_pc']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Deadweight Loss</span><span class="mc-val">0.000</span></div>
  <div class="mc-row"><span class="mc-lbl">Umur cadangan</span><span class="mc-val">{life_pc:.1f} tahun</span></div>
  <span class="badge badge-g">P = MC · Efisien Statik</span>
</div>""", unsafe_allow_html=True)

with col_oli:
    st.markdown(f"""
<div class="market-card oli">
  <div class="mc-name">🔶 Oligopoli Cournot (n={n_firms})</div>
  <div class="mc-row"><span class="mc-lbl">Q* produksi</span><span class="mc-val">{m['q_oli']:.3f} unit</span></div>
  <div class="mc-row"><span class="mc-lbl">P* harga</span><span class="mc-val">{m['p_oli']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Surplus konsumen</span><span class="mc-val">{m['cs_oli']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Deadweight Loss</span><span class="mc-val">{m['dwl_oli']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Umur cadangan</span><span class="mc-val">{life_oli:.1f} tahun</span></div>
  <span class="badge badge-y">Antara PC & Monopoli</span>
</div>""", unsafe_allow_html=True)

with col_mono:
    st.markdown(f"""
<div class="market-card mono">
  <div class="mc-name">⚠️ Monopoli</div>
  <div class="mc-row"><span class="mc-lbl">Q* produksi</span><span class="mc-val">{m['q_mono']:.3f} unit</span></div>
  <div class="mc-row"><span class="mc-lbl">P* harga</span><span class="mc-val">{m['p_mono']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Surplus konsumen</span><span class="mc-val">{m['cs_mono']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Deadweight Loss</span><span class="mc-val">{m['dwl_mono']:.3f}</span></div>
  <div class="mc-row"><span class="mc-lbl">Umur cadangan</span><span class="mc-val">{life_mono:.1f} tahun</span></div>
  <span class="badge badge-r">P > MC · Inefisien</span>
</div>""", unsafe_allow_html=True)

margin = hba_m - mc_m
if margin > 0:
    msg = (f"Margin keuntungan = Rp {margin:.2f} jt/ton. "
           f"Persaingan sempurna menghabiskan cadangan paling cepat ({life_pc:.1f} tahun) "
           f"karena Q* tertinggi. Monopoli memperlambat deplesi ({life_mono:.1f} tahun) "
           f"tetapi menciptakan DWL = {m['dwl_mono']:.3f} — kerugian kesejahteraan masyarakat. "
           f"Oligopoli Cournot (n={n_firms}) berada di tengah: umur cadangan {life_oli:.1f} tahun, "
           f"DWL = {m['dwl_oli']:.3f}. Semakin banyak perusahaan (n→∞), oligopoli mendekati persaingan sempurna.")
    st.markdown(f'<div class="insight-box">💡 <strong>Kesimpulan Struktur Pasar:</strong>{msg}</div>',
                unsafe_allow_html=True)
else:
    st.markdown('<div class="warn-box">⚠️ Harga di bawah MC — produksi tidak menguntungkan di semua struktur pasar.</div>',
                unsafe_allow_html=True)

st.markdown('<div class="section-label">Tabel perbandingan lengkap</div>', unsafe_allow_html=True)
df_cmp = pd.DataFrame({
    "Indikator": ["Q* produksi (unit)", "P* harga (skala)", "Surplus Konsumen",
                  "Surplus Produsen", "Total Surplus", "Deadweight Loss",
                  "Stok cadangan (juta ton)", "Umur cadangan (tahun)"],
    "Persaingan Sempurna": [
        f"{m['q_pc']:.4f}", f"{m['p_pc']:.4f}", f"{m['cs_pc']:.4f}",
        "0.0000", f"{m['cs_pc']:.4f}", "0.0000",
        f"{stok:.0f}", f"{life_pc:.1f}"
    ],
    f"Oligopoli (n={n_firms})": [
        f"{m['q_oli']:.4f}", f"{m['p_oli']:.4f}", f"{m['cs_oli']:.4f}",
        f"{m['ps_oli']:.4f}", f"{m['cs_oli']+m['ps_oli']:.4f}", f"{m['dwl_oli']:.4f}",
        f"{stok:.0f}", f"{life_oli:.1f}"
    ],
    "Monopoli": [
        f"{m['q_mono']:.4f}", f"{m['p_mono']:.4f}", f"{m['cs_mono']:.4f}",
        f"{m['ps_mono']:.4f}", f"{m['cs_mono']+m['ps_mono']:.4f}", f"{m['dwl_mono']:.4f}",
        f"{stok:.0f}", f"{life_mono:.1f}"
    ],
})
st.dataframe(df_cmp, use_container_width=True, hide_index=True)

st.markdown('<div class="section-label">Kurva permintaan & posisi ekuilibrium</div>', unsafe_allow_html=True)
q_range = np.linspace(0, A / B * 1.05, 300)
p_range = A - B * q_range

fig = go.Figure()
q_fill = np.linspace(0, m["q_pc"], 100)
p_fill = A - B * q_fill
fig.add_trace(go.Scatter(
    x=np.concatenate([[0], q_fill, [m["q_pc"], 0]]),
    y=np.concatenate([[A], p_fill, [m["p_pc"], m["p_pc"]]]),
    fill="toself", fillcolor="rgba(29,158,117,0.08)",
    line=dict(color="rgba(0,0,0,0)"), name="Surplus Konsumen (PC)", showlegend=True
))
fig.add_trace(go.Scatter(x=q_range, y=p_range, mode="lines",
    line=dict(color="#185FA5", width=2.5), name="Kurva Permintaan D"))
q_mr = np.linspace(0, A / B, 300)
p_mr = A - 2 * B * q_mr
fig.add_trace(go.Scatter(x=q_mr, y=p_mr, mode="lines",
    line=dict(color="#A32D2D", width=1.5, dash="dot"), name="MR (Monopoli)"))
fig.add_hline(y=m["mc_u"], line_dash="dash", line_color="#888780",
              annotation_text="MC", annotation_font_color="#888780")
fig.add_trace(go.Scatter(
    x=[m["q_pc"], m["q_oli"], m["q_mono"]],
    y=[m["p_pc"], m["p_oli"], m["p_mono"]],
    mode="markers+text",
    marker=dict(size=12, color=["#1D9E75", "#BA7517", "#A32D2D"],
        symbol=["circle", "diamond", "square"], line=dict(color="white", width=2)),
    name="Ekuilibrium",
    text=["PC", f"Oli (n={n_firms})", "Mono"], textposition="top center"
))
for q_eq, p_eq, col in [(m["q_pc"], m["p_pc"], "#1D9E75"),
                          (m["q_oli"], m["p_oli"], "#BA7517"),
                          (m["q_mono"], m["p_mono"], "#A32D2D")]:
    if q_eq > 0:
        fig.add_shape(type="line", x0=q_eq, x1=q_eq, y0=0, y1=p_eq,
                      line=dict(color=col, width=1, dash="dot"))
fig.update_layout(title="Kurva Permintaan & Posisi Ekuilibrium Tiga Struktur Pasar",
                  xaxis_title="Q (kuantitas, juta ton)",
                  yaxis_title="P (harga, skala model)", height=400, **PLOT_STYLE)
ax(fig)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""<div class="insight-box">
  💡 <strong>Interpretasi Kurva:</strong>
    Kurva D (biru) adalah fungsi permintaan pasar batubara. Garis MR (merah putus-putus) selalu
    di bawah D karena monopolis harus menurunkan harga untuk menjual lebih banyak.
    <strong>Efisiensi dinamis</strong> mensyaratkan bahwa harga bersih sumber daya harus tumbuh
    sesuai tingkat diskonto (Aturan Hotelling). Pasar persaingan sempurna efisien secara statik
    (P = MC, DWL = 0) namun berpotensi menguras cadangan terlalu cepat. Monopoli justru
    memperlambat ekstraksi — sebuah "<em>conservation effect</em>" yang tidak disengaja — tetapi
    menciptakan inefisiensi alokasi (DWL = {m['dwl_mono']:.3f} unit). Pasar batubara Indonesia
    lebih mendekati oligopoli dengan beberapa perusahaan besar mendominasi ekspor.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Grafik perbandingan indikator utama</div>', unsafe_allow_html=True)
labels3 = ["Persaingan", f"Oligopoli (n={n_firms})", "Monopoli"]
colors3 = ["#1D9E75", "#BA7517", "#A32D2D"]
fig_bar = make_subplots(rows=1, cols=4,
    subplot_titles=["Q* Produksi", "P* Harga", "Total Surplus", "Umur Cadangan (thn)"])
vals = [
    [m["q_pc"], m["q_oli"], m["q_mono"]],
    [m["p_pc"], m["p_oli"], m["p_mono"]],
    [m["cs_pc"], m["cs_oli"]+m["ps_oli"], m["cs_mono"]+m["ps_mono"]],
    [life_pc if life_pc < 9999 else 0,
     life_oli if life_oli < 9999 else 0,
     life_mono if life_mono < 9999 else 0],
]
for col_i, v in enumerate(vals, 1):
    fig_bar.add_trace(go.Bar(x=labels3, y=v, marker_color=colors3, showlegend=False), row=1, col=col_i)
fig_bar.update_layout(height=300, paper_bgcolor="white", plot_bgcolor="#f8f9fb",
                       font=dict(color="#1a1a2e", family="Inter"),
                       margin=dict(t=45, b=20, l=30, r=10))
fig_bar.update_xaxes(gridcolor="#edf2f7", linecolor="#dee2e6", tickfont=dict(size=10))
fig_bar.update_yaxes(gridcolor="#edf2f7", linecolor="#dee2e6", tickfont=dict(size=10))
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""<div class="insight-box">
    💡 <strong>Implikasi Kebijakan Struktur Pasar:</strong>
    Grafik batang ini mengkonfirmasi trade-off fundamental dalam ekonomi sumber daya: efisiensi alokasi
    vs. keberlanjutan. Pemerintah dapat memanfaatkan <em>conservation effect</em> monopoli/oligopoli melalui
    regulasi produksi (<em>quota</em>) atau royalti yang mendorong pembatasan output — tanpa harus
    mengizinkan monopoli murni. Alternatif lain: internalisasi biaya lingkungan melalui pajak karbon
    (Pigou) agar MC yang digunakan dalam keputusan produksi mencerminkan biaya sosial penuh,
    sehingga keseimbangan pasar lebih mendekati optimalitas sosial.
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# BAGIAN 3 — EFISIENSI DINAMIS & ATURAN HOTELLING
# ══════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⏳ Bagian 3: Efisiensi Dinamis & Aturan Hotelling</div>', unsafe_allow_html=True)

st.markdown("""<div class="theory-box">
    📖 <strong>Aturan Hotelling:</strong>
    Harold Hotelling (1931) menurunkan kondisi optimalitas intertemporal untuk sumber daya tak terbarukan:
    <br><br>
    <strong>dP/dt = r · P</strong> &nbsp;→&nbsp; <strong>λ(t) = λ₀ · eʳᵗ</strong>
    <br><br>
    di mana λ adalah <em>Marginal User Cost</em> (MUC) atau <em>royalti Hotelling</em> — nilai
    kesempatan yang hilang ketika satu ton batubara diekstraksi hari ini daripada disimpan untuk masa depan.
    Aturan ini menyatakan: agar pasar sumber daya efisien secara intertemporal, harga bersih (harga dikurangi MC)
    harus tumbuh eksponensial setara tingkat diskonto <em>r</em>. T* adalah titik waktu ketika MUC mencapai
    choke price dikurangi MC — saat itulah ekstraksi berhenti secara optimal.
    <br><br>Formula T*: &nbsp;<strong>T* = (1/r) · ln[(Choke Price − MC) / λ₀]</strong>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Parameter Hotelling</div>', unsafe_allow_html=True)
h1, h2, h3, h4 = st.columns(4)
with h1:
    r = st.slider("Tingkat diskonto r (%)", 1.0, 25.0, 5.0, 0.5,
                  key="r_tab2", help="Tingkat diskonto sosial/pasar") / 100
with h2:
    muc0_k = st.slider("MUC awal λ₀ (ribu Rp/ton)", 1, 200, 15, 1,
                        key="muc0", help="Marginal User Cost awal")
    muc0 = muc0_k * 1000
with h3:
    mc2_m = st.slider("MC (juta Rp/ton)", 0.1, 2.5, 0.28, 0.05,
                       key="mc2", help="Biaya marginal produksi")
    mc2 = mc2_m * 1e6
with h4:
    cp_m = st.slider("Choke price (juta Rp/ton)", 1.0, 20.0, 8.6, 0.5,
                      key="cp", help="Harga tertinggi saat permintaan = 0")
    cp = cp_m * 1e6

gap = cp - mc2
if gap > 0 and muc0 > 0:
    t_star = (1 / r) * np.log(gap / muc0)
else:
    t_star = None

st.markdown('<div class="section-label">Hasil kalkulasi Hotelling</div>', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    t_star_display = f"{t_star:.1f}" if t_star is not None else "—"

    st.markdown(f"""
    <div class="metric-card">
        <span class="num num-blue">{t_star_display}</span>
        <span class="lbl">T* umur cadangan (tahun)</span>
    </div>
    """, unsafe_allow_html=True)
with m2:
    yr = int(2025 + t_star) if t_star else "—"
    st.markdown(f"""<div class="metric-card">
        <span class="num num-purple">{yr}</span>
        <span class="lbl">Cadangan habis (~tahun)</span>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-card">
        <span class="num">{muc0/1000:.0f} rb</span>
        <span class="lbl">MUC awal λ₀ (Rp/ton)</span>
    </div>""", unsafe_allow_html=True)
with m4:
    muc10 = muc0 * np.exp(r * 10)
    st.markdown(f"""<div class="metric-card">
        <span class="num num-amber">{muc10/1e6:.2f} jt</span>
        <span class="lbl">MUC pada t=10 thn (Rp)</span>
    </div>""", unsafe_allow_html=True)
with m5:
    muc50 = muc0 * np.exp(r * 50)
    st.markdown(f"""<div class="metric-card">
        <span class="num num-red">{muc50/1e6:.1f} jt</span>
        <span class="lbl">MUC pada t=50 thn (Rp)</span>
    </div>""", unsafe_allow_html=True)

if t_star:
    base_t = (1 / R_BASE) * np.log((CP_BASE - MC_BASE) / MUC0_BASE)
    st.markdown(f"""<div class="insight-box">
        💡 <strong>Interpretasi Hotelling:</strong>
        Dengan diskonto r = {r*100:.1f}%, cadangan optimal habis dalam <strong>{t_star:.1f} tahun</strong>
        (~{int(2025+t_star)}). {"Lebih cepat" if t_star < base_t else "Lebih lambat"} dari baseline r=5%
        ({base_t:.0f} tahun). MUC tumbuh eksponensial dari Rp {muc0/1000:.0f} ribu/ton
        menjadi Rp {muc50/1e6:.1f} jt/ton pada t=50.
        {"⚡ Diskonto tinggi mencerminkan preferensi kuat pada konsumsi saat ini — generasi mendatang dinilai lebih rendah. Ini mendorong eksploitasi lebih cepat dan memperpendek T*." if r > R_BASE else "🌱 Diskonto rendah mencerminkan penghargaan lebih tinggi terhadap generasi mendatang — insentif konservasi lebih kuat, T* lebih panjang."}
        <br><br><em>Catatan kritis:</em>Jalur ekstraksi riil MBAP tidak sesederhana model Hotelling
        karena adanya faktor substitusi energi terbarukan, perubahan teknologi penambangan, regulasi pemerintah,
        dan ketidakpastian harga pasar global yang tidak terinternalisasi dalam model teoretis murni.
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Pertumbuhan MUC & titik T*</div>', unsafe_allow_html=True)
if t_star:
    t_max = min(t_star * 1.5, 300)
    t_arr = np.linspace(0, t_max, 400)
    muc_arr = muc0 * np.exp(r * t_arr)
    fig_hot = go.Figure()
    fig_hot.add_trace(go.Scatter(
        x=t_arr, y=muc_arr, mode="lines", name="MUC(t) = λ₀·eʳᵗ",
        line=dict(color="#534AB7", width=2.5),
        fill="tozeroy", fillcolor="rgba(83,74,183,0.07)"
    ))
    fig_hot.add_hline(y=gap, line_dash="dash", line_color="#A32D2D",
                       annotation_text="Choke − MC (batas ekstraksi)",
                       annotation_font_color="#A32D2D", annotation_position="top left")
    fig_hot.add_vline(x=t_star, line_dash="dot", line_color="#1D9E75",
                       annotation_text=f"T* = {t_star:.1f} thn",
                       annotation_font_color="#1D9E75")
    fig_hot.update_layout(
        title="Jalur Pertumbuhan MUC — Aturan Hotelling: dλ/dt = r·λ",
        xaxis_title="Tahun ke-", yaxis_title="MUC (Rp/ton)",
        height=360, **PLOT_STYLE
    )
    ax(fig_hot)
    st.plotly_chart(fig_hot, use_container_width=True)

    st.markdown(f"""<div class="insight-box">
       💡 <strong>Analisis Jalur MUC:</strong>
        Kurva ungu menunjukkan jalur pertumbuhan MUC (λ) yang harus terjadi agar ekstraksi MBAP
        efisien secara intertemporal. Ketika λ mencapai garis merah (Choke Price − MC = Rp {gap/1e6:.1f} jt/ton),
        tidak ada lagi keuntungan dari ekstraksi — ini adalah <strong>titik T* = {t_star:.1f} tahun</strong>.
        Area di bawah kurva merepresentasikan nilai sumber daya yang dikonsumsi selama periode tersebut.
        <br><br>Jika MUC aktual MBAP tumbuh lebih lambat dari r·λ, itu sinyal <em>over-extraction</em>
        (menguras terlalu cepat). Jika tumbuh lebih cepat, ada <em>under-extraction</em>
        (menahan terlalu banyak). Keseimbangan ini yang disebut <strong>efisiensi alokasi intertemporal</strong>.
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Sensitivitas T* terhadap tingkat diskonto</div>', unsafe_allow_html=True)
r_vals  = np.linspace(0.01, 0.25, 100)
t_stars = [(1/rv)*np.log(gap/muc0) if gap > 0 and muc0 > 0 else 0 for rv in r_vals]
r_table = [1, 2, 3, 5, 8, 10, 15, 20]
t_table = [(1/(rv/100))*np.log(gap/muc0) if gap > 0 else 0 for rv in r_table]

cl, cr = st.columns([3, 2])
with cl:
    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(
        x=r_vals*100, y=t_stars, mode="lines",
        line=dict(color="#8b5cf6", width=2.5),
        fill="tozeroy", fillcolor="rgba(139,92,246,0.06)",
        name="T*(r)"
    ))
    fig_sens.add_vline(x=r*100, line_dash="dot", line_color="#185FA5",
                        annotation_text=f"r = {r*100:.1f}%",
                        annotation_font_color="#185FA5")
    fig_sens.update_layout(
        title="T* vs Tingkat Diskonto",
        xaxis_title="r (%)", yaxis_title="T* (tahun)",
        height=280, **PLOT_STYLE
    )
    ax(fig_sens)
    st.plotly_chart(fig_sens, use_container_width=True)
with cr:
    df_sens = pd.DataFrame({
        "r (%)": r_table,
        "T* (tahun)": [f"{t:.1f}" for t in t_table],
        "Habis (~thn)": [str(int(2025+t)) for t in t_table],
    })
    st.dataframe(df_sens, use_container_width=True, hide_index=True)
    st.markdown("""<div style="font-size:0.78rem;color:#6c757d;margin-top:8px">
        📌 Hubungan invers: diskonto tinggi → T* pendek → eksploitasi lebih cepat.
        Diskonto rendah = menilai kesejahteraan generasi mendatang lebih tinggi.
    </div>""", unsafe_allow_html=True)

st.markdown("""<div class="insight-box">
   💡 <strong>Sensitivitas & Implikasi Kebijakan:</strong>
    Grafik sensitivitas menunjukkan betapa pentingnya pilihan tingkat diskonto dalam menentukan nasib
    cadangan sumber daya. Perbedaan 1% saja pada r dapat menggeser T* puluhan tahun.
    <br><br>Implikasi kebijakan: pemerintah dapat menggunakan <strong>tingkat royalti</strong> sebagai
    instrumen untuk menyesuaikan efektif <em>r</em> yang dihadapi produsen — royalti tinggi meningkatkan
    biaya oportunitas ekstraksi saat ini, efektif "merendahkan" r dan mendorong konservasi.
    Ini lebih efisien daripada kuota produksi yang kaku karena bersifat fleksibel dan berbasis harga.
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# BAGIAN 4 — GREEN PARADOX
# ══════════════════════════════════════════════════════════════════════
st.markdown('<hr class="divider-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌍 Bagian 4: Fenomena Green Paradox</div>', unsafe_allow_html=True)

st.markdown("""<div class="theory-box">
    📖 <strong>Teori Green Paradox:</strong>
    Hans-Werner Sinn (2008) mengemukakan bahwa kebijakan lingkungan yang diumumkan jauh hari sebelum
    berlaku justru dapat <em>mempercepat</em> emisi dalam jangka pendek — berlawanan dengan tujuannya.
    <br><br>Mekanisme: Produsen batubara yang rasional mengetahui bahwa nilai aset mereka akan turun
    ketika pajak karbon berlaku. Respons optimal: ekstraksi maksimum <em>sebelum</em> pajak berlaku
    untuk memaksimalkan <em>present value</em>. Hasilnya adalah "<em>race to extract</em>" yang
    paradoksnya meningkatkan total emisi kumulatif.
    <br><br>Relevansi untuk MBAP: Indonesia berencana mengembangkan pajak karbon sebagai bagian dari
    komitmen NDC (Nationally Determined Contribution). Bagaimana desain implementasinya akan sangat
    menentukan apakah Green Paradox terjadi.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Parameter skenario kebijakan</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    tax_k = st.slider("Pajak karbon (ribu Rp/ton CO₂)", 0, 1000, 300, 25,
                       help="Besaran pajak yang direncanakan pemerintah")
with g2:
    lag   = st.slider("Pajak berlaku (tahun ke-)", 1, 15, 5, 1,
                       help="Berapa tahun dari sekarang pajak mulai berlaku")
with g3:
    accel = st.slider("Percepatan produksi pra-pajak (%)", 0, 80, 30, 5,
                       help="Persentase peningkatan produksi sebelum pajak berlaku") / 100

base_prod = 3.0
years   = list(range(2025, 2045))
n_years = len(years)

prod_base  = [base_prod] * n_years
prod_accel = []
for i in range(n_years):
    if i < lag:
        prod_accel.append(base_prod * (1 + accel))
    else:
        post_ratio  = max(0.2, 1 - (tax_k / 1500))
        lag_ratio   = max(0.0, 1 - (accel * lag / max(1, n_years - lag)))
        prod_accel.append(base_prod * post_ratio * lag_ratio)

em_base  = [p * 2.5 for p in prod_base]
em_accel = [p * 2.5 for p in prod_accel]
cum_base  = list(np.cumsum(em_base))
cum_accel = list(np.cumsum(em_accel))

total_base  = sum(em_base)
total_accel = sum(em_accel)
delta_em    = total_accel - total_base
pct_change  = delta_em / total_base * 100 if total_base > 0 else 0

st.markdown('<div class="section-label">Dampak emisi kumulatif (2025–2044)</div>', unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)
with p1:
    st.markdown(f"""<div class="metric-card">
        <span class="num num-blue">{total_base:.1f}</span>
        <span class="lbl">Emisi baseline (Mt CO₂)</span>
    </div>""", unsafe_allow_html=True)
with p2:
    col_cls = "num-red" if delta_em > 0 else "num-green"
    st.markdown(f"""<div class="metric-card">
        <span class="num {col_cls}">{total_accel:.1f}</span>
        <span class="lbl">Emisi + paradox (Mt CO₂)</span>
    </div>""", unsafe_allow_html=True)
with p3:
    st.markdown(f"""<div class="metric-card">
        <span class="num {col_cls}">{delta_em:+.1f}</span>
        <span class="lbl">Selisih emisi (Mt CO₂)</span>
    </div>""", unsafe_allow_html=True)
with p4:
    st.markdown(f"""<div class="metric-card">
        <span class="num {col_cls}">{pct_change:+.1f}%</span>
        <span class="lbl">Perubahan emisi (%)</span>
    </div>""", unsafe_allow_html=True)

if delta_em > 5:
    st.markdown(f"""<div class="danger-box">
        ⚠️ <strong>Green Paradox Terdeteksi!</strong>
        Pajak Rp {tax_k}rb/ton yang berlaku {lag} tahun ke depan memicu akselerasi produksi
        {int(accel*100)}% selama periode pra-pajak. Emisi kumulatif naik
        <strong>{delta_em:+.1f} Mt CO₂ ({pct_change:+.1f}%)</strong> —
        berlawanan dengan tujuan kebijakan lingkungan. Ini adalah bukti empiris teori Sinn (2008).
        <strong>Solusi:</strong>pajak berlaku segera dengan kenaikan bertahap
        (<em>escalating carbon price</em>), bukan diumumkan jauh hari tanpa implementasi segera.
    </div>""", unsafe_allow_html=True)
elif delta_em < -5:
    st.markdown(f"""<div class="success-box">
       ✅ <strong>Kebijakan Efektif</strong> — Emisi turun {abs(delta_em):.1f} Mt CO₂ ({pct_change:.1f}%).
        Pajak cukup besar dan/atau lag implementasi cukup pendek sehingga tidak memicu paradox.
        Ini adalah desain kebijakan yang tepat sesuai rekomendasi literatur ekonomi lingkungan.
    </div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="warn-box">
        ⚡ <strong>Dampak Marginal</strong> — Paradox kecil. Pertimbangkan menaikkan pajak atau
        memperpendek lag implementasi untuk efek reduksi emisi yang lebih signifikan.
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Volume produksi: baseline vs skenario Green Paradox</div>', unsafe_allow_html=True)
bar_colors = ["rgba(226,75,74,0.8)" if i < lag else "rgba(83,74,183,0.7)"
              for i in range(n_years)]
fig_gp = go.Figure()
fig_gp.add_trace(go.Bar(x=years, y=prod_base, name="Baseline",
                         marker_color="rgba(83,74,183,0.25)", marker_line_width=0))
fig_gp.add_trace(go.Bar(x=years, y=prod_accel, name="+ Green Paradox",
                         marker_color=bar_colors, marker_line_width=0))
fig_gp.add_vline(x=2025 + lag - 0.5, line_dash="dash", line_color="#BA7517",
                  annotation_text=f"Pajak berlaku {2025+lag}",
                  annotation_font_color="#BA7517")
fig_gp.update_layout(
    title="Volume Produksi Tahunan (juta ton)",
    xaxis_title="Tahun", yaxis_title="Produksi (juta ton)",
    barmode="overlay", height=320, **PLOT_STYLE
)
ax(fig_gp)
st.plotly_chart(fig_gp, use_container_width=True)

st.markdown(f"""<div class="insight-box">
    💡 <strong>Analisis Produksi:</strong>
    Batang merah (periode pra-pajak) menunjukkan peningkatan produksi {int(accel*100)}% di atas baseline
    selama {lag} tahun sebelum pajak berlaku. Ini adalah manifestasi "<em>race to extract</em>" —
    MBAP dan produsen lain akan berupaya memaksimalkan ekstraksi saat biaya masih rendah.
    Setelah pajak berlaku, produksi turun tajam (batang ungu gelap) karena pajak membuat sebagian
    cadangan tidak lagi layak secara ekonomis — bergeser dari <em>reserve</em> kembali ke <em>resource</em>
    dalam kerangka Taksonomi McKelvey. Ironisnya, total emisi kumulatif bisa lebih tinggi karena
    front-loading produksi sebelum pajak berlaku.
</div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Emisi CO₂ kumulatif</div>', unsafe_allow_html=True)
fig_em = go.Figure()
fig_em.add_trace(go.Scatter(x=years, y=cum_base, mode="lines",
    name="Emisi kumulatif baseline",
    line=dict(color="#534AB7", width=2.5)))
fig_em.add_trace(go.Scatter(x=years, y=cum_accel, mode="lines",
    name="Emisi kumulatif + paradox",
    line=dict(color="#A32D2D", width=2.5),
    fill="tonexty", fillcolor="rgba(226,75,74,0.08)"))
fig_em.update_layout(
    title="Emisi CO₂ Kumulatif 2025–2044 (Mt)",
    xaxis_title="Tahun", yaxis_title="Mt CO₂ (kumulatif)",
    height=300, **PLOT_STYLE
)
ax(fig_em)
st.plotly_chart(fig_em, use_container_width=True)

st.markdown(f"""<div class="insight-box">
    💡 <strong>Interpretasi Emisi Kumulatif:</strong>
    Area merah antara dua kurva adalah <em>excess emissions</em> yang terjadi akibat Green Paradox —
    emisi tambahan sebesar {delta_em:+.1f} Mt CO₂ ({pct_change:+.1f}%) dibandingkan baseline.
    Secara kumulatif, ini bisa berarti kebijakan lingkungan justru mempercepat perubahan iklim
    dalam jangka menengah meski berhasil mengurangi emisi jangka panjang.
    <br><br>Ini merupakan kegagalan pasar ganda: eksternalitas negatif emisi (biaya sosial tidak
    terinternalisasi) <em>dan</em> respons spekulatif terhadap kebijakan yang tidak efektif.
    Keduanya membutuhkan intervensi pemerintah yang dirancang cermat untuk menghindari
    memperparah distorsi yang ada .
</div>""", unsafe_allow_html=True)

st.markdown("""<div class="insight-box">
    💡 <strong>Mekanisme Green Paradox & Tiga Solusi Berbasis Bukti:</strong>
    Ketika pemerintah mengumumkan pajak karbon yang baru berlaku beberapa tahun ke depan,
    produsen rasional mempercepat ekstraksi sekarang — nilai sekarang cadangan turun setelah
    pajak berlaku. Hasilnya: emisi jangka pendek justru <em>meningkat</em>, berlawanan dengan
    tujuan kebijakan. <br><br><strong>Tiga solusi rekomendasi kebijakan:</strong>
    <br>① <strong>Escalating Carbon Price</strong> — Pajak berlaku segera dengan kenaikan bertahap
    dan terjadwal, menghilangkan insentif untuk front-loading produksi;
    <br>② <strong>Kuota Produksi Absolut</strong> — Berbasis anggaran karbon (<em>carbon budget</em>),
    membatasi total ekstraksi selama periode tertentu secara legal;
    <br>③ <strong>Moratorium Ekspansi Konsesi</strong> — Mencegah pembukaan blok baru sambil
    mendorong transisi investasi ke energi terbarukan melalui insentif fiskal positif.
</div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""<div style="font-size:0.78rem;color:#adb5bd;text-align:center;padding:8px 0;line-height:2">
    <strong>PBL 3</strong> — Ekonomi Sumber Daya Alam &amp; Lingkungan &nbsp;·&nbsp;
    Analisis Intertemporal dan Dinamika Alokasi Sumber Daya <em>Depletable</em><br>
    👥 👥 <strong>Kelompok:</strong> 
Arif Hamdani (10090224008) · 
Bambang Karta Wijaya (10090224025) · 
Moh Bayu Mustofa (10090224030)
    👨‍🏫 <strong>Dosen Pengampu:</strong> Yuhka Sundaya, S.E., M.Si.<br>
    Universitas Islam Bandung · Fakultas Ekonomi &amp; Bisnis · 2026
</div>""", unsafe_allow_html=True)