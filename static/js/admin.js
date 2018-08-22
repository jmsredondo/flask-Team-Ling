$(document).ready(function () {
    initgenre();
    initbooks();
    initusers();
});

//Book functions
function initbooks() {
    //request list of all books
    $.ajax({
        url: "/book",
        dataType: "JSON"
    }).done(function (data) {
        for (var i = 0; i < data.length; i++) {
            var html = `<div class="column">
              <div class="post-module hover">
                <div class="thumbnail">
                  <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/photo-1429043794791-eb8f26f44081.jpeg"/>
                </div>
                <div class="post-content">
                  <h1 class="title">${data[i].book_name}</h1>
                  <h2 class="sub_title">${data[i].description}</h2>
                  <p class="description">New York, the largest city in the U.S., is an architectural marvel with plenty of historic monuments, magnificent buildings and countless dazzling skyscrapers.</p>
                  <div class="post-meta">
                 </div>
                </div></div></div>`;
            $('#bookslist').append(html);
        }
    });
    //request info of a genre
    var id = 1;
    $.ajax({
        url: "/book/" + id,
        dataType: "JSON"
    }).done(function (data) {
        console.log(data);
    });
}

// Genre functions
function initgenre() {
    //request list of all genres
    $.ajax({
        url: "/genre",
        dataType: "JSON"
    }).done(function (data) {
        for (var i = 0; i < data.length; i++) {
            var html = `<div class="fx-wrap"> 
                <div class="card">
            <div class="front">
                <div class="image">
                    <p class="heading">${data[i].type}</p>
                </div>
                <div class="text">
                    <p>${data[i].genre}</p>
                </div>
            </div>
          </div>
        </div> 
        </div>`;
            $('#genreTiles').append(html);
        }
    });
    //request info of a genre
    var id = 1;
    $.ajax({
        url: "/genre/" + id,
        dataType: "JSON"
    }).done(function (data) {
        console.log(data);
    });
}

//User functions

function initusers() {
    $.ajax({
        url: "/users-list",
        dataType: "JSON"
    }).done(function (data) {
        for (var i = 1; i < data.length; i++) {
            console.log(data);
        }
    });
    var username = "jsmith";
    $.ajax({
        url: "/users/" + username,
        dataType: "JSON"
    }).done(function (data) {
        console.log(data);
    })
}

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