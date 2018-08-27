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

function remove_book(id) {
    $.ajax({
        url: '/book/' + id,
        method: "DELETE",
        dataType: "JSON"
    }).done(function (data) {
        ulist('/book');
        $('#deleteBookConfirm').modal('hide');
    })
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
                        "defaultContent": "<button class=\"btnViewGenre pe-7s-look btn btn-info btn-fill\" value=\"view\"></button>\n" +
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
    $(document).ready(function () {
        sessionStorage.removeItem("imgData");
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


                $.ajax({
                    url: "/bg/" + book_id,
                    dataType: 'json',
                    crossDomain: true,
                    xhrFields: {
                        withCredentials: true
                    },
                    success: function (response) {
                        console.log(response.length);

                        const x = document.getElementById("genreSelect");
                        var i = 0;
                        for (i; i < response.length; i++) {
                            const option = document.createElement("option");
                            option.text = response[i]["genre_desc"];
                            option.value = response[i]["genre_id"];
                            x.add(option);
                        }
                    }
                });
            }
        });
    });
}

function ulist(x) {
    $.ajax({
        url: x,
        cache: false,
        dataType: "html",
        success: function (data) {
            // document.location.href = (x);
            $("#div1").html(data)
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
    }
    else {
        $('#deleteBookConfirm').modal();
        $('#deleteBook').val(data.id);
    }
}

function booklist() {
    //Delete Genre
    $('#deleteBook').click(function () {
        var id = $(this).val();
        remove_book(id);
    });
    const count = 0;
    $.ajax({
        url: "/bookgenrelist",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            const table = $('#booklist').DataTable({
                "data": response,
                "columns": [
                    {"data": "id"},
                    {"data": "book_name"},
                    {"data": "image"},
                    {"data": "genre"},
                    {
                        "defaultContent": "<button class=\"pe-7s-look btn btn-info btn-fill\" value=\"view\"></button>\n" +
                        "<button class=\"pe-7s-trash btn btn-danger btn-fill\" value=\"delete\"></button>\n"
                    }
                ]
            });
            $('#booklist tbody').on('click', 'button', function () {
                var data = table.row($(this).parents('tr')).data();
                var action = $(this).val();
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

function add_book() {
    $.ajax({
        url: "/genre",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {

            console.log(response.length);

            const x = document.getElementById("genreSelect");
            var i = 0;
            for (i; i < response.length; i++) {
                const option = document.createElement("option");
                option.text = response[i]["genre"];
                option.value = response[i]["id"];
                x.add(option);
            }
        }
    });

    sessionStorage.removeItem("imgData");

    $('input#file').on('change', function () {
        console.log(this);

        var reader = new FileReader();
        reader.onload = function (e) {
            console.log(reader.result + '->' + typeof reader.result);
            var thisImage = reader.result;
            sessionStorage.setItem("imgData", thisImage);
        };
        reader.readAsDataURL(this.files[0]);
    });

    // process the form
    $('form').submit(function (event) {

        const bookname = $('#bookname').val();
        const description = $('#description').val();
        const genre = $("#genreSelect").val() || [];
        const formData = JSON.stringify({
            "bookname": bookname,
            "description": description,
            "image": sessionStorage.getItem("imgData"),
            "genre": genre
        });

        // process the form
        $.ajax({
            type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/book', // the url where we want to POST
            data: formData, // our data object
            contentType: 'application/json', // what type of data do we send to the server
            dataType: 'json', // what type of data do we expect back from the server
        })
        // using the done promise callback
            .done(function (data) {

                // log data to the console so we can see
                console.log(data);
                // process the form
                $.ajax({
                    type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                    url: '/genre/addbook/' + data.id, // the url where we want to POST
                    data: formData, // our data object
                    contentType: 'application/json', // what type of data do we send to the server
                    dataType: 'json', // what type of data do we expect back from the server
                })
                // using the done promise callback
                    .done(function (data) {

                        // log data to the console so we can see
                        console.log(data);

                        // here we will handle errors and validation messages
                    });

                // here we will handle errors and validation messages
            });


        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

}

function add_book_genre_form() {

    $.ajax({
        url: "/genre",
        dataType: 'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {

            console.log(response.length);

            const x = document.getElementById("genreSelect");
            var i = 0;
            for (i; i < response.length; i++) {
                const option = document.createElement("option");
                option.text = response[i]["genre"];
                option.value = response[i]["id"];
                x.add(option);
            }
        }
    });

    $('input#file').on('change', function () {
        // console.log(this);

        var reader = new FileReader();
        reader.onload = function (e) {
            console.log(reader.result + '->' + typeof reader.result);
            var thisImage = reader.result;
            sessionStorage.setItem("imgData", thisImage);
        };
        reader.readAsDataURL(this.files[0]);

    });

    // process the form
    $('form').submit(function (event) {

        const bookname = $('#bookname').val();
        const description = $('#description').val();
        const image = $('#file').val();
        const genre = $("#genreSelect").val() || [];
        const formData = JSON.stringify({
            "bid": sessionStorage.getItem('b_id'),
            "bookname": bookname,
            "description": description,
            // "image": image,
            "image": sessionStorage.getItem("imgData"),
            "genre": genre
        });

        console.log(formData);
        // process the form
        $.ajax({
            type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/editbook', // the url where we want to POST
            data: formData, // our data object
            contentType: 'application/json', // what type of data do we send to the server
            dataType: 'json', // what type of data do we expect back from the server
        })
        // using the done promise callback
            .done(function (data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
}

function edit_genre_form() {

    // process the form
    $('form').submit(function (event) {

        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = JSON.stringify({
            "gid": sessionStorage.getItem("genre_id"),
            "genre": $('#genre').val(),
            "type": $('#type').val()
        });

        // process the form
        $.ajax({
            type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/update_genre', // the url where we want to POST
            data: formData, // our data object
            contentType: 'application/json', // what type of data do we expect back from the server
            dataType: 'json', // what type of data do we expect back from the server

        })
        // using the done promise callback
            .done(function (data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

}

function add_genre() {
    // process the form
    $('form').submit(function (event) {

        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = JSON.stringify({
            "genre": $('#genre').val(),
            "type": $('#type').val()
        });


        // process the form
        $.ajax({
            type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/genre', // the url where we want to POST
            data: formData, // our data object
            contentType: 'application/json', // what type of data do we expect back from the server
            dataType: 'json', // what type of data do we expect back from the server

        })
        // using the done promise callback
            .done(function (data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
}
