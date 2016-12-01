$(document).ready(function() {
  $(".like-button").click(on_like_clicked);
});

function on_like_clicked(event) {
  var $button = $(this);
  var $movie = $button.parents(".movie-card");
  var movie_id = $movie.data("movie-id");

  $.ajax({
    url: "/like/" + movie_id,
    method: "POST",
    success: function(result) {
      $button.find(".material-icons").text("favorite");
    }
  });
}
