/**
 * Created by theo on 8/2/17.
 */

var baseu =  window.location.href.replace(where, "") + "/";
var where = window.location.pathname;


$("#up").click(function () {
    var type = $("#dj").val();
    if (type == "on") {
        window.location = baseu + "upload"
    } else {
        window.location = baseu + "uploadimg"
    }
});
$("#down").click(function () {
    var type = $("#tp").val();
    if (type == "on") {
        window.location =  baseu +"datcsv"

    } else {
        /*JSON*/
    }
});
