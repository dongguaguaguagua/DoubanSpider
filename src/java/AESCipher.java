import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class AESCipher {

    public static final String AES_CBC(String str, String str2) {
        try {
            SecretKeySpec abs_secret = generate_abs_secret(str2);
            byte[] decode = Base64.getDecoder().decode(str);
            String IV = "DOUBANFRODOAPPIV";
            Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
            cipher.init(2, abs_secret, new IvParameterSpec(IV.getBytes()));
            return new String(cipher.doFinal(decode));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static SecretKeySpec generate_abs_secret(String str) throws Exception {
        byte[] bArr;
        if (str == null) {
            str = "";
        }
        StringBuilder sb = new StringBuilder(16);
        sb.append(str);
        while (sb.length() < 16) {
            sb.append("\u0000");
        }
        if (sb.length() > 16) {
            sb.setLength(16);
        }
        bArr = sb.toString().getBytes("UTF-8");
        return new SecretKeySpec(bArr, "AES");
    }

    public static void main(String[] args) {
        String sig_secret_key2 = "74CwfJd4+7LYgFhXi1cx0IQC35UQqYVFycCE+EVyw1E=";
        String sig_secret_key1 = "bHUvfbiVZUmm2sQRKwiAcw==";
        String app_signature_base64 = """
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
E6tVeW3UdHC1UvzyB7Qcxiu4sBiEO1koToQTWw==";
""";
        String decryptedText = AES_CBC(sig_secret_key2, app_signature_base64);
        System.out.println("Decrypted Text: " + decryptedText);
    }
}
