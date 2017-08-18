/**
 * Created by theo on 8/2/17.
 */
var cat = ["reaching ..."];
var nb = 5;
var info = [];
var width = screen.width;
var height = screen.height;
var note = 0;
var baseu;
var where;

function getit() {
    var res = [];
    res.push(info[nb - 1].idimage);
    return res
}

$(document).ready(function () {
    where = window.location.pathname;
    baseu = window.location.href.replace(where, "") + "/";

    if (where.indexOf('quizz') !== -1) {
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
        waitsetup();
        fill();
    }
});

$("#tinderslide").jTinder({

    onDislike: function (item) {

        if (where.indexOf('quizz') !== -1) {
            $("#brand").text("Is this a \"" + cat[nb - 2] + " \" ?");
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
            $("#brand").text("Is this a \"" + cat[nb] + "\" ?");
            $.ajax({
                type: "POST",
                url: baseu + "saveswipe",
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
                            url: baseu + "logswipes",
                            processData: false,
                            contentType: false,
                            data: form
                        });
                    }
                }
            });
            if (item.index() == 0) {
                if (where.indexOf('main') !== -1) {
                    window.location = baseu + "main"
                } else if (where.indexOf('raw') !== -1) {
                    window.location = baseu + "raw"
                }
                else {
                    $("#vald").css("display", "inline-block");

                    setTimeout(function () {
                            $("#vlad").css("display", "none");
                            window.location = "swipes"
                        }
                        ,
                        (1700)
                    );
                }
            }
        }
    },
    onLike: function (item) {
        if (where.indexOf('quizz') !== -1) {
            $("#brand").text("Is this a \"" + cat[nb - 2] + "\" ?");
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
            $("#brand").text("Is this a \"" + cat[nb] + "\" ?");
            $.ajax({
                    type: "POST",
                    url: baseu + "saveswipe",
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
                                url: baseu + "logswipes",
                                processData: false,
                                contentType: false,
                                data: form
                            });
                        }
                    }
                }
            );
            if (item.index() == 0) {
                if (where.indexOf('main') !== -1) {
                    window.location = baseu + "main"
                } else if (where.indexOf('raw') !== -1) {
                    window.location = baseu + "raw"
                }
                else {
                    $("#vald").css("display", "inline-block");
                    setTimeout(function () {
                            $("#vlad").css("display", "none");
                            window.location = "swipes"
                        }
                        ,
                        (1700)
                    );

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
        url: baseu + "savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            window.location = baseu + "quizz"
        }
    })
}

function fill() {
    $.ajax({
        type: "GET",
        url: baseu + "getfive",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            var i = 1;
            var fin = new Date();
            if (fin.getTime() - debut.getTime() > 1700) {
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
                    $("#brand").text("Is this a \"" + cat[nb] + "\" ?");
                    i++;
                });
                $("#load").css("display", "none");
            } else {
                setTimeout(function () {
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
                            $("#brand").text("Is this a \"" + cat[nb] + "\" ?");
                            i++;
                        });
                        $("#load").css("display", "none");
                    }
                    ,
                    (1700 - (fin.getTime() - debut.getTime()))
                );
            }

            var form = new FormData();
            form.append("idimg", info[4].idimage);
            form.append("idtype", info[4].idtype);

            $.ajax({

                type: "POST",
                url: baseu + "logswipes",
                processData: false,
                contentType: false,
                data: form

            });
        }
    })
    ;
}

$("#skip").click(function () {

    var firm = new FormData();
    firm.append("action", "skip");
    firm.append("ids", info[nb - 1].idimage);
    firm.append("idtype", info[nb - 1].idtype);
    $.ajax({
        type: "POST",
        url: baseu + "logm/swipe",
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
            waitsetup();
            fill()
        }
    }
});


function waitsetup() {
    debut = new Date();
    $("#load").css("display", "inline-block");
}
