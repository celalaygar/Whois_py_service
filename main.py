from flask import Flask, request, jsonify
import whois 
import os 

app = Flask(__name__)

def get_domain_info(domain):

    try:
        w = whois.whois(domain)
        if w.domain_name:
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
            return {"Status": "Available", "Domain": domain}
    except Exception as e:
        print(f"Error: {e}")
        return {"Status": "Available or access error", "Domain": domain}

@app.route('/check_domains', methods=['POST'])
def check_domains():

    data = request.get_json()

    if not data or 'siteName' not in data or 'extensions' not in data:
        return jsonify({"error": "Invalid request body. 'siteName' and 'extensions' fields are required."}), 400

    site_name = data['siteName']
    extensions = data['extensions']

    results = []

    for ext in extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        full_domain = f"{site_name}{ext}"
        domain_info = get_domain_info(full_domain)
        results.append(domain_info)

    return jsonify(results)

SUPPORTED_EXTENSIONS = [
    ".com", ".org", ".net", ".io", ".co", ".dev", ".app", ".info", ".xyz",
    ".ai", ".tech", ".blog", ".shop", ".store", ".site", ".online", ".cloud",
    ".digital", ".email", ".group", ".live", ".media", ".news", ".solutions",
    ".today", ".top", ".world", ".biz", ".mobi", ".name"
]

@app.route('/get_extensions', methods=['GET'])
def get_extensions():
    """
    Servis tarafından desteklenen domain uzantılarının listesini döndürür.
    """
    return jsonify({"supported_extensions": SUPPORTED_EXTENSIONS})

if __name__ == '__main__':

    port = int(os.getenv("APP_PORT", 7112))
    app.run(host='0.0.0.0', port=port, debug=True)
