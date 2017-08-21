/**
 * Created by theo on 8/2/17.
 */
var info;
var images;
var baseu;
var where;


$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    waitsetup(false);
    fillit();
});

$('body').on('click', '#skip', function () {
    var imgs = [];
    waitsetup(false);
    images.forEach(function (row) {
        imgs.push(row.idimage)
    });
    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("ids", imgs);
    firm.append("idtype", info.idtype);
    $.ajax({
        type: "POST",
        url: baseu + "logm/reverse",
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
            waitsetup(false);
            fillit()
        }
    }
});


$('body').on('click', '#save', function () {
    waitsetup(true);
    var img = $(".selec").attr("value");
    var form = new FormData();
    form.append("image", img);
    form.append("idtype", info.idtype);
    pop();
    $.ajax({
        type: "POST",
        url: baseu + "saverev",
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
                }
                else {
                    fillit()
                }
            }
        }
    });
});

function fillit() {
    $("#fill").empty();
    $.ajax({
        type: "GET",
        url: baseu + "getreverse",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            images = eval(info.images);
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 3000) {
                $("#title").text("Choose the more fitting image to describe");
                $("#title").append(" the '" + info.label + "' category");
                images.forEach(function (image) {
                    $("#fill").append("<img id='img'  value='" + image.idimage + "' src='" + image.imagepath + "'/>")
                });
                $("#load").css("display", "none");
                $("#fill").css("display", "grid");
            } else {
                setTimeout(function () {
                    $("#title").text("Choose the more fitting image to describe");
                    $("#title").append(" the '" + info.label + "' category");
                    images.forEach(function (image) {
                        $("#fill").append("<img  id='img' value='" + image.idimage + "' src='" + image.imagepath + "'/>")
                    });
                    $("#load").css("display", "none");
                    $("#fill").css("display", "grid");
                }, (3000 - (fin.getTime() - debut.getTime())));

            }
        }
    });
}

function waitsetup(test) {
    debut = new Date();


    if (test) {
        $("#fill").css("display", "none");
        $("#vald").css("display", "inline-block");
        setTimeout(function () {
            $("#load").css("display", "inline-block");
            $("#vald").css("display", "none");
        }, (1800));
    } else {
        $("#load").css("display", "inline-block");
        $("#fill").css("display", "none");
    }
}


$('body').on('click', 'img', function () {
    $("img").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
});

