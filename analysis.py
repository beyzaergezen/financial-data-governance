import pandas as pd
import numpy as np


#veri kalitesini kontrol ediyor ve sonuçları çıkarıyor.
def analiz_et(df):

    print("eksik değerler:")
    print(df.isna().sum())

    print("\nDuplicate kayıt sayısı:")
    print(df.duplicated().sum())

    print("\nveri tipleri:")
    print(df.dtypes)

    # Kişisel veri kolonları
    kisisel_veri_kolonları = [
        "ad",
        "soyisim",
        "tc_kimlik_no",
        "dogum_tarihi",
        "telefon",
        "email",
        "adres"
    ]

    bulunan_kisisel_veriler = [
        kolon for kolon in kisisel_veri_kolonları
        if kolon in df.columns
    ]

    print("\ntespit edilen kişisel veri kolonları:")
    print(bulunan_kisisel_veriler)

    # Gizlilik seviyeleri
    gizlilik_seviyeleri = {
        "tc_kimlik_no": "çok yüksek",
        "telefon": "yüksek",
        "email": "yüksek",
        "adres": "yüksek",
        "dogum_tarihi": "orta",
        "ad": "orta",
        "soyisim": "orta"
    }

    print("\ngizlilik seviyesi önerileri:")

    for kolon in bulunan_kisisel_veriler:
        seviye = gizlilik_seviyeleri.get(kolon, "Belirlenmeli")
        print(f"{kolon}: {seviye}")

    # Kalite kuralları
    kalite_kurallari = {
        "customer_id": "Benzersiz olmalıdır.",
        "tc_kimlik_no": "Boş olmamalı, 11 haneli olmalı, 0 ile başlamamalı, boşuk-özel karakter içermemeli ve benzersiz olmalıdır.",
        "ad": "Boş olmamalıdır.",
        "soyisim": "Boş olmamalıdır.",
        "telefon": "Boş olmamalı ve geçerli telefon formatında olmalıdır.",
        "email": "Boş olmamalı ve geçerli e-posta formatında olmalıdır.",
        "dogum_tarihi": "Geçerli bir tarih olmalıdır.",
        "yas": "18 ile 90 arasında olmalıdır.",
        "aylik_gelir": "Negatif olmamalıdır.",
        "bakiye": "Negatif olmamalıdır.",
        "islem_sayisi": "Negatif olmamalıdır.",
        "toplam_islem_tutari": "Negatif olmamalıdır.",
        "son_islem_tarihi": "Geçerli bir tarih olmalıdır.",
        "kayit_tarihi": "Geçerli bir tarih olmalıdır."
    }

    print("\nkalite kuralı önerileri:")

    for kolon, kural in kalite_kurallari.items():
        if kolon in df.columns:
            print(f"{kolon}: {kural}")

    # Kalite kontrolleri
    gecersiz_yas = df[
        (df["yas"] < 18) | (df["yas"] > 90)
    ]

    print("\ngeçersiz yaş kayıt sayısı:")
    print(len(gecersiz_yas))

    gecersiz_bakiye = df[df["bakiye"] < 0]

    print("\ngeçersiz bakiye kayıt sayısı:")
    print(len(gecersiz_bakiye))

    gecersiz_gelir = df[df["aylik_gelir"] < 0]

    print("\ngeçersiz aylık gelir kayıt sayısı:")
    print(len(gecersiz_gelir))

    gecersiz_islem = df[df["islem_sayisi"] < 0]

    print("\ngeçersiz işlem sayısı kayıt sayısı:")
    print(len(gecersiz_islem))

    gecersiz_toplam_tutar = df[
        df["toplam_islem_tutari"] < 0
    ]

    print("\ngeçersiz toplam işlem tutarı kayıt sayısı:")
    print(len(gecersiz_toplam_tutar))

    # Doğum tarihi kontrolü
    print("\nDoğum tarihi aralığı:")
    print("En eski:", df["dogum_tarihi"].min())
    print("En yeni:", df["dogum_tarihi"].max())

    gecersiz_dogum_tarihi = df[
        df["dogum_tarihi"] > pd.Timestamp.today()
    ]

    print("\ngeçersiz doğum tarihi kayıt sayısı:")
    print(len(gecersiz_dogum_tarihi))

    # Son işlem tarihi kontrolü
    gecersiz_son_islem = df[
        df["son_islem_tarihi"] > pd.Timestamp.today()
    ]

    print("\ngeçersiz son işlem tarihi kayıt sayısı:")
    print(len(gecersiz_son_islem))

    # Kayıt tarihi kontrolü
    gecersiz_kayit_tarihi = df[
        df["kayit_tarihi"] > pd.Timestamp.today()
    ]

    print("\ngeçersiz kayıt tarihi kayıt sayısı:")
    print(len(gecersiz_kayit_tarihi))

    # Veri kalite raporu
    kalite_raporu = {
        "Eksik değer": df.isna().sum().sum(),
        "Duplicate": df.duplicated().sum(),
        "Geçersiz yaş": len(gecersiz_yas),
        "Geçersiz bakiye": len(gecersiz_bakiye),
        "Geçersiz aylık gelir": len(gecersiz_gelir),
        "Geçersiz işlem sayısı": len(gecersiz_islem),
        "Geçersiz toplam işlem tutarı": len(gecersiz_toplam_tutar),
        "Geçersiz doğum tarihi": len(gecersiz_dogum_tarihi),
        "Geçersiz son işlem tarihi": len(gecersiz_son_islem),
        "Geçersiz kayıt tarihi": len(gecersiz_kayit_tarihi)
    }

    print("\n" + "=" * 40)
    print("VERİ KALİTE RAPORU")
    print("=" * 40)

    for kontrol, sonuc in kalite_raporu.items():
        print(f"{kontrol}: {sonuc}")

    # Anomali tespiti - IQR
    Q1 = df["bakiye"].quantile(0.25)
    Q3 = df["bakiye"].quantile(0.75)

    print("\nbakiye için:")
    print("Q1:", Q1)
    print("Q3:", Q3)

    IQR = Q3 - Q1

    print("IQR:", IQR)

    alt_sinir = Q1 - 1.5 * IQR
    ust_sinir = Q3 + 1.5 * IQR

    print("Alt sınır:", alt_sinir)
    print("Üst sınır:", ust_sinir)

    anomali_bakiye = df[
        (df["bakiye"] < alt_sinir) |
        (df["bakiye"] > ust_sinir)
    ]

    print("\nanomali olarak tespit edilen bakiye kayıt sayısı:")
    print(len(anomali_bakiye))

    print("\nanomali olan müşteriler:")
    print(
        anomali_bakiye[
            ["customer_id", "ad", "soyisim", "bakiye"]
        ]
    )

    # Pasif müşteri analizi
    bir_yil_once = (
        pd.Timestamp.today() -
        pd.DateOffset(years=1)
    )

    pasif_musteriler = df[
        df["son_islem_tarihi"] < bir_yil_once
    ]

    print("\npasif müşteri sayısı:")
    print(len(pasif_musteriler))

    print("\npasif müşterilerden ilk 10 kayıt:")

    print(
        pasif_musteriler[
            [
                "customer_id",
                "ad",
                "soyisim",
                "son_islem_tarihi",
                "islem_sayisi"
            ]
        ].head(10)
    )

   
        # Kolon bazlı veri kalitesi detayları
    kalite_detaylari = pd.DataFrame({
        "Kolon": df.columns,
        "Eksik Değer": [
            int(df[kolon].isna().sum())
            for kolon in df.columns
        ]
    })

    # Bakiye anomalilerini ilgili kolona ekle
    kalite_detaylari["Anomali"] = 0

    if "bakiye" in df.columns:
        kalite_detaylari.loc[
            kalite_detaylari["Kolon"] == "bakiye",
            "Anomali"
        ] = len(anomali_bakiye)

    # Bütün sonuçları tek yerde topluyoruz
    sonuclar = {
        "eksik_deger_sayisi": int(df.isna().sum().sum()),
        "duplicate_sayisi": int(df.duplicated().sum()),
        "anomali_sayisi": int(len(anomali_bakiye)),
        "toplam_kayit_sayisi": int(len(df)),
        "tekil_musteri_sayisi": int(df["customer_id"].nunique()),
        "pasif_musteri_sayisi": int(
            pasif_musteriler["customer_id"].nunique()
        ),
        "kisisel_veri_kolonlari": bulunan_kisisel_veriler,
        "gizlilik_seviyeleri": gizlilik_seviyeleri,
        "kalite_kurallari": kalite_kurallari,
        "kalite_detaylari":kalite_detaylari
    }

    return sonuclar


