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
                                        <img src="${data[i].image}"/>
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
                  <img src="${data[i].image}"/>
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
            alert('Book added to your library.')
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
                         style="background-image: url(${data[i].image})"></div>
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
                        <button type="button" class="btn btn-primary left" data-toggle="modal" data-target="#ModalCenter${data[i].id}">Add Comment</button>
                        <a href="#">Read More</a>
                    </p>
                </div>
            </div>
               <div class="modal fade" id="ModalCenter${data[i].id}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                      <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLongTitle">Add a Comment to the Book:  ${data[i].bookName}</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                              <span aria-hidden="true">&times;</span>
                            </button>
                          </div>
                          <div class="modal-body">
                           <form action="/rate" id="rateandcomment">
                               <input type="hidden" id="${data[i].bookName}">
                              <!-- user id sana i lagay d2 idk kung paano kukunin -->
                              Comment: <br>
                              <textarea rows="10" cols="50" name="comment" id="comment" placeholder="Enter Comment Here..."></textarea>
                              <br>
                              Rating: <br>
                              <div class="rating">
                              <label>
                                <input type="radio" name="rating" value="1" />
                                <span class="icon">★</span>
                              </label>
                              <label>
                                <input type="radio" name="rating" value="2" />
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                              </label>
                              <label>
                                <input type="radio" name="rating" value="3" />
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>   
                              </label>
                              <label>
                                <input type="radio" name="rating" value="4" />
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                              </label>
                              <label>
                                <input type="radio" name="rating" value="5" />
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                                <span class="icon">★</span>
                              </label>
                            </div>
                            </form>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <!-- this will be the trigger for saving -->
                            <button type="button" class="btn btn-primary">Save Comment</button> 
                          </div>
                        </div>
                      </div>
                    </div>`;
            }
            $('#myLibraryDivH').html(html);

        },
        dataType: 'JSON'
    });
}
