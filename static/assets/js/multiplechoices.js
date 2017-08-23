/**
 * Created by theo on 7/4/17.
 */
var note = 0;
var info = {};
var id;
var baseu;
var where;
var debut;

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "");
    console.log(where.indexOf('quizz'));
    waitsetup(false);
    if (where.indexOf('quizz') !== -1) {
        var fin = new Date();

        $("#img").attr("src", "static/assets/img/datasets/json/2_minard_map.jpg");
        setTimeout(function () {
            $("#img").css("display", "inline-block");
            $(".but").css("display", "inline-block");
            $("#load").css("display", "none");
        }, (3200 - (fin.getTime() - debut.getTime())));
    } else {
        getimg();
    }
});

function getimg() {
    $.ajax({
        type: "GET",
        url: baseu + "/getimgmul",
        success: function (data) {
            info = JSON.parse(data);

            var i = 0;
            var temp;
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 3200) {
                info.types.forEach(function (type) {
                    temp = $('#' + i).text(type.label);
                    temp.attr("value", type.idtype);
                    i++;
                });
                id = info.image.id;
                $("#img").attr("src", info.image.path);
                $("#img").css("display", "inline-block");
                $(".but").css("display", "inline-block");
                $("#load").css("display", "none");

            } else {
                $("#img").attr("src", info.image.path);
                info.types.forEach(function (type) {
                    temp = $('#' + i).text(type.label);
                    temp.attr("value", type.idtype);
                    i++;
                });
                id = info.image.id;
                $("#img").attr("src", info.image.path);
                setTimeout(function () {
                    $("#img").css("display", "inline-block");
                    $(".but").css("display", "inline-block");
                    $("#load").css("display", "none");
                }, (3200 - (fin.getTime() - debut.getTime())));
            }


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
    clear();
    waitsetup(true);
    if (where.indexOf('quizz') !== -1) {
        done(text);
    } else {
        save(text)
    }
});

function clear() {
    $(".btnvali").each(function () {
        $(this).removeClass('u');
        $(this).removeClass('s');
        $(this).css("color", "#FFF");
        $(this).css("background-color", "#343d46")
    });

}


$('body').on('click', '#skip', function () {
    clear();
    waitsetup(false);
    if (where.indexOf('quizz') !== -1) {
        done("");
    } else {
        var firm = new FormData();
        firm.append("action", "skip");
        firm.append("id", id);
        $.ajax({
            type: "POST",
            url: baseu + "/logmultiple",
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
        url: baseu + "/savemultiple",
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
        url: baseu + "/savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function () {

            setTimeout(function () {
                $("#vald").css("display", "none");
                window.location = baseu + "/quizz"
            }, (1700));
        }
    })
}

function waitsetup(test) {
    debut = new Date();
    if (test) {
        $("#img").css("display", "none");
        $(".but").css("display", "none");
        $("#vald").css("display", "inline-block");
        setTimeout(function () {
            $("#load").css("display", "inline-block");
            $("#vald").css("display", "none");
        }, (1800));
    } else {
        $("#img").css("display", "none");
        $(".but").css("display", "none");
        $("#load").css("display", "inline-block");
    }

}