#müşterileri bakiyelerine ve işlem sayılarına göre düşük-orta-yüksek segmentliyor.
def davranis_segmentasyonu(df):

    df=df.copy()

    df["segment"]="Orta"

    islem_medyan=df["islem_sayisi"].median()
    bakiye_medyan=df["bakiye"].median()

    df.loc[
        (df["bakiye"]>=bakiye_medyan)&
        (df["islem_sayisi"]>=islem_medyan),
        "segment"
    ]="Yüksek"
    df.loc[
        (df["bakiye"]<bakiye_medyan)&
        (df["islem_sayisi"]<islem_medyan),
        "segment"
    ]="Düşük"

    return df


#her kolon için kişisel veri, gizlilik, erişim, kalite gereksinimi ve iş kuralı tablosu oluşturuyor.
def veri_yönetisimi(df):
     kisisel_veri_kolonlari=[
         "ad",
         "soyisim",
         "tc_kimlik_no",
         "dogum_tarihi",
         "telefon",
         "email",
         "adres",
         "bakiye",
         "islem_sayisi",
         "son_islem_tarihi"
     ]

     gizlilik_seviyeleri={
        "tc_kimlik_no":"çok yüksek",
        "dogum_tarihi":"yüksek",
        "telefon":"yüksek",
        "email":"yüksek",
        "adres":"yüksek",
        "ad":"orta",
        "soyisim":"orta",
        "bakiye":"çok yüksek",
        "islem_tarihi":"yüksek"
    }

     # Kalite gereksinimleri: alanın teknik olarak doğru, eksiksiz ve
     # standart biçimde tutulması için gereken kontrollerdir.
     kalite_gereksinimleri={
        "customer_id":"Tekil olmalıdır",
        "tc_kimlik_no":"11 haneli olmalı; boşluk ve özel karakter içermemeli",
        "dogum_tarihi":"Geçerli tarih formatında olmalı",
        "telefon":"Geçerli telefon formatında olmalı",
        "email":"Geçerli e-posta formatında olmalı",
        "adres":"Boş olmamalı ve metin olarak kaydedilmeli",
        "ad":"Metin olmalı ve boş olmamalı",
        "soyisim":"Metin olmalı ve boş olmamalı",
        "sehir":"Standart şehir adlarından biri olmalı",
        "meslek":"Tanımlı meslek kategorilerinden biri olmalı",
        "hesap_turu":"Tanımlı hesap türlerinden biri olmalı",
        "yas":"18 ile 90 arasında sayısal bir değer olmalı",
        "aylik_gelir":"Sayısal ve sıfırdan büyük ya da eşit olmalı",
        "bakiye":"Sayısal ve sıfırdan büyük ya da eşit olmalı",
        "islem_sayisi":"Tam sayı ve sıfırdan büyük ya da eşit olmalı",
        "toplam_islem_tutari":"Sayısal ve sıfırdan büyük ya da eşit olmalı",
        "son_islem_tarihi":"Geçerli tarih formatında olmalı",
        "kayit_tarihi":"Geçerli tarih formatında olmalı",
        "ay":"YYYY-AA dönem biçiminde olmalı"
    }

     # İş kuralları: alanın kurumun işleyişi ve karar süreçleri açısından
     # nasıl kullanılacağını belirleyen kurallardır.
     is_kurallari={
        "customer_id":"Her müşteri için tekil kimlik kullanılmalı",
        "tc_kimlik_no":"Aynı kimlik numarasıyla birden fazla müşteri kaydı açılmamalı",
        "dogum_tarihi":"Gelecek tarih olamaz; müşteri yaş politikasıyla uyumlu olmalı",
        "telefon":"Müşteri iletişimi için güncel ve doğrulanmış olmalı",
        "email":"İletişim izni bulunan müşterilerde güncel e-posta bulunmalı",
        "adres":"Müşteriyle iletişim için güncel ikamet adresi tutulmalı",
        "ad":"Müşteri işlemlerinde resmi ad bilgisi kullanılmalı",
        "soyisim":"Müşteri işlemlerinde resmi soyad bilgisi kullanılmalı",
        "sehir":"Müşterinin güncel adresiyle tutarlı olmalı",
        "meslek":"Müşteri profili ve ürün değerlendirmesinde güncel olmalı",
        "hesap_turu":"Müşterinin aktif ürün ilişkisini doğru yansıtmalı",
        "yas":"Yasal ürün ve hesap kullanım koşullarıyla uyumlu olmalı",
        "aylik_gelir":"Finansal uygunluk değerlendirmesinde güncel gelir kullanılmalı",
        "bakiye":"Hesap bakiyesi ilgili dönem sonu durumunu yansıtmalı",
        "islem_sayisi":"İşlem yoğunluğu müşteri aktivitesiyle tutarlı olmalı",
        "toplam_islem_tutari":"İşlem tutarı müşteri hareketleriyle tutarlı olmalı",
        "son_islem_tarihi":"Gelecek tarih olamaz; pasif müşteri sınıflamasında kullanılmalı",
        "kayit_tarihi":"Müşteri kaydı, gerçekleşen işlemlerden sonra olamaz",
        "veri_guncelleme_tarihi":"Güncel tarih olmalıdır",
        "ay":"Her müşteri için ilgili dönemde tek kayıt bulunmalı"
    }

     yönetisim=[]

     for kolon in df.columns:

        if kolon in kisisel_veri_kolonlari:
            kisisel_veri="Evet"
            gizlilik=gizlilik_seviyeleri.get(
                kolon,
                "Yüksek"
            )
            erisim="Kısıtlı"
        else:

            kisisel_veri="Hayır"
            gizlilik="Düşük"
            erisim="İç Kullanım"

        kalite=kalite_gereksinimleri.get(
            kolon,
            "Eksik değer ve veri tipi kontrol edilmeli"
        )

        is_kurali=is_kurallari.get(
            kolon,
            "İş kuralı tanımlanmalı"
        )

        yönetisim.append({
            "Kolon":kolon,
            "Kişisel Veri":kisisel_veri,
            "Gizlilik Seviyesi":gizlilik,
            "Erişim Seviyesi":erisim,
            "Kalite Gereksinimleri":kalite,
            "İş Kuralları":is_kurali
        })

     return pd.DataFrame(yönetisim)



