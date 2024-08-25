import java.security.Signature;
import java.util.Base64;

public class getAppSignature {
    public static void main(String[] args) {
        // 假设这是你已知的 encodeToString
        String encodeToString = """
MIICUjCCAbsCBEty1MMwDQYJKoZIhvcNAQEEBQAwcDELMAkGA1UEBhMCemgxEDAOBgNVBAgTB0Jl
aWppbmcxEDAOBgNVBAcTB0JlaWppbmcxEzARBgNVBAoTCkRvdWJhbiBJbmMxFDASBgNVBAsTC0Rv
dWJhbiBJbmMuMRIwEAYDVQQDEwlCZWFyIFR1bmcwHhcNMTAwMjEwMTU0NjExWhcNMzcwNjI3MTU0
NjExWjBwMQswCQYDVQQGEwJ6aDEQMA4GA1UECBMHQmVpamluZzEQMA4GA1UEBxMHQmVpamluZzET
MBEGA1UEChMKRG91YmFuIEluYzEUMBIGA1UECxMLRG91YmFuIEluYy4xEjAQBgNVBAMTCUJlYXIg
VHVuZzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAg622fxLuwQtC8KLYp5gHk0OmfrFiIisz
kzPLBhKPZDHjYS1URhQpzf00T8qg2oEwJPPELjN2Q7YOoax8UINXLhMgFQkyAvMfjdEOSfoKH93p
v2d4n/IjQc/TaDKu6yb53DOq76HTUYLcfLKOXaGwGjAp3QqTqP9LnjJjGZCdSvMCAwEAATANBgkq
hkiG9w0BAQQFAAOBgQA3MovcB3Hv4bai7OYHU+gZcGQ/8sOLAXGD/roWPX3gm9tyERpGztveH35p
aI3BrUWg2Vir0DRjbR48b2HxQidQTVIH/HOJHV0jgYNDviD18/cBwKuLiBvdzc2Fte+zT0nnHXMy
E6tVeW3UdHC1UvzyB7Qcxiu4sBiEO1koToQTWw==
        """;

        // 解码 Base64 字符串
        byte[] decodedBytes = Base64.getDecoder().decode(encodeToString);

        try {
            // 创建 Signature 对象
            Signature signature = Signature.getInstance("SHA1withRSA");
            // signature.initVerify(/* 这里需要提供相应的公钥 */);
            signature.update(decodedBytes);

            // 你可以在这里进一步验证签名或进行其他操作
            // 例如，验证签名的有效性需要使用相应的公钥和数据

            System.out.println("Decoded bytes length: " + decodedBytes.length);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
