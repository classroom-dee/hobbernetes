$(document).ready(function() {
    // load widget data
    $.getJSON('/widgets', funciton(data) {
        data.forEach(widget => {
            $('#widget-table tbody').append(`
                <tr data-iframe="${widget.iframe_code}">
                    <td>${widget.name}</td>
                    <td>${widget.description}</td>
                </tr>
            `);
        });

        // click event for table rows
        $('#widget-table tbody tr').click(function() {
            const iframeCode = $(this).data('iframe');
            $('#widget-preview').html(iframeCode);
        });
    });

    // copy widget function
    $('#copy-widget').click(function() {
        const code = $('#widget-preview').html();
        navigator.clipboard.writeText(code);
        alert('Widget code copied to clipboard!');
    });
});