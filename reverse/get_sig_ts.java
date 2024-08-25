public static Pair<String, String> get_sig_ts_pair(String req_url, String req_method, String req_header) {
    String decode;
    String str = null;
    if (TextUtils.isEmpty(req_url)) {
        return null;
    }
    String str2 = FrodoApi.b().e.b; // 获取密钥str2
    if (TextUtils.isEmpty(str2)) {
        return null;
    }
    StringBuilder str_builder = a.f(req_method); // 初始化StringBuilder
    String encodedPath = HttpUrl.parse(req_url).encodedPath(); // 解析URL路径
    if (encodedPath == null || (decode = Uri.decode(encodedPath)) == null) {
        return null;
    }
    if (decode.endsWith("/")) {
        decode = a.cut_string(decode, -1, 0); // 去掉路径末尾的'/'
    }
    str_builder.append(StringPool.AMPERSAND); // 添加'&'
    str_builder.append(Uri.encode(decode)); // 添加解码后的路径
    if (!TextUtils.isEmpty(req_header)) {
        str_builder.append(StringPool.AMPERSAND); // 添加'&'
        str_builder.append(req_header); // 添加请求头信息
    }
    long currentTimeMillis = System.currentTimeMillis() / 1000; // 获取当前时间的秒数
    str_builder.append(StringPool.AMPERSAND); // 添加'&'
    str_builder.append(currentTimeMillis); // 添加时间戳
    String sb = str_builder.toString(); // 构建最终字符串
    try {
        SecretKeySpec secretKeySpec = new SecretKeySpec(str2.getBytes(), LiveHelper.HMAC_SHA1); // 初始化HMAC密钥
        Mac mac = Mac.getInstance(LiveHelper.HMAC_SHA1); // 获取HMAC实例
        mac.init(secretKeySpec); // 初始化HMAC
        str = Base64.encodeToString(mac.doFinal(sb.getBytes()), 2); // 生成签名并进行Base64编码
    } catch (Exception e) {
        e.printStackTrace(); // 异常处理
    }
    return new Pair<>(str, String.valueOf(currentTimeMillis)); // 返回签名和时间戳
}
