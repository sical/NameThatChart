/**
 * Created by theo on 8/2/17.
 */
var started = true;
$(document).ready(function () {
        document.getElementById("value").focus();
        if (window.location.href.indexOf('quizz') !== -1) {
            $("#imgdisp").attr("src", "static/assets/img/datasets/json/3.JPG");
            $("#skip").hide();
        } else {
            $.ajax({
                type: "GET",
                url: "../getnextimg",
                processData: false,
                success: function (data) {
                    console.log("LAAAAAA "+data );
                    $("#imgdisp").attr("src", data);
                    furm = new FormData();
                    furm.append("action", "page loaded");
                    $.ajax({
                        type: "POST",
                        url: "../logaction",
                        processData: false,
                        contentType: false,
                        data: furm
                    });
                }
            });
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
        url: "../report/" + string,
        processData: false,
        contentType: false,
        success: function (data) {
            pop();
            $("#skip").click()
        }
    });
}

$("#save").click(function () {
    var text = $("#value").val();
    $("#value").val('');
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
            url: "../savenote",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                window.location = "../quizz"
            }
        })
    } else {

        var form = new FormData();
        var reg = /[\(,\)\\~\`\"\{\}\+\=\#\\][^²;:\\\/£$*¤µ¨%§!?.&\n\r><@]*/ig;
        text = text.replace(reg, "");
        form.append("name", text);
        pop();

        $.ajax({
            type: "POST",
            url: "./savetext",
            enctype: 'mulipart/form-data',
            processData: false,
            contentType: false,
            data: form,
            success: function () {
                if (window.location.href.indexOf('hybrid') !== -1) {
                    window.location = "../hybrid"
                } else {
                    if (window.location.href.indexOf('main') !== -1) {
                        window.location = "../main"
                    } else if (window.location.href.indexOf('raw') !== -1) {
                        window.location = "../raw"
                    }
                    else {
                        $.ajax({
                            type: "GET",
                            url: "../getnextimg",
                            processData: false,
                            contentType: false,
                            success: function (data) {
                                $("#imgdisp").attr("src", data);
                            }
                        });
                    }
                }
            }
        });
    }
});

$("#skip").click(function () {
    firm = new FormData();
    firm.append("action", "skip");
    $.ajax({
        type: "POST",
        url: "../logaction",
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

            $.ajax({
                type: "GET",
                url: "../getnextimg",
                processData: false,
                contentType: false,
                success: function (data) {
                    $("#imgdisp").attr("src", data);

                }
            });
        }
    }
});

$("#value").on('input', function () {
    if (window.location.href.indexOf('quizz') !== -1) {
    } else {
        if ($("#value").val() != undefined) {
            if ($("#value").val().length == 1 && started) {
                started = false;
                firm = new FormData();
                firm.append("action", "started typing");
                $.ajax({
                    type: "POST",
                    url: "../logaction",
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