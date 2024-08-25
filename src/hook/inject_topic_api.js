// Douban v7.13.0
Java.perform(function() {
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            if (className.indexOf("com.douban.frodo.network.ApiSignatureInterceptor") !== -1) {
                // let ApiSignatureInterceptor = Java.use("com.douban.frodo.network.ApiSignatureInterceptor");
                // ApiSignatureInterceptor["intercept"].implementation = function (chain) {
                //     console.log(`ApiSignatureInterceptor.intercept is called: chain=${chain}`);
                //     let result = this["intercept"](chain);
                //     console.log(`ApiSignatureInterceptor.intercept result=${result}`);
                //     return result;
                // };
                let Request = Java.use("okhttp3.Request");
                Request["header"].implementation = function (str) {
                    console.log(`Request.header is called: str=${str}`);
                    let result = this["header"](str);
                    console.log(`Request.header result=${result}`);
                    return result;
                };

                let ApiSignatureHelper = Java.use("com.douban.frodo.network.ApiSignatureHelper");
                ApiSignatureHelper["a"].overload('java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function (str, str2, str3) {
                    console.log(`ApiSignatureHelper.a is called: str=${str}, str2=${str2}, str3=${str3}`);
                    let result = this["a"](str, str2, str3);
                    console.log(`ApiSignatureHelper.a result=${result}`);
                    return result;
                };
            }
        },
        onComplete: function() {
            console.log("complete")
        }
    });
});