#aylara göre işlem sayısı ve toplam işlem tutarının değişimini görebilmek için
def trend_analizi(df):
    df=df.copy()

    df["son_islem_tarihi"]=pd.to_datetime(
        df["son_islem_tarihi"],
        errors="coerce"
    )

    df=df.dropna(subset=["son_islem_tarihi"])

    # Gelecek tarihleri çıkar
    bugun = pd.Timestamp.today().normalize()

    df = df[df["son_islem_tarihi"] <= bugun]

    # Ay bilgisi oluştur
    df["ay"] = df["son_islem_tarihi"].dt.to_period("M").astype(str)

    # Aylık trend hesapla
    trend = df.groupby("ay").agg(
        islem_sayisi=("islem_sayisi", "sum"),
        toplam_islem_tutari=("toplam_islem_tutari", "sum")
    ).reset_index()

    return trend



#müşteri veri seti genel olarak düzgün mü, her müşterinin 12 ayı var mı, eksik/duplicate/negatif kayıt var mı, kredi mantığı bozulmuş mu, meslek dağılımı nasıl, gelir-harcama ortalamaları ne.
def musteri_verisi_kontrol(df):
    print("\n")
    print("=" * 50)
    print("MÜŞTERİ VERİ SETİ KONTROLÜ")
    print("=" * 50)

    # 1. Satır ve kolon sayısı
    print("\n1. VERİ SETİ BOYUTU")
    print("Toplam kayıt:", len(df))
    print("Toplam kolon:", len(df.columns))

    # 2. Benzersiz müşteri sayısı
    print("\n2. MÜŞTERİ KONTROLÜ")
    benzersiz_musteri = df["customer_id"].nunique()
    print("Benzersiz müşteri sayısı:", benzersiz_musteri)

    # 3. Her müşterinin kaç ayı var?
    ay_sayilari = df.groupby("customer_id")["ay"].nunique()

    print("\n3. AY KONTROLÜ")
    print("Müşteri başına beklenen ay sayısı: 12")
    print("12 ayı olan müşteri sayısı:",
          int((ay_sayilari == 12).sum()))
    print("12 aydan farklı kaydı olan müşteri sayısı:",
          int((ay_sayilari != 12).sum()))

    # 4. Eksik değer kontrolü
    print("\n4. EKSİK DEĞER KONTROLÜ")
    eksik = df.isna().sum()

    if eksik.sum() == 0:
        print("Eksik değer bulunmamaktadır.")
    else:
        print(eksik[eksik > 0])

    # 5. Duplicate kontrolü
    print("\n5. DUPLICATE KONTROLÜ")
    duplicate = df.duplicated().sum()
    print("Duplicate kayıt sayısı:", duplicate)

    # 6. Negatif değer kontrolü
    finansal_kolonlar = [
        "aylik_gelir",
        "aylik_harcama",
        "vadeli_bakiye",
        "vadesiz_bakiye",
        "kredi_limiti",
        "kullanilan_kredi",
        "kalan_kredi_borcu",
        "toplam_islem_tutari"
    ]

    print("\n6. NEGATİF DEĞER KONTROLÜ")

    for kolon in finansal_kolonlar:
        negatif = (df[kolon] < 0).sum()
        print(f"{kolon}: {negatif}")

    # 7. Kredi limiti kontrolü
    print("\n7. KREDİ LİMİTİ KONTROLÜ")

    limit_asimi = (
        df["kullanilan_kredi"] > df["kredi_limiti"]
    ).sum()

    print(
        "Kredi limitini aşan kayıt sayısı:",
        limit_asimi
    )

    # 8. Kalan borç kontrolü
    print("\n8. KREDİ BORCU KONTROLÜ")

    borc_asimi = (
        df["kalan_kredi_borcu"] > df["kullanilan_kredi"]
    ).sum()

    print(
        "Kullanılan krediden fazla kalan borç:",
        borc_asimi
    )

    # 9. Meslek dağılımı
    print("\n9. MESLEK DAĞILIMI")

    meslek_dagilimi = (
        df[["customer_id", "meslek"]]
        .drop_duplicates()["meslek"]
        .value_counts()
    )

    print(meslek_dagilimi)

    # 10. Gelir ve harcama özeti
    print("\n10. GELİR - HARCAMA ÖZETİ")

    print(
        "Ortalama aylık gelir:",
        round(df["aylik_gelir"].mean(), 2)
    )

    print(
        "Ortalama aylık harcama:",
        round(df["aylik_harcama"].mean(), 2)
    )

    # 11. Sonuç
    print("\n")
    print("=" * 50)
    print("KONTROL TAMAMLANDI")
    print("=" * 50)

