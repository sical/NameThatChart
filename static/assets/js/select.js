/**
 * Created by theo on 8/2/17.
 */
var type;
var info;
$(document).ready(function () {
    if (window.location.href.indexOf('quizz') !== -1) {
        fillthem2();
    } else {
        fillthem();
    }
});
$('body').on('click', 'img', function () {
    $("img").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
    pop();
    if (window.location.href.indexOf('quizz') !== -1) {
        var note = 0;
        if ($(this).attr("value") == 2) {
            note = 4
        }
        var form = new FormData();
        form.append("note", note);
        $.ajax({
            type: "POST",
            url: "../savenote",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                window.location = "../main"
            }
        })
    } else {
        var form = new FormData();
        form.append("idimage", $(this).attr("value"));
        form.append("idtype", type);
        $.ajax({
            type: "POST",
            url: "../saveselect",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                if (window.location.href.indexOf('main') !== -1) {
                    window.location = "../main"
                } else if (window.location.href.indexOf('raw') !== -1) {
                    window.location = "../raw"
                }
                else {
                    $("#fill").empty();
                    $("#brand").text(" Select the picture which best describe : ");
                    fillthem();
                }
            }
        })
    }
});

function fillthem() {
    $.ajax({
        type: "GET",
        url: "../getselect",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            $("#brand").append(info.name);
            type = info.idtype;
            info.imgs.forEach(function (img) {
                $("#fill").append("<img id='imgsel' value='" + img.id + "' src='" + img.path + "' />");
                var form = new FormData();
                form.append("idimg", img.id);
                form.append("idtype", type);
                $.ajax({
                    type: "POST",
                    url: "../logsel",
                    processData: false,
                    contentType: false,
                    data: form
                })
            });
        }
    });
}

function fillthem2() {
    var imgues = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_205.gif", "static/assets/img/datasets/quizz/1.png", "static/assets/img/datasets/quizz/0.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_224.gif", "static/assets/img/datasets/quizz/3.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_91.gif"];
    $("#brand").append("Histogram");
    var i = 0;
    imgues.forEach(function (img) {
        $("#fill").append("<img id='imgsel' value='" + i + "' src=" + img + " />")
    })
}

$("#skip").click(function () {
    var images = [];
    info.imgs.forEach(function (row) {
        images.push(row.id)
    });

    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("ids", images);
    firm.append("idtype", type);
    $.ajax({
        type: "POST",
        url: "../logm/selection",
        processData: false,
        contentType: false,
        data: firm
    });
    if (window.location.href.indexOf('hybrid') !== -1) {
        window.location = "../hybrid"
    } else {
        if (window.location.href.indexOf('main') !== -1) {
            window.location = "../main"
        } else if (window.location.href.indexOf('raw') !== -1) {
            window.location = "../raw"
        }
        else {
            fillthem()
        }
    }
});