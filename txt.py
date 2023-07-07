from flask import Flask, request
from Crypto.Cipher import AES
import subprocess
import base64
import re

app = Flask(__name__)

@app.route('/flash/addcrypted2', methods=['POST'])
def handle_post_request():

    link = ""
    
    jk = request.form.get('jk')
    crypted_str = request.form.get('crypted')

    match = re.search(r"'([^']*)'", jk)
    if match:
        key_str = str(match.group(1))        
        # Decodificamos la contraseña en base16
        key_str = base64.b16decode(key_str).decode('utf-8')

        key = key_str.encode('utf-8')
        crypted = crypted_str.encode('utf-8')

        # Decodificamos el texto desde Base64 a binario
        enc = base64.b64decode(crypted)
        cipher = AES.new(key, AES.MODE_CBC, iv=key)
        # Desencriptamos el texto
        link = cipher.decrypt(enc)
        # Eliminamos el relleno
        link = link.rstrip(b'\x00')

        link = link.decode('utf-8')  # Convert bytes to string
        print(link)
        # link = link.splitlines()  # Split the string into a list using newline as the delimiter
        #subprocess.run("pbcopy", text=True, input=link)
        
    return link

if __name__ == "__main__":
    app.run(debug=True, port=9666)