#müşterilerin spesifik olarak her biri hakkında tek bir satrda bilgi vermesi için.
def musteri_ozet_tablosu(df):

    musteri_ozet = df.groupby(
        ["customer_id", "meslek", "yas"]
    ).agg(
        ortalama_aylik_gelir=("aylik_gelir", "mean"),
        ortalama_aylik_harcama=("aylik_harcama", "mean"),
        ortalama_vadeli_bakiye=("vadeli_bakiye", "mean"),
        ortalama_vadesiz_bakiye=("vadesiz_bakiye", "mean"),
        ortalama_kredi_limiti=("kredi_limiti", "mean"),
        ortalama_kullanilan_kredi=("kullanilan_kredi", "mean"),
        ortalama_kalan_kredi_borcu=("kalan_kredi_borcu", "mean"),
        toplam_islem_sayisi=("islem_sayisi", "sum"),
        toplam_islem_tutari=("toplam_islem_tutari", "sum")
    ).reset_index()

    #aylık tasarruf
    musteri_ozet["aylik_tasarruf"]=(
        musteri_ozet["ortalama_aylik_gelir"]
        -musteri_ozet["ortalama_aylik_harcama"]
    )

    #tasarruf oranı
    musteri_ozet["tasarruf_orani"]=(
        musteri_ozet["aylik_tasarruf"]
        /musteri_ozet["ortalama_aylik_gelir"]
        *100
    )

    return musteri_ozet


#mesleklere göre gruplayarak meslek bazında istatistikleri görebilmek için.
def meslek_analizi(musteri_ozet):

    meslek_ozet = musteri_ozet.groupby("meslek").agg(
        ortalama_gelir=("ortalama_aylik_gelir", "mean"),
        ortalama_harcama=("ortalama_aylik_harcama", "mean"),
        ortalama_tasarruf=("aylik_tasarruf", "mean"),
        ortalama_tasarruf_orani=("tasarruf_orani", "mean"),
        ortalama_vadeli_bakiye=("ortalama_vadeli_bakiye", "mean"),
        ortalama_vadesiz_bakiye=("ortalama_vadesiz_bakiye", "mean"),
        ortalama_kredi_limiti=("ortalama_kredi_limiti", "mean"),
        ortalama_kullanilan_kredi=("ortalama_kullanilan_kredi", "mean"),
        ortalama_kredi_borcu=("ortalama_kalan_kredi_borcu", "mean")
    ).reset_index()

    return meslek_ozet


#gene mesleklere göre spesifik analiz
def meslek_tasarruf_analizi(meslek_ozet):

    meslek_ozet = meslek_ozet.copy()

    # Aylık tasarruf
    meslek_ozet["aylik_tasarruf"] = (
        meslek_ozet["ortalama_gelir"]
        - meslek_ozet["ortalama_harcama"]
    )

    # Tasarruf oranı
    meslek_ozet["tasarruf_orani"] = (
        meslek_ozet["aylik_tasarruf"]
        / meslek_ozet["ortalama_gelir"]
    ) * 100

    return meslek_ozet



def meslek_kredi_analizi(meslek_ozet):

    meslek_ozet=meslek_ozet.copy()

    meslek_ozet["kredi_kullanim_orani"]=(
        meslek_ozet["ortalama_kullanilan_kredi"]
        /meslek_ozet["ortalama_kredi_limiti"]
    )*100

    return meslek_ozet


