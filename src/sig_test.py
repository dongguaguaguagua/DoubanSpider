import hmac
import base64
import hashlib
import time
from urllib.parse import urlparse, unquote, quote

def get_sig_ts_pair(req_url, req_method, req_header):
    if not req_url:
        return None

    # 密钥
    str2 = "bHUvfbiVZUmm2sQRKwiAcw=="  # 请替换为实际的密钥

    # 解析URL路径并解码
    parsed_url = urlparse(req_url)
    encoded_path = parsed_url.path
    if not encoded_path:
        return None

    decode = unquote(encoded_path)
    if decode.endswith('/'):
        decode = decode[:-1]

    # 构建签名字符串
    str_builder = [req_method, '&', quote(decode)]
    if req_header:
        str_builder.extend(['&', req_header])

    # current_time = int(time.time())
    current_time = 1723182117
    str_builder.extend(['&', str(current_time)])
    sb = ''.join(str_builder)

    # 生成签名
    try:
        secret_key = str2.encode()
        message = sb.encode()
        digester = hmac.new(secret_key, message, hashlib.sha1)
        signature = base64.b64encode(digester.digest()).decode()
    except Exception as e:
        print(e)
        return None

    return signature, str(current_time)

# 示例调用
req_url = "http://example.com/path/to/resource"
req_method = "GET"
req_header = "header_value"
signature, timestamp = get_sig_ts_pair(req_url, req_method, req_header)
print(f"Signature: {signature}, Timestamp: {timestamp}")
