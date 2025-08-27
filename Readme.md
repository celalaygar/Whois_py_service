
# Flask WHOIS Domain Checker Service

This project provides a simple Flask-based REST API to check WHOIS information for a list of domains. It takes a base `siteName` and a list of extensions, then constructs full domain names and queries their WHOIS records.

## 📱 Features

- **WHOIS Lookup**: Retrieves registration details (creation date, expiration date, registrar, name servers, etc.) for domains.
- **Domain Availability Check**: Identifies if a domain is registered or available.
- **RESTful API**: Provides a POST endpoint for easy integration.
- **Dockerized**: Ready to be deployed as a Docker container.

## Project Structure

```
.
├── Main.py             # The main Flask application file
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker build instructions
```

## 🚀  Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Docker (if you plan to run it in a container)

### ⚙️ Local Setup

Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

- Flask
- python-whois

Run the Flask application:

```bash
python Main.py
```

The service will start on `http://0.0.0.0:7112`.

### Docker Setup

Build the Docker image:

```bash
docker build -t flask-whois-app .
```

Run the Docker container:

```bash
docker run -p 7112:7112 flask-whois-app
```

The service will be accessible at `http://localhost:7112`.

## API Usage

### Endpoint

`POST /check_domains`

`GET /get_extensions`

### Request Body

```json
{
  "siteName": "home",
  "extensions": [".com", ".org", ".net", ".io", ".co", ".dev", ".app", ".xyz"]
}
```

### Example curl Command

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "siteName": "home",
           "extensions": [".com", ".org", ".net", ".io", ".co", ".dev", ".app", ".xyz"]
         }' \
     http://localhost:7112/check_domains
```

### Response

#### For Registered Domains

```json
{
  "Status": "Registered",
  "Domain": "home.com",
  "Registrar": "GoDaddy Corporate Domains, LLC",
  "CreationDate": "1993-12-16 05:00:00",
  "ExpirationDate": "2031-12-15 05:00:00",
  "UpdatedDate": "[datetime.datetime(2022, 4, 9, 3, 55, 51), datetime.datetime(2022, 4, 9, 3, 53, 51)]",
  "NameServers": ["NS2-02.AZURE-DNS.NET", "NS3-02.AZURE-DNS.ORG", "NS4-02.AZURE-DNS.INFO"],
  "Emails": ["abuse@gcd.com", "anonymous-registrant@brandsight.com", "anonymous-tech@brandsight.com"]
}
```

#### For Available Domains

```json
{
  "Status": "Available",
  "Domain": "home.dev"
}
```

#### For Invalid Request

```json
{
  "error": "Invalid request body. 'siteName' and 'extensions' fields are required."
}
```
### Example curl Command

```bash
curl -X GET http://localhost:7112/get_extensions
```
#### Response For 200 OK

```json
{
  "supported_extensions": [
    ".com", ".org", ".net", ".io", ".co", ".dev", ".app", ".xyz", ".ai",
    ".tech", ".web", ".dev", ".cn", ".com.tr", ".tr", ".en", ".de"
  ]
}

```

### Example Full Response

*(Omitted here for brevity, see your example)*

## ⚙️ Nginx Configuration (Optional)

```nginx
server {
    listen 3303;
    server_name localhost;

    location /serach_domains/ {
        proxy_pass http://127.0.0.1:7112/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 150;
        proxy_send_timeout 150;
        proxy_read_timeout 150;
        send_timeout 150;
    }
}
```

Remember to reload Nginx after making changes:

```bash
sudo systemctl reload nginx
# or
sudo service nginx reload
```
