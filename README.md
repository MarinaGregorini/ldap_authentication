
# Flask LDAP Authentication API

Simple API to authenticate users against an LDAP server using Flask and ldap3.

---

## Features

- LDAP user authentication
- Fetches user info like displayName and email
- REST API with /api/auth and /api/health endpoints
- Uses environment variables for config

---

## Project Structure

```
.
├── app.py             # Flask app with REST endpoints
├── ldap_service.py    # LDAP authentication logic
├── .env               # Environment variables (not included)
├── requirements.txt   # Python dependencies
```

---

## Setup

1. Clone the repo:

```bash
git clone https://github.com/MarinaGregorini/ldap_authentication.git
cd ldap_authentication
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with:

```ini
LDAP_ADMIN_PASSWORD=your_ldap_admin_password
FLASK_SECRET_KEY=your_flask_secret_key
```

5. Edit `ldap_service.py` to set your LDAP server details:

```python
self.ldap_server = '<your_ldap_server>'
self.bind_dn = '<your_bind_dn>'
self.search_base = '<your_search_base>'
```

---

## Running the app

```bash
python app.py
```

API runs at: http://127.0.0.1:5000

---

## API Endpoints

### POST `/api/auth`

Authenticate user via LDAP.

**Request example:**

```json
{
  "username": "johnsmith",
  "password": "user_password"
}
```

**Success response:**

```json
{
  "status": "success",
  "user": {
    "username": "johnsmith",
    "display_name": "John Smith",
    "email": "john.smith@example.com"
  }
}
```

**Error response:**

```json
{
  "status": "error",
  "message": "Invalid credentials"
}
```

### GET `/api/health`

Check if the API is running.

**Response:**

```json
{ "status": "healthy" }
```
