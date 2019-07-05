function clearSession() {
    sessionStorage.clear();
    location.href='login.html';
};

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    return results[1] || 0;
}

function processLogin() {
    var username =  $("#username" ).val();
    var password = $("#password" ).val();

    var datadir = {
        username: username,
        password: password
    };

    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/login',
        type: 'POST',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {
            var result = JSON.parse(data.body);
            console.log(result);
            if(result.result){
                sessionStorage.setItem('username', result.userdata.username);
                sessionStorage.setItem('name', result.userdata.name);
                sessionStorage.setItem('email', result.userdata.email);
                location.href='index.html';
            }else{
                $("#message").html(result.message);
            }
            
            console.log(data);
        },
        error: function(data) {
            console.log(data);
            console.log("Failed");
        },        
        data: JSON.stringify(datadir)
    });    
}


function processSignup() {
    var username =  $("#username" ).val();
    var password = $("#password" ).val();
    var password1 = $("#password1" ).val();
    var name = $("#name" ).val();
    var email = $("#email" ).val();

    var datadir = {
        username: username,
        password: password,
        name: name,
        email: email
    };

    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/signup',
        type: 'POST',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {
            var result = JSON.parse(data.body);
            console.log(result);
            $("#message").html(result.message);
            if(result.result){
                sessionStorage.setItem('username', result.userdata.username);
                $("#messageaction").html("Click  <a href=\"confirmemail.html\">here</a> to confirm your email");
            }
        },
        error: function() {
            console.log("Failed");
        },        
        data: JSON.stringify(datadir)
    });    
}

function loadConfirmEmailPage(){
    var username = $("#username").val();
    var code = $("#code").val();

    var datadir = {
        username: username,
        code: code
    };

    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/confirmemail',
        type: 'POST',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {
            var result = JSON.parse(data.body);
            console.log(result);
            if(result.result){                
                $("#confirmemail-message").html(result.message);
                $("#confirmemail-message-action").html("Click  <a href=\"login.html\">here</a> to login");                
            }else{
                $("#confirmemail-message").html(result.message);
            }
            
            console.log(data);
        },
        error: function(data) {
            console.log(data);
            console.log("Failed");
        },        
        data: JSON.stringify(datadir)
    });  
}


function uploadPhoto(){
    var title = $("#title").val();
    var description = $("#description").val();
    var tags = $("#tags").val();
    var imageFile = $('#imagefile')[0].files[0];
    var contenttype = imageFile.type;
    var filename=imageFile.name;
    console.log(imageFile);
    console.log(filename);

    $.ajax({
        url: ' https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/uploadphoto/'+filename,
        type: 'PUT',
        crossDomain: true,
        contentType: contenttype,
        processData: false,
        statusCode: {
        200: function(data) {
            console.log(data);
            console.log("Uploaded");
            processAddPhoto(filename, title, description, tags);
         }
        },       
        data: imageFile
    }); 
}

function searchPhotos(){
    var query = $("#query").val();

    var datadir = {
        query: query
    };

    console.log(datadir);

    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/search',
        type: 'POST',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {                        
            console.log(data);
            sessionStorage.setItem('query', query);
            sessionStorage.setItem('searchdata', JSON.stringify(data));
            location.href='search.html';            
        },
        error: function() {
            console.log("Failed");
        },        
        data: JSON.stringify(datadir)
    }); 
}

