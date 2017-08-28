/**
 * Created by theo on 8/2/17.
 */
var started = true;
var debut;
var id;
var baseu;
var where;

$(document).ready(function () {

    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    waitsetup(false);
    document.getElementById("tofill").focus();
    if (where.indexOf('quizz') !== -1) {
        $("#report").hide();
        var fin = new Date();
        if (fin.getTime() - debut.getTime() > 3000) {
            $("#img").attr("src", "/static/assets/img/datasets/quizz/3.JPG");
            $("#img").css("display", "inline-block");
            $("#load").css("display", "none");
        } else {
            $("#img").attr("src", "/static/assets/img/datasets/quizz/3.JPG");
            setTimeout(function () {
                $("#img").css("display", "inline-block");
                $("#load").css("display", "none");
            }, (3000 - (fin.getTime() - debut.getTime())));
        }

    } else if (where.indexOf('generated') !== -1) {
        gen();
    } else {
        waitandload();
    }
});


$('body').on('click', '#save', function () {
    if ($("#tofill").val().length > 3) {
        if ($("#btn").find("input") != undefined) {
            $("#btn").find("input").remove();
        }

        waitsetup(true);

        var text = $("#tofill").val();
        $("#tofill").val('');
        if (where.indexOf('quizz') !== -1) {
            if (text == 'tree map' || text == 'treemap') {
                note = 4
            }
            else {
                note = 0
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
        } else {

            var form = new FormData();
            var reg = /[\(,\)\\~\`\"\{\}\`\'\=\#][^²;:\\\/£$*¤µ¨%§!?.&\n\r><@]*/ig;
            text = text.replace(reg, "");
            form.append("name", text);
            form.append("id", id);
            form.append("url", window.location.href);
            $.ajax({
                type: "POST",
                url: baseu + "savetext",
                enctype: 'mulipart/form-data',
                processData: false,
                contentType: false,
                data: form,
                success: function () {
                    if (where.indexOf('hybrid') !== -1) {
                        window.location = baseu + "hybrid"
                    } else {
                        if (where.indexOf('main') !== -1) {
                            window.location = baseu + "main"
                        } else if (where.indexOf('raw') !== -1) {
                            window.location = baseu + "raw"
                        } else if (where.indexOf('generated') !== -1) {
                            waitandload();
                            var fin = new Date();
                            if (fin.getTime() - debut.getTime() > 3200) {
                                window.location = baseu + "textualimg"
                            } else {
                                setTimeout(function () {
                                    window.location = baseu + "textualimg";
                                }, (3000 - (fin.getTime() - debut.getTime())));
                            }

                        }
                        else {
                            waitandload();

                        }


                    }
                }
            });
        }
    }
});

$('body').on('click', '#skip', function () {
    if ($("#btn").find("input") != undefined) {
        $("#btn").find("input").remove();
    }
    waitsetup(false);
    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("id", id);
    firm.append("url", window.location.href);
    $.ajax({
        type: "POST",
        url: baseu + "logaction",
        processData: false,
        contentType: false,
        data: firm
    });
    if (where.indexOf('hybrid') !== -1) {
        window.location = baseu + "hybrid"
    } else {
        if (where.indexOf('main') !== -1) {
            window.location = baseu + "main"
        } else if (where.indexOf('raw') !== -1) {
            window.location = baseu + "raw"
        } else if (where.indexOf('generated') !== -1) {
            window.location = baseu + "textualimg"
        }

        else {
            waitandload();
        }
    }
});

$('body').on('input', '#tofill', function () {
    if (where.indexOf('quizz') !== -1) {
    } else {
        if ($("#tofill").val() != undefined) {
            if ($("#tofill").val().length == 1 && started) {
                started = false;
                var firm = new FormData();
                firm.append("action", "started typing");
                firm.append("id", id);
                firm.append("url", window.location.href);
                $.ajax({
                    type: "POST",
                    url: baseu + "logaction",
                    processData: false,
                    contentType: false,
                    data: firm
                });
            }
        }
    }
});

window.onkeydown = function (e) {
    var code = e.keyCode ? e.keyCode : e.which;
    if (code === 13) { //up key
        $("#save").click()
    }
};

function waitandload() {
    $.ajax({

        type: "GET",
        url: baseu + "getnextimg",
        processData: false,
        contentType: false,
        success: function (data) {
            var fin = new Date();
            data = JSON.parse(data);
            id = data[1];
            window.history.pushState("", "", gethash());
            if (fin.getTime() - debut.getTime() > 3200) {
                $("#img").attr("src", data[0]);
                $("#img").attr("value", id);
                $("#img").css("display", "inline-block");
                $("#title").css("display", "inline-block");
                $("#load").css("display", "none");
                $("#upl").css("display", "none");
            } else {
                $("#img").attr("src", data[0]);
                $("#img").attr("value", id);
                setTimeout(function () {
                    $("#title").css("display", "inline-block");
                    $("#img").css("display", "inline-block");
                    $("#load").css("display", "none");
                    $("#upl").css("display", "none");
                }, (3200 - (fin.getTime() - debut.getTime())));
            }
            var furm = new FormData();
            furm.append("action", "page loaded");
            furm.append("id", id);
            furm.append("url", window.location.href);
            $.ajax({
                type: "POST",
                url: baseu + "logaction",
                processData: false,
                contentType: false,
                data: furm
            });
        }
    });
}
function waitsetup(test) {
    debut = new Date();
    if (test) {
        $("#img").css("display", "none");
        $("#upl").css("display", "inline");
        $("#load").css("display", "inline-block");
        $("#title").css("display", "none");
    } else {
        $("#img").css("display", "none");
        $("#title").css("display", "none");
        $("#load").css("display", "inline-block");
    }

}


function gethash() {
    var base = baseu + "generated/";
    var hash = $.base64.encode('textualimg/' + id);
    return base + hash
}


function gen() {

    var form = new FormData();
    form.append("action", $("#id").val());
    $.ajax({

        type: "POST",
        url: baseu + "getimgbyid",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            var fin = new Date();
            data = JSON.parse(data);
            data = JSON.parse(data);
            id = data[0].idimage;
            if (fin.getTime() - debut.getTime() > 3000) {

                $("#img").attr("src", data[0].path);
                $("#img").attr("value", id);
                $("#img").css("display", "inline-block");
                $("#title").css("display", "inline-block");

                $("#load").css("display", "none");
            } else {

                $("#img").attr("src", data[0].path);
                $("#img").attr("value", id);
                setTimeout(function () {
                    $("#img").css("display", "inline-block");
                    $("#title").css("display", "inline-block");
                    $("#load").css("display", "none");
                }, (3000 - (fin.getTime() - debut.getTime())));
            }

        }
    });
}