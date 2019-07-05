// Comment
var Comment = function() {
    "use strict";

    // Handle Comment Form
    var handleCommentForm = function() {
        $().ready(function() {
            // validate the comment form when it is submitted
            $("#comment-form").validate();
        });
    }

    return {
        init: function() {
            handleCommentForm(); // initial setup for comment form
        }
    }
}();

$(document).ready(function() {
    Comment.init();
});
