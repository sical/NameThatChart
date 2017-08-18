/**
 * Created by theo on 8/2/17.
 */
var type;
var info;
var debut;
var baseu;
var where;


$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    if (where.indexOf('quizz') !== -1) {
        fillthem2();
        $("#gen").hide();
    } else {
        waitsetup(false);
        fillthem();
    }
});

$('body').on('click', '#img', function () {
    $(".cont").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
});

$('body').on('click', '#save', function () {
    var test = $('#fill').find(".selec").length;
    if (test == 0) {

    } else {
        waitsetup(true);
        if (where.indexOf('quizz') !== -1) {
            var note = 0;
            if ($(this).attr("value") == 2) {
                note = 4
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
                    window.location = baseu + "main"
                }
            })
        } else {
            var form = new FormData();
            form.append("idimage", $('.selec').attr("value"));
            form.append("idtype", type);
            $.ajax({
                type: "POST",
                url: baseu + "saveselect",
                processData: false,
                contentType: false,
                data: form,
                success: function () {
                    if (where.indexOf('main') !== -1) {
                        window.location = baseu + "main"
                    } else if (where.indexOf('raw') !== -1) {
                        window.location = baseu + "raw"
                    }
                    else {
                        $("#title").text(" Select the picture which best describe : ");
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
        url: baseu + "getselect",
        processData: false,
        contentType: false,
        success: function (data) {

            info = JSON.parse(data);
            $("#title").append(info.name);
            type = info.idtype;

            var fin = new Date();
            console.log(debut.getTime() + " debut");
            console.log(fin.getTime() + " fin");
            console.log(fin.getTime() - debut.getTime() + " diff");
            if (fin.getTime() - debut.getTime() > 5000) {
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
                    url: baseu + "logm/selection",
                    processData: false,
                    contentType: false,
                    data: form
                });
                $(".cont").css("display", "inline-block");
                $("#load").css("display", "none");

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
                    url: baseu + "logm/selection",
                    processData: false,
                    contentType: false,
                    data: form
                });
                setTimeout(function () {
                    console.log("AAAAAAAAAuUuUUu");
                    $(".cont").css("display", "inline-block");
                    $("#load").css("display", "none");
                }, (5000 - (fin.getTime() - debut.getTime())));
            }


        }
    });
}

function fillthem2() {
    $("#fill").empty();
    var imgues = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_205.gif", "static/assets/img/datasets/quizz/1.png", "static/assets/img/datasets/quizz/0.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_224.gif", "static/assets/img/datasets/quizz/3.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_91.gif"];
    $("#title").append("Histogram");
    var i = 0;
    imgues.forEach(function (img) {
        $("#fill").append("<img class='imgsel cont' value='" + i + "' src=" + img + " />")
    })
}

$('body').on('click', '#skip', function () {
    waitsetup(false);
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
        url: baseu + "logm/selection",
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
        }
        else {
            $("#title").text("Select the picture which best describe ");
            fillthem()
        }
    }
    $(".cont").each(function () {
        $(this).removeClass('unselec')
    });
    $('#fill').find(".selec").removeClass("selec");

});

function waitsetup(test) {
    debut = new Date();
    console.log(debut.getTime());
    if (test) {
        $(".cont").css("display", "none");
        $("#vald").css("display", "inline-block");
        setTimeout(function () {
            $("#load").css("display", "inline-block");
            $("#vald").css("display", "none");
        }, (1800));
    } else {
        $(".cont").css("display", "none");
        $("#load").css("display", "inline-block");
    }
}