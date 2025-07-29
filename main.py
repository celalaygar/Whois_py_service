# Gerekli kütüphaneleri içe aktarıyoruz
from flask import Flask, request, jsonify
import whois # WHOIS sorguları için kütüphane

# Flask uygulamasını başlatıyoruz
app = Flask(__name__)

# WHOIS sorgusu yapan fonksiyon (kullanıcının sağladığı koddan alınmıştır)
def get_domain_info(domain):
    """
    Belirtilen domain için WHOIS bilgilerini alır.
    Domain kayıtlıysa detaylı bilgi, değilse "Available" durumu döner.
    Hata durumunda "Available or access error" döner.
    Tüm yanıt anahtarları İngilizce olacaktır.
    """
    try:
        w = whois.whois(domain)
        if w.domain_name:
            # Domain kayıtlıysa detaylı bilgileri döndür
            return {
                "Status": "Registered",
                "Domain": domain,
                "Registrar": w.registrar,
                "CreationDate": str(w.creation_date), # Tarih nesnelerini string'e çeviriyoruz
                "ExpirationDate": str(w.expiration_date),
                "UpdatedDate": str(w.updated_date),
                "NameServers": w.name_servers,
                "Emails": w.emails,
            }
        else:
            # Domain boşta ise
            return {"Status": "Available", "Domain": domain}
    except Exception as e:
        # WHOIS sorgusu sırasında bir hata oluşursa
        print(f"Error: {e}")
        return {"Status": "Available or access error", "Domain": domain}

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
        return jsonify({"error": "Invalid request body. 'siteName' and 'extensions' fields are required."}), 400

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
