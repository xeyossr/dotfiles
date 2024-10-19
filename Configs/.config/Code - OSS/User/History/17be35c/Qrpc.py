import requests
from bs4 import BeautifulSoup

# URL'yi belirleyin
url = 'https://www.bakuelectronics.az/catalog/noutbuklar-komputerler/noutbuklar/acer-aspire156i5-1235u16gb1tb-ssdmx550-2gbfree-dossilver.html'  # Değiştirin

# Web sayfasını çekin
response = requests.get(url)

# Eğer istek başarılıysa
if response.status_code == 200:
    # HTML içeriğini BeautifulSoup ile analiz edin
    soup = BeautifulSoup(response.content, 'html.parser')

    # product__price--cur sınıfına sahip öğeyi seçin
    price_element = soup.find(class_='product__price--cur')
    
    if price_element:
        # İçeriği al ve HTML etiketlerini kaldır
        price_text = price_element.get_text(strip=True)  # strip=True ile baştaki ve sondaki boşlukları temizler
        print(price_text)  # Sonucu yazdır

else:
    print(f"İstek başarısız oldu: {response.status_code}")
