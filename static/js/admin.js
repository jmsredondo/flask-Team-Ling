function create_book() {
    $.ajax({
        type: "POST",
        url: '/addbook',
        data: {'bookName':'book','image':'description'},
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
        data: {'type':'typegenre','genre':'genre'},
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
