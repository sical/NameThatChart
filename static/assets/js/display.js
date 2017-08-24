/**
 * Created by theo on 8/2/17.
 */
var info = [];
$(document).ready(function () {
    console.log($("#id").val());
    if (!isNaN(parseInt($("#id").val()))) {
        dispoutofid()
    } else {

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
                    info = JSON.parse(info).slice(0, 50);
                    $("#res").text("results limited to 50 if  the filter is empty");
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
                    if (idimage.length > 0) {
                        if (info.length >= 1) {
                            $("#res").text(info.length + " results found");
                        } else {
                            $("#res").text(info.length + " result found");

                        }
                        info.forEach(function (img) {
                            $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                        });

                    } else {
                        $("#res").text("results limited to 50 if  the filter is empty");
                        info = info.slice(0, 50);
                        info.forEach(function (img) {
                            $("#fill").append("<img class='idata' value='" + img.id + "' src='" + img.path + "'>")
                        });
                    }
                }
                catch
                    (err) {
                    $("#res").text(0 + " result found");
                }
            }
        })
    }
});


function dispoutofid() {
    var modal = document.getElementById('myModal');
    var btn = document.getElementById("myBtn");
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = "block";
    var form = new FormData();
    form.append("action", $("#id").val());

    $.ajax({
        type: "POST",
        url: "../" + "getimgbyid",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            var image = JSON.parse(JSON.parse(data));


            $(".modal-body").empty();
            $(".modal-body").append("<img  class='imgmod' src='" + image[0].path + "'/>");
            $("#mh").text("Image N°" + image[0].idimage);
            var form = new FormData();
            form.append("idimg", "" + image[0].idimage);
            $.ajax({
                type: "POST",
                url: "../getimginfotype",
                processData: false,
                contentType: false,
                data: form,
                success: function (data) {
                    data = JSON.parse(data);
                    $(".modal-body").append("<div class='imginfo'> <ul class='list-group'> <li class='list-group-item'>Textual <span class='badge'>" + data.text + "</span></li> <li class='list-group-item'>Selection<span class='badge'>" + data.select + "</span></li> <li class='list-group-item'>Swipes<span class='badge'>" + data.swipe + "</span></li> </ul> </div>");
                    $("#mf").text("Classified " + (parseInt(data.text) + parseInt(data.swipe) + parseInt(data.select)) + " times")
                }
            });
            $.ajax({
                type: "POST",
                url: "../topclass",
                processData: false,
                contentType: false,
                data: form,
                success: function (data) {
                    info = JSON.parse(data);
                    str = "<div class='imginfo'> <ul class='list-group'>";
                    info.forEach(function (row) {
                        str += " <li class='list-group-item'>" + row.name + " <span class='badge'>" + row.value + "</span></li>"
                    });
                    $(".modal-body").append(str + "</ul> </div></div>")
                }
            })
        }
    });
}