def finansal_musteri_segmentasyonu(musteri_ozet):

    musteri_ozet = musteri_ozet.copy()

    # Kredi kullanım oranını oluştur
    if "kredi_kullanim_orani" not in musteri_ozet.columns:

        if (
            "kullanilan_kredi" in musteri_ozet.columns
            and "kredi_limiti" in musteri_ozet.columns
        ):

            musteri_ozet["kredi_kullanim_orani"] = (
                musteri_ozet["kullanilan_kredi"]
                / musteri_ozet["kredi_limiti"]
            ) * 100

        elif (
            "ortalama_kullanilan_kredi" in musteri_ozet.columns
            and "ortalama_kredi_limiti" in musteri_ozet.columns
        ):

            musteri_ozet["kredi_kullanim_orani"] = (
                musteri_ozet["ortalama_kullanilan_kredi"]
                / musteri_ozet["ortalama_kredi_limiti"]
            ) * 100

        else:
            raise ValueError(
                "Kredi kullanım oranı hesaplanamadı. "
                "Gerekli kredi kolonları bulunamadı."
            )

    # Müşteri segmentini belirle
    def segment_belirle(satir):

        if satir["kredi_kullanim_orani"] >= 20:
            return "Kredi odaklı"

        elif satir["tasarruf_orani"] >= 50:
            return "Finansal güçlü"

        elif satir["tasarruf_orani"] < 30:
            return "Yüksek harcama"

        else:
            return "Dengeli"

    musteri_ozet["segment"] = musteri_ozet.apply(
        segment_belirle,
        axis=1
    )

    return musteri_ozet


#
def segment_karar_destek(musteri_segmentli):

    karar_df = musteri_segmentli.copy()

    def karar_belirle(segment):

        if segment == "Finansal güçlü":
            return pd.Series([
                "Fırsat",
                "Finansal ürünlerin değerlendirilmesi ve müşteri ilişkisinin geliştirilmesi"
            ])

        elif segment == "Kredi odaklı":
            return pd.Series([
                "İzleme",
                "Kredi kullanımı ve borçluluk durumunun yakından takip edilmesi"
            ])

        elif segment == "Yüksek harcama":
            return pd.Series([
                "İzleme",
                "Harcama davranışının ve tasarruf potansiyelinin takip edilmesi"
            ])

        else:
            return pd.Series([
                "Dengeli",
                "Mevcut müşteri ilişkisinin korunması ve uygun ürünlerin değerlendirilmesi"
            ])

    karar_df[["risk_firsat", "onerilen_aksiyon"]] = (
        karar_df["segment"].apply(karar_belirle)
    )

    return karar_df


def karar_destek_gelistir(karar_df):

    karar_df=karar_df.copy()

    gerekce=[]

    for _, row in karar_df.iterrows():

        segment=row["segment"]
        tasarruf=row["tasarruf_orani"]
        kredi=row["kredi_kullanim_orani"]

        #yüksek risk/yüksek öncelik
        if kredi >=30:
            gerekce.append(
                "kredi kullanım oranı yüksek olduğu için finansal durum yakından incelenmelidir."
            )

        #orta risk
        elif kredi >= 20:
            gerekce.append(
                "kredi kullanım oranı orta seviyede olduğu için müşreti izlenmelidir."
            )

        #finansal fırsat
        elif segment== "Finansal güçlü" and tasarruf >= 50:
            gerekce.append(
                "yüksek tasarruf oranı ve güçlü finansal yapı nedeniyle ürün fırsatı değerlendirilebilir. "
            )

        #yüksek harcama
        elif segment== "Yüksek harcama":
            gerekce.append(
                "harcama davranışı nedeniyle müşteri davranışı incelenmelidir."
            )

        #normal müşteri
        else:
            gerekce.append(
                "belirgin bir risk veya fırsat göstergesi bulunmamaktadır."
            )

    karar_df["karar_gerekcesi"]=gerekce

    return karar_df
       


if __name__=="__main__":
    # Excel dosyasını okuyoruz
    df = pd.read_excel("sample_data/test_data.xlsx")

    # Fonksiyonu çalıştırıyoruz
    sonuclar = analiz_et(df)

    musteri_df=pd.read_excel("1000_musteri_12_ay_finansal_veri_seti.xlsx")
    musteri_verisi_kontrol(musteri_df)

    musteri_ozet = musteri_ozet_tablosu(musteri_df)

    musteri_segmentli=finansal_musteri_segmentasyonu(musteri_ozet)


    print("\n")
    print("=" * 50)
    print("MÜŞTERİ ÖZET TABLOSU")
    print("=" * 50)

    print(musteri_ozet.head(10))



    meslek_ozet=meslek_analizi(musteri_ozet)

    print("/n")
    print("="*50)
    print("MESLEK BAZLI FİNANSAL ANALİZ")
    print("="*50)

    print(meslek_ozet)



    meslek_tasarruf = meslek_tasarruf_analizi(meslek_ozet)

    print("\n")
    print("=" * 50)
    print("MESLEK BAZLI TASARRUF ANALİZİ")
    print("=" * 50)

    print(
        meslek_tasarruf[
            [
                "meslek",
                "ortalama_gelir",
                "ortalama_harcama",
                "aylik_tasarruf",
                "tasarruf_orani"
            ]
        ]
    )



    meslek_kredi = meslek_kredi_analizi(meslek_ozet)

    print("\n")
    print("=" * 50)
    print("MESLEK BAZLI KREDİ ANALİZİ")
    print("=" * 50)

    print(
        meslek_kredi[
            [
                "meslek",
                "ortalama_kredi_limiti",
                "ortalama_kullanilan_kredi",
                "ortalama_kredi_borcu",
                "kredi_kullanim_orani"
            ]
        ]
    )

    print("\n")
    print("=" * 50)
    print("MÜŞTERİ SEGMENTASYONU")
    print("=" * 50)

    print(
        musteri_segmentli[
            [
                "customer_id",
                "meslek",
                "tasarruf_orani",
                "kredi_kullanim_orani",
                "segment"
            ]
        ].head(10)
    )

    karar_destek = segment_karar_destek(musteri_segmentli)

    karar_destek=karar_destek_gelistir(karar_destek)

    print("\n")
    print("=" * 50)
    print("KARAR DESTEK ANALİZİ")
    print("=" * 50)

    print(
        karar_destek[
            [
                "customer_id",
                "meslek",
                "segment",
                "tasarruf_orani",
                "kredi_kullanim_orani",
                "risk_firsat",
                "onerilen_aksiyon",
                "karar_gerekcesi"
            ]
        ].head(10)
    )



    print("\nSONUÇLAR")
    print(sonuclar)


    print("\n" + "=" * 50)
    print("SEGMENT BAZLI FİNANSAL ANALİZ")
    print("=" * 50)

    # Segment bilgisini müşteri özet tablosuna ekliyoruz
    musteri_ozet = musteri_ozet.merge(
        musteri_segmentli[["customer_id", "segment"]],
        on="customer_id",
        how="left"
    )


    segment_analizi = musteri_segmentli.groupby("segment").agg(
        musteri_sayisi=("customer_id", "count"),
        ortalama_gelir=("ortalama_aylik_gelir", "mean"),
        ortalama_harcama=("ortalama_aylik_harcama", "mean"),
        ortalama_tasarruf=("aylik_tasarruf", "mean"),
        ortalama_tasarruf_orani=("tasarruf_orani", "mean"),
        ortalama_kredi_limiti=("ortalama_kredi_limiti", "mean"),
        ortalama_kullanilan_kredi=("ortalama_kullanilan_kredi", "mean"),
        ortalama_kredi_kullanim_orani=("kredi_kullanim_orani", "mean")
    ).reset_index()

    print(segment_analizi)




