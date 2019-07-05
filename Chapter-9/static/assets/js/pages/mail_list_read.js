/* ------------------------------------------------------------------------------
*
*  # Inbox page - Reading
*
*  Specific JS code additions for mail_list_read.html page
*
*  Version: 1.0
*  Latest update: Dec 5, 2016
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Grab first letter from sender name and add it to avatar
    // ------------------------------

    // Title
    var $title = $('.letter-icon-title'),
        letter = $title.eq(0).text().charAt(0).toUpperCase();

    // Icon
    var $icon = $title.parent().parent().find('.letter-icon');
        $icon.eq(0).text(letter);

});
