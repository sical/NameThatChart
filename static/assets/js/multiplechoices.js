/**
 * Created by theo on 7/4/17.
 */
var note = 0;
var info;
var id;
var baseu;
var where;
var debut;
var types = [];

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    waitsetup(false);
    if (where.indexOf('quizz') !== -1) {
        $("#report").hide();
        var fin = new Date();

        $("#img").attr("src", "static/assets/img/datasets/json/2_minard_map.jpg");
        setTimeout(function () {
            $("#img").css("display", "inline-block");
            $(".but").css("display", "inline-block");
            $("#load").css("display", "none");
        }, (3200 - (fin.getTime() - debut.getTime())));
    } else if (where.indexOf('generated') !== -1) {
        gen();
    } else {
        getimg();
    }
});

function getimg() {
    $.ajax({
        type: "GET",
        url: baseu + "getimgmul",
        success: function (data) {
            info = JSON.parse(data);
            id = info.image.id;
            window.history.pushState("", "", gethash());
            var i = 0;
            var temp;
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 2200) {
                info.types.forEach(function (type) {
                    temp = $('#' + i).text(type.label);
                    temp.attr("value", type.idtype);
                    i++;
                });
                id = info.image.id;
                $("#img").attr("src", info.image.path);
                $("#img").attr("value", id);
                $("#img").css("display", "inline-block");
                $(".but").css("display", "inline-block");
                $("#load").css("display", "none");

            } else {
                id = info.image.id;
                $("#img").attr("src", info.image.path);
                info.types.forEach(function (type) {
                    temp = $('#' + i).text(type.label);
                    temp.attr("value", type.idtype);
                    i++;
                });

                $("#img").attr("src", info.image.path);
                $("#img").attr("value", id);
                setTimeout(function () {
                    $("#img").css("display", "inline-block");
                    $(".but").css("display", "inline-block");
                    $("#load").css("display", "none");
                }, (2200 - (fin.getTime() - debut.getTime())));
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
    $(this).css("background-color", "#343d46");
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
            url: baseu + "logmultiple",
            processData: false,
            contentType: false,
            data: firm
        });
        getimg();
    }
});

function save(idtype) {
    var form = new FormData();
    form.append("idimage", id);
    form.append("idtype", idtype);
    $.ajax({
        type: "POST",
        url: baseu + "savemultiple",
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
        url: baseu + "savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function () {

            setTimeout(function () {
                $("#vald").css("display", "none");
                window.location = baseu + "quizz"
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


function gethash() {
    var temp = "";
    info.types.forEach(function (type) {
        temp += type.idtype + "%" + type.label + "|"
    });

    var base = baseu + "generated/";
    var hash = $.base64.encode('multiple/' + id + "!" + temp);
    return base + hash
}


function gen() {
    var form = new FormData();
    var tempu = $("#id").val();

    tempu = tempu.split("!");
    var img = tempu[0];
    id = img;
    tempu.splice(0, 1);

    var tempt = tempu[0].split("|");
    tempt.forEach(function (row) {
        types.push(row.split("%"))
    });

    types.pop();
    form.append("action", img);

    $.ajax({
        type: "POST",
        url: baseu + "getimgbyid",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            info = JSON.parse(data);
            info = JSON.parse(info)[0];
            var i = 0;
            var temp;
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 2200) {
                types.forEach(function (type) {
                    temp = $('#' + i).text(type[1]);
                    temp.attr("value", type[0]);
                    i++;
                });

                $("#img").attr("src", info.path);
                $("#img").attr("value", id);
                $("#img").css("display", "inline-block");
                $(".but").css("display", "inline-block");
                $("#load").css("display", "none");

            } else {
                $("#img").attr("value", id);
                $("#img").attr("src", info.path);
                types.forEach(function (type) {
                    temp = $('#' + i).text(type[1]);
                    temp.attr("value", type[0]);
                    i++;
                });
                $("#img").attr("src", info.path);
                setTimeout(function () {
                    $("#img").css("display", "inline-block");
                    $(".but").css("display", "inline-block");
                    $("#load").css("display", "none");
                }, (2200 - (fin.getTime() - debut.getTime())));
            }


        }
    });
}