import os
import requests
from PIL import Image, UnidentifiedImageError

# Klasör oluştur
os.makedirs("pages", exist_ok=True)

# Ayarlar
BASE_URL = "https://online.fliphtml5.com/tsyqb/baad/files/large/{}.webp"
START_PAGE = 1
END_PAGE = 200  # Kaç sayfa olduğunu bilmiyorsan büyük tut
downloaded_images = []

for page_num in range(START_PAGE, END_PAGE + 1):
    url = BASE_URL.format(page_num)
    response = requests.get(url)

    if response.status_code == 200:
        img_path = f"pages/page_{page_num}.webp"
        with open(img_path, "wb") as f:
            f.write(response.content)

        # Dosya gerçekten resim mi kontrol et
        try:
            with Image.open(img_path) as im:
                im.verify()  # Sadece doğrulama
            downloaded_images.append(img_path)
            print(f"✓ İndirildi: {img_path}")
        except UnidentifiedImageError:
            print(f"⛔ Geçersiz resim (bozuk veya HTML döndü): {img_path}")
            os.remove(img_path)
            break  # Dosya yoksa muhtemelen kitap bitti
    else:
        print(f"⛔ Sayfa bulunamadı: {url}")
        break

# PDF oluştur
if downloaded_images:
    pdf_images = [Image.open(img).convert("RGB") for img in downloaded_images]
    pdf_images[0].save("flipbook.pdf", save_all=True, append_images=pdf_images[1:])
    print("✅ PDF başarıyla oluşturuldu: flipbook.pdf")
else:
    print("⚠ Hiçbir görsel indirilemedi, PDF oluşturulamadı.")
