import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def generate_abs_secret(key: str) -> bytes:
    if key is None:
        key = ""
    key = key.ljust(16, '\0')[:16]  # 确保密钥长度为16字节
    return key.encode('utf-8')

def aes_cbc(ciphertext: str, key: str) -> str:
    try:
        abs_secret = generate_abs_secret(key)
        decode = base64.b64decode(ciphertext)
        IV = "DOUBANFRODOAPPIV".encode('utf-8')
        cipher = AES.new(abs_secret, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(decode)
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"Error: {e}")
        return ciphertext

def get_apikey() -> str:
    with open('app_signature_base64.txt', 'r') as f:
        app_signature_base64 = f.read().strip()

    sig_secret_key2 = "74CwfJd4+7LYgFhXi1cx0IQC35UQqYVFycCE+EVyw1E="
    return aes_cbc(sig_secret_key2, app_signature_base64)

def get_secret_key() -> str:
    with open('app_signature_base64.txt', 'r') as f:
        app_signature_base64 = f.read().strip()

    sig_secret_key1 = "bHUvfbiVZUmm2sQRKwiAcw=="
    return aes_cbc(sig_secret_key1, app_signature_base64)

