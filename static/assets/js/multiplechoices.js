/**
 * Created by theo on 7/4/17.
 */

var note = 0;

$(document).ready(function () {
    console.log(window.location.href);
    if (!window.location.href.indexOf('quizz') !== -1) {
        getimg();
    }

});


function getimg() {
    $.ajax({
        type: "GET",
        url: "./getimg",
        success: function (data) {
            console.log(data);
            $("#disp").attr("src", "/static/" + data);
        }
    });
}


$("#0").click(function (event) {

    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {
        event.preventDefault();
        var text = $("#0").text().split(' ').join('_');
        console.log(text);
        $.ajax({
            type: "POST",
            url: "./savemultiple",
            data: {
                'name': text,
                'url': $("#disp").attr('src')
            },
            success: function (data) {
                console.log(data)
            }
        });
    }
});

$("#1").click(function (event) {
    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {
        event.preventDefault();
        var text = $("#1").text().split(' ').join('_');
        ;
        $.ajax({
            type: "POST",
            url: "./savemultiple",
            data: {
                'name': text,
                'url': $("#disp").attr('src')
            },
            success: function (data) {
                console.log(data)
            }
        });
    }
});

$("#2").click(function (event) {
    console.log(window.location.href);
    if (window.location.href.indexOf('quizz') !== -1) {
        note = 5;
        done();


    } else {

        event.preventDefault();
        var text = $("#2").text().split(' ').join('_');
        $.ajax({
            type: "POST",
            url: "./savemultiple",
            data: {
                'name': text,
                'url': $("#disp").attr('src')
            },
            success: function (data) {
                console.log(data)
            }
        });
    }
});

$("#3").click(function (event) {
    if (window.location.href.indexOf('quizz') !== -1) {
        done();

    } else {

        event.preventDefault();
        var text = $("#3").text().split(' ').join('_');

        $.ajax({
            type: "POST",
            url: "./savemultiple",
            data: {
                'name': text,
                'url': $("#disp").attr('src')
            },

            success: function (data) {
                console.log(data)
            }
        });
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