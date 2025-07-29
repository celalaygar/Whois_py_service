# Gerekli kütüphaneleri içe aktarıyoruz
from flask import Flask, request, jsonify
import whois # WHOIS sorguları için kütüphane

# Flask uygulamasını başlatıyoruz
app = Flask(__name__)

# WHOIS sorgusu yapan fonksiyon (kullanıcının sağladığı koddan alınmıştır)
def get_domain_info(domain):
    """
    Belirtilen domain için WHOIS bilgilerini alır.
    Domain kayıtlıysa detaylı bilgi, değilse "Boşta" durumu döner.
    Hata durumunda "Boşta veya erişim hatası" döner.
    """
    try:
        w = whois.whois(domain)
        if w.domain_name:
            # Domain kayıtlıysa detaylı bilgileri döndür
            return {
                "Durum": "Kayıtlı",
                "Domain": domain,
                "Registrar": w.registrar,
                "Oluşturulma Tarihi": str(w.creation_date), # Tarih nesnelerini string'e çeviriyoruz
                "Bitiş Tarihi": str(w.expiration_date),
                "Güncellenme Tarihi": str(w.updated_date),
                "Name Servers": w.name_servers,
                "E-posta": w.emails,
            }
        else:
            # Domain boşta ise
            return {"Durum": "Boşta", "Domain": domain}
    except Exception as e:
        # WHOIS sorgusu sırasında bir hata oluşursa
        print(f"Hata: {e}")
        return {"Durum": "Boşta veya erişim hatası", "Domain": domain}

# REST servisimiz için POST endpoint'i tanımlıyoruz
@app.route('/check_domains', methods=['POST'])
def check_domains():
    """
    POST isteği ile gelen siteName ve extensions listesini kullanarak
    domainlerin WHOIS bilgilerini kontrol eder ve JSON olarak döndürür.
    """
    # İstek gövdesini JSON olarak almaya çalışıyoruz
    data = request.get_json()

    # Gerekli alanların (siteName ve extensions) istekte olup olmadığını kontrol ediyoruz
    if not data or 'siteName' not in data or 'extensions' not in data:
        # Eksik veya hatalı istek durumunda hata mesajı döndürüyoruz
        return jsonify({"error": "Geçersiz istek gövdesi. 'siteName' ve 'extensions' alanları gereklidir."}), 400

    site_name = data['siteName']
    extensions = data['extensions']

    # Sonuçları depolamak için boş bir liste oluşturuyoruz
    results = []

    # Her bir uzantı için domain kontrolü yapıyoruz
    for ext in extensions:
        full_domain = f"{site_name}{ext}" # Tam domain adını oluşturuyoruz
        domain_info = get_domain_info(full_domain) # WHOIS sorgusunu çalıştırıyoruz
        results.append(domain_info) # Sonucu listeye ekliyoruz

    # Tüm sonuçları JSON formatında döndürüyoruz
    return jsonify(results)

# Uygulamayı sadece bu dosya doğrudan çalıştırıldığında başlatıyoruz
if __name__ == '__main__':
    # Uygulamayı hata ayıklama modunda çalıştırıyoruz (geliştirme için)
    # Gerçek bir ortamda debug=False yapmanız önerilir
    app.run(debug=True)

