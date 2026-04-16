# gemini_chatbot
# 🤖 Gemini Multi-Interface Chatbot

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.1-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Google Gemini 2.0 Flash modelini kullanarak geliştirilmiş, hem terminal (CLI) hem de web arayüzü (Streamlit) üzerinden çalışan akıllı bir sohbet botu.

## 🌟 Öne Çıkan Özellikler

- **Çift Arayüz:** İster terminal üzerinden hızlıca mesajlaşın, ister Streamlit ile modern bir web arayüzü kullanın.
- **Akıllı Dil Algılama:** Türkçe ve İngilizce girişleri otomatik algılar ve ilgili dilde yanıt verir.
- **Geçmiş Yönetimi:** Sohbet geçmişini temizleme ve görüntüleme komutları.
- **Hafif ve Hızlı:** `gemini-2.0-flash` modeli sayesinde düşük gecikme süreli yanıtlar.

## 🛠️ Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu klonlayın:**
   ```bash
   git clone [https://github.com/kullaniciadi/gemini-chatbot.git](https://github.com/kullaniciadi/gemini-chatbot.git)
   cd gemini-chatbot
2. Sanal Ortam (Virtual Environment) Oluşturun
Proje bağımlılıklarını izole etmek için bir sanal ortam oluşturup aktifleştirin:

Windows için:

Bash
python -m venv venv
venv\Scripts\activate
macOS/Linux için:

Bash
python -m venv venv
source venv/bin/activate

3. Bağımlılıkları Yükleyin
Gerekli kütüphaneleri (google-generativeai, streamlit, python-dotenv) yüklemek için:

Bash
pip install -r requirements.txt

4. API Anahtarını Tanımlayın
Proje dizininde .env adında bir dosya oluşturun ve içine Gemini API anahtarınızı ekleyin:

Kod snippet'i
GEMINI_API_KEY=buraya_api_anahtarinizi_yazin
Proje iki farklı arayüz seçeneği sunar:

A. Web Arayüzü (Streamlit)
Modern ve kullanıcı dostu bir tarayıcı deneyimi için:

Bash
streamlit run web_app.py
B. Terminal Arayüzü (CLI)
Hızlı ve komut satırı odaklı bir deneyim için:

Bash
python main.py
Terminal Komutları:

help: Komut listesini gösterir.

clear: Sohbet geçmişini temizler.

history: Geçmiş mesajları listeler.

language tr|en|auto: Dil modunu değiştirir.

exit: Programdan çıkar.
