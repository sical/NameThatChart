/**
 * Created by theo on 8/2/17.
 */
var info = [];
$(document).ready(function () {
    var form = new FormData();
    form.append("action", "_");
    $.ajax({
        type: "POST",
        url: "../getimgbytype",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            info = JSON.parse(JSON.parse(data));
            info.forEach(function (img) {
                $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
            });
        }
    })
});
$("#sh").on('input', function () {
    var idimage;
    var form;
    $("#fill").empty();
    if (!isNaN(parseInt($(this).val()))) {
      idimage  = $(this).val();
       form = new FormData();
        form.append("action", "" + idimage);
        $.ajax({
            type: "POST",
            url: "../getimgbyid",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                info = JSON.parse(data);
                info.forEach(function (img) {
                    $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                });
            }
        });
    }
    else {
        idimage = $(this).val();
        form = new FormData();
        form.append("action", "" + idimage);
        $.ajax({
            type: "POST",
            url: "../getimgbytype",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                info = JSON.parse(data);
                info.forEach(function (img) {
                    $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                });
            }
        })
    }
});