from Crypto.Util.Padding import pad, unpad
from flask import Flask, jsonify, request, render_template
import q3_MatheusLima as q3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode
#A questão escolhida foi a 3.

app = Flask(__name__, template_folder='template_folder')

key = get_random_bytes(16).hex()
iv = get_random_bytes(16)
key_bytes = bytes.fromhex(key)

encrypt_password = lambda password: b64encode(AES.new(key_bytes,
                                    AES.MODE_CBC, iv).encrypt(pad(str(password).encode(), AES.block_size)))

decrypt_password = lambda ciphertext: unpad(AES.new(key_bytes, AES.MODE_CBC, iv).decrypt(b64decode(ciphertext)),
                                            AES.block_size).decode().strip()

users = lambda: {
    "test": encrypt_password("123"),
    "aaaa": encrypt_password("abc")
}

welcome = lambda: f'WELCOME {request.form["username"]}! <br> Consulta: {q3.show_query()}'
wrong = lambda: "WRONG PASSWORD"
invalid = lambda: "User does not exist!"
"""
Em vez de descriptografar a senha armazenada usando decrypt_password, chama-se diretamente a função encrypt_password 
para criptografar a senha fornecida pelo usuário.
"""
password_matches = lambda dic: dic.get(request.form["username"]) == encrypt_password(request.form["password"])
check_password = lambda: welcome() if password_matches(users()) else wrong()
check_if_user_exists = lambda: check_password() if f'{request.form["username"]}' in users() else invalid()
reqresp = lambda: check_if_user_exists() if request.method == 'POST' else render_template('index.html')

app.add_url_rule('/index/', 'index', reqresp, methods=['GET', 'POST'])
app.run(host='0.0.0.0', port=8080)