def ai_ozet_hazirla(yönetisim_df):

    ozet = []

    # 1. Çok yüksek gizlilik seviyesindeki kolonlar
    cok_yuksek = yönetisim_df[
        yönetisim_df["Gizlilik Seviyesi"].str.lower() == "çok yüksek"
    ]

    if len(cok_yuksek) > 0:
        ozet.append("KRİTİK GİZLİLİK RİSKLERİ:")

        for _, satir in cok_yuksek.iterrows():
            ozet.append(
                f"- {satir['Kolon']} kolonu çok yüksek gizlilik seviyesindedir. "
                f"Erişimi kısıtlı tutulmalıdır."
            )

    # 2. Yüksek gizlilik seviyesindeki kolonlar
    yuksek = yönetisim_df[
        yönetisim_df["Gizlilik Seviyesi"].str.lower() == "yüksek"
    ]

    if len(yuksek) > 0:
        ozet.append("\nYÜKSEK GİZLİLİK SEVİYESİNE SAHİP KOLONLAR:")

        for _, satir in yuksek.iterrows():
            ozet.append(
                f"- {satir['Kolon']} kolonu yüksek gizlilik seviyesindedir."
            )

    # 3. Kişisel veriler
    kisisel = yönetisim_df[
        yönetisim_df["Kişisel Veri"].str.lower() == "evet"
    ]

    ozet.append(
        f"\nKİŞİSEL VERİ DURUMU: "
        f"{len(kisisel)} kolon kişisel veri içermektedir."
    )

    # 4. Kalite gereksinimleri
    ozet.append("\nVERİ KALİTESİ DEĞERLENDİRMESİ:")

    for _, satir in yönetisim_df.iterrows():

        kalite = satir["Kalite Gereksinimleri"]

        if pd.notna(kalite):
            ozet.append(
                f"- {satir['Kolon']}: {kalite}"
            )

    # 5. İş kuralları
    ozet.append("\nİŞ KURALLARI DEĞERLENDİRMESİ:")

    for _, satir in yönetisim_df.iterrows():

        is_kurali = satir["İş Kuralları"]

        if pd.notna(is_kurali):
            ozet.append(
                f"- {satir['Kolon']}: {is_kurali}"
            )

    # 6. Genel değerlendirme
    ozet.append("\nGENEL DEĞERLENDİRME:")

    ozet.append(
        f"- Toplam {len(yönetisim_df)} kolon incelenmiştir."
    )

    ozet.append(
        f"- {len(kisisel)} kolon kişisel veri olarak değerlendirilmiştir."
    )

    ozet.append(
        f"- {len(cok_yuksek)} kolon çok yüksek gizlilik seviyesindedir."
    )

    return "\n".join(ozet)

def risk_degerlendir(yönetisim_df):

    yönetisim_df.columns=yönetisim_df.columns.str.strip()

    print("RİSK FONKSİYONU SÜTUNLARI:", yönetisim_df.columns.tolist())

    riskler = []

    for _, satir in yönetisim_df.iterrows():

        gizlilik = str(satir.get("Gizlilik Seviyesi", "")).lower()

        if gizlilik == "çok yüksek":
            risk = "Kritik"
        elif gizlilik == "yüksek":
            risk = "Yüksek"
        elif gizlilik == "orta":
            risk = "Orta"
        else:
            risk = "Düşük"

        riskler.append(risk)

    yönetisim_df = yönetisim_df.copy()
    yönetisim_df["Risk Seviyesi"] = riskler

    return yönetisim_df



