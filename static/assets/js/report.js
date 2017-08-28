/**
 * Created by theo on 7/27/17.
 */

$('body').on('click', '#report', function () {
    report();
});


function report() {
    var ids = getids();
    var form = new FormData();
    form.append("ids", ids);
    form.append("url", window.location.href);

    if (where.indexOf("generated") != -1) {
        var temp = where.split("/");
        where = "/" + $.base64.decode(temp[2]).split("/")[0]
    }
    $.ajax({
        type: "POST",
        url:  baseu +"report" + where ,
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            $("#skip").click()
        }
    });
}

function getids() {
    result = [];
    $("body").find("img").each(function () {
        if ($(this).attr("value") != undefined) {
            result.push($(this).attr("value"))
        }
    });

    if (result.length == 0) {
        result = getit();
    }
    return result
}
