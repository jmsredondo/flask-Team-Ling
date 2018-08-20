$(document).ready(function () {
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
});

