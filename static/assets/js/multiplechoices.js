/**
 * Created by theo on 7/4/17.
 */
var note = 0;
var info = {};
var id;

$(document).ready(function () {
    console.log(window.location.href);
    if (window.location.href.indexOf('quizz') !== -1) {
        $("#img").attr("src", "static/assets/img/datasets/json/2_minard_map.jpg")
    } else {
        getimg();
    }
});

function getimg() {
    $.ajax({
        type: "GET",
        url: "../getimgmul",
        success: function (data) {
            info = JSON.parse(data);
            var i = 0;
            var temp;
            info.types.forEach(function (type) {
                temp = $('#' + i).text(type.label);
                temp.attr("value", type.idtype);
                i++;
            });
            id = info.image.id;
            $("#img").attr("src", info.image.path);
        }
    });
}

$('body').on('click', '.btnvali', function () {
    $(".btnvali").each(function () {
        $(this).addClass('u');
        $(this).css("color", "#FFF");
        $(this).css("background-color", "#65737e")
    });
    $('.s').removeClass('s');
    $(this).addClass('s');
    $(this).css("color", "lightgreen");
    $(this).css("background-color", "#343d46;");
    $(this).removeClass('u');
});

$('body').on('click', '#save', function () {
    var text = $(".s").val();
    if (window.location.href.indexOf('quizz') !== -1) {
        done(text);
    } else {
        save(text)
    }
});

$('body').on('click', '#skip', function () {
    if (window.location.href.indexOf('quizz') !== -1) {
        done("");
    } else {
        var firm = new FormData();
        firm.append("action", "skip");
        firm.append("id", id);
        $.ajax({
            type: "POST",
            url: "../logmultiple",
            processData: false,
            contentType: false,
            data: firm
        });
        getimg();
    }
});

function save(idtype) {
    var form = new FormData();
    form.append("idimage", info.image.id);
    form.append("idtype", idtype);
    $.ajax({
        type: "POST",
        url: "../savemultiple",
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            getimg()
        }
    })
}


function done(text) {
    if (text == "Minard's map") {
        note += 5;
    }
    var form = new FormData();
    form.append("note", note);
    $.ajax({
        type: "POST",
        url: "../savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            window.location = "../quizz"
        }
    })
}
