/**
 * Created by theo on 8/18/17.
 */
var tasks = ["textvote", "selection", "swipe", "multiple", "reverse"];
var headerR = ["ID", "User", "Task", "Bug", "IDimage", "ImageLink"];
var headerT = ["", "Textual", "Selection", "Swipes", "Multiple", "Reverse"];
$(document).ready(function () {
    filltasks();
    fillbasic()
});

$("#reports").click(function () {
    if ($(this).attr("value") == 0) {
        $(this).text("Display Tasks");
        $(this).attr("value", 1);
        $("tbody").empty();
        fillreports();
        var i = 0;
        $("#head").find("th").each(function () {
            $(this).text(headerR[i]);
            i++;
        })
    } else {
        $(this).text("Display Reports");
        $(this).attr("value", 0);
        filltasks();
    }
});


function filltasks() {

    var temp = "<tr id='im1'><th>Unique Images</th><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td></tr><tr id='usr1'><th>Unique Users</th><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td></tr><tr id='ski'><th>Number of images Skipped</th><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td><td class='tof'></td></tr><tr id='clas'><th>Most common Classes</th><td class='tof'></td><td class='tof'></td> <td class='tof'></td><td class='tof'></td><td class='tof'></td></tr>";

    $('#tabcont').empty();
    $("#tabcont").append(temp);

    var i = 0;
    $("#head").find("th").each(function () {
        $(this).text(headerT[i]);
        i++;
    });


    $.ajax({
        type: "GET",
        url: "../adminstats",
        processData: false,
        contentType: false,
        success: function (data) {
            var temp = JSON.parse(data);
            var i = 0;
            $("#im1").find(".tof").each(function () {
                $(this).text(temp[tasks[i]].image);
                i++;
            });
            i = 0;
            $("#usr1").find(".tof").each(function () {
                $(this).text(temp[tasks[i]].user);
                i++;
            });
            i = 0;
            $("#ski").find(".tof").each(function () {
                $(this).text(temp[tasks[i]].skipped);
                i++;
            });
            i = 0;
            $("#clas").find(".tof").each(function () {
                $(this).empty();
                $(this).append("<ul>");
                for (var u = 0; u < temp[tasks[i]].classes.length; u++) {
                    $(this).append("<li>" + temp[tasks[i]].classes[u].cl + " <span class='badge' style='float:right'>" + temp[tasks[i]].classes[u].nb + "</span></li>")
                }
                i++;
                $(this).append("</ul>");
            })
        }
    });
}

function fillreports() {
    $.ajax({
        type: "GET",
        url: "../getreports",
        processData: false,
        contentType: false,
        success: function (data) {
            var temp = JSON.parse(data);
            var tof = $("tbody");
            var str = "";
            temp.forEach(function (row) {
                str = "<tr>";
                $.each(row, function (key, value) {
                    if (key != 'path') {
                        str += "<td>" + value + "</td>"
                    } else {
                        str += "<td><a href='" + value + "'>See the picture</a></td>"
                    }
                });
                str += "</tr>";
                tof.append(str);
                srt = ""
            })

        }
    });

}

function fillbasic() {
    $.ajax({
        type: "GET",
        url: "../getbasicstats",
        processData: false,
        contentType: false,
        success: function (data) {
            var info =JSON.parse(data);
            $("#basic").html("Total  of <strong>"+info.users + " users </strong>  have sorted  <strong>"+info.saves +" times  </strong> some of the <strong>"+info.images + " images </strong>  available  into <strong>"+info.types +" categories  </strong>")
        }

    });
}

