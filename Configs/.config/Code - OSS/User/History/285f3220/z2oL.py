import argparse
import json
import os
import openai

# Ayarların saklanacağı dosya adı
SETTINGS_FILE = "settings.json"

# API anahtarını settings.json'a yazan fonksiyon
def save_api_key(api_key):
    settings = {"api_key": api_key}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    print("API Key başarıyla kaydedildi.")

# settings.json'dan API anahtarını okuyan fonksiyon
def load_api_key():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            return settings.get("api_key")
    return None

# API anahtarını doğrulamak için giriş fonksiyonu
def get_api_key():
    api_key = load_api_key()
    if not api_key:
        api_key = input("Lütfen API Key girin: ")
        save_api_key(api_key)
    return api_key

# ChatGPT API'sine istek gönderen fonksiyon
def chat_with_gpt(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Model versiyonunu buraya girin
            prompt=prompt,
            max_tokens=150,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

# Ana fonksiyon
def main():
    # Argparse kullanarak komut satırı argümanlarını ayarlıyoruz
    parser = argparse.ArgumentParser(description="Terminal üzerinden ChatGPT")
    parser.add_argument("-t", "--token", type=str, help="API anahtarı")
    args = parser.parse_args()

    # Eğer kullanıcı --token veya -t ile API key girdiyse onu settings.json'a kaydediyoruz
    if args.token:
        save_api_key(args.token)
        print("Yeni API Key ayarlandı.")
    else:
        # API anahtarını yüklüyoruz veya soruyoruz
        api_key = get_api_key()

        while True:
            prompt = input("\nChatGPT'ye sorunuz: ")
            if prompt.lower() in ["exit", "quit"]:
                print("Çıkış yapılıyor...")
                break
            response = chat_with_gpt(prompt, api_key)
            if response:
                print("\nChatGPT Cevap:\n", response)

if __name__ == "__main__":
    main()
