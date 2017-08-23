/**
 * Created by theo on 8/2/17.
 */

var baseu;
var where;

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    baseu = baseu.replace(window.location.search, "");
    if (window.location.search.indexOf("m=dGV4dHV") != -1) {
        window.history.pushState("/", "/", where);
        $("#vald").css("display", "inline-block");
        setTimeout(function () {
            $("#vald").css("display", "none");


        }, 2000)

    } else {

    }
})
;






