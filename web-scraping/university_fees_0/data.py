import pandas as pd
import re

# CSV dosyasını oku
df = pd.read_csv("2020_ücret.csv")

# Gereksiz açıklamaları ve boş alanları temizle
df["Bölüm/Fakülte"] = df["Bölüm/Fakülte"].apply(lambda x: re.sub(r'Öğrenim ücret.*|öğretim ücret.*', '', str(x)).strip())

# Ücret sütununu yalnızca sayıları içerecek şekilde formatla ve "TL" ibaresini kaldır
df["Ücret"] = df["Ücret"].apply(lambda x: re.sub(r'[^\d]', '', str(x)) if pd.notna(x) else x)

# Bölüm/Fakülte sütununda "diğer lisans programları" veya benzeri ifadeleri "Tüm Programlar" olarak değiştir
df["Bölüm/Fakülte"] = df["Bölüm/Fakülte"].apply(lambda x: "Tüm Programlar" if pd.notna(x) and ("diğer lisans programları" in x.lower() or "tüm lisans programları" in x.lower()) else x)

# Düzenlenen CSV'yi kaydet
df.to_csv("universiteler_duzenli.csv", index=False)

print("Veri başarıyla düzenlendi ve 'universiteler_duzenli.csv' dosyasına kaydedildi.")
