$(document).ready(function() {
  $("#follow-form").submit(on_form_submit);
});

function on_form_submit() {
  event.preventDefault();
  var $form = $(this);
  $.ajax({
    type: $form.attr('method'),
    url: $form.attr('action'),
    data: $form.serialize(),
    success: function (data) {
      location.reload();
    }
  })
}