function loadSearchPage(){
    var query = sessionStorage.getItem('query');
    var data = JSON.parse(sessionStorage.getItem('searchdata'));
    console.log(data);
    $("#searchquery-container").html("Showing search results for: "+query);
    var htmlstr="";
    $.each(data.body, function(index, value) {
        //console.log(value);
        htmlstr = htmlstr + '<div class=\"cbp-item idea web-design theme-portfolio-item-v2 theme-portfolio-item-xs\"> <div class=\"cbp-caption\"> <div class=\"cbp-caption-defaultWrap theme-portfolio-active-wrap\"> <img src=\"'+value.URL+'\" alt=\"\"> <div class=\"theme-icons-wrap theme-portfolio-lightbox\"> <a class=\"cbp-lightbox\" href=\"'+value.URL+'\" data-title=\"Portfolio\"> <i class=\"theme-icons theme-icons-white-bg theme-icons-sm radius-3 icon-focus\"></i> </a> </div> </div> </div> <div class=\"theme-portfolio-title-heading\"> <h4 class=\"theme-portfolio-title\"><a href=\"viewphoto.html?id='+value.PhotoID+'\">'+value.Title+'</a></h4> <span class=\"theme-portfolio-subtitle\">by '+value.Username+'<br>'+value.CreationTime+'</span> </div> </div>';
                });
        //console.log(htmlstr);
        $('#portfolio-4-col-grid-search').html(htmlstr);
        handlePortfolio4ColGridSearch();        
}

function processAddPhoto(filename, title, description, tags){
    var username = sessionStorage.getItem('username');    
    var uploadedFileURL = "http://cloudcomputingcourse2017.s3-website-us-east-1.amazonaws.com/photos/"+ filename;

    var datadir = {
        username: username,
        title: title,
        description: description,
        tags: tags,
        uploadedFileURL: uploadedFileURL
    };

    console.log(datadir);

    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/photos',
        type: 'POST',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {                        
            console.log(data);
            location.href='index.html';            
        },
        error: function() {
            console.log("Failed");
        },        
        data: JSON.stringify(datadir)
    }); 
}

function handlePortfolio4ColGridSearch() {
        $('#portfolio-4-col-grid-search').cubeportfolio({
            filters: '#portfolio-4-col-grid-filter',
            layoutMode: 'grid',
            defaultFilter: '*',
            animationType: 'rotateRoom',
            gapHorizontal: 30,
            gapVertical: 30,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 1500,
                cols: 4
            }, {
                width: 1100,
                cols: 4
            }, {
                width: 800,
                cols: 4
            }, {
                width: 550,
                cols: 2
            }, {
                width: 320,
                cols: 1
            }],
            caption: ' ',
            displayType: 'bottomToTop',
            displayTypeSpeed: 100,

            // lightbox
            lightboxDelegate: '.cbp-lightbox',
            lightboxGallery: true,
            lightboxTitleSrc: 'data-title',
            lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>',
        });
    }

function handlePortfolio4ColGrid() {
        $('#portfolio-4-col-grid').cubeportfolio({
            filters: '#portfolio-4-col-grid-filter',
            layoutMode: 'grid',
            defaultFilter: '*',
            animationType: 'rotateRoom',
            gapHorizontal: 30,
            gapVertical: 30,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 1500,
                cols: 4
            }, {
                width: 1100,
                cols: 4
            }, {
                width: 800,
                cols: 4
            }, {
                width: 550,
                cols: 2
            }, {
                width: 320,
                cols: 1
            }],
            caption: ' ',
            displayType: 'bottomToTop',
            displayTypeSpeed: 100,

            // lightbox
            lightboxDelegate: '.cbp-lightbox',
            lightboxGallery: true,
            lightboxTitleSrc: 'data-title',
            lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>',
        });
    }

function checkIfLoggedIn(){
    var email = sessionStorage.getItem('email');
    var username = sessionStorage.getItem('username');
    if (email == null || username == null) {
            location.href='login.html';
    }
}

