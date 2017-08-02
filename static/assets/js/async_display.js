/**
 * Created by theo on 8/2/17.
 */
var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
    modal.style.display = "none";
};
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

$("body").on("click", ".idata", function () {
    modal.style.display = "block";
    $(".modal-body").empty();
    $(".modal-body").append("<img  class='imgmod' src='" + $(this).attr('src') + "'/>");
    $("#mh").text("Image N°" + $(this).attr('value'));
    var form = new FormData();
    form.append("idimg", "" + $(this).attr('value'));
    $.ajax({
        type: "POST",
        url: "../getimginfotype",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            data = JSON.parse(data);
            $(".modal-body").append("<div class='imginfo'> <ul class='list-group'> <li class='list-group-item'>Textual <span class='badge'>" + data.text + "</span></li> <li class='list-group-item'>Selection<span class='badge'>" + data.select + "</span></li> <li class='list-group-item'>Swipes<span class='badge'>" + data.swipe + "</span></li> </ul> </div>");
            $("#mf").text("Classified " + (parseInt(data.text) + parseInt(data.swipe) + parseInt(data.select)) + " times")
        }
    });
    $.ajax({
        type: "POST",
        url: "../topclass",
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            info = JSON.parse(data);
            str = "<div class='imginfo'> <ul class='list-group'>";
            info.forEach(function (row) {
                str += " <li class='list-group-item'>" + row.name + " <span class='badge'>" + row.value + "</span></li>"
            });
            $(".modal-body").append(str + "</ul> </div></div>")
        }
    });
});