/* ------------------------------------------------------------------------------
*
*  # Blog page - detailed
*
*  Specific JS code additions for blog page kit - detailed view
*
*  Version: 1.0
*  Latest update: Oct 10, 2016
*
* ---------------------------------------------------------------------------- */

$(function() {
    

    // CKEditor
    // ------------------------------

    CKEDITOR.replace( 'add-comment', {
        height: '200px',
        removeButtons: 'Subscript,Superscript',
        toolbarGroups: [
            { name: 'styles' },
            { name: 'editing',     groups: [ 'find', 'selection' ] },
            { name: 'basicstyles', groups: [ 'basicstyles' ] },
            { name: 'paragraph',   groups: [ 'list', 'blocks', 'align' ] },
            { name: 'links' },
            { name: 'insert' },
            { name: 'colors' },
            { name: 'tools' },
            { name: 'others' },
            { name: 'document',    groups: [ 'mode', 'document', 'doctools' ] }
        ]
    });    
});
