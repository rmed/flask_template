$(document).ready(function() {
    // ...

    // INCLUDE AT THE END OF THE "ready" EVENT

    // Async loading
    $.each($('.async-load'), function(idx, item) {
        asyncLoad($(item));
    });
});
