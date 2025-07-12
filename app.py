from flask import Flask, request, jsonify
from dotenv import load_dotenv
from ldap_service import LDAPAuthService
import os

# Configuração inicial
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Inicializa o serviço LDAP
auth_service = LDAPAuthService()

@app.route('/api/auth', methods=['POST'])
def auth_endpoint():
    """
    Endpoint de autenticação
    Exemplo de requisição:
    {
        "username": "123456",
        "password": "senha_do_usuario"
    }
    """
    data = request.get_json()
    
    # Validação básica
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "status": "error",
            "message": "Username and password are required"
        }), 400
    
    # Autenticação
    authenticated, response = auth_service.authenticate(data['username'], data['password'])
    
    if authenticated:
        return jsonify({
            "status": "success",
            "user": response
        })
    else:
        return jsonify({
            "status": "error",
            "message": response.get("message", "Authentication failed")
        }), 401

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está online"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='127.0.0.0', port=5000)