/**
 * Created by theo on 8/2/17.
 */
var info;
var images;
var baseu;
var where;
var type;

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";
    if (where.indexOf('generated') !== -1) {
        waitsetup(false);
        gen();
    } else {
        waitsetup(false);
        fillit();
    }

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
    form.append("idtype", type);
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
            window.history.pushState("", "", gethash());
            images = eval(info.images);
            type = info.idtype;
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 3000) {
                $("#title").text("Choose the more fitting image to describe");
                $("#title").append(" the '" + info.label + "' category");
                images.forEach(function (image) {
                    $("#fill").append("<img id='img'  value='" + image.idimage + "' src='" + image.path + "'/>")
                });
                $("#load").css("display", "none");
                $("#fill").css("display", "grid");
            } else {
                setTimeout(function () {
                    $("#title").text("Choose the more fitting image to describe");
                    $("#title").append(" the '" + info.label + "' category");
                    images.forEach(function (image) {
                        $("#fill").append("<img  id='img' value='" + image.idimage + "' src='" + image.path + "'/>")
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

function gethash() {

    var str = "";
    info.images.forEach(function (row) {
        str += row.idimage + "-";
    });
    str = str.substr(0, str.length - 1);
    str += "-|" + info.idtype + "|" + info.label;

    var base = baseu + "generated/";
    var hash = $.base64.encode('reverse/' + id);
    return base + hash
}


function gen() {
    $("#fill").empty();
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
    tempstr = tempstr.substr(0, tempstr.length - 14);

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
            images = info;
            type = types[1];
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 3000) {

                $("#title").text("Choose the more fitting image to describe");
                $("#title").append(" the '" + types[2] + "' category");

                images.forEach(function (image) {
                    $("#fill").append("<img id='img'  value='" + image.idimage + "' src='" + image.path + "'/>")
                });
                $("#load").css("display", "none");
                $("#fill").css("display", "grid");
            } else {
                setTimeout(function () {
                    $("#title").text("Choose the more fitting image to describe");
                    $("#title").append(" the '" + types[2] + "' category");
                    images.forEach(function (image) {
                        $("#fill").append("<img  id='img' value='" + image.idimage + "' src='" + image.path + "'/>")
                    });
                    $("#load").css("display", "none");
                    $("#fill").css("display", "grid");
                }, (3000 - (fin.getTime() - debut.getTime())));

            }
        }
    });
}