import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.AbstractMap;
import java.util.Map;

public class SignatureHelper {

    public static Map.Entry<String, String> getSignature(String urlPath, String method, String bearerKey, String secretKey, long timeStamp) {
        String decode;
        String signature = null;

        if (urlPath == null || urlPath.isEmpty()) {
            return null;
        }

        if (secretKey == null || secretKey.isEmpty()) {
            return null;
        }

        StringBuilder sb = new StringBuilder();
        sb.append(method);

        String encodedPath = null;
        try {
            URI uri = new URI(urlPath);
            encodedPath = uri.getPath();
        } catch (URISyntaxException e) {
            e.printStackTrace();
            return null;
        }

        decode = URLDecoder.decode(encodedPath);
        if (decode == null) {
            return null;
        }

        if (decode.endsWith("/")) {
            decode = decode.substring(0, decode.length() - 1);
        }

        sb.append("&");
        sb.append(URLEncoder.encode(decode));

        if (bearerKey != null && !bearerKey.isEmpty()) {
            sb.append("&");
            sb.append(bearerKey);
        }

        sb.append("&");
        sb.append(timeStamp);

        try {
            SecretKeySpec secretKeySpec = new SecretKeySpec(secretKey.getBytes(), "HmacSHA1");
            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(secretKeySpec);
            signature = new String(java.util.Base64.getEncoder().encode(mac.doFinal(sb.toString().getBytes())));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

        return new AbstractMap.SimpleEntry<>(signature, String.valueOf(timeStamp));
    }

    public static void main(String[] args) {
        String urlPath = "https://frodo.douban.com/api/v2/notification_chart?apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Huawei_Market&udid=1bda1ed0f16fa2e16734de5ed9b7d639d155ec2a&os_rom=miui6&oaid=7b184f162f3d188e&timezone=Asia%2FShanghai";
        String method = "GET";
        String bearerKey = "c42a3dc7a510e0814c7eb956ef32a183";
        String secretKey = "bf7dddc7c9cfe6f7";
        long timeStamp = 1724395209;

        Map.Entry<String, String> result = getSignature(
            urlPath,
            method,
            bearerKey,
            secretKey,
            timeStamp
        );

        if (result != null) {
            System.out.println("Signature: " + result.getKey());
            System.out.println("Timestamp: " + result.getValue());
        }
    }
}
