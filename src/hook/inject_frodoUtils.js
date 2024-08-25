// let AES = Java.use("com.douban.frodo.utils.crypto.AES");
// AES["a"].overload('java.lang.String', 'java.lang.String').implementation = function (str, str2) {
//     console.log(`AES.a is called: str=${str}, str2=${str2}`);
//     let result = this["a"](str, str2);
//     console.log(`AES.a result=${result}`);
//     return result;
// };
Java.perform(function() {
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            // console.log(className)
            if (className.indexOf("com.douban.frodo.utils.crypto.AES") !== -1){
                let AES = Java.use("com.douban.frodo.utils.crypto.AES");
                // Hooking the a(String, String) method
                AES.a.overload('java.lang.String', 'java.lang.String').implementation = function(str, str2) {
                    console.log("Hooked method a(String, String)");
                    console.log("str: " + str);
                    console.log("str2: " + str2);

                    var result = this.a(str, str2);

                    console.log("Result: " + result);
                    return result;
                };

                // Hooking the a(String) method (if exists)
                AES.a.overload('java.lang.String').implementation = function(str) {
                    console.log("Hooked method a(String)");
                    console.log("str: " + str);

                    var result = this.a(str);

                    console.log("Result: " + result);
                    return result;
                };

                let FrodoUtils = Java.use("com.douban.frodo.baseproject.util.FrodoUtils");
                let c = FrodoUtils._c.value;
                let b = FrodoUtils._b.value;
                console.log(b)
                console.log(c)

                let AppContext = Java.use("com.douban.frodo.utils.AppContext");
                AppContext["a"].overload().implementation = function () {
                    let result = this["a"]();
                    // com.douban.frodo.FrodoApplication@d4f330c
                    console.log(`AppContext.a result=${result}`);
                    return result;
                };
            }
        },
        onComplete: function() {
            console.log("complete")
        }
    });
});
