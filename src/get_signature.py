import hmac
import hashlib
import base64
from urllib.parse import urlparse, quote, unquote
from get_secret import get_secret_key
from get_signature import *

def custom_quote(s):
    return quote(s, safe='').replace('/', '%2F')

def get_signature(url_path, bearer_key, secret_key, timestamp) -> str:
    if not url_path or not secret_key:
        return ""

    # 构造基础字符串
    sb = ["GET"]

    parsed_url = urlparse(url_path)
    decoded_path = unquote(parsed_url.path)

    if decoded_path.endswith("/"):
        decoded_path = decoded_path[:-1]

    sb.append(custom_quote(decoded_path))

    if bearer_key:
        sb.append(bearer_key)

    sb.append(str(timestamp))

    # 使用 '&' 连接组件
    base_string = "&".join(sb)

    # 生成 HMAC-SHA1 签名
    try:
        signature = base64.b64encode(hmac.new(secret_key.encode(), base_string.encode(), hashlib.sha1).digest()).decode()
    except Exception as e:
        return f"生成签名时出错: {e}"

    return signature

print(get_signature(
    url_path="https://frodo.douban.com/api/v2/user/165389773/interests?type=movie&status=done&start=100&count=20&common_interest=0&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Huawei_Market&udid=1bda1ed0f16fa2e16734de5ed9b7d639d155ec2a&os_rom=miui6&oaid=7b184f162f3d188e&timezone=Asia/Shanghai",
    bearer_key="c42a3dc7a510e0814c7eb956ef32a183",
    secret_key=get_secret_key(),
    timestamp=1724508124,
))