def aksiyon_oner(yönetisim_df):

    aksiyonlar = []

    # Her alan için, sorun tespit edildiği iddia edilmeyen koruyucu kontroller.
    kolon_kontrolleri = {
        "customer_id": "Müşteri ID’lerinin tekilliği ve boş olup olmadığı periyodik olarak kontrol edilmelidir.",
        "ad": "Ad alanlarında boş değer kontrolü yapılmalı; gerektiğinde resmi müşteri kaynağıyla doğrulanmalıdır.",
        "soyisim": "Soyisim alanlarında boş değer kontrolü yapılmalı; gerektiğinde resmi müşteri kaynağıyla doğrulanmalıdır.",
        "tc_kimlik_no": "TC kimlik numaraları maskelenmeli, erişim yetkili kullanıcılarla sınırlandırılmalı ve benzersizlik kontrolü uygulanmalıdır.",
        "dogum_tarihi": "Tarih formatı, gelecek tarih ve yaş aralığı kontrolleri uygulanmalıdır.",
        "telefon": "Telefon numaralarının biçimi ve güncelliği periyodik olarak doğrulanmalıdır.",
        "email": "E-posta formatı, iletişim izni ve güncellik kontrolleri uygulanmalıdır.",
        "adres": "Adres alanlarının eksiksizliği ve güncelliği düzenli olarak kontrol edilmelidir.",
        "sehir": "Şehir adları standart bir referans listesiyle eşleştirilmelidir.",
        "meslek": "Meslek bilgileri tanımlı kategoriler üzerinden standartlaştırılmalıdır.",
        "hesap_turu": "Hesap türü bilgisi müşterinin aktif ürün bilgileriyle periyodik olarak karşılaştırılmalıdır.",
        "yas": "Yaş değerlerinin tanımlı aralıkta olup olmadığı kontrol edilmelidir.",
        "aylik_gelir": "Negatif veya sıra dışı gelir değerleri kaynak kayıtlarla doğrulanmalıdır.",
        "bakiye": "Negatif bakiye ve bakiye anomalileri için düzenli kontrol uygulanmalıdır.",
        "islem_sayisi": "Negatif veya olağandışı işlem sayıları kaynak sistemle doğrulanmalıdır.",
        "toplam_islem_tutari": "Negatif veya sıra dışı işlem tutarları kaynak sistemle mutabıklaştırılmalıdır.",
        "son_islem_tarihi": "Gelecek tarih kontrolü yapılmalı; pasif müşteri sınıflaması için son işlem tarihi izlenmelidir.",
        "kayit_tarihi": "Kayıt tarihinin geçerli ve gelecekte olmayan bir tarih olduğu kontrol edilmelidir.",
        "veri_guncelleme_tarihi": "Verinin güncelliği için son güncelleme tarihi periyodik olarak izlenmelidir.",
        "ay": "Her müşteri-dönem için tekil kayıt kontrolü uygulanmalıdır."
    }

    for _, satir in yönetisim_df.iterrows():

        risk = str(satir["Risk Seviyesi"]).lower()
        kolon = satir["Kolon"]
        oneri = kolon_kontrolleri.get(kolon)

        if oneri is None:
            if risk == "kritik":
                oneri = "Erişim kısıtı ve düzenli veri güvenliği kontrolü uygulanmalıdır."
            elif risk == "yüksek":
                oneri = "Düzenli kalite kontrolü ve erişim denetimi uygulanmalıdır."
            elif risk == "orta":
                oneri = "Periyodik kalite kontrolü ve veri sorumlusu takibi uygulanmalıdır."
            else:
                oneri = "Standart kalite kontrol planına dahil edilmelidir."

        aksiyonlar.append({
            "Kolon": kolon,
            "Risk Seviyesi": satir["Risk Seviyesi"],
            "Önerilen Kontroller": oneri
        })

    return pd.DataFrame(aksiyonlar)



def donem_karsilastir(eski_df, yeni_df):

    eski_sonuclar = analiz_et(eski_df)
    yeni_sonuclar = analiz_et(yeni_df)

    # Eski dönem veri kalitesi skoru
    eski_kalite_skoru = max(
        0,
        100 - (
            eski_sonuclar["eksik_deger_sayisi"]
            + eski_sonuclar["duplicate_sayisi"]
            + eski_sonuclar["anomali_sayisi"]
        ) / len(eski_df) * 100
    ) if len(eski_df) > 0 else 0

    # Yeni dönem veri kalitesi skoru
    yeni_kalite_skoru = max(
        0,
        100 - (
            yeni_sonuclar["eksik_deger_sayisi"]
            + yeni_sonuclar["duplicate_sayisi"]
            + yeni_sonuclar["anomali_sayisi"]
        ) / len(yeni_df) * 100
    ) if len(yeni_df) > 0 else 0

    # Karşılaştırma tablosu
    karsilastirma = pd.DataFrame({
        "Gösterge": [
            "Eksik Değer",
            "Duplicate",
            "Anomali",
            "Pasif Müşteri",
            "Veri Kalitesi Skoru"
        ],

        "Eski Dönem": [
            eski_sonuclar["eksik_deger_sayisi"],
            eski_sonuclar["duplicate_sayisi"],
            eski_sonuclar["anomali_sayisi"],
            eski_sonuclar["pasif_musteri_sayisi"],
            round(eski_kalite_skoru, 2)
        ],

        "Yeni Dönem": [
            yeni_sonuclar["eksik_deger_sayisi"],
            yeni_sonuclar["duplicate_sayisi"],
            yeni_sonuclar["anomali_sayisi"],
            yeni_sonuclar["pasif_musteri_sayisi"],
            round(yeni_kalite_skoru, 2)
        ]
    })

    # İyi yöndeki değişimler pozitif, kötü yöndeki değişimler negatif gösterilir.
    # Veri kalitesi skorunda artış; diğer sorun göstergelerinde azalış iyileşmedir.
    ham_değişim = karsilastirma["Yeni Dönem"] - karsilastirma["Eski Dönem"]
    yön = karsilastirma["Gösterge"].apply(
        lambda gösterge: 1 if gösterge == "Veri Kalitesi Skoru" else -1
    )
    karsilastirma["İyileşme Miktarı"] = ham_değişim * yön

    karsilastirma["İyileşme %"] = (
        karsilastirma["İyileşme Miktarı"]
        / karsilastirma["Eski Dönem"].abs()
        * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0).round(2)

    def yorumla(satir):

        gösterge = satir["Gösterge"]
        değişim = satir["İyileşme Miktarı"]

        if değişim == 0:
            return "Değişim yok"

        if değişim > 0:
            return "İyileşme"
        else:
            return "Kötüleşme"

    karsilastirma["Yorum"] = karsilastirma.apply(
        yorumla,
        axis=1
    )



    return karsilastirma


