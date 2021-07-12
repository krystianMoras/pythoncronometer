# GWT constants
GWTHeader = "3B6C5196158464C5643BA376AF05E7F1"
GWTAUTH = f"7|0|5|https://cronometer.com/cronometer/|{GWTHeader}|com.cronometer.client.CronometerService|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|"
gwtHeaders = {"content-type": "text/x-gwt-rpc; charset=UTF-8",
              "x-gwt-module-base": "https://cronometer.com/cronometer/",
              "x-gwt-permutation": "7B121DC5483BF272B1BC1916DA9FA963"}
GWTGenerateAuthFormat = GWTGenerateAuthToken = "7|0|8|https://cronometer.com/cronometer/|"+GWTHeader+"|com.cronometer.client.CronometerService|generateAuthorizationToken|java.lang.String/2004016611|I|com.cronometer.client.data.AuthScope/3337242207|{nonce}|1|2|3|4|4|5|6|6|7|8|{userid}|3600|7|2|"
GWTLogoutFormat = "7|0|6|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|logout|java.lang.String/2004016611|{nonce}|1|2|3|4|1|5|6|"
# GWT urls
GWTBaseURL = "https://cronometer.com/cronometer/app"
# Urls
exportURL = "https://cronometer.com/export"
loginPageURL = "https://cronometer.com/login/"
regularHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
loginRequestURL = "https://cronometer.com/login"
