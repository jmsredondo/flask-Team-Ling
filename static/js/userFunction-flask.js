$(document).ready(function () {
    //Search function for book
    $('#bookSearchH').click(function () {
        var searchValue = $('#inputValueH').val();
        $.ajax({
            url: "/book",
            dataType: "JSON"
        }).done(function (data) {
            var html = "";
            var i = 0;
            if (searchValue) {
                for (i; i < data.length; i++) {
                    var bookName = data[i].book_name;
                    if (bookName.toUpperCase().includes(searchValue.toUpperCase())) {
                        html += `<div class="column">
                                        <div class="post-module">
                                        <div class="thumbnail">
                                        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/photo-1429043794791-eb8f26f44081.jpeg"/>
                                    </div><div class="post-content">
                                    <h1 class="title">${bookName}</h1>
                                    <h2 class="sub_title shorten">${data[i].description} asdasdzxczc qdcasdcqwedcad</h2>
                                    <p class="description">New York, the largest city in the U.S., is an architectural marvel with plenty of historic monuments, magnificent buildings and countless dazzling skyscrapers.</p>
                                    <div class="post-meta">
                                    <a href="#" class="fancy-button bg-gradient1"><span onclick="addToLibrary(${data[i].id})"><i class="fas fa-plus-circle"></i>Add to Library</span></a>
                                    </div></div></div></div>`;

                    }
                }
                if (html) {
                    $('#bookslist').html(html);
                } else {
                    $('#bookslist').html("<span>Sorry, We don't have what you're looking for.</span>")
                }
            } else {
                getallbooks();
            }

        });
    });
    initgenre();
    getallbooks();
    initusers();
    viewMyLibrary();
});

//Book functions
function getallbooks() {
    //request list of all books
    $.ajax({
        url: "/book",
        dataType: "JSON"
    }).done(function (data) {
        var html = "";
        for (var i = 0; i < data.length; i++) {
            var bookName = data[i].book_name;
            html += `<div class="column">
              <div class="post-module">
                <div class="thumbnail">
                  <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/photo-1429043794791-eb8f26f44081.jpeg"/>
                </div>
                <div class="post-content">
                  <h1 class="title">${bookName}</h1>
                  <h2 class="sub_title shorten">${data[i].description} asdasdzxczc qdcasdcqwedcad</h2>
                  <p class="description">New York, the largest city in the U.S., is an architectural marvel with plenty of historic monuments, magnificent buildings and countless dazzling skyscrapers.</p>
                  <div class="post-meta">
                  <a href="#" class="fancy-button bg-gradient1"><span onclick="addToLibrary(${data[i].id})"><i class="fas fa-plus-circle"></i>Add to Library</span></a>
                 </div>
                </div></div></div>`;
        }
        $('#bookslist').html(html);

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


function addToLibrary(id) {
    $.ajax({
        type: "POST",
        url: '/library',
        data: JSON.stringify({'bookid': id}),
        success: function (data) {


        },
        contentType: 'application/JSON'
    });
}

function viewMyLibrary() {
    $.ajax({
        type: "GET",
        url: '/library',
        success: function (data) {
            var html = "";
            for (var i = 0; i < data.length; i++) {
                html += ` <div class="blog-card alt">
                <div class="meta">
                    <div class="photo"
                         style="background-image: url(https://storage.googleapis.com/chydlx/codepen/blog-cards/image-2.jpg)"></div>
                    <ul class="details">
                        <li class="author"><a href="#">Jane Doe</a></li>
                        <li class="date">July. 15, 2015</li>
                        <li class="tags">
                            <ul>
                                <li><a href="#">Learn</a></li>
                                <li><a href="#">Code</a></li>
                                <li><a href="#">JavaScript</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div class="description">
                    <h1>${data[i].bookName}</h1>
                    <h2>Java is not the same as JavaScript</h2>
                    <p>${data[i].description}</p>
                    <p class="read-more">
                        <a href="#">Read More</a>
                    </p>
                </div>
            </div>`;
            }
            $('#myLibraryDivH').html(html);

        },
        dataType: 'JSON'
    });
}