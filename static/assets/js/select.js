/**
 * Created by theo on 8/2/17.
 */
var type;
var info;
var debut;
var baseu;
var where;
var ids;

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    if (where.indexOf('quizz') !== -1) {
        $("#report").hide();
        waitsetup(false);
        fillthem2();


    } else if (where.indexOf('generated') !== -1) {
        waitsetup();
        gen();
    } else {
        waitsetup(false);
        fillthem();
    }
});

$('body').on('click', '.cont', function () {
    $(".cont").each(function () {
        $(this).addClass('unselec');
        $(this).css('border', 'solid 2px')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).css('border', 'solid limegreen 5px');
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
                    setTimeout(function () {
                        $("#upl").css("display", "none");
                        window.location = baseu + "main"
                    }, (1700));
                }
            })
        } else {
            var form = new FormData();
            form.append("idimage", $('.selec').attr("value"));
            form.append("idtype", type);
            form.append("url", window.location.href);
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
    clearsel();
    if (where.indexOf('quizz') !== -1) {

    } else {
        var images;
        $.ajax({
            type: "GET",
            url: baseu + "getselect",
            processData: false,
            contentType: false,
            success: function (data) {

                info = JSON.parse(data);
                window.history.pushState("", "", gethash());
                $("#title").append(info.name);
                type = info.idtype;

                var fin = new Date();
                if (fin.getTime() - debut.getTime() > 2500) {
                    images = info.imgs;
                    var image;
                    ids = [];

                    $("#fill").find(".cont").each(function () {
                        image = images.pop();
                        ids.push(image.idimage);
                        $(this).attr("value", image.idimage);
                        $(this).attr("src", image.path);

                    });

                    var form = new FormData();
                    form.append("action", "visible");
                    form.append("ids", ids);
                    form.append("idtype", type);
                    form.append("url", window.location.href);

                    $.ajax({
                        type: "POST",
                        url: baseu + "logm/selection",
                        processData: false,
                        contentType: false,
                        data: form
                    });
                    $(".cont").css("display", "inline");
                    $("#title").css("display", "inline-block");
                    $("#btn").css("display", "inline-block");
                    $("#load").css("display", "none");
                    $("#upl").css("display", "none");

                } else {
                    images = info.imgs;
                    var image;
                    ids = [];

                    $("#fill").find(".cont").each(function () {
                        image = images.pop();
                        ids.push(image.idimage);
                        $(this).attr("value", image.idimage);
                        $(this).attr("src", image.path);
                    });

                    var form = new FormData();
                    form.append("ids", ids);
                    form.append("action", "visible");
                    form.append("idtype", type);
                    form.append("url", window.location.href);
                    $.ajax({
                        type: "POST",
                        url: baseu + "logm/selection",
                        processData: false,
                        contentType: false,
                        data: form
                    });
                    setTimeout(function () {
                        $(".cont").css("display", "inline");
                        $("#title").css("display", "inline-block");
                        $("#btn").css("display", "inline-block");
                        $("#load").css("display", "none");
                        $("#upl").css("display", "none");
                    }, (2500 - (fin.getTime() - debut.getTime())));
                }


            }

        });
    }
}

function fillthem2() {
    var imgues = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_205.gif", "static/assets/img/datasets/quizz/1.png", "static/assets/img/datasets/quizz/0.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_224.gif", "static/assets/img/datasets/quizz/3.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/BarGraph_91.gif"];
    $("#title").append("'Histogram'");
    var i = 0;
    $("#fill").find(".cont").each(function () {
        $(this).attr("value", i);
        $(this).attr("src", imgues[i]);
        i++
    });

    setTimeout(function () {
        $(".cont").css("display", "inline-block");
        $("#title").css("display", "inline-block");
        $("#btn").css("display", "inline-block");
        $("#load").css("display", "none");
        $("#upl").css("display", "none");
    }, (1800));
}

