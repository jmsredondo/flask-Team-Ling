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

function userView() {
    const uname = sessionStorage.getItem('us');
    $.ajax({
        url: "/users/" + uname,
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            const firstname = response.firstname;
            const lastname = response.lastname;
            const phone = response.phone;
            const username = response.username;
            const emailaddress = response.email;

            $('#firstname').val(firstname);
            $('#lastname').val(lastname);
            $('#phone').val(phone);
            $('#email').val(emailaddress);
            $('#username').val(username);
        }
    });
}

function genrelist() {
    //Delete Genre
    $('#deleteGenre').click(function () {
        var id = $(this).val();
        deleteGenre(id);
    });
    var count = 0;
    $.ajax({
        url: "http://localhost:5000/genre",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            var table = $('#genrelist').DataTable({
                "data": response,
                "columns": [
                    {"data": "id"},
                    {"data": "genre"},
                    {"data": "type"},
                    {
                        "defaultContent": "        <button class=\"btnViewGenre pe-7s-look btn btn-info btn-fill\" value=\"view\"></button>\n" +
                        "<button class=\"btnDeleteGenre pe-7s-trash btn btn-danger btn-fill\" value=\"delete\"></button>\n"
                    }
                ],
            });
            $('#genrelist tbody').on('click', 'button', function () {
                var data = table.row($(this).parents('tr')).data();
                var action = $(this).val();
                genreAction(action, data);
            });
        }
    });
}

function view_genre_form() {
    const genre_id = sessionStorage.getItem('genre_id');
    $.ajax({
        url: "/genre/" + genre_id,
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            const genre = response.genre;
            const type = response.type;

            $('#genre').val(genre);
            $('#type').val(type);
        }
    });
}

function view_book_form() {
    const book_id = sessionStorage.getItem('b_id');
    $.ajax({
        url: "/book/" + book_id,
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            const bookname = response.book_name;
            const description = response.description;
            const image = response.image;

            $('#bookname').val(bookname);
            $('#description').val(description);
            $("#image").attr("src", image);
        }
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


function genreAction(action, data) {
    if (action === 'view') {
        sessionStorage.setItem("genre_id", data.id);
        ulist('/view-genre')
    } else {
        $('#deleteGenreConfirm').modal();
        $('#deleteGenre').val(data.id);
    }
}

function users_list() {
    $.ajax({
        url: "http://localhost:5000/users-list",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            var table = $('#users').DataTable({
                "data": response,
                "columns": [
                    {"data": "id"},
                    {"data": "username"},
                    {"data": "firstname"},
                    {"data": "lastname"},
                    {"data": "balance"},
                    {
                        "defaultContent": "<div class=\"row\">\n" +
                        "    <div class=\"col-md-3\">\n" +
                        "        <button class=\"pe-7s-look btn btn-info btn-fill\" value=\"view\"></button>\n" +
                        "    </div>\n"
                    }
                ]
            });
            $('#users tbody').on('click', 'button', function () {
                var data = table.row($(this).parents('tr')).data();
                sessionStorage.setItem('us', data.username);
                ulist('/view-user');
            });
        }
    });
}

function bookAction(action, data) {
    if (action === 'view') {
        sessionStorage.setItem("b_id", data.id);
        ulist('/view-book')
    } else {
        $('#deleteBookConfirm').modal();
        $('#deleteBook').val(data.id);
    }
}

function booklist() {
    var count = 0;
    $.ajax({
        url: "/book",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            var table = $('#booklist').DataTable({
                "data": response,
                "columns": [
                    {"data": "id"},
                    {"data": "book_name"},
                    {"data": "image"},
                    {"data": "description"},
                    {
                        "defaultContent": "<button class=\"pe-7s-look btn btn-info btn-fill\" value=\"view\"></button>\n" +
                        "        <button class=\"btnDeleteBook pe-7s-trash btn btn-danger btn-fill\" value=\"delete\"></button>\n"
                    }
                ]
            });
            $('#booklist tbody').on('click', 'button', function () {
                const data = table.row($(this).parents('tr')).data();
                const action = $(this).val();
                bookAction(action, data);
            });
        }
    });
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
