/**
 * Created by theo on 8/2/17.
 */
$("#up").click(function () {
    var type = $("#dj").val();
    console.log(type);
    if (type == "on") {
        window.location = "../upload"
    } else {
        window.location = "../uploadimg"
    }
});
$("#down").click(function () {
    var type = $("#tp").val();
    if (type == "on") {
        window.location = "../datcsv"

    } else {
        /*JSON*/
    }
});
