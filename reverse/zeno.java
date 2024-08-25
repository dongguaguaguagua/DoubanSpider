package com.douban.zeno;

import android.text.TextUtils;
import android.util.Log;
import com.douban.frodo.utils.IOUtils;
import com.google.gson.Gson;
import com.mcxiaoke.next.http.HttpMethod;
import com.mcxiaoke.next.http.NextClient;
import com.mcxiaoke.next.http.NextParams;
import com.mcxiaoke.next.http.NextRequest;
import com.mcxiaoke.next.http.NextResponse;
import com.tencent.thumbplayer.core.downloadproxy.utils.TPDLIOUtil;
import i.c.a.a.a;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;

/* loaded from: classes7.dex */
public class ZenoClient {
    public ZenoConfig a;
    public Gson b;
    public NextClient c;
    public Async d;
    public String e;
    public boolean f;

    public ZenoClient(ZenoConfig zenoConfig) {
        a(zenoConfig, new OkHttpClient());
    }

    public final void a(ZenoConfig zenoConfig, OkHttpClient okHttpClient) {
        IOUtils.a(zenoConfig, "config can not be null.");
        IOUtils.a(okHttpClient, "client can not be null.");
        this.a = zenoConfig;
        this.c = new NextClient(okHttpClient);
        this.d = new Async(this);
    }

    public <T> ZenoRequest<T> b(ZenoRequest<T> zenoRequest) {
        String str;
        if (this.a != null) {
            NextRequest nextRequest = zenoRequest.a;
            if (!TextUtils.isEmpty(zenoRequest.e)) {
                str = zenoRequest.e;
            } else {
                str = this.e;
            }
            if (!TextUtils.isEmpty(str)) {
                nextRequest.c.a("Authorization", String.format("Bearer %s", str));
            }
            ZenoConfig zenoConfig = this.a;
            if (zenoConfig != null) {
                Map<String, String> map = zenoConfig.f4814h;
                if (map != null) {
                    if (nextRequest != null) {
                        NextParams nextParams = nextRequest.c;
                        if (nextParams != null) {
                            for (Map.Entry<String, String> entry : map.entrySet()) {
                                nextParams.a(entry.getKey(), entry.getValue());
                            }
                        } else {
                            throw null;
                        }
                    } else {
                        throw null;
                    }
                }
                if (!TextUtils.isEmpty(zenoConfig.e)) {
                    nextRequest.c.a("User-Agent", zenoConfig.e);
                }
            }
            ZenoConfig zenoConfig2 = this.a;
            if (zenoConfig2 != null) {
                Map<String, String> map2 = zenoConfig2.f4815i;
                if (map2 != null) {
                    nextRequest.b(map2);
                }
                Map<String, String> map3 = zenoConfig2.f4816j;
                if (map3 != null) {
                    nextRequest.a(map3);
                }
                HashMap hashMap = new HashMap();
                hashMap.put("udid", zenoConfig2.d);
                hashMap.put("apikey", zenoConfig2.a);
                hashMap.put("os_rom", zenoConfig2.f);
                hashMap.put("channel", zenoConfig2.f4813g);
                if (HttpMethod.supportBody(nextRequest.a)) {
                    nextRequest.a(hashMap);
                } else {
                    nextRequest.b(hashMap);
                }
            }
            if (this.f || zenoRequest.f4817g) {
                StringBuilder a = a.a("wrapRequest token=", str, " fullUrl=");
                a.append(nextRequest.b());
                Log.d("Zeno", a.toString());
            }
        }
        return zenoRequest;
    }

    public ZenoClient(ZenoConfig zenoConfig, OkHttpClient okHttpClient) {
        a(zenoConfig, okHttpClient);
    }

    public synchronized Gson a() {
        if (this.b == null) {
            this.b = IOUtils.e();
        }
        return this.b;
    }

    public String a(String str) {
        if (!str.startsWith("/")) {
            str = a.f("/", str);
        }
        return new HttpUrl.Builder().scheme(TPDLIOUtil.PROTOCOL_HTTPS).host(this.a.c).encodedPath(str).build().toString();
    }

    public <T> T a(ZenoRequest<T> zenoRequest) throws ZenoException {
        NextResponse nextResponse = null;
        try {
            try {
                if (zenoRequest.f4818h) {
                    b(zenoRequest);
                }
                if (this.f || zenoRequest.f4817g) {
                    Log.d("Zeno", "execute request=" + zenoRequest);
                }
                NextResponse a = this.c.a(zenoRequest.a);
                ZenoResponse zenoResponse = new ZenoResponse(a.a);
                if (this.f || zenoRequest.f4817g) {
                    Log.d("Zeno", "execute response=" + zenoResponse);
                }
                if (a.a.isSuccessful()) {
                    T a2 = zenoRequest.c.a(zenoResponse);
                    ZenoProcessor<T> zenoProcessor = zenoRequest.d;
                    if (zenoProcessor != null) {
                        zenoProcessor.a(a2);
                    }
                    a.a.body().close();
                    return a2;
                }
                throw ZenoException.wrap(zenoResponse);
            } catch (IOException e) {
                if (this.f || zenoRequest.f4817g) {
                    Log.w("Zeno", "execute error=" + e);
                }
                throw ZenoException.wrap(e);
            }
        } catch (Throwable th) {
            if (0 != 0) {
                nextResponse.a.body().close();
            }
            throw th;
        }
    }
}
