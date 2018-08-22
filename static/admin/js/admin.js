function ulist(x) {
    $.ajax({
        url: x,
        cache: false,
        dataType: "html",
        success: function (data) {
            $("#div1").html(data);
        }
    });
}