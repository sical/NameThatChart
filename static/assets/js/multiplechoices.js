/**
 * Created by theo on 7/4/17.
 */

var note = 0;
var info = {};
$(document).ready(function () {
    console.log(window.location.href);
    if (window.location.href.indexOf('quizz') !== -1) {
        $("#imgdisp").attr("src", "static/assets/img/datasets/json/2_minard_map.jpg")
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
            console.log(info);

            var i = 0;
            info.types.forEach(function (type) {
                $('#' + i).text(type.label);
                $('#' + i).attr("value", type.idtype);

                i++;
            });
            $("#imgdisp").attr("src", info.image.path);
        }
    });
}


$("#0").click(function (event) {

    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {
        event.preventDefault();
        var text = $("#0").val();
        save(text)

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
        success : function () {
            getimg()
        }


    })
}

$("#1").click(function (event) {
    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {
        event.preventDefault();
        var text = $("#1").val();
        save(text)
    }
});

$("#2").click(function (event) {
    console.log(window.location.href);
    if (window.location.href.indexOf('quizz') !== -1) {
        note = 5;
        done();


    } else {

        event.preventDefault();
        var text = $("#2").val();
        save(text)
    }
});

$("#3").click(function (event) {
    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {

        event.preventDefault();
        var text = $("#3").val();
        save(text)
    }
});

function done() {
    var form = new FormData();
    console.log(note);
    form.append("note", note);
    $.ajax({
        type: "POST",
        url: "../savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            window.location = "../quizz"
        }
    })
}