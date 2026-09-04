import contextlib
import base64
import io
import re
from pathlib import Path
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from analysis import (
    aksiyon_oner,
    ai_analiz_verisi_olustur,
    ai_donemsel_analiz_verisi_olustur,
    ai_finansal_analiz_verisi_olustur,
    analiz_et,
    davranis_segmentasyonu,
    donem_karsilastir,
    finansal_musteri_segmentasyonu,
    karar_destek_gelistir,
    musteri_ozet_tablosu,
    risk_degerlendir,
    segment_karar_destek,
    trend_analizi,
    veri_yönetisimi,
)


st.set_page_config(
    page_title="VakıfBank Veri Laboratuvarı",
    page_icon="💛",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --vg-primary: #ffcc00;
        --vg-secondary: #ff8a00;
        --vg-pink: #ff4f81;
        --vg-green: #28c76f;
        --vg-panel: rgba(31, 31, 35, 0.92);
        --vg-border: rgba(255, 204, 0, 0.28);
        --vg-text-soft: #d8d1bd;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 88% 4%, rgba(255, 204, 0, 0.16), transparent 25%),
            radial-gradient(circle at 8% 78%, rgba(255, 79, 129, 0.08), transparent 22%),
            linear-gradient(145deg, #111114 0%, #1a1917 55%, #121214 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #242218 0%, #151517 68%);
        border-right: 1px solid var(--vg-border);
    }

    [data-testid="stSidebar"] h2 {
        color: var(--vg-primary);
        letter-spacing: 0.02em;
    }

    h1, h2, h3 {
        color: #fff9e8;
        letter-spacing: -0.02em;
    }

    h1 {
        padding-bottom: 0.35rem;
        border-bottom: 3px solid var(--vg-primary);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(40, 38, 31, 0.98), rgba(24, 24, 27, 0.98));
        border: 1px solid var(--vg-border);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25), inset 0 3px 0 rgba(255, 204, 0, 0.75);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) rotate(-0.3deg);
        border-color: var(--vg-primary);
    }

    [data-testid="stMetricLabel"] {
        color: var(--vg-text-soft);
    }

    [data-testid="stMetricValue"] {
        color: var(--vg-primary);
    }

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(35, 33, 27, 0.9);
        border: 2px dashed rgba(255, 204, 0, 0.65);
        border-radius: 16px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--vg-border);
        border-radius: 16px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--vg-border);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--vg-text-soft);
    }

    div[role="radiogroup"] label[data-baseweb="radio"] {
        padding: 7px 9px;
        border-radius: 9px;
        transition: background-color 0.18s ease;
    }

    div[role="radiogroup"] label[data-baseweb="radio"]:hover {
        background: rgba(255, 204, 0, 0.13);
    }

    [data-testid="stToggle"] {
        background: rgba(38, 36, 30, 0.75);
        border: 1px solid rgba(255, 204, 0, 0.2);
        border-radius: 10px;
        padding: 8px 12px;
    }

    .stButton > button,
    [data-testid="stBaseButton-secondary"] {
        border-color: rgba(255, 204, 0, 0.65);
        border-radius: 12px;
    }

    .stButton > button:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: var(--vg-primary);
        color: var(--vg-primary);
    }

    hr {
        border-color: var(--vg-border);
    }

    .vb-hero {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 14% 12%, rgba(255, 242, 195, 0.22), transparent 24%),
            linear-gradient(120deg, #d8b24a 0%, #c99a28 55%, #a96f12 100%);
        color: #151515;
        border-radius: 24px;
        padding: 24px 28px;
        margin: 2px 0 22px 0;
        border: 1px solid rgba(255, 224, 145, 0.38);
        box-shadow: 0 16px 42px rgba(92, 61, 8, 0.34), inset 0 1px 0 rgba(255,255,255,0.25);
    }
    .vb-hero::after {
        content: "";
        position: absolute;
        width: 190px;
        height: 190px;
        right: -55px;
        top: -85px;
        border: 28px solid rgba(255, 229, 164, 0.22);
        border-radius: 50%;
    }
    .vb-official-logo {
        display: inline-block;
        width: 190px;
        background: #ffffff;
        border-radius: 12px;
        padding: 7px 11px;
        margin-bottom: 12px;
        box-shadow: 0 6px 18px rgba(50, 36, 0, 0.16);
    }
    .vb-hero h1 {
        color: #151515;
        border: 0;
        margin: 0;
        padding: 0;
        font-size: 2.15rem;
    }
    .vb-hero p { margin: 7px 0 0; font-weight: 650; }
    .vb-mascot {
        position: absolute;
        right: 42px;
        bottom: 24px;
        z-index: 2;
    }
    .vb-mascot-face {
        display: grid;
        place-items: center;
        width: 78px;
        height: 78px;
        border-radius: 50%;
        background: rgba(255,255,255,0.38);
        font-size: 3rem;
        box-shadow: 0 8px 22px rgba(80,48,0,0.14);
        transform: rotate(4deg);
        animation: vb-bounce 2.8s ease-in-out infinite;
    }
    @keyframes vb-bounce {
        0%, 100% { transform: translateY(0) rotate(4deg); }
        50% { transform: translateY(-5px) rotate(-3deg); }
    }
    @media (max-width: 900px) {
        .vb-mascot { position: relative; right: auto; bottom: auto; margin-top: 18px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


ANA_KOLONLAR = {
    "customer_id", "ad", "soyisim", "tc_kimlik_no", "dogum_tarihi",
    "telefon", "email", "adres", "sehir", "meslek", "hesap_turu",
    "yas", "aylik_gelir", "bakiye", "islem_sayisi",
    "toplam_islem_tutari", "son_islem_tarihi", "kayit_tarihi",
    "veri_guncelleme_tarihi",
}

FINANSAL_KOLONLAR = {
    "customer_id", "meslek", "yas", "ay", "aylik_gelir",
    "aylik_harcama", "vadeli_bakiye", "vadesiz_bakiye", "kredi_limiti",
    "kullanilan_kredi", "kalan_kredi_borcu", "islem_sayisi",
    "toplam_islem_tutari",
}

KISISSEL_KOLONLAR = {
    "ad", "soyisim", "tc_kimlik_no", "telefon", "email", "adres"
}

AY_SIRASI = {
    "ocak": 1,
    "subat": 2,
    "mart": 3,
    "nisan": 4,
    "mayis": 5,
    "haziran": 6,
    "temmuz": 7,
    "agustos": 8,
    "eylul": 9,
    "ekim": 10,
    "kasim": 11,
    "aralik": 12,
}

KOLON_ETIKETLERI = {
    "customer_id": "Müşteri ID",
    "meslek": "Meslek",
    "yas": "Yaş",
    "ay": "Ay",
    "segment": "Segment",
    "musteri_sayisi": "Müşteri Sayısı",
    "ortalama_aylik_gelir": "Ortalama Aylık Gelir",
    "ortalama_aylik_harcama": "Ortalama Aylık Harcama",
    "ortalama_vadeli_bakiye": "Ortalama Vadeli Bakiye",
    "ortalama_vadesiz_bakiye": "Ortalama Vadesiz Bakiye",
    "ortalama_kredi_limiti": "Ortalama Kredi Limiti",
    "ortalama_kullanilan_kredi": "Ortalama Kullanılan Kredi",
    "ortalama_kalan_kredi_borcu": "Ortalama Kalan Kredi Borcu",
    "toplam_islem_sayisi": "12 Aylık Toplam İşlem Sayısı",
    "toplam_islem_tutari": "12 Aylık Toplam İşlem Tutarı",
    "aylik_tasarruf": "Ortalama Aylık Tasarruf",
    "tasarruf_orani": "Tasarruf Oranı",
    "kredi_kullanim_orani": "Kredi Kullanım Oranı",
    "ortalama_gelir": "Ortalama Gelir",
    "ortalama_harcama": "Ortalama Harcama",
    "ortalama_tasarruf": "Ortalama Tasarruf",
    "ortalama_tasarruf_orani": "Ortalama Tasarruf Oranı",
    "ortalama_kredi_kullanim_orani": "Ortalama Kredi Kullanım Oranı",
    "risk_firsat": "Risk / Fırsat",
    "onerilen_aksiyon": "Önerilen Aksiyon",
    "karar_gerekcesi": "Karar Gerekçesi",
    "islem_sayisi": "İşlem Sayısı",
}


@st.cache_data(show_spinner=False)
def excel_oku(dosya_bytes):
    return pd.read_excel(io.BytesIO(dosya_bytes))


def dosya_oku(dosya, gerekli_kolonlar, veri_adi):
    if dosya is None:
        return None

    try:
        df = excel_oku(dosya.getvalue())
    except Exception as hata:
        st.error(f"{veri_adi} okunamadı: {hata}")
        return None

    eksik_kolonlar = sorted(gerekli_kolonlar - set(df.columns))
    if eksik_kolonlar:
        st.error(
            f"{veri_adi} beklenen yapıda değil. Eksik kolonlar: "
            + ", ".join(eksik_kolonlar)
        )
        return None

    return df


def analizleri_hazirla(df):
    # analysis.py içindeki eski tanılama yazıları kullanıcı ekranına taşınmasın.
    with contextlib.redirect_stdout(io.StringIO()):
        sonuclar = analiz_et(df)
        yonetisim = risk_degerlendir(veri_yönetisimi(df))
        trend = trend_analizi(df)
    segmentler = davranis_segmentasyonu(df)
    return sonuclar, yonetisim, trend, segmentler


def veri_kalitesi_skoru(sonuclar):
    toplam = sonuclar["toplam_kayit_sayisi"]
    sorun = (
        sonuclar["eksik_deger_sayisi"]
        + sonuclar["duplicate_sayisi"]
        + sonuclar["anomali_sayisi"]
    )
    return max(0.0, 100 - (sorun / toplam * 100)) if toplam else 0.0


def guvenli_onizleme(df, satir=5):
    onizleme = df.head(satir).copy()
    for kolon in KISISSEL_KOLONLAR.intersection(onizleme.columns):
        onizleme[kolon] = "••••••"
    return onizleme


def cizgi_grafigi(df, x, y, baslik=None, y_domain=None):
    kolonlar = [y] if isinstance(y, str) else list(y)
    grafik_df = df[[x] + kolonlar].copy()
    grafik_df = grafik_df.replace([np.inf, -np.inf], np.nan).dropna()
    if grafik_df.empty:
        st.info("Bu grafik için gösterilecek yeterli veri bulunmuyor.")
        return

    uzun = grafik_df.melt(x, var_name="Gösterge", value_name="Değer")
    x_sirasi = uzun[x].drop_duplicates().tolist()
    y_ekseni = alt.Y("Değer:Q", title="Değer")
    if y_domain is not None:
        y_ekseni = alt.Y(
            "Değer:Q",
            title="Değer",
            scale=alt.Scale(domain=y_domain, zero=False),
        )

    grafik = (
        alt.Chart(uzun)
        .mark_line(point=True)
        .encode(
            x=alt.X(f"{x}:N", title=x, sort=x_sirasi),
            y=y_ekseni,
            color=alt.Color(
                "Gösterge:N", title="Gösterge",
                scale=alt.Scale(range=["#ffcc00", "#ff8a00", "#ff4f81", "#28c76f", "#38bdf8"]),
            ),
            tooltip=[x, "Gösterge", alt.Tooltip("Değer:Q", format=",.2f")],
        )
        .properties(height=320)
    )
    if baslik:
        grafik = grafik.properties(title=baslik)
    st.altair_chart(grafik, use_container_width=True)


def sutun_grafigi(veri, kategori, deger, baslik=None):
    grafik_df = veri[[kategori, deger]].copy()
    grafik_df[deger] = pd.to_numeric(grafik_df[deger], errors="coerce")
    grafik_df = grafik_df.replace([np.inf, -np.inf], np.nan).dropna()
    if grafik_df.empty:
        st.info("Bu grafik için gösterilecek yeterli veri bulunmuyor.")
        return

    grafik = (
        alt.Chart(grafik_df)
        .mark_bar()
        .encode(
            x=alt.X(f"{kategori}:N", title=kategori, sort="-y"),
            y=alt.Y(f"{deger}:Q", title=deger),
            tooltip=[kategori, alt.Tooltip(f"{deger}:Q", format=",.2f")],
            color=alt.Color(
                f"{kategori}:N", legend=None,
                scale=alt.Scale(range=["#ffcc00", "#ff8a00", "#ff4f81", "#28c76f", "#38bdf8"]),
            ),
        )
        .properties(height=320)
    )
    if baslik:
        grafik = grafik.properties(title=baslik)
    st.altair_chart(grafik, use_container_width=True)


def kaynak_bilgisi(dosya, df):
    st.caption(
        f"Kaynak: {dosya.name} · {len(df)} kayıt · "
        f"{df['customer_id'].nunique()} tekil müşteri"
    )


def tablo_kolon_ayarlari(df):
    ayarlar = {}
    for kolon in df.columns:
        normal_kolon = str(kolon).lower().translate(
            str.maketrans("çğıöşü", "cgiosu")
        )
        etiket = KOLON_ETIKETLERI.get(
            kolon,
            str(kolon).replace("_", " ").title(),
        )

        if not pd.api.types.is_numeric_dtype(df[kolon]):
            ayarlar[kolon] = st.column_config.Column(etiket)
        elif (
            "orani" in normal_kolon
            or "skoru" in normal_kolon
            or "%" in str(kolon)
        ):
            ayarlar[kolon] = st.column_config.NumberColumn(
                etiket, format="%.2f%%"
            )
        elif (
            "sayisi" in normal_kolon
            or "musteri" in normal_kolon
            or "eksik deger" in normal_kolon
            or "duplicate" in normal_kolon
            or "anomali" in normal_kolon
            or str(kolon) in {"yas", "customer_id", "musteri_sayisi"}
        ):
            ayarlar[kolon] = st.column_config.NumberColumn(
                etiket, format="%d"
            )
        else:
            ayarlar[kolon] = st.column_config.NumberColumn(
                etiket, format="%.2f"
            )
    return ayarlar


def donem_siralama_anahtari(donem_adi):
    normal = donem_adi.lower().translate(
        str.maketrans("çğıöşü", "cgiosu")
    )

    tarih_eslesmesi = re.search(r"(20\d{2})[-_. ](0?[1-9]|1[0-2])", normal)
    if tarih_eslesmesi:
        yil, ay = tarih_eslesmesi.groups()
        return int(yil), int(ay), normal

    for ay_adi, ay_sirasi in AY_SIRASI.items():
        if ay_adi in normal:
            return 0, ay_sirasi, normal

    return 9999, 99, normal



st.markdown(
    f"""
    <div class="vb-hero">
        <h1>Veri Yönetişimi Laboratuvarı 🚀</h1>
        <p>Veri kalitesi, müşteri davranışı, finansal içgörü ve yapay zekâ aynı yerde.</p>
        <div class="vb-mascot">
            <div class="vb-mascot-face" title="Minik veri arısı">🐝✨</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("📂 Veri Kaynakları")
    ana_dosya = st.file_uploader(
        "👥 Ana müşteri verisi", type=["xlsx"], key="v2_ana"
    )
    finansal_dosya = st.file_uploader(
        "💰 12 aylık finansal veri", type=["xlsx"], key="v2_finansal"
    )
    donem_dosyalari = st.file_uploader(
        "📅 Dönem dosyaları", type=["xlsx"], accept_multiple_files=True,
        key="v2_donemler",
    )

    st.divider()
    sayfa = st.radio(
        "Bölüm",
        [
            "Ana Gösterge Paneli",
            "Veri Kalitesi",
            "Müşteri Analizi",
            "Veri Yönetişimi ve Risk",
            "Finansal Analiz",
            "Dönemsel Analiz",
            "AI Veri Asistanı",
        ],
        format_func=lambda ad: {
            "Ana Gösterge Paneli": "🏠 Ana Gösterge Paneli",
            "Veri Kalitesi": "✨ Veri Kalitesi",
            "Müşteri Analizi": "👥 Müşteri Analizi",
            "Veri Yönetişimi ve Risk": "🛡️ Veri Yönetişimi ve Risk",
            "Finansal Analiz": "💰 Finansal Analiz",
            "Dönemsel Analiz": "📅 Dönemsel Analiz",
            "AI Veri Asistanı": "🤖 AI Veri Asistanı",
        }[ad],
    )


ana_df = dosya_oku(ana_dosya, ANA_KOLONLAR, "Ana müşteri verisi")
finansal_df = dosya_oku(
    finansal_dosya, FINANSAL_KOLONLAR, "Finansal müşteri verisi"
)

sonuclar = yonetisim_df = trend_df = segmentli_df = None
if ana_df is not None:
    sonuclar, yonetisim_df, trend_df, segmentli_df = analizleri_hazirla(ana_df)


if sayfa == "Ana Gösterge Paneli":
    st.header("Ana Gösterge Paneli")
    if ana_df is None:
        st.info("Başlamak için sol panelden ana müşteri Excel dosyasını yükleyin.")
    else:
        kaynak_bilgisi(ana_dosya, ana_df)
        aktif = sonuclar["tekil_musteri_sayisi"] - sonuclar["pasif_musteri_sayisi"]
        kolonlar = st.columns(6)
        kolonlar[0].metric("Toplam Kayıt", sonuclar["toplam_kayit_sayisi"])
        kolonlar[1].metric("Tekil Müşteri", sonuclar["tekil_musteri_sayisi"])
        kolonlar[2].metric("Aktif Müşteri", aktif)
        kolonlar[3].metric("Pasif Müşteri", sonuclar["pasif_musteri_sayisi"])
        kolonlar[4].metric("Duplicate", sonuclar["duplicate_sayisi"])
        kolonlar[5].metric("Kalite Skoru", f"%{veri_kalitesi_skoru(sonuclar):.2f}")

        st.subheader("Güvenli Veri Önizlemesi")
        st.caption("Kişisel alanlar önizlemede otomatik olarak maskelenmiştir.")
        onizleme = guvenli_onizleme(ana_df)
        st.dataframe(
            onizleme,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(onizleme),
        )

        c1, c2 = st.columns(2)
        with c1:
            dagilim = pd.DataFrame({
                "Durum": ["Aktif", "Pasif"],
                "Müşteri Sayısı": [aktif, sonuclar["pasif_musteri_sayisi"]],
            })
            sutun_grafigi(dagilim, "Durum", "Müşteri Sayısı", "Müşteri Durumu")
        with c2:
            segment_dagilimi = (
                segmentli_df["segment"].value_counts().rename_axis("Segment")
                .reset_index(name="Müşteri Sayısı")
            )
            sutun_grafigi(
                segment_dagilimi, "Segment", "Müşteri Sayısı",
                "Davranış Segmentleri",
            )


elif sayfa == "Veri Kalitesi":
    st.header("Veri Kalitesi")
    if ana_df is None:
        st.info("Bu bölüm için ana müşteri verisini yükleyin.")
    else:
        kaynak_bilgisi(ana_dosya, ana_df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Eksik Değer", sonuclar["eksik_deger_sayisi"])
        c2.metric("Duplicate", sonuclar["duplicate_sayisi"])
        c3.metric("Anomali", sonuclar["anomali_sayisi"])
        c4.metric("Kalite Skoru", f"%{veri_kalitesi_skoru(sonuclar):.2f}")

        with st.expander("Skor nasıl hesaplanıyor?"):
            st.write(
                "100 − ((eksik değer + duplicate + anomali) / toplam kayıt × 100). "
                "Skor sıfırın altına düşemez."
            )

        st.subheader("Kolon Bazlı Kalite Detayları")
        kalite_detaylari = sonuclar["kalite_detaylari"]
        st.dataframe(
            kalite_detaylari,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(kalite_detaylari),
        )
        st.subheader("Dönemsel Trend Analizi")
        st.dataframe(
            trend_df,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(trend_df),
        )
        cizgi_grafigi(
            trend_df,
            "ay",
            "toplam_islem_tutari",
            "Toplam İşlem Tutarı Trendi",
        )

        st.subheader("Aylık İşlem Sayısı")
        cizgi_grafigi(
            trend_df,
            "ay",
            "islem_sayisi",
            "Aylık İşlem Sayısı",
        )


elif sayfa == "Müşteri Analizi":
    st.header("Müşteri Analizi")
    if ana_df is None:
        st.info("Bu bölüm için ana müşteri verisini yükleyin.")
    else:
        kaynak_bilgisi(ana_dosya, ana_df)
        st.subheader("Davranış Segmentasyonu")
        st.write("Segmentler bakiye ve işlem sayısı medyanlarına göre üretilir.")
        st.dataframe(
            segmentli_df[["customer_id", "bakiye", "islem_sayisi", "segment"]]
            .head(25),
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(
                segmentli_df[["customer_id", "bakiye", "islem_sayisi", "segment"]]
            ),
        )
        segment_dagilimi = (
            segmentli_df["segment"].value_counts().rename_axis("Segment")
            .reset_index(name="Müşteri Sayısı")
        )
        sutun_grafigi(segment_dagilimi, "Segment", "Müşteri Sayısı")


elif sayfa == "Veri Yönetişimi ve Risk":
    st.header("Veri Yönetişimi ve Risk")
    if ana_df is None:
        st.info("Bu bölüm için ana müşteri verisini yükleyin.")
    else:
        kaynak_bilgisi(ana_dosya, ana_df)
        aksiyon_df = aksiyon_oner(yonetisim_df)
        c1, c2, c3, c4 = st.columns(4)
        riskler = yonetisim_df["Risk Seviyesi"].value_counts()
        c1.metric("Kritik", int(riskler.get("Kritik", 0)))
        c2.metric("Yüksek", int(riskler.get("Yüksek", 0)))
        c3.metric("Orta", int(riskler.get("Orta", 0)))
        c4.metric("Düşük", int(riskler.get("Düşük", 0)))

        st.subheader("Veri Sözlüğü ve Risk Envanteri")
        st.dataframe(
            yonetisim_df,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(yonetisim_df),
        )
        st.subheader("Önerilen Kontroller")
        st.dataframe(
            aksiyon_df,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(aksiyon_df),
        )

        risk = (
            yonetisim_df["Risk Seviyesi"].value_counts()
            .rename_axis("Seviye").reset_index(name="Kolon Sayısı")
        )
        sutun_grafigi(risk, "Seviye", "Kolon Sayısı", "Risk")


elif sayfa == "Finansal Analiz":
    st.header("1000 Müşterilik Finansal Analiz")
    if finansal_df is None:
        st.info("Bu bölüm için sol panelden 12 aylık finansal veriyi yükleyin.")
    else:
        kaynak_bilgisi(finansal_dosya, finansal_df)
        with contextlib.redirect_stdout(io.StringIO()):
            finansal_ozet = musteri_ozet_tablosu(finansal_df)
            finansal_segment = finansal_musteri_segmentasyonu(finansal_ozet)
            karar = karar_destek_gelistir(segment_karar_destek(finansal_segment))

        c1, c2, c3 = st.columns(3)
        c1.metric("Aylık Kayıt", len(finansal_df))
        c2.metric("Tekil Müşteri", finansal_df["customer_id"].nunique())
        c3.metric("Kapsanan Ay", finansal_df["ay"].nunique())

        st.subheader("Finansal Segmentler")
        finansal_ozet_kolonlari = [
            "customer_id",
            "meslek",
            "ortalama_aylik_gelir",
            "ortalama_aylik_harcama",
            "aylik_tasarruf",
            "tasarruf_orani",
            "kredi_kullanim_orani",
            "segment",
        ]
        tum_finansal_kolonlar = st.toggle(
            "Tüm finansal kolonları göster",
            key="tum_finansal_kolonlar",
        )
        finansal_gorunum = (
            finansal_segment
            if tum_finansal_kolonlar
            else finansal_segment[finansal_ozet_kolonlari]
        )
        st.dataframe(
            finansal_gorunum,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(finansal_gorunum),
        )
        segment_dagilimi = (
            finansal_segment["segment"].value_counts().rename_axis("Segment")
            .reset_index(name="Müşteri Sayısı")
        )
        sutun_grafigi(segment_dagilimi, "Segment", "Müşteri Sayısı")

        st.subheader("Segment Bazlı Finansal Analiz")
        segment_analizi = (
            finansal_segment
            .groupby("segment")
            .agg(
                musteri_sayisi=("customer_id", "count"),
                ortalama_gelir=("ortalama_aylik_gelir", "mean"),
                ortalama_harcama=("ortalama_aylik_harcama", "mean"),
                ortalama_tasarruf=("aylik_tasarruf", "mean"),
                ortalama_tasarruf_orani=("tasarruf_orani", "mean"),
                ortalama_kredi_limiti=("ortalama_kredi_limiti", "mean"),
                ortalama_kullanilan_kredi=(
                    "ortalama_kullanilan_kredi", "mean"
                ),
                ortalama_kredi_kullanim_orani=(
                    "kredi_kullanim_orani", "mean"
                ),
            )
            .reset_index()
        )
        st.dataframe(
            segment_analizi,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(segment_analizi),
        )

        st.subheader("12 Aylık Müşteri Özeti ve Karar Destek Analizi")
        st.caption(
            "‘Ortalama’ ile başlayan değerler müşterinin 12 aylık "
            "ortalamasını, ‘toplam’ ile başlayan değerler ise 12 aylık "
            "toplamını göstermektedir."
        )
        karar_ozet_kolonlari = [
            "customer_id",
            "meslek",
            "segment",
            "tasarruf_orani",
            "kredi_kullanim_orani",
            "risk_firsat",
            "onerilen_aksiyon",
            "karar_gerekcesi",
        ]
        tum_karar_kolonlari = st.toggle(
            "Karar tablosundaki tüm finansal kolonları göster",
            key="tum_karar_kolonlari",
        )
        karar_gorunum = (
            karar if tum_karar_kolonlari else karar[karar_ozet_kolonlari]
        )
        st.dataframe(
            karar_gorunum,
            use_container_width=True,
            column_config=tablo_kolon_ayarlari(karar_gorunum),
        )


elif sayfa == "Dönemsel Analiz":
    st.header("Dönemsel Kalite ve Risk Analizi")
    if len(donem_dosyalari) < 2:
        st.info("Karşılaştırma için sol panelden en az iki dönem dosyası yükleyin.")
    else:
        donemler = {}
        gecersizler = []
        for dosya in donem_dosyalari:
            df = dosya_oku(dosya, ANA_KOLONLAR, dosya.name)
            if df is None:
                gecersizler.append(dosya.name)
            else:
                donemler[dosya.name.rsplit(".", 1)[0]] = df

        donemler = dict(
            sorted(
                donemler.items(),
                key=lambda oge: donem_siralama_anahtari(oge[0]),
            )
        )

        if not gecersizler and len(donemler) >= 2:
            adlar = list(donemler)
            karsilastirma = donem_karsilastir(
                donemler[adlar[-2]], donemler[adlar[-1]]
            )
            st.subheader(f"{adlar[-2]} → {adlar[-1]} Karşılaştırması")
            st.dataframe(
                karsilastirma,
                use_container_width=True,
                column_config=tablo_kolon_ayarlari(karsilastirma),
            )

            trend_satirlari = []
            for ad, df in donemler.items():
                with contextlib.redirect_stdout(io.StringIO()):
                    sonuc = analiz_et(df)
                skor = veri_kalitesi_skoru(sonuc)
                trend_satirlari.append({
                    "Dönem": ad,
                    "Veri Kalitesi Skoru": skor,
                    "Eksik Değer": sonuc["eksik_deger_sayisi"],
                    "Duplicate": sonuc["duplicate_sayisi"],
                    "Anomali": sonuc["anomali_sayisi"],
                    "Pasif Müşteri": sonuc["pasif_musteri_sayisi"],
                })

            donem_trendi = pd.DataFrame(trend_satirlari)
            st.subheader("Dönemsel Sonuçlar")
            st.dataframe(
                donem_trendi,
                use_container_width=True,
                column_config=tablo_kolon_ayarlari(donem_trendi),
            )
            skor_alt_sinir = max(
                0,
                float(donem_trendi["Veri Kalitesi Skoru"].min()) - 0.5,
            )
            skor_ust_sinir = min(
                100,
                float(donem_trendi["Veri Kalitesi Skoru"].max()) + 0.5,
            )
            cizgi_grafigi(
                donem_trendi, "Dönem", "Veri Kalitesi Skoru",
                "Veri Kalitesi Skoru Trendi",
                y_domain=[skor_alt_sinir, skor_ust_sinir],
            )
            cizgi_grafigi(
                donem_trendi, "Dönem",
                ["Eksik Değer", "Duplicate", "Anomali"],
                "Veri Kalitesi Problemleri",
            )


elif sayfa == "AI Veri Asistanı":
    st.header("AI Veri Asistanı")

    if ana_df is None and finansal_df is None and not donem_dosyalari:
        st.warning("AI asistanını kullanmak için ana müşteri verisini, 12 aylık finansal veriyi veya dönem dosyalarını yükleyin.")
    else:
        ai_verisi = {}

        if ana_df is not None:
            ai_verisi["veri_yonetisimi"] = ai_analiz_verisi_olustur(
                ana_df, sonuclar, yonetisim_df, trend_df, segmentli_df
            )

        if finansal_df is not None:
            with contextlib.redirect_stdout(io.StringIO()):
                ai_verisi["finansal_analiz"] = ai_finansal_analiz_verisi_olustur(
                    finansal_df
                )

        if donem_dosyalari:
            ai_donemler = {}
            for dosya in donem_dosyalari:
                df = dosya_oku(dosya, ANA_KOLONLAR, dosya.name)
                if df is not None:
                    ai_donemler[dosya.name.rsplit(".", 1)[0]] = df

            ai_donemler = dict(
                sorted(
                    ai_donemler.items(),
                    key=lambda oge: donem_siralama_anahtari(oge[0]),
                )
            )

            if ai_donemler:
                with contextlib.redirect_stdout(io.StringIO()):
                    ai_verisi["donemsel_analiz"] = (
                        ai_donemsel_analiz_verisi_olustur(ai_donemler)
                    )

        st.subheader("AI’ye hazırlanmış güvenli bağlam")
        st.caption(
            "Ham kişisel veriler yerine yalnızca toplulaştırılmış veri yönetişimi, finansal ve dönemsel analiz sonuçları kullanılır."
        )

        with st.expander("Hazırlanan analiz özetini göster"):
            st.json(ai_verisi)

        soru = st.chat_input("Veri seti hakkında bir soru sorun")

        if soru:
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                st.error("OPENAI_API_KEY bulunamadı. .env dosyasını kontrol edin.")
            else:
                with st.chat_message("user"):
                    st.write(soru)

                with st.chat_message("assistant"):
                    with st.spinner("Analiz ediliyor..."):
                        try:
                            client = OpenAI(api_key=api_key)

                            yanit = client.responses.create(
                                model="gpt-5.4-mini",
                                instructions=(
                                    "Sen bir veri yönetişimi ve finansal analiz asistanısın. "
                                    "Yalnızca verilen anonim analiz özetine dayanarak Türkçe yanıt ver. "
                                    "Veride olmayan bilgi uydurma. Kısa, açık ve yöneticiye uygun öneriler sun. "
                                    "Son dönemdeki eksik ay verisini kesin düşüş gibi yorumlama. "
                                    "Finansal veri mevcutsa meslek, tasarruf, kredi kullanımı ve finansal segmentler hakkında yanıt verebilirsin. "
                                    "Dönem dosyaları mevcutsa yalnızca yüklenen dönemleri karşılaştır; yüklenmeyen aylar hakkında çıkarım yapma."
                                ),
                                input=(
                                    "Anonim analiz özeti:\n"
                                    + json.dumps(ai_verisi, ensure_ascii=False)
                                    + "\n\nKullanıcının sorusu:\n"
                                    + soru
                                ),
                                max_output_tokens=500,
                            )

                            st.write(yanit.output_text)

                        except Exception as hata:
                            st.error(f"AI bağlantısında hata oluştu: {hata}")     




   
