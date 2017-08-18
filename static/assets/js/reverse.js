/**
 * Created by theo on 8/2/17.
 */
var info;
var images;
var baseu;

$(document).ready(function () {
    baseu = window.location.href.replace(window.location.pathname,"") +"/";
    waitsetup();
    fillit();
});

$('body').on('click', '#skip', function () {
    var imgs = [];
    waitsetup();
    images.forEach(function (row) {
        imgs.push(row.idimage)
    });
    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("ids", imgs);
    firm.append("idtype", info.idtype);
    $.ajax({
        type: "POST",
        url: "../logm/reverse",
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
            waitsetup();
            fillit()
        }
    }
});


$('body').on('click', '#save', function () {
    waitsetup();
    console.log("LUUUUUUUU");
    var img = $(".selec").attr("value");
    var form = new FormData();
    form.append("image", img);
    form.append("idtype", info.idtype);
    pop();
    $.ajax({
        type: "POST",
        url: "../saverev",
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
        url: "../getreverse",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            images = eval(info.images);
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 1000) {
                $("#brand").text("Choose the more fitting image to describe");
                $("#brand").append(" the '" + info.label + "' category");
                images.forEach(function (image) {
                    $("#fill").append("<img id='img'  value='" + image.idimage + "' src='" + image.imagepath + "'/>")
                });
                $("#load").css("visibility", "hidden");
                $("#fill").css("visibility", "visible");
            } else {
                setTimeout(function () {
                    $("#brand").text("Choose the more fitting image to describe");
                    $("#brand").append(" the '" + info.label + "' category");
                    images.forEach(function (image) {
                        $("#fill").append("<img  id='img' value='" + image.idimage + "' src='" + image.imagepath + "'/>")
                    });
                    console.log("LAAAAAAAAAAAAAAAAAAAAAAAAA");
                    $("#load").css("visibility", "hidden");
                    $("#fill").css("visibility", "visible");
                }, (1000 - (fin.getTime() - debut.getTime())));

            }
        }
    });
}

function waitsetup() {
    debut = new Date();
    $("#load").css("visibility", "visible");
    $("#fill").css("visibility", "hidden");
}


$('body').on('click', 'img', function () {
    $("img").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
});

