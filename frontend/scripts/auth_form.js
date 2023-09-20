$(() => {
    console.log(1)
    $(document).ready(function() {
        $(".js-auth-form").on("submit", function(event) {
            event.preventDefault();

            var formData = $(this).serialize();


            $.ajax({
                type: "POST",
                url: "/api/auth/send-email/",
                data: formData,
                dataType: "json",
                success: function(data) {
                    if (data.success) {
                        $("#response-message").html(data.message);
                    } else {
                        $("#response-message").html(data.message);
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        });
    });
});
