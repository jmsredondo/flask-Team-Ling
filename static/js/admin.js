$(document).ready(function () {
    initgenre();
    initbooks();
});

function initbooks() {
      //request list of all books
    $.ajax({
        url: "/book",
        dataType: "JSON"
    }).done(function (data) {
        for (var i = 0; i <data.length; i++){
            var html = `<div class="column">
              <div class="demo-title">Normal</div>
              <div class="post-module">
                <div class="thumbnail">
                  <div class="date">
                    <div class="day">27</div>
                    <div class="month">Mar</div>
                  </div><img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/photo-1429043794791-eb8f26f44081.jpeg"/>
                </div>
                <div class="post-content">
                  <div class="category">Genre</div>
                  <h1 class="title">${data[i].book_name}</h1>
                  <h2 class="sub_title">${data[i].description}</h2>
                  <p class="description">New York, the largest city in the U.S., is an architectural marvel with plenty of historic monuments, magnificent buildings and countless dazzling skyscrapers.</p>
                  <div class="post-meta"><span class="timestamp"><i class="fa fa-clock-">o</i> 6 mins ago</span><span class="comments"><i class="fa fa-comments"></i><a href="#"> 39 comments</a></span></div>
                </div></div></div>`;
            $('#bookslist').append(html);
            console.log(data[i])
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
function initgenre() {
       //request list of all genres
    $.ajax({
        url: "/genre",
        dataType: "JSON"
    }).done(function (data) {
        for (var i = 0; i <data.length; i++){
            var html = `<div class="card"
             src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZIbTuWRSqUVqo_Qdo4O9PKBwhRuwHBcmDdJlDez5oSwdXel-7pw">
            <div class="front">
                <div class="image">
                    <p class="heading">${data[i].genre}</p>
                </div>
                <div class="text">
                    <header class="clearfix">
                        <button class="flip"><span class="zmdi zmdi-replay"></span></button>
                    </header>
                    <p>Description</p>
                </div>
            </div>
            <div class="back">
              <div class="text">
                <header class="clearfix">
                  <button class="flip"><span class="zmdi zmdi-replay"></span></button>
                </header><b>"You can flip me all day."</b>
                <p>I have flexbox with fallbacks, I'm not browser prefixed (so watch out, this is a prototype) but my animations are pure css if your into that sort of thing.</p>
              </div>
            </div>
          </div>
        </div>`;
            $('#genreTiles').append(html);
            console.log(data[i].id,data[i].type)
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