function loadHomePage(){
    checkIfLoggedIn();
    $("#userdata-container").html("Logged in as "+sessionStorage.getItem('name')+" ("+sessionStorage.getItem('username')+")");
    var datadir = {};
    var htmlstr="";
    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/photos',
        type: 'GET',
        crossDomain: true,
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            $.each(data, function(index, value) {
                //console.log(value);
                htmlstr = htmlstr + '<div class=\"cbp-item idea web-design theme-portfolio-item-v2 theme-portfolio-item-xs\"> <div class=\"cbp-caption\"> <div class=\"cbp-caption-defaultWrap theme-portfolio-active-wrap\"> <img src=\"'+value.URL+'\" alt=\"\"> <div class=\"theme-icons-wrap theme-portfolio-lightbox\"> <a class=\"cbp-lightbox\" href=\"'+value.URL+'\" data-title=\"Portfolio\"> <i class=\"theme-icons theme-icons-white-bg theme-icons-sm radius-3 icon-focus\"></i> </a> </div> </div> </div> <div class=\"theme-portfolio-title-heading\"> <h4 class=\"theme-portfolio-title\"><a href=\"viewphoto.html?id='+value.PhotoID+'\">'+value.Title+'</a></h4> <span class=\"theme-portfolio-subtitle\">by '+value.Username+'<br>'+value.CreationTime+'</span> </div> </div>';
                });
            console.log(htmlstr);
            $('#portfolio-4-col-grid').html(htmlstr);
            handlePortfolio4ColGrid();
            
        },
        error: function() {
            console.log("Failed");
        }
    });    
}

function loadAddPhotosPage(){
    checkIfLoggedIn();
    $("#userdata-container").html("Logged in as "+sessionStorage.getItem('name')+" ("+sessionStorage.getItem('username')+")");
}

function loadViewPhotoPage(){
    checkIfLoggedIn();
    $("#userdata-container").html("Logged in as "+sessionStorage.getItem('name')+" ("+sessionStorage.getItem('username')+")");
    PhotoID=$.urlParam('id');
    console.log(PhotoID);
    var htmlstr="";
    var tagstr="";
    $.ajax({
        url: 'https://swz197o3of.execute-api.us-east-1.amazonaws.com/dev/photos/'+PhotoID,
        type: 'GET',
        crossDomain: true,
        dataType: 'json',
        contentType: "application/json",
        success: function(data) {            
            console.log(data);
            photo=data[0];
            htmlstr = htmlstr + '<img class=\"img-responsive\" src=\"'+photo.URL+'\" alt=\"\"> <div class=\"blog-grid-content\"> <h2 class=\"blog-grid-title-lg\"><a class=\"blog-grid-title-link\" href=\"#\">'+photo.Title+'</a></h2> <p>By: '+photo.Username+'</p> <p>Uploaded: '+photo.CreationTime+'</p> <p>'+photo.Description+'</p></div>'
            $('#viewphoto-container').html(htmlstr);
            tags=photo.Tags.split(',');
            console.log(tags)
            $.each(tags, function(index, value) {
                tagstr=tagstr+'<li><a class=\"radius-50\" href=\"#\">'+value+'</a></li>';
            });
            $('#tags-container').html(tagstr);
        },
        error: function() {
            console.log("Failed");
        }
    });   
}

$(document).ready(function(){
    $("#loginform" ).submit(function(event) {
      processLogin();
      event.preventDefault();
    });

    $("#signupform" ).submit(function(event) {
      processSignup();
      event.preventDefault();
    });

    $("#addphotoform" ).submit(function(event) {
      uploadPhoto();
      event.preventDefault();
    });

    $("#searchform" ).submit(function(event) {
      searchPhotos();
      event.preventDefault();
    });

    $("#confirmemail-form" ).submit(function(event) {
      loadConfirmEmailPage();
      event.preventDefault();
    });


    var pathname = window.location.pathname; 
    console.log(pathname);

    if(pathname=='/index.html'){
        loadHomePage();
    }else if(pathname=='/addphoto.html'){
        loadAddPhotosPage();
    }else if(pathname=="/viewphoto.html"){
        loadViewPhotoPage();
    }else if(pathname=="/search.html"){
        loadSearchPage();
    }else if(pathname=="/confirmemail.html"){
        var username =  sessionStorage.getItem('username');
        $("#username").val(username);        
    }


    $("#logoutlink" ).click(function(event) {
      clearSession();
      event.preventDefault();
    });

});