/**
 * Created by theo on 8/2/17.
 */
$("#send").click(function () {
    var form = new FormData();
    form.append("name", $("#name").val());
    form.append("url", $("#url").val());
    form.append("cat", $("#sel").val());

    $.ajax({
        type: "POST",
        url: "../saveupimg",
        processData: false,
        contentType: false,
        data: form,
        success: function () {
            window.location = "../admin"
        }
    });
});

$("#imgInp").change(function () {
    upload(this.files[0]);
});

$(document).on('dragenter', '#drag', function () {
    $(this).css('border', '3px dashed red');
    return false;
});

$(document).on('dragover', '#drag', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).css('border', '3px dashed red');
    return false;
});

$(document).on('dragleave', '#drag', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).css('border', '3px dashed green');
    return false;
});

$(document).on('drop', '#drag', function (e) {
    if (e.originalEvent.dataTransfer) {
        if (e.originalEvent.dataTransfer.files.length) {
            // Stop the propagation of the event
            e.preventDefault();
            e.stopPropagation();
            $(this).css('border', '3px dashed green');
            // Main function to upload
            fileri = e.originalEvent.dataTransfer.files
        }
    }
    else {
        $(this).css('border', '3px dashed #BBBBBB');
    }
    return false;
});

function upload(f) {
    var form = new FormData();
    form.append("local", f);
    $.ajax({
        type: "POST",
        url: "../upjsonimg",
        enctype: 'mulipart/form-data',
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            if (data == 'ok') {
                $("#pop").show();
                window.location = "../admin"
            }
        }
    });
    return false;
}
