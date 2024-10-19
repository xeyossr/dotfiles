#!/bin/bash

while true; do
    echo "swww indirilsin mi? (Y/n)"
    read -r answer

    # Varsayılan olarak "Y" kabul ediliyor.
    if [[ -z "$answer" || "$answer" =~ ^[Yy]$ ]]; then
        echo "İndiriliyor..."
        # Buraya indirme komutunu ekle
        # break  # İndirme işlemi tamamlandıktan sonra döngüden çıkabilirsin
    elif [[ "$answer" =~ ^[Nn]$ ]]; then
        echo "İndirilmedi, bir sonraki soruya geçiliyor."
        # Burada bir sonraki soru veya işlem ekleyebilirsin
    else
        echo "Lütfen 'Y' veya 'N' yazın."
    fi

    # Burada bir sonraki soruyu sorabilirsin
    echo "Diğer bir işlem yapmak ister misiniz? (Y/n)"
    read -r next_action

    if [[ -z "$next_action" || "$next_action" =~ ^[Yy]$ ]]; then
        echo "Devam ediliyor..."
        # Yeni bir işlem ekleyebilirsin
    elif [[ "$next_action" =~ ^[Nn]$ ]]; then
        echo "Program sonlandırılıyor."
        exit 0  # Programdan çık
    else
        echo "Geçersiz giriş. Program sonlandırılıyor."
        exit 1  # Hata durumu
    fi
done
