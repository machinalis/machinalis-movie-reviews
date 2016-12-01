$(document).ready(function() {
  $(".like-button").click(on_like_clicked);
});

function on_like_clicked(event) {
  event.preventDefault();

  var $button = $(this);
  var $movie = $button.parents(".movie-card");
  var movie_id = $movie.data("movie-id");

  $.ajax({
    url: "/like/" + movie_id,
    method: "POST",
    success: function(result) {
      var $icon = $button.find(".material-icons")
      var text = $icon.text()
      var new_value = text.trim().toLowerCase() === "favorite" ? "favorite_border" : "favorite";
      $icon.text(new_value);
    }
  });
}
