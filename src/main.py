"""
=============================================================
  ANALISIS DATA PESERTA DIDIK SMP NEGERI KOTA BANDUNG
  Sumber Data: simdik.bandung.go.id (Dinas Pendidikan Kota Bandung)
  Semester: 2025/2026 Genap
=============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 1. KONFIGURASI GLOBAL
# ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "data_smp_negeri_bandung.csv"
OUTPUT_DIR = BASE_DIR / "output_grafik"
OUTPUT_DIR.mkdir(exist_ok=True)

# Palet warna konsisten
WARNA_L   = "#2563EB"   # biru — laki-laki
WARNA_P   = "#DB2777"   # pink — perempuan
WARNA_TOT = "#059669"   # hijau — total

plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
    "figure.dpi":       120,
})

# ─────────────────────────────────────────────────────────────
# 2. LOAD DATA
# ─────────────────────────────────────────────────────────────

df = pd.read_csv(DATA_FILE)

# Pastikan kolom numerik bersih
df["jumlah_laki_laki"]    = pd.to_numeric(df["jumlah_laki_laki"],    errors="coerce")
df["jumlah_perempuan"]    = pd.to_numeric(df["jumlah_perempuan"],    errors="coerce")
df["total_peserta_didik"] = pd.to_numeric(df["total_peserta_didik"], errors="coerce")

# ─────────────────────────────────────────────────────────────
# 3. RINGKASAN STATISTIK
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("INFORMASI DATASET")
print("=" * 60)
print(f"Jumlah Sekolah      : {len(df)}")
print(f"Jumlah Kecamatan    : {df['kecamatan'].nunique()}")
print(f"Total Peserta Didik : {df['total_peserta_didik'].sum():,}")
print(f"  Laki-laki         : {df['jumlah_laki_laki'].sum():,}")
print(f"  Perempuan         : {df['jumlah_perempuan'].sum():,}")
print()
print(df[["nama_sekolah", "kecamatan", "jumlah_laki_laki",
          "jumlah_perempuan", "total_peserta_didik"]].head(10).to_string(index=False))

print("\n" + "=" * 60)
print("STATISTIK DESKRIPTIF")
print("=" * 60)
print(df[["jumlah_laki_laki", "jumlah_perempuan", "total_peserta_didik"]].describe().round(2))

rata_l = df["jumlah_laki_laki"].mean()
rata_p = df["jumlah_perempuan"].mean()
print(f"\nRata-rata Laki-laki  : {rata_l:.2f}")
print(f"Rata-rata Perempuan  : {rata_p:.2f}")

# Agregasi per kecamatan
kec = df.groupby("kecamatan").agg(
    jumlah_sekolah    =("nama_sekolah",    "count"),
    total_laki_laki   =("jumlah_laki_laki","sum"),
    total_perempuan   =("jumlah_perempuan","sum"),
    total_peserta_didik=("total_peserta_didik","sum"),
).reset_index().sort_values("total_peserta_didik", ascending=False)

print("\n" + "=" * 60)
print("TOTAL PESERTA DIDIK PER KECAMATAN (Top 15)")
print("=" * 60)
print(kec.head(15).to_string(index=False))

# ─────────────────────────────────────────────────────────────
# 4. GRAFIK 1 — Bar: Total Peserta Didik per Kecamatan
# ─────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 6))

bars = ax.bar(
    kec["kecamatan"],
    kec["total_peserta_didik"],
    color=WARNA_TOT,
    edgecolor="white",
    linewidth=0.7,
    zorder=3,
)

# Label nilai di atas batang
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 30,
        f"{int(bar.get_height()):,}",
        ha="center", va="bottom",
        fontsize=7, color="#374151",
    )

ax.set_title("Total Peserta Didik SMP Negeri per Kecamatan\nKota Bandung — Semester 2025/2026 Genap",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Kecamatan", fontsize=11)
ax.set_ylabel("Jumlah Peserta Didik", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.xticks(rotation=55, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_total_per_kecamatan.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 1 disimpan.")

# ─────────────────────────────────────────────────────────────
# 5. GRAFIK 2 — Grouped Bar: L vs P per Kecamatan (Top 15)
# ─────────────────────────────────────────────────────────────

top15 = kec.head(15).reset_index(drop=True)
x     = np.arange(len(top15))
lebar = 0.38

fig, ax = plt.subplots(figsize=(14, 6))
b1 = ax.bar(x - lebar/2, top15["total_laki_laki"],   lebar, label="Laki-laki",  color=WARNA_L, zorder=3)
b2 = ax.bar(x + lebar/2, top15["total_perempuan"],    lebar, label="Perempuan",  color=WARNA_P, zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(top15["kecamatan"], rotation=50, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
ax.set_title("Perbandingan Peserta Didik L & P per Kecamatan (Top 15)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Kecamatan", fontsize=11)
ax.set_ylabel("Jumlah Peserta Didik", fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_grouped_bar_lp.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 2 disimpan.")

# ─────────────────────────────────────────────────────────────
# 6. GRAFIK 3 — Pie: Rasio Laki-laki vs Perempuan
# ─────────────────────────────────────────────────────────────

total_l = df["jumlah_laki_laki"].sum()
total_p = df["jumlah_perempuan"].sum()

fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    [total_l, total_p],
    labels=["Laki-laki", "Perempuan"],
    colors=[WARNA_L, WARNA_P],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(edgecolor="white", linewidth=2),
    pctdistance=0.75,
)
for at in autotexts:
    at.set_fontsize(13)
    at.set_fontweight("bold")
    at.set_color("white")

ax.set_title(f"Rasio Peserta Didik L vs P\n"
             f"Total: {total_l + total_p:,} siswa",
             fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_pie_rasio_gender.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 3 disimpan.")

# ─────────────────────────────────────────────────────────────
# 7. GRAFIK 4 — Histogram Distribusi Total per Sekolah
# ─────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["total_peserta_didik"], bins=15, color=WARNA_TOT,
        edgecolor="white", linewidth=0.8, alpha=0.85, zorder=3)

# KDE overlay (pakai numpy, tanpa scipy)
data_clean = df["total_peserta_didik"].dropna().values
xs = np.linspace(data_clean.min(), data_clean.max(), 300)
bw = 1.06 * data_clean.std() * len(data_clean) ** (-1/5)  # Silverman's rule
kde_vals = np.array([
    np.mean(np.exp(-0.5 * ((xs[i] - data_clean) / bw) ** 2) / (bw * np.sqrt(2 * np.pi)))
    for i in range(len(xs))
])
ax2 = ax.twinx()
ax2.plot(xs, kde_vals, color="#DC2626", linewidth=2, label="KDE")
ax2.set_ylabel("Densitas", fontsize=10, color="#DC2626")
ax2.tick_params(axis="y", labelcolor="#DC2626")
ax2.set_ylim(0)
ax2.spines["right"].set_visible(True)

ax.set_title("Distribusi Jumlah Peserta Didik per Sekolah",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Jumlah Peserta Didik per Sekolah", fontsize=11)
ax.set_ylabel("Frekuensi (Jumlah Sekolah)", fontsize=11)
ax.axvline(df["total_peserta_didik"].mean(), color="#F59E0B", linestyle="--",
           linewidth=1.5, label=f"Rata-rata: {df['total_peserta_didik'].mean():.0f}")
ax.legend(fontsize=9, loc="upper left")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_distribusi_total.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 4 disimpan.")

# ─────────────────────────────────────────────────────────────
# 8. GRAFIK 5 — Heatmap Korelasi
# ─────────────────────────────────────────────────────────────

num_cols = ["jumlah_laki_laki", "jumlah_perempuan", "total_peserta_didik",
            "jumlah_rombel", "jumlah_guru"]
corr = df[num_cols].corr()
labels = ["Laki-laki", "Perempuan", "Total PD", "Rombel", "Guru"]

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(
    corr,
    annot=True, fmt=".2f",
    cmap="coolwarm", center=0,
    linewidths=0.5, linecolor="white",
    xticklabels=labels,
    yticklabels=labels,
    ax=ax,
    annot_kws={"size": 11},
)
ax.set_title("Korelasi Antar Variabel Numerik",
             fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_heatmap_korelasi.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 5 disimpan.")

# ─────────────────────────────────────────────────────────────
# 9. GRAFIK 6 — Top 10 Sekolah Terbesar
# ─────────────────────────────────────────────────────────────

top10 = df.nlargest(10, "total_peserta_didik")[
    ["nama_sekolah", "jumlah_laki_laki", "jumlah_perempuan"]
].set_index("nama_sekolah")

fig, ax = plt.subplots(figsize=(11, 6))
top10.plot(kind="barh", stacked=True, color=[WARNA_L, WARNA_P],
           edgecolor="white", linewidth=0.7, ax=ax)
ax.set_title("10 SMP Negeri dengan Peserta Didik Terbanyak",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Jumlah Peserta Didik", fontsize=11)
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
ax.legend(["Laki-laki", "Perempuan"], fontsize=10)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_top10_sekolah.png", bbox_inches="tight")
plt.show()
print("✔ Grafik 6 disimpan.")

print("\n" + "=" * 60)
print(f"Semua grafik tersimpan di folder: {OUTPUT_DIR}/")
print("=" * 60)
