/**
 * Created by theo on 8/2/17.
 */

var cat = [""];
var nb = 5;
var info = [];
var width = screen.width;
var height = screen.height;
var note = 0;
var baseu;
var where;
var tempg;
var s = false;
function getit() {
    var res = [];
    res.push(info[nb - 1].id);
    return res
}

$(document).ready(function () {
    where = window.location.pathname;
    console.log(where);
    baseu = window.location.href.replace(where, "") + "/";
    if (where.indexOf('quizz') !== -1) {
        var path = ["https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis16cat/BubbleChart_147.jpg", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/AreaGraph_16.gif", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/ParetoChart_499.png", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/RadarPlot_640.jpg", "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/downloadApi/vis10cat/VennDiagram_1024.gif"];
        cat = ["Saving .... ", "scatter plot", "Area chart", "Bar Chart", "Radar Chart", "Bubble Chart"];
        $("#report").hide();
        for (var i = 0; i < 5; i++) {
            var temp = $('.pane' + (i + 1));
            temp.css("width", "75%");
            temp.css("height", "55%");
            temp.css("max-width", "800px");
            temp.css("background-color", "#FFF");
            temp.css("border", "solid 1px");
            temp.css("background-image", 'url("' + path[i] + '")');
            $("#" + i + "_txt").text("");
        }
        $("#title").text("is this a \"" + cat[5] + "\" category");
    }
    else if (where.indexOf('generated') !== -1) {
        waitsetup();
        gen();
    } else {
        waitsetup();
        fill();
    }
})
;

$("#tinderslide").jTinder({
    number: nb,
    onDislike: function (item) {
        tempg = this;
        s = true;
        if (item.index() > nb - 1) {
            item.prevObject.remove(item.index());

            tempg.number = nb;

        } else {

            if (where.indexOf('quizz') !== -1) {
                $("#title").text("Is this a \"" + cat[nb - 1] + " \" ?");
                if (nb == 1 || nb == 3 || nb == 5) {
                    note += 1
                }
                if (nb == 1) {
                    $("#upl").css("display", "inline-block");
                    $("#load").css("display", "inline-block");
                    $("#title").css("display", "none");
                    done(note);
                }

            } else {

                var form = new FormData();
                form.append("vote", false);
                form.append("idimage", info[nb - 1].id);
                form.append("idtype", info[nb - 1].idtype);
                form.append("url", window.location.href);
                $("#title").text("Is this a \"" + cat[nb - 1] + "\" ?");
                nb = nb - 1;
                $.ajax({
                    type: "POST",
                    url: baseu + "saveswipe",
                    processData: false,
                    contentType: false,
                    data: form,
                    success: function () {
                        if (nb > 0) {
                            var form = new FormData();
                            form.append("idimg", info[nb - 1].id);
                            form.append("idtype", info[nb - 1].idtype);
                            form.append("url", window.location.href);
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
                if (nb == 0) {
                    $("#title").css("display", "none");
                    if (where.indexOf('main') !== -1) {
                        window.location = baseu + "main"
                    } else if (where.indexOf('raw') !== -1) {
                        window.location = baseu + "raw"
                    }
                    else {
                        $("#upl").css("display", "inline-block");
                        $("#load").css("display", "inline-block");
                        $("#title").css("display", "none");

                        setTimeout(function () {
                                $("#upl").css("display", "none");
                                $("#load").css("display", "none");
                                window.location = baseu + "swipes"
                            }
                            ,
                            (1700)
                        );

                    }
                }
            }
        }
    },
    onLike: function (item) {
        tempg = this;
        s = true;
        if (where.indexOf('quizz') !== -1) {
            $("#title").text("Is this a \"" + cat[nb - 1] + "\" ?");

            if (item.index() == 1 || item.index() == 3) {
                note += 1
            }
            nb -= 1;
            if (item.index() == 0) {
                $("#title").css("display", "none");

                $("#upl").css("display", "inline-block");
                $("#load").css("display", "inline-block");
                done(note);
            }
        } else {

            var form = new FormData();
            form.append("vote", true);
            form.append("idimage", info[nb - 1].id);
            form.append("idtype", info[nb - 1].idtype);
            form.append("url", window.location.href);
            $("#title").text("Is this a \"" + cat[nb - 1] + "\" ?");
            nb = nb - 1;
            $.ajax({
                    type: "POST",
                    url: baseu + "saveswipe",
                    processData: false,
                    contentType: false,
                    data: form,
                    success: function () {
                        if (nb > 0) {
                            var form = new FormData();
                            form.append("idimg", info[nb - 1].id);
                            form.append("idtype", info[nb - 1].idtype);
                            form.append("url", window.location.href);

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
            if (nb == 0) {
                $("#title").css("display", "none");
                if (where.indexOf('main') !== -1) {
                    window.location = baseu + "main"
                } else if (where.indexOf('raw') !== -1) {
                    window.location = baseu + "raw"
                }
                else {
                    $("#upl").css("display", "inline-block");
                    $("#load").css("display", "inline-block");
                    $("#title").css("display", "none");


                    setTimeout(function () {
                            $("#upl").css("display", "none");
                            $("#load").css("display", "none");
                            window.location = baseu + "swipes"
                        }
                        ,
                        (1700)
                    );

                }
            }
        }
    }
    ,
    animationRevertSpeed: 200,
    animationSpeed: 400,
    threshold: 1,
    likeSelector: '.like',
    dislikeSelector: '.dislike',
})
;

function done(val) {
    var form = new FormData();
    form.append("note", val);
    $.ajax({
        type: "POST",
        url: baseu + "savenote",
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            setTimeout(function () {
                $("#upl").css("display", "none");
                $("#load").css("display", "none");
                window.location = baseu + "quizz"
            }, (1700));

        }
    })
}


$("#yes").click(function () {
    if (s) {
        $(".pane" + nb).fadeOut(500);
        setTimeout(function () {
            $(".pane" + nb + 1).css("display", "none");
        }, 500);
        tempg.onLike($(".pane" + nb));
        tempg.number = nb;
    } else {
        vote(true)
    }

});

$("#no").click(function () {
    if (s) {
        $(".pane" + nb).fadeOut(500);
        setTimeout(function () {
            $(".pane" + nb + 1).css("display", "none");
        }, 500);

        tempg.onDislike($(".pane" + nb));
        tempg.number = nb;

    } else {
        vote(false);
    }

});

function fill() {

    $.ajax({
        type: "GET",
        url: baseu + "getfive",
        processData: false,
        contentType: false,
        success: function (data) {
            info = JSON.parse(data);
            window.history.pushState("", "", gethash());
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
                    temp.attr("value", img.id);
                    $("#" + i + "_txt").text(img.label);
                    $("#title").text("Is this a \"" + cat[nb] + "\" ?");
                    i++;
                });
                $("#load").css("display", "none");
                $("#upl").css("display", "none");
                $("#title").css("display", "inline-block");

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
                            temp.attr("value", img.id);
                            $("#" + i + "_txt").text(img.label);
                            $("#title").text("Is this a \"" + cat[nb] + "\" ?");
                            i++;
                        });
                        $("#load").css("display", "none");
                        $("#upl").css("display", "none");
                        $("#title").css("display", "inline-block");

                    }
                    ,
                    (1700 - (fin.getTime() - debut.getTime()))
                );
            }

            var form = new FormData();
            form.append("idimg", info[4].id);
            form.append("idtype", info[4].idtype);
            form.append("url", window.location.href);
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

function vote(vote) {
    var temp = $('.pane' + nb);
    temp.fadeOut(500);
    setTimeout(function () {
        temp.hide();
        $(".pane" + nb + 1).css("display", "none");
        temp.css("z-index", "-4");
    }, 500);

    if (where.indexOf('quizz') !== -1) {
        $("#title").text("Is this a \"" + cat[nb - 1] + "\" ?");
        if (nb == 2 || nb == 4) {
            note += 1
        }
        nb -= 1;
        if (nb == 0) {
            $("#title").css("display", "none");
            done(note);
        }
    } else {
        var form = new FormData();
        form.append("vote", vote);
        form.append("idimage", info[nb - 1].id);
        form.append("idtype", info[nb - 1].idtype);
        form.append("url", window.location.href);
        $("#title").text("Is this a \"" + cat[nb - 1] + "\" ?");
        nb = nb - 1;
        $.ajax({
                type: "POST",
                url: baseu + "saveswipe",
                processData: false,
                contentType: false,
                data: form,
                success: function () {
                    if (nb > 0) {
                        var form = new FormData();

                        form.append("idimg", info[nb - 1].id);
                        form.append("idtype", info[nb - 1].idtype);
                        form.append("url", window.location.href);
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
        if (nb == 0) {
            $("#title").css("display", "none");
            if (where.indexOf('main') !== -1) {
                window.location = baseu + "main"
            } else if (where.indexOf('raw') !== -1) {
                window.location = baseu + "raw"
            }
            else {
                $("#upl").css("display", "inline-block");
                $("#load").css("display", "inline-block");
                $("#title").css("display", "none");

                setTimeout(function () {
                        $("#upl").css("display", "none");
                        $("#load").css("display", "none");
                        window.location = baseu + "swipes"
                    }
                    ,
                    (1700)
                );

            }
        }
    }
}

$("#skip").click(function () {
    if (where.indexOf('quizz') !== -1) {
        nb--;
        if (nb == 0) {
            $(".pane" + (nb + 1)).fadeOut(500);
            setTimeout(function () {
                $(".pane" + nb + 1).css("display", "none");
            }, 500);

            $("#upl").css("display", "inline-block");
            $("#load").css("display", "inline-block");
            $("#title").css("display", "none");

            setTimeout(function () {
                    $("#upl").css("display", "none");
                    $("#load").css("display", "none");
                    done(note)
                }
                ,
                (1700)
            );


        } else {
            if (s) {
                $(".pane" + (nb + 1)).fadeOut(500);
                setTimeout(function () {
                    $(".pane" + nb + 1).css("display", "none");
                }, 500);
                tempg.number = nb;

            } else {
                $(".pane" + (nb + 1)).fadeOut(500);
                setTimeout(function () {
                    $(".pane" + nb + 1).css("display", "none");
                }, 500);
            }
        }
    } else {
        var firm = new FormData();
        firm.append("action", "skip");
        firm.append("ids", info[nb - 1].id);
        firm.append("idtype", info[nb - 1].idtype);
        firm.append("url", window.location.href);
        $.ajax({
            type: "POST",
            url: baseu + "logm/swipe",
            processData: false,
            contentType: false,
            data: firm
        });
        nb = nb - 1;
        $("#title").text("Is this a \"" + cat[nb] + "\" ?");


        if (nb == 0) {
            if (where.indexOf('main') !== -1) {
                window.location = baseu + "main"
            } else if (where.indexOf('raw') !== -1) {
                window.location = baseu + "raw"
            }
            else {
                $("#upl").css("display", "inline-block");
                $("#load").css("display", "inline-block");
                $("#title").css("display", "inline-block");

                setTimeout(function () {
                        $("#upl").css("display", "none");
                        $("#load").css("display", "none");
                        window.location = baseu + "swipes"
                    }
                    ,
                    (1700)
                );

            }
        } else {
            if (s) {
                $(".pane" + (nb + 1)).fadeOut(500);
                setTimeout(function () {
                    $(".pane" + nb + 1).css("display", "none");
                }, 500);
                tempg.number = nb;

            } else {
                $(".pane" + (nb + 1)).fadeOut(500);
                setTimeout(function () {
                    $(".pane" + nb + 1).css("display", "none");
                }, 500);
            }
        }

    }
})
;

function waitsetup() {
    debut = new Date();
    $("#load").css("display", "inline-block");
    $("#upl").css("display", "inline-block");
    $("#title").css("display", "none");

}

function gethash() {
    var str = "";
    info.forEach(function (row) {
        str += row.id + "_" + row.label + "_" + row.idtype + "-";
    });
    str = str.substr(0, str.length - 1);
    var base = baseu + "generated/";
    var hash = $.base64.encode('swipes/' + str);
    return base + hash

}

function gen() {
    var form = new FormData();
    var temp = $("#id").val();
    temp = temp.split("-");
    console.log(temp);
    var infotemp = [];

    temp.forEach(function (row) {
        infotemp.push(row.split("_"))
    });

    var tempstr = "";
    infotemp.forEach(function (row) {
        tempstr += row[0] + " or idimage= "
    });
    tempstr = tempstr.substr(0, tempstr.length - 12);
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
            var i = 0;
            infotemp.forEach(function (row) {
                info[i]['label'] = row[1];
                info[i]['idtype'] = row[2];
                i++
            });
            console.log(info);
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
                    temp.attr("value", img.id);
                    $("#" + i + "_txt").text(img.label);
                    $("#title").text("Is this a \"" + cat[nb] + "\" ?");
                    i++;
                });
                $("#load").css("display", "none");
                $("#title").css("display", "inline-block");

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
                            temp.attr("value", img.id);
                            $("#" + i + "_txt").text(img.label);
                            $("#title").text("Is this a \"" + cat[nb] + "\" ?");
                            i++;
                        });
                        $("#load").css("display", "none");
                        $("#title").css("display", "inline-block");

                    }
                    ,
                    (1700 - (fin.getTime() - debut.getTime()))
                );
            }

            var form = new FormData();
            form.append("idimg", info[4].id);
            form.append("idtype", info[4].idtype);
            form.append("url", window.location.href);
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
