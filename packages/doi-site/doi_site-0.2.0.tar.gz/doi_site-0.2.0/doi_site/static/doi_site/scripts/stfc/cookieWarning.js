/////////////////////////////////////////////////////////////
//
// Based on code by Scott Herbert (www.scott-herbert.com)
// http://code.google.com/p/cookie-warning/downloads/detail?name=cookiewarning.js&can=2&q=
// 

function getCookie(c_name) {
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == c_name) {
            return unescape(y);
        }
    }
}

function displayNotification() {

    var message = "<div id=\"cookiewarning\">";

    // open warning box padding:10px;width:960px
    message = message + "<div style='position: relative; top: -20px; padding:10px;height:2em;background:#e8bdd3;color:black;z-index:1000; margin-bottom: -50px;'>";

    // this is the message displayed to the user.
    message = message + "This site uses cookies to help make it more useful and reliable. Our <a style=\"color: #330066;\ font-weight:bold;\" href=\"http://www.stfc.ac.uk/privacy.aspx\">cookies</a> page explains what they are, which ones we use, and how you can manage or remove them.";

    message = message + "&nbsp;<a style=\"color: #330066;\ font-weight:bold;\" href=\"JavaScript:setCookie('stfcCookieCheck',null,365);\">Don't show this message again</a>";

    // and this closes everything off.
    message = message + "</div></div>";

    document.writeln(message);

}

function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value;

    // set cookie warning to hidden.
    var cw = document.getElementById("cookiewarning");
    if (cw != null) {
        cw.innerHTML = "";
    }


   
}

function checkCookie() {

    var cookieName = "stfcCookieCheck";
    var cookieChk = getCookie(cookieName);
    if (cookieChk != null && cookieChk != "") {
        // the stfcCookieCheck cookie exists so we can assume the person has read the notification
        // within the last year
        setCookie(cookieName, cookieChk, 365); // set the cookie to expire in a year.
    }
    else {
        // No cookie exists, so display the notification.
        displayNotification();
    }
}

checkCookie();

