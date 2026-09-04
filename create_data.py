import pandas as pd
import numpy as np
n=10000
customer_id=np.arange(1, n+1)
isimler = ["Ahmet", "Ayşe", "Mehmet", "Zeynep", "Elif", "Emre", "Merve", "Can", "Buse", "Burak", "Beyza", "Deniz", "Dilara", "Emre", "Fatih"]
soyisimler = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Aydın", "Öztürk", "Arslan", "Doğan", "Kurt", "Yaşar", "Bulut"]
sehirler = ["Ankara", "İstanbul", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Samsun"]
meslekler = ["Mühendis", "Öğretmen", "Doktor", "Avukat", "Memur", "Öğrenci", "Muhasebeci", "Teknisyen", "Bankacı", "Esnaf", "Yazar", "Psikolog"]
hesap_turleri = ["Vadesiz", "Vadeli", "Kredi"]

isim=np.random.choice(isimler, size=n)
soyisim=np.random.choice(soyisimler, size=n)
sehir=np.random.choice(sehirler, size=n)
meslek=np.random.choice(meslekler, size=n)
hesap_turu=np.random.choice(hesap_turleri, size=n)

df=pd.DataFrame({
    "customer_id":customer_id,
    "ad":isim,
    "soyisim":soyisim,
    "sehir":sehir,
    "meslek":meslek,
    "hesap_turu":hesap_turu

})

yas=np.random.randint(18, 90, size=n)
aylik_gelir=np.random.randint(25000, 500000, size=n)
bakiye=np.random.uniform(0, 5000000, size=n).round(2)
islem_sayisi=np.random.randint(0, 150, size=n)
toplam_islem_tutari=np.random.uniform(0, 1000000, size=n).round(2)

dogum_tarihi = pd.to_datetime("1960-01-01") + pd.to_timedelta(
    np.random.randint(0, 17500, size=n), unit="D"
)

son_islem_tarihi = pd.to_datetime("2024-01-01") + pd.to_timedelta(
    np.random.randint(0, 950, size=n), unit="D"
)

kayit_tarihi = pd.to_datetime("2018-01-01") + pd.to_timedelta(
    np.random.randint(0, 3000, size=n), unit="D"
)

veri_guncelleme_tarihi = pd.Timestamp("2026-08-10")


telefon = [
    f"05{np.random.randint(100000000, 1000000000)}"
    for _ in range(n)
]

email = [
    f"musteri{i}@example.com"
    for i in range(1, n + 1)
]

adresler = [
    "Çankaya, Ankara",
    "Kadıköy, İstanbul",
    "Konak, İzmir",
    "Nilüfer, Bursa",
    "Muratpaşa, Antalya",
    "Seyhan, Adana",
    "Selçuklu, Konya",
    "Atakum, Samsun",

]

adres = np.random.choice(adresler, size=n)

tc_kimlik_no = [
    f"TEST{str(i).zfill(8)}"
    for i in range(1, n + 1)
]

df = pd.DataFrame({
    "customer_id": customer_id,
    "ad": isim,
    "soyisim": soyisim,
    "tc_kimlik_no": tc_kimlik_no,
    "dogum_tarihi": dogum_tarihi,
    "telefon": telefon,
    "email": email,
    "adres": adres,
    "sehir": sehir,
    "meslek": meslek,
    "hesap_turu": hesap_turu,
    "yas": yas,
    "aylik_gelir": aylik_gelir,
    "bakiye": bakiye,
    "islem_sayisi": islem_sayisi,
    "toplam_islem_tutari": toplam_islem_tutari,
    "son_islem_tarihi": son_islem_tarihi,
    "kayit_tarihi": kayit_tarihi,
    "veri_guncelleme_tarihi": veri_guncelleme_tarihi
})


print(df.head())
print(df.shape)

df.to_excel("sample_data/customer_data.xlsx", index=False)



test_df=df.copy()
test_df.loc[10:19, "email"]=None
test_df.loc[50:59, "telefon"]=None
test_df.loc[100:109, "adres"]=None

duplicate_rows=test_df.iloc[200:205].copy()

test_df=pd.concat([test_df, duplicate_rows], ignore_index=True)

test_df.loc[300:304, "yas"] = [12, 15, 95, 100, 10]

test_df.loc[400:404, "bakiye"]=[-100, -500, -1000, -2500, -50]

test_df.loc[500:504, "aylik_gelir"]=[-1000, -2500, -5000, -750, -3000]

test_df.loc[600:604, "islem_sayisi"]=[-1,-5, -10, -20, -3]

test_df.loc[700:704, "toplam_islem_tutari"]=[-100, -500, -1000, -2500, -50]

test_df.loc[800:804, "son_islem_tarihi"]=[
    "2027-01-01",
    "2027-03-15",
    "2028-05-20",
    "2027-11-10",
    "2029-01-01"
]

test_df.loc[900:904, "kayit_tarihi"] = [
    "2027-01-10",
    "2027-05-20",
    "2028-02-15",
    "2027-09-01",
    "2029-03-10"
]

test_df.loc[1000:1004, "bakiye"] = [
    15000000,
    18000000,
    25000000,
    30000000,
    50000000
]

test_df.to_excel("sample_data/test_data.xlsx", index=False)

print("Test veri setinin boyutu:", test_df.shape)

