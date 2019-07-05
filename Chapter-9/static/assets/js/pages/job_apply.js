/* ------------------------------------------------------------------------------
*
*  # Job search - apply
*
*  Specific JS code additions for job search page kit - apply
*
*  Version: 1.0
*  Latest update: Jan 10, 2017
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Select2 select
    // ------------------------------

    // With search
    $('.select').select2();

    // Without search
    $('.select-simple').select2({
        minimumResultsForSearch: Infinity
    });


    // Date picker
    // ------------------------------

    // Default functionality
    $(".datepicker").datepicker();


    // Styled form components
    // ------------------------------

    // Checkboxes, radios
    $(".styled").uniform({ radioClass: 'choice' });

    // File input
    $(".file-styled").uniform({
        fileButtonClass: 'action btn bg-pink-400'
    });
  
});
