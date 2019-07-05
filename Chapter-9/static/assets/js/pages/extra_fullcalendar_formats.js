/* ------------------------------------------------------------------------------
*
*  # Fullcalendar time and language options
*
*  Specific JS code additions for extra_fullcalendar_formats.html page
*
*  Version: 1.1
*  Latest update: Mar 20, 2017
*
* ---------------------------------------------------------------------------- */

$(function() {


    // Add events
    // ------------------------------

    // Default events
    var events = [
        {
            title: 'All Day Event',
            start: '2014-11-01'
        },
        {
            title: 'Long Event',
            start: '2014-11-07',
            end: '2014-11-10'
        },
        {
            id: 999,
            title: 'Repeating Event',
            start: '2014-11-09T16:00:00'
        },
        {
            id: 999,
            title: 'Repeating Event',
            start: '2014-11-16T16:00:00'
        },
        {
            title: 'Conference',
            start: '2014-11-11',
            end: '2014-11-13'
        },
        {
            title: 'Meeting',
            start: '2014-11-12T10:30:00',
            end: '2014-11-12T12:30:00'
        },
        {
            title: 'Lunch',
            start: '2014-11-12T12:00:00'
        },
        {
            title: 'Meeting',
            start: '2014-11-12T14:30:00'
        },
        {
            title: 'Happy Hour',
            start: '2014-11-12T17:30:00'
        },
        {
            title: 'Dinner',
            start: '2014-11-12T20:00:00'
        },
        {
            title: 'Birthday Party',
            start: '2014-11-13T07:00:00'
        },
        {
            title: 'Click for Google',
            url: 'http://google.com/',
            start: '2014-11-28'
        }
    ];



    // Date formats
    // ------------------------------

    $('.fullcalendar-formats').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,basicWeek,basicDay'
        },
        views: {
            month: {
                titleFormat: 'LL',
                columnFormat: 'dddd'
            },
            week: {
                titleFormat: 'MMM Do YY',
                columnFormat: 'ddd D'
            },
            day: {
                titleFormat: 'dddd',
                columnFormat: 'dddd'
            }
        },
        timeFormat: 'H:mm', // uppercase H for 24-hour clock
        defaultDate: '2014-11-12',
        editable: true,
        events: events
    });



    // Internationalization
    // ------------------------------

    // Set default language
    var initialLocaleCode = 'en';


    // Build the language selector's options
    $.each($.fullCalendar.locales, function(localeCode) {
        $('#lang-selector').append(
            $('<option/>')
            .attr('value', localeCode)
            .prop('selected', localeCode == initialLocaleCode)
            .text(localeCode)
        );
    });


    // Re-render the calendar when the selected option changes
    $('#lang-selector').on('change', function() {
        if (this.value) {
            $('.fullcalendar-languages').fullCalendar('option', 'locale', this.value);
        }
    });


    // Render calendar
    $('.fullcalendar-languages').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listMonth'
        },
        defaultDate: '2014-11-12',
        locale: initialLocaleCode,
        buttonIcons: false, // show the prev/next text
        weekNumbers: true,
        editable: true,
        events: [
            {
                title: 'All Day Event',
                start: '2014-11-01'
            },
            {
                title: 'Long Event',
                start: '2014-11-07',
                end: '2014-11-10'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2014-11-09T16:00:00'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2014-11-16T16:00:00'
            },
            {
                title: 'Conference',
                start: '2014-11-11',
                end: '2014-11-13'
            },
            {
                title: 'Meeting',
                start: '2014-11-12T10:30:00',
                end: '2014-11-12T12:30:00'
            },
            {
                title: 'Lunch',
                start: '2014-11-12T12:00:00'
            },
            {
                title: 'Meeting',
                start: '2014-11-12T14:30:00'
            },
            {
                title: 'Happy Hour',
                start: '2014-11-12T17:30:00'
            },
            {
                title: 'Dinner',
                start: '2014-11-12T20:00:00'
            },
            {
                title: 'Birthday Party',
                start: '2014-11-13T07:00:00'
            },
            {
                title: 'Click for Google',
                url: 'http://google.com/',
                start: '2014-11-28'
            }
        ]
    });


    // We're using Select2 for language select
    $('.select').select2({
        width: 100,
        minimumResultsForSearch: Infinity,
        containerCssClass: 'bg-slate-700',
        dropdownCssClass: 'bg-slate-700'
    });
    
});
