/**
 * Created by theo on 8/2/17.
 */
var info;
var images;
$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "../getreverse",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            images = eval(info.images);
            $("#brand").append(" the '" + info.label + "' category");
            images.forEach(function (image) {
                $("#containssel").append("<img  class='imgtoch' value='" + image.idimage + "' src='" + image.imagepath + "'/>")
            })
        }
    });
});

$("#skip").click(function () {
    var imgs = [];
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
            fillit()
        }
    }
});

$('#containssel').on('click', 'img', function () {
    $("img").each(function () {
        $(this).addClass('unselec')
    });
    $('.selec').removeClass('selec');
    $(this).addClass('selec');
    $(this).removeClass('unselec');
});

$("#save").click(function () {
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
    $.ajax({
        type: "GET",
        url: "../getreverse",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            images = eval(info.images);
            $("#brand").text("Choose the more fitting image to describe");
            $("#brand").append(" the '" + info.label + "' category");
            $("img").remove();
            images.forEach(function (image) {
                $("#containssel").append("<img  class='imgtoch' value='" + image.idimage + "' src='" + image.imagepath + "'/>")
            })
        }
    });
}