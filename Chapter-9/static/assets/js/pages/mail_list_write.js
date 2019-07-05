/* ------------------------------------------------------------------------------
*
*  # Inbox page - Writing
*
*  Specific JS code additions for mail_list_write.html page
*
*  Version: 1.0
*  Latest update: Dec 5, 2016
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Plugins
    // ------------------------------

    // Summernote editor
    $('.summernote').summernote({
        height: 1240
    });


    // Related form components
    // ------------------------------

    // Styled checkboxes/radios
    $(".link-dialog input[type=checkbox], .note-modal-form input[type=radio]").uniform({
        radioClass: 'choice'
    });

    // Styled file input
    $(".note-image-input").uniform({
        fileButtonClass: 'action btn bg-warning-400'
    });

});
