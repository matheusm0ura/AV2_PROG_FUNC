import mysql.connector
from flask import Flask, request, render_template
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

app = Flask(__name__, template_folder='template_folder')

# Chave e iv para criptografia AES
key = get_random_bytes(16)  # Chave de 128 bits
iv = get_random_bytes(16)   # Vetor de inicialização de 128 bits

def encrypt_password(password):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Convertendo a senha para bytes e garantindo que tenha um comprimento múltiplo de 16
    password_bytes = password.encode().ljust(16)
    ciphertext = cipher.encrypt(password_bytes)
    return b64encode(ciphertext)


def decrypt_password(ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(b64decode(ciphertext))
    # Removendo o preenchimento (padding) e decodificando de bytes para string
    return decrypted.rstrip(b'\0').decode()

# Dicionário de usuários com senhas criptografadas
users = {
    "test": encrypt_password("123"),
    "aaaa": encrypt_password("abc")
}

def welcome():
    return f'WELCOME {request.form["username"]}!'

def wrong():
    return "WRONG PASSWORD"

def invalid():
    return "User does not exist!"

def password_matches(password):
    # Descriptografando a senha armazenada
    stored_password = decrypt_password(users.get(request.form["username"]))
    # Comparando a senha fornecida com a senha armazenada
    return stored_password == password


def check_password():
    return welcome() if password_matches(request.form["password"]) else wrong()

def check_if_user_exists():
    return check_password() if request.form["username"] in users else invalid()

def reqresp():
    if request.method == 'POST':
        return check_if_user_exists()
    else:
        return render_template('index.html')

app.add_url_rule('/index/', 'index', reqresp, methods=['GET', 'POST'])
app.run(host='0.0.0.0', port=8080)
