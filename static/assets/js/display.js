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
            try {
                info = JSON.parse(data);
                info = JSON.parse(info);
                if (info.length >= 1) {
                    $("#res").text(info.length + " results found");
                } else {
                    $("#res").text(info.length + " result found");
                }
                info.forEach(function (img) {
                    $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                });
            }
            catch (err) {
                $("#res").text(0 + " result found");
            }
        }
    })
});
$("#sh").on('input', function () {
    var idimage;
    var form;
    $("#fill").empty();
    if (!isNaN(parseInt($(this).val()))) {
        idimage = $(this).val();
        form = new FormData();
        form.append("action", "" + idimage);
        $.ajax({
            type: "POST",
            url: "../getimgbyid",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                try {
                    info = JSON.parse(data);
                    info = JSON.parse(info);
                    if (info.length >= 1) {
                        $("#res").text(info.length + " results found");
                    } else {
                        $("#res").text(info.length + " result found");

                    }
                    info.forEach(function (img) {
                        $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                    });
                }
                catch (err) {
                    $("#res").text(0 + " result found");
                }
            }
        });
    }
    else {
        idimage = $(this).val();
        form = new FormData();
        form.append("action", "" + idimage);
        $("#fill").empty();

        $.ajax({
            type: "POST",
            url: "../getimgbytype",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                try {
                    info = JSON.parse(data);
                    info = JSON.parse(info);
                    if (info.length >= 1) {
                        $("#res").text(info.length + " results found");
                    } else {
                        $("#res").text(info.length + " result found");

                    }
                    info.forEach(function (img) {
                        $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                    });
                }
                catch (err) {
                    $("#res").text(0 + " result found");
                }
            }
        })
    }
});