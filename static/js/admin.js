
function create_book() {
    $.ajax({
        type: "POST",
        url: '/addbook',
        data: {'bookName': 'book', 'image': 'description'},
        success: function () {

        },
        dataType: 'JSON'
    });
}

function remove_book() {
    $.ajax({
        type: "DELETE",
        url: '/deletebook/11',
        success: function () {

        },
    });
}


function create_genre() {
    $.ajax({
        type: "POST",
        url: '/addGenre',
        data: {'type': 'typegenre', 'genre': 'genre'},
        success: function () {

        },
        dataType: 'JSON'
    });
}

function remove_genre() {
    $.ajax({
        type: "DELETE",
        url: '/deleteGenre/21',
        success: function () {

        },
    });
}

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


function genreAction(action, id) {
    if (action === 'view') {
        ulist('/view-genre/' + id)
    } else {
        $('#deleteGenreConfirm').modal();
        $('#deleteGenre').val(id);
    }

}

function deleteGenre(id) {
    $.ajax({
        url: "/genre/" + id,
        method: "DELETE",
        dataType: "JSON"
    }).done(function (data) {
        ulist("/genres");
        $('#deleteGenreConfirm').modal('hide');
    })
}
