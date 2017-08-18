/**
 * Created by theo on 8/2/17.
 */
var started = true;
var debut;
var id;
var baseu;
var where;
$(document).ready(function () {

        waitsetup();
        where = window.location.pathname;
        baseu = window.location.href.replace(where, "") + "/";
        document.getElementById("tofill").focus();
        if (window.location.href.indexOf('quizz') !== -1) {
            $("#gen").hide();

            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 1000) {
                $("#img").attr("src", "/static/assets/img/datasets/quizz/3.JPG");
                $("#img").css("opacity", "1");
                $("#load").css("visibility", "hidden");
            } else {
                $("#img").attr("src", "/static/assets/img/datasets/quizz/3.JPG");
                setTimeout(function () {
                    $("#img").css("opacity", "1");
                    $("#load").css("visibility", "hidden");
                }, (1000 - (fin.getTime() - debut.getTime())));
            }


        } else if (window.location.href.indexOf('generated') !== -1) {
            gen();
        } else {
            waitandload();
        }
    }
);

$("#nd").click(function (event) {
    event.preventDefault();
    report("no_display")
});

$("#ii").click(function (event) {
    event.preventDefault();
    report("Inappropriate_image")
});

$("#hmc").click(function (event) {
    event.preventDefault();
    report("miss_classification")
});

function report(string) {
    $.ajax({
        type: "POST",
        url: baseu + "report/" + string,
        processData: false,
        contentType: false,
        success: function (data) {
            pop();
            $("#skip").click()
        }
    });
}

$('body').on('click', '#save', function () {
    if ($("#btn").find("input") != undefined) {
        $("#btn").find("input").remove();
        $("#gen").show();
    }
    waitsetup();

    var text = $("#tofill").val();
    $("#tofill").val('');
    if (window.location.href.indexOf('quizz') !== -1) {
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
                window.location = baseu + "quizz"
            }
        })
    } else {

        var form = new FormData();
        var reg = /[\(,\)\\~\`\"\{\}\`\'\=\#][^²;:\\\/£$*¤µ¨%§!?.&\n\r><@]*/ig;
        text = text.replace(reg, "");
        form.append("name", text);
        form.append("id", id);
        pop();

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
                        window.location = baseu + "main"
                    }
                    else {
                        waitandload();

                    }


                }
            }
        });
    }
});

$('body').on('click', '#skip', function () {
    if ($("#btn").find("input") != undefined) {
        $("#btn").find("input").remove();
        $("#gen").show();
    }
    waitsetup();
    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("id", id);
    $.ajax({
        type: "POST",
        url: "../logaction",
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
            window.location = baseu + "main"
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

function pop() {
    $("#pop").show();
    $("#pop").delay(4300).fadeOut(500);
}

function waitandload() {
    $.ajax({

        type: "GET",
        url: baseu + "getnextimg",
        processData: false,
        contentType: false,
        success: function (data) {
            var fin = new Date();
            data = JSON.parse(data);
            console.log(data);
            id = data[1];
            window.history.pushState("", "", gethash());
            console.log(gethash());
            if (fin.getTime() - debut.getTime() > 1000) {
                $("#img").attr("src", data[0]);
                $("#img").css("opacity", "1");
                $("#load").css("visibility", "hidden");
            } else {
                $("#img").attr("src", data[0]);
                setTimeout(function () {
                    $("#img").css("opacity", "1");
                    $("#load").css("visibility", "hidden");
                }, (1000 - (fin.getTime() - debut.getTime())));
            }
            var furm = new FormData();
            furm.append("action", "page loaded");
            furm.append("id", id);
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
function waitsetup() {
    debut = new Date();
    $("#load").css("visibility", "visible");
    $("#img").css("opacity", "0");
}


$("#gen").click(function () {
    hash();
});

function hash() {
    $("#gen").hide();
    $("#btn").append("<input type='text' value='" + gethash() + "'/>")
}

function gethash() {
    base = baseu + "generated/";
    var hash = $.base64.encode('textualimg/' + id);
    return base + hash
}