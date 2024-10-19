#!/bin/bash

# slurp ile alanı seç ve seçilen alanı değişkene ata
selected_area=$(slurp)

# 0.3 saniye bekle
sleep 0.3

# grim ile ekran görüntüsünü kaydet
grim -g "$selected_area" - | swappy -f - -o ~/Pictures/Screenshots/$(date '+%Y-%m-%d_%H-%M-%S').png
