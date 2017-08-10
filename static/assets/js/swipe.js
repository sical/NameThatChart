/**
 * Created by theo on 8/2/17.
 */
var cat = ["reaching ..."];
var nb = 5;
var info = [];
var width = screen.width;
var height = screen.height;
var note = 0;

function getit() {
    var res = [];
    res.push(info[nb - 1].idimage);
    return res
}

$(document).ready(function () {
    if (window.location.href.indexOf('quizz') !== -1) {
        var path = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis16cat/BubbleChart_147.jpg", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/AreaGraph_16.gif", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/ParetoChart_499.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/RadarPlot_640.jpg", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/VennDiagram_1024.gif"];
        cat = ["scatter plot", "Area chart", "Bar Chart", "Radar Chart", "Bubble Chart"];

        for (var i = 0; i < 5; i++) {
            var temp = $('.pane' + (i + 1));
            temp.css("width", "75%");
            temp.css("height", "55%");
            temp.css("max-width", "800px");
            temp.css("background-color", "#FFF");
            temp.css("border", "solid 1px");
            temp.css("background-image", 'url("' + path[i] + '")');
            $("#" + i + "_txt").text("");
            $("#brand").text("Does this belongs in \"" + cat[4] + "\" category");
        }
    } else {
        $("#load").css("visibility", "visible");
        fill();
    }
});

$("#tinderslide").jTinder({

    onDislike: function (item) {

        if (window.location.href.indexOf('quizz') !== -1) {
            $("#brand").text("Does this belongs in \"" + cat[nb - 2] + " \" category");
            nb -= 1;
            if (item.index() == 0 || item.index() == 2 || item.index() == 4) {
                note += 1
            }
            if (item.index() == 0) {

                done(note);
            }
        } else {
            nb = nb - 1;
            var form = new FormData();
            form.append("vote", false);
            form.append("idimage", info[item.index()].idimage);
            form.append("idtype", info[item.index()].idtype);
            $("#brand").text("Does this belongs in \"" + cat[nb] + "\" category");
            $.ajax({
                type: "POST",
                url: "../saveswipe",
                processData: false,
                contentType: false,
                data: form,
                success: function () {
                    if (item.index() - 1 >= 0) {
                        var form = new FormData();
                        form.append("idimg", info[item.index() - 1].idimage);
                        form.append("idtype", info[item.index() - 1].idtype);
                        $.ajax({
                            type: "POST",
                            url: "../logswipes",
                            processData: false,
                            contentType: false,
                            data: form
                        });
                    }
                }
            });
            if (item.index() == 0) {
                if (window.location.href.indexOf('main') !== -1) {
                    window.location = "../main"
                } else if (window.location.href.indexOf('raw') !== -1) {
                    window.location = "../raw"
                }
                else {
                    $("#load").css("visibility", "visible");
                    window.location = "swipes"
                }
            }
        }
    },
    onLike: function (item) {
        if (window.location.href.indexOf('quizz') !== -1) {
            $("#brand").text("Does this belongs in \"" + cat[nb - 2] + "\" category");
            nb -= 1;
            if (item.index() == 1 || item.index() == 3) {
                note += 1
            }
            if (item.index() == 0) {
                done(note);
            }
        } else {
            nb = nb - 1;
            var form = new FormData();
            form.append("vote", true);
            form.append("idimage", info[item.index()].idimage);
            form.append("idtype", info[item.index()].idtype);
            $("#brand").text("Does this belongs in \"" + cat[nb] + "\" category");
            $.ajax({
                    type: "POST",
                    url: "../saveswipe",
                    processData: false,
                    contentType: false,
                    data: form,
                    success: function () {
                        if (item.index() - 1 >= 0) {
                            var form = new FormData();
                            form.append("idimg", info[item.index() - 1].idimage);
                            form.append("idtype", info[item.index() - 1].idtype);
                            $.ajax({

                                type: "POST",
                                url: "../logswipes",
                                processData: false,
                                contentType: false,
                                data: form
                            });
                        }
                    }
                }
            );
            if (item.index() == 0) {
                if (window.location.href.indexOf('main') !== -1) {
                    window.location = "../main"
                } else if (window.location.href.indexOf('raw') !== -1) {
                    window.location = "../raw"
                }
                else {
                    $("#load").css("visibility", "visible");
                    window.location = "swipes"
                }
            }
        }
    },
    animationRevertSpeed: 200,
    animationSpeed: 400,
    threshold: 1,
    likeSelector: '.like',
    dislikeSelector: '.dislike'
});

function done(val) {
    var form = new FormData();
    form.append("note", val);
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
}

function fill() {
    $.ajax({
        type: "GET",
        url: "../getfive",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            var i = 1;
            var fin = new Date();
            info.forEach(function (img) {
                cat.push(img.label);
                var temp = $('.pane' + i);
                temp.css("width", "75%");
                temp.css("height", "55%");
                temp.css("max-width", "800px");
                temp.css("background-color", "#FFF");
                temp.css("border", "solid 1px");
                temp.css("background-image", 'url("' + img.path + '")');
                temp.attr("value", img.idimage);
                $("#" + i + "_txt").text(img.label);
                $("#brand").text("Does this belongs in \"" + cat[nb] + "\" category");
                i++;
            });

            var form = new FormData();
            form.append("idimg", info[4].idimage);
            form.append("idtype", info[4].idtype);
            $("#load").css("visibility", "hidden");
            $.ajax({

                type: "POST",
                url: "../logswipes",
                processData: false,
                contentType: false,
                data: form

            });
        }
    });
}

$("#skip").click(function () {

    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("ids", info[nb - 1].idimage);
    firm.append("idtype", info[nb - 1].idtype);
    $.ajax({
        type: "POST",
        url: "../logm/swipe",
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
            fill()
        }
    }
});


function waitsetup() {
    debut = new Date();
    $("#load").css("visibility", "visible");
}
