/* ------------------------------------------------------------------------------
*
*  # Orders history
*
*  Specific JS code additions for ecommerce_orders_history.html page
*
*  Version: 1.0
*  Latest update: Aug 1, 2015
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Table setup
    // ------------------------------

    // Initialize
    var table = $('.table-orders-history').DataTable({
        autoWidth: false,
        columnDefs: [
            {
                visible: false,
                targets: 0
            },
            {
                targets: 1,
                width: 400
            },
            { 
                orderable: false,
                width: 16,
                targets: 7
            }
        ],
        order: [[ 0, 'asc' ]],
        dom: '<"datatable-header datatable-header-accent"fBl><"datatable-scroll-wrap"t><"datatable-footer"ip>',
        language: {
            search: '<span>Filter:</span> _INPUT_',
            searchPlaceholder: 'Type to filter...',
            lengthMenu: '<span>Show:</span> _MENU_',
            paginate: { 'first': 'First', 'last': 'Last', 'next': '&rarr;', 'previous': '&larr;' }
        },
        lengthMenu: [ 25, 50, 75, 100 ],
        displayLength: 25,
        buttons: [
            {
                extend: 'pdfHtml5',
                text: 'Export to PDF <i class="icon-file-pdf position-right"></i>',
                className: 'btn bg-teal-400',
                orientation: 'landscape',
                exportOptions: {
                    columns: [ 1, 2, 3, 4, 5, 6 ],
                    stripHtml: true
                },
                customize: function (doc) {
                    doc.content[1].table.widths = Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }
            }
        ],
        drawCallback: function (settings) {
            var api = this.api();
            var rows = api.rows({ page: 'current' }).nodes();
            var last = null;
 
            api.column(0, { page: 'current' }).data().each(function(group, i) {
                if (last !== group) {
                    $(rows).eq(i).before(
                        '<tr class="active group border-double"><td colspan="8" class="text-semibold">' + group + '</td></tr>'
                    );
 
                    last = group;
                }
            });

            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').addClass('dropup');
        },
        preDrawCallback: function(settings) {
            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').removeClass('dropup');
        }
    });

    // Order by the grouping
    $('.table-orders-history tbody').on( 'click', 'tr.group', function() {
        var currentOrder = table.order()[0];
        if (currentOrder[0] === 0 && currentOrder[1] === 'asc') {
            table.order([0, 'desc']).draw();
        }
        else {
            table.order([0, 'asc']).draw();
        }
    });


    // External table additions
    // ------------------------------
    
    // Enable Select2 select for the length option
    $('.dataTables_length select').select2({
        minimumResultsForSearch: Infinity,
        width: 'auto'
    });

});
