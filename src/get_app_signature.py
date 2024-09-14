# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# import base64
# # from androguard.core.bytecodes.apk import APK
# from androguard.core.apk import APK

# def get_apk_signature(apk_path):
#     apk = APK(apk_path)
#     signatures = apk.get_signatures()
#     if signatures:
#         signature = signatures[0]
#         encoded_signature = base64.b64encode(signature).decode('')
#         return encoded_signature
#     else:
#         raise ValueError("No signatures found in APK")

# apk_path = "/Users/hzy/Downloads/豆瓣_7.48.0.apk"
# signature_base64 = get_apk_signature(apk_path)

import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 假设这是你的Base64编码字符串
with open('app_signature_base64.txt', 'r') as f:
    app_signature_base64 = f.read().strip()

# 解码Base64字符串
decoded_bytes = base64.b64decode(app_signature_base64)