$('body').on('click', '#skip', function () {


    waitsetup(false);
    if (where.indexOf('quizz') !== -1) {
        var note = 0;

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
                    $("#upl").css("display", "none");
                    window.location = baseu + "main"
                }, (1700));
            }
        })
    } else {
        var firm = new FormData();
        firm.append("action", "skip");
        firm.append("ids", ids);
        firm.append("idtype", type);
        firm.append("url", window.location.href);
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
    }
});

function waitsetup(test) {
    debut = new Date();
    if (test) {
        $(".cont").css("display", "none");
        $("#upl").css("display", "inline-block");
        $("#load").css("display", "inline-block");
        $("#title").css("display", "none");
        $("#btn").css("display", "none");

    } else {
        $(".cont").css("display", "none");
        $("#load").css("display", "inline-block");
        $("#title").css("display", "none");
        $("#btn").css("display", "none");
        $("#upl").css("display", "inline-block");

    }
}

function clearsel() {
    $(".cont").each(function () {
        $(this).removeClass('unselec');
        $(this).removeClass('selec');
        $(this).css('border', 'solid 2px');
        $(this).css('opactity', '1');
    });
}

function gethash() {
    var str = "";
    info.imgs.forEach(function (row) {
        str += row.idimage + "-";
    });
    str = str.substr(0, str.length - 1);
    str += "-|" + info.idtype + "|" + info.name;
    var base = baseu + "generated/";
    var hash = $.base64.encode('selectimg/' + str);
    return base + hash

}

function gen() {
    if (where.indexOf('quizz') !== -1) {

    } else {
        var images;
        var form = new FormData();
        var temp = $("#id").val();

        temp = temp.split("-");
        var types = temp.pop();

        types = types.split("|");

        var tempstr = "";
        temp.forEach(function (row) {
            tempstr += row + " or idimage= "
        });

        type = types[1];
        tempstr = tempstr.substr(0, tempstr.length - 13);
        form.append("action", tempstr);


        $.ajax({
            type: "POST",
            url: baseu + "getimgbyid",
            processData: false,
            contentType: false,
            data: form,
            success: function (data) {
                info = JSON.parse(data);
                info = JSON.parse(info);

                $("#title").append(types[2]);

                var fin = new Date();
                if (fin.getTime() - debut.getTime() > 5000) {
                    images = info;
                    var image;
                    ids = [];

                    $("#fill").find(".cont").each(function () {
                        image = images.pop();
                        ids.push(image.idimage);
                        $(this).attr("value", image.idimage);
                        $(this).attr("src", image.path);

                    });

                    var form = new FormData();
                    form.append("action", "visible");
                    form.append("ids", ids);
                    form.append("idtype", types[1]);
                    form.append("url", window.location.href);
                    $.ajax({
                        type: "POST",
                        url: baseu + "logm/selection",
                        processData: false,
                        contentType: false,
                        data: form
                    });
                    $(".cont").css("display", "inline");
                    $("#title").css("display", "inline-block");
                    $("#btn").css("display", "inline-block");
                    $("#load").css("display", "none");
                    $("#upl").css("display", "none");

                } else {
                    images = info;
                    var image;
                    ids = [];
                    $("#fill").find(".cont").each(function () {
                        image = images.pop();
                        ids.push(image.idimage);
                        $(this).attr("value", image.idimage);
                        $(this).attr("src", image.path);
                    });

                    var form = new FormData();
                    form.append("ids", ids);
                    form.append("action", "visible");
                    form.append("idtype", types[1]);
                    form.append("url", window.location.href);
                    $.ajax({
                        type: "POST",
                        url: baseu + "logm/selection",
                        processData: false,
                        contentType: false,
                        data: form
                    });
                    setTimeout(function () {
                        $(".cont").css("display", "inline");
                        $("#title").css("display", "inline-block");
                        $("#btn").css("display", "inline-block");
                        $("#load").css("display", "none");
                        $("#upl").css("display", "none");
                    }, (2500 - (fin.getTime() - debut.getTime())));
                }


            }

        });
    }
}