def donemsel_trend_analizi(donemler):
    
    trend_sonuclari = []

    for donem_adi, df in donemler.items():

        sonuclar = analiz_et(df)

        toplam_kayit = len(df)

        toplam_sorun = (
            sonuclar["eksik_deger_sayisi"]
            + sonuclar["duplicate_sayisi"]
            + sonuclar["anomali_sayisi"]
        )

        if toplam_kayit > 0:
            kalite_skoru = max(
                0,
                100 - (toplam_sorun / toplam_kayit * 100)
            )
        else:
            kalite_skoru = 0

        trend_sonuclari.append({
            "Dönem": donem_adi,
            "Eksik Değer": sonuclar["eksik_deger_sayisi"],
            "Duplicate": sonuclar["duplicate_sayisi"],
            "Anomali": sonuclar["anomali_sayisi"],
            "Pasif Müşteri": sonuclar["pasif_musteri_sayisi"],
            "Veri Kalitesi Skoru": round(kalite_skoru, 2)
        })

    return pd.DataFrame(trend_sonuclari)



def ai_analiz_verisi_olustur(df, sonuclar, yönetisim_df, trend, segmentli_df):
    
    # Genel veri kalitesi
    eksik = sonuclar["eksik_deger_sayisi"]
    duplicate = sonuclar["duplicate_sayisi"]
    anomali = sonuclar["anomali_sayisi"]
    pasif = sonuclar["pasif_musteri_sayisi"]

    toplam_kayit = len(df)
    tekil_musteri = df["customer_id"].nunique()

    toplam_sorun = eksik + duplicate + anomali

    if toplam_kayit > 0:
        kalite_skoru = max(
            0,
            100 - (toplam_sorun / toplam_kayit * 100)
        )
    else:
        kalite_skoru = 0

    # Risk bilgileri
    risk_sayilari = (
        yönetisim_df["Risk Seviyesi"]
        .value_counts()
        .to_dict()
    )

    # Gizlilik bilgileri
    gizlilik_sayilari = (
        yönetisim_df["Gizlilik Seviyesi"]
        .value_counts()
        .to_dict()
    )

    # Kişisel veri bilgisi
    kisisel_veri_sayilari = (
        yönetisim_df["Kişisel Veri"]
        .value_counts()
        .to_dict()
    )

    # Müşteri segmentleri
    segment_sayilari = (
        segmentli_df["segment"]
        .value_counts()
        .to_dict()
    )

    # Trend bilgileri
    trend_bilgileri = trend.to_dict(orient="records")

    # AI'a gönderilecek özet veri
    ai_verisi = {
        "genel": {
            "toplam_kayit": toplam_kayit,
            "tekil_musteri": tekil_musteri,
            "aktif_musteri": tekil_musteri - pasif,
            "pasif_musteri": pasif,
            "veri_kalitesi_skoru": round(kalite_skoru, 2)
        },

        "veri_kalitesi": {
            "eksik_deger": eksik,
            "duplicate": duplicate,
            "anomali": anomali
        },

        "riskler": risk_sayilari,

        "gizlilik": gizlilik_sayilari,

        "kisisel_veri": kisisel_veri_sayilari,

        "musteri_segmentleri": segment_sayilari,

        "trend": trend_bilgileri
    }

    return ai_verisi


def ai_finansal_analiz_verisi_olustur(finansal_df):
    """Finansal dosyadan AI'a gönderilecek anonim ve toplulaştırılmış özeti üretir."""
    musteri_ozet = musteri_ozet_tablosu(finansal_df)
    segmentli_df = finansal_musteri_segmentasyonu(musteri_ozet)

    meslek_ozeti = (
        segmentli_df.groupby("meslek")
        .agg(
            musteri_sayisi=("customer_id", "nunique"),
            ortalama_gelir=("ortalama_aylik_gelir", "mean"),
            ortalama_harcama=("ortalama_aylik_harcama", "mean"),
            ortalama_tasarruf_orani=("tasarruf_orani", "mean"),
            ortalama_kredi_kullanim_orani=("kredi_kullanim_orani", "mean"),
        )
        .round(2)
        .reset_index()
    )

    kapsanan_ay = (
        int(finansal_df["ay"].nunique())
        if "ay" in finansal_df.columns
        else None
    )

    return {
        "genel": {
            "aylik_kayit": int(len(finansal_df)),
            "tekil_musteri": int(finansal_df["customer_id"].nunique()),
            "kapsanan_ay": kapsanan_ay,
            "ortalama_tasarruf_orani": round(float(segmentli_df["tasarruf_orani"].mean()), 2),
            "ortalama_kredi_kullanim_orani": round(
                float(segmentli_df["kredi_kullanim_orani"].mean()), 2
            ),
        },
        "finansal_segmentler": segmentli_df["segment"].value_counts().to_dict(),
        "meslek_bazli_ozet": meslek_ozeti.to_dict(orient="records"),
    }


def ai_donemsel_analiz_verisi_olustur(donemler):
    """Yüklenen herhangi bir dönem dosyası grubu için anonim analiz özeti üretir."""
    donem_trendi = donemsel_trend_analizi(donemler)

    ozet = {
        "yuklenen_donem_sayisi": int(len(donemler)),
        "donemsel_sonuclar": donem_trendi.to_dict(orient="records"),
    }

    if len(donemler) >= 2:
        adlar = list(donemler)
        karsilastirma = donem_karsilastir(
            donemler[adlar[-2]], donemler[adlar[-1]]
        )
        ozet["son_iki_donem_karsilastirmasi"] = {
            "eski_donem": adlar[-2],
            "yeni_donem": adlar[-1],
            "bulgular": karsilastirma.to_dict(orient="records"),
        }

    return ozet


