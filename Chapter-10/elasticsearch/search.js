function search() {
  $('#noresults').hide();
  $('#results').empty();
  $('#loading').show();
  var query = $('input#search').val();
  $.ajax({
    url: 'https://<enter-cluster-endpoint>/books/_search?q=' + query,
    type: 'GET',
    crossDomain: true,
    dataType: 'json',
    contentType: "application/json",
    success: function(response) {
      var results = response['hits']['hits'];
      if (results.length > 0) {
        $('#loading').hide();

        $('#results').append('<center><p>Found ' + 
              results.length + ' results.</p></center>');

        console.log(results);
        for (var item in results) {
          let url = 'https://amazon.com/dp/' + results[item]._id;
          let image = results[item]._source.image_url;
          let title = results[item]._source.title;
          let author = results[item]._source.author;
          let category = results[item]._source.category;

          $('#results').append('<div class="row">'+
            '<div class="col-md-3" style="text-align:right">' +            
            '<a href="' + url + '">'+
            '<img src="' + image + '" width="50%"></a></div>' +
            '<div class="col-md-9"><h3><a href="' + url + '">' + 
            title + '</a></h3><p>by ' + author + '</p><p>Category: ' + 
            category + '</p></div></div><br>');

          $('#loading').hide();
        }
      } else {
        $('#noresults').show();
        $('#loading').hide();
      }
    },
    error: function() {
      console.log("Failed");
      $('#noresults').show();
      $('#loading').hide();
    }
  });
}

$(document).ready(function() {
  $('#search').on('keypress', function(e) {
    if (e.which === 13) {
      search();
    }
  });
});