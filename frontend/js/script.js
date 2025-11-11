$(document).ready(function() {
    $('#banquetForm').submit(function(event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                $('#statusMessage').html('<div class="alert alert-success">Заявка успешно отправлена!</div>');
                form.trigger("reset");
            },
            error: function() {
                $('#statusMessage').html('<div class="alert alert-danger">Ошибка отправки заявки.</div>');
            }
        });
    });
});
