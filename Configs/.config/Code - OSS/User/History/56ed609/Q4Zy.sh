#!/bin/bash

echo "Swww indirilsin mi? (Y/n)"
read -r answer

# Varsayılan olarak "Y" kabul ediliyor.
if [[ -z "$answer" || "$answer" =~ ^[Yy]$ ]]; then
    echo "İndiriliyor..."
    # Buraya indirme komutunu ekle
else
    echo "İndirilmedi."
fi
