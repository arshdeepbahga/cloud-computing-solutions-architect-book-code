/* ------------------------------------------------------------------------------
*
*  # Customers
*
*  Specific JS code additions for ecommerce_customers.html page
*
*  Version: 1.0
*  Latest update: Mar 20, 2017
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Chart configuration
    // ------------------------------

    // Base
    require.config({
        paths: {
            echarts: 'assets/js/plugins/visualization/echarts'
        }
    });

    // Configuration
    require(

        // Add necessary charts
        [
          'echarts',
          'echarts/theme/limitless',
          'echarts/chart/line',
          'echarts/chart/bar'
        ],


        // Charts setup
        function (ec, limitless) {

            // Initialize charts
            var line_bar = ec.init(document.getElementById('customers_chart'), limitless);

            // Charts options
            line_bar_options = {

                // Setup grid
                grid: {
                    x: 55,
                    x2: 45,
                    y: 35,
                    y2: 25
                },

                // Add custom colors
                color: ['#EF5350', '#03A9F4','#4CAF50'],

                // Add tooltip
                tooltip: {
                    trigger: 'axis'
                },

                // Add legend
                legend: {
                    data: ['New customers','Returned customers','Orders']
                },

                // Horizontal axis
                xAxis: [{
                    type: 'category',
                    data: ['January','February','March','April','May','June','July','August','September','October','November','December']
                }],

                // Vertical axis
                yAxis: [
                    {
                        type: 'value',
                        name: 'Visitors',
                        axisLabel: {
                            formatter: '{value}k'
                        }
                    },
                    {
                        type: 'value',
                        name: 'Orders',
                        axisLabel: {
                            formatter: '{value}k'
                        }
                    }
                ],

                // Add series
                series: [
                    {
                        name: 'New customers',
                        type: 'bar',
                        data: [20, 49, 70, 232, 256, 767, 1356, 1622, 326, 200, 64, 33]
                    },
                    {
                        name: 'Returned customers',
                        type: 'bar',
                        data: [26, 59, 90, 264, 287, 707, 1756, 1822, 487, 188, 60, 23]
                    },
                    {
                        name: 'Orders',
                        type: 'line',
                        yAxisIndex: 1,
                        data: [20, 22, 33, 45, 63, 102, 203, 234, 230, 165, 120, 62]
                    }
                ]
            };

            // Apply options
            line_bar.setOption(line_bar_options);

            // Resize charts
            window.onresize = function () {
                setTimeout(function (){
                    line_bar.resize();
                }, 200);
            }
        }
    );


    // Table setup
    // ------------------------------

    // Initialize
    $('.table-customers').DataTable({
        autoWidth: false,
        columnDefs: [
            {
                targets: 0,
                width: 400
            },
            { 
                orderable: false,
                width: 16,
                targets: 6
            },
            {
                className: 'control',
                orderable: false,
                targets: -1
            },
        ],
        order: [[ 0, 'asc' ]],
        dom: '<"datatable-header datatable-header-accent"fBl><""t><"datatable-footer"ip>',
        language: {
            search: '<span>Search people:</span> _INPUT_',
            searchPlaceholder: 'Type to filter...',
            lengthMenu: '<span>Show:</span> _MENU_',
            paginate: { 'first': 'First', 'last': 'Last', 'next': '&rarr;', 'previous': '&larr;' }
        },
        lengthMenu: [ 25, 50, 75, 100 ],
        displayLength: 50,
        responsive: {
            details: {
                type: 'column',
                target: -1
            }
        },
        buttons: [
            {
                extend: 'pdfHtml5',
                text: 'Export list <i class="icon-file-pdf position-right"></i>',
                className: 'btn bg-blue',
                orientation: 'landscape',
                exportOptions: {
                    columns: [ 0, 1, 2, 3, 4, 5 ],
                    stripHtml: true
                },
                customize: function (doc) {
                    doc.content[1].table.widths = Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }
            }
        ],
        drawCallback: function (settings) {
            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').addClass('dropup');
        },
        preDrawCallback: function(settings) {
            $(this).find('tbody tr').slice(-3).find('.dropdown, .btn-group').removeClass('dropup');
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
