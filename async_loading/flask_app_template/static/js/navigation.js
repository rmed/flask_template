//...

// INCLUDE AT THE END OF THE FILE

/**
 * Perform asynchronous loading of data.
 *
 * This replaces the HTML of the container with the data obtained in the
 * AJAX request. This is executed automatically on load for all elements that
 * have the `.async-load` class.
 *
 * @param $container container element that will have its contents replaced.
 */
function asyncLoad($container) {
    // Get loader
    var loader = $container.data('loader');

    if (!loader) {
        return;
    }

    // Update content
    $.ajax({
        url: loader,
        type: 'GET',
        success: function(data) {
            // Update content
            $container.html(data);

            // Reattach additional events here
            //...
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('[ERROR] ' + xhr.responseText);
            showNotification('error', 'asyncLoad error');
        }
    });
}
