/**
 * Created by theo on 7/27/17.
 */
$("#nd").click(function (event) {
    event.preventDefault();

    report("no_display")
});

$("#ii").click(function (event) {
    event.preventDefault();

    report("Inappropriate_image")
});

$("#hmc").click(function (event) {
    event.preventDefault();

    report("miss_classification")
});
function report(string) {
    var temp = window.location.href.split("/");

    where = temp[temp.length - 1];
    var ids = getids();
    console.log(ids);
    var form = new FormData();
    form.append("ids", ids);
    $.ajax({
        type: "POST",
        url: "../report/" + where + "/" + string,
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            pop();
            $("#skip").click()
        }
    });


}

function getids() {
    result = [];

    $("img").each(function () {
        result.push($(this).attr("value"))
    });

    if (result.length ==0) {
        result=getit();
    }
    return result
}

function pop() {
    $("#pop").show();
    $("#pop").delay(4300).fadeOut(500);
}
