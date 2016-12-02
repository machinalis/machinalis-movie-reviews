$(document).ready(function() {
  $(".follow-button").click(on_follow_click);
});

function on_follow_click(event) {
  event.preventDefault();
  var $this = $(this);

  $.ajax({
    type: "post",
    url: $this.data("api-url"),
    success: function (data) {
      location.reload();
    }
  })
}

