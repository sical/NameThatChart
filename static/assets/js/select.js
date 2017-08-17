/**
 * Created by theo on 8/2/17.
 */
var type;
var info;
var debut;

$(document).ready(function () {
    if (window.location.href.indexOf('quizz') !== -1) {
        fillthem2();
        $("#gen").hide();
    } else {
        waitsetup();
        fillthem();
    }
});

$('#fill').on('click', 'img', function () {
    $(".cont").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
});


$('#save').click(function () {
    var test = $('#fill').find(".selec").length;
    $('#fill').find(".selec").removeClass("");
    console.log(test);
    if (test == 0) {

    } else {
        waitsetup();

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
                success: function () {
                    window.location = "../main"
                }
            })
        } else {
            var form = new FormData();
            form.append("idimage", $('.selec').attr("value"));
            form.append("idtype", type);
            $.ajax({
                type: "POST",
                url: "../saveselect",
                processData: false,
                contentType: false,
                data: form,
                success: function () {
                    if (window.location.href.indexOf('main') !== -1) {
                        window.location = "../main"
                    } else if (window.location.href.indexOf('raw') !== -1) {
                        window.location = "../raw"
                    }
                    else {
                        $("#brand").text(" Select the picture which best describe : ");
                        fillthem();
                    }
                }
            })
        }
        $(".cont").each(function () {
            $(this).removeClass('unselec')
        });
        $('#fill').find(".selec").removeClass("selec");

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

            var fin = new Date();

            if (fin.getTime() - debut.getTime() > 1500) {
                var images = info.imgs;
                var image;
                var ids = [];

                $("#fill").find(".cont").each(function () {
                    image = images.pop();
                    ids.push(image.id);
                    $(this).attr("value", image.id);
                    $(this).attr("src", image.path);

                });

                var form = new FormData();
                form.append("action", "visible");
                form.append("ids", ids);
                form.append("idtype", type);
                $.ajax({
                    type: "POST",
                    url: "../logm/selection",
                    processData: false,
                    contentType: false,
                    data: form
                });
                $(".cont").css("visibility", "visible");
                $("#load").css("visibility", "hidden");

            } else {
                var images = info.imgs;
                var image;
                var ids = [];

                $("#fill").find(".cont").each(function () {
                    image = images.pop();
                    ids.push(image.id);
                    $(this).attr("value", image.id);
                    $(this).attr("src", image.path);
                });

                var form = new FormData();
                console.log(info);
                form.append("ids", ids);
                form.append("action", "visible");
                form.append("idtype", type);
                $.ajax({
                    type: "POST",
                    url: "../logm/selection",
                    processData: false,
                    contentType: false,
                    data: form
                });
                setTimeout(function () {
                    $(".cont").css("visibility", "visible");
                    $("#load").css("visibility", "hidden");
                }, (1500 - (fin.getTime() - debut.getTime())));
            }


        }
    });
}

function fillthem2() {
    $("#fill").empty();
    var imgues = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_205.gif", "static/assets/img/datasets/quizz/1.png", "static/assets/img/datasets/quizz/0.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_224.gif", "static/assets/img/datasets/quizz/3.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_91.gif"];
    $("#brand").append("Histogram");
    var i = 0;
    imgues.forEach(function (img) {
        $("#fill").append("<img class='imgsel cont' value='" + i + "' src=" + img + " />")
    })
}

$("#skip").click(function () {
    waitsetup();
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
            $("#brand").text("Select the picture which best describe ");
            fillthem()
        }
    }
    $(".cont").each(function () {
        $(this).removeClass('unselec')
    });
    $('#fill').find(".selec").removeClass("selec");

});

function waitsetup() {
    debut = new Date();
    $(".cont").css("visibility", "hidden");
    $("#load").css("visibility", "visible");
}