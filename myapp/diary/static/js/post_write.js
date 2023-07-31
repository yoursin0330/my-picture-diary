function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('.post-form').on('submit', function(e){
    e.preventDefault();
    console.log("form submitted")
    createPost();
    $('.post-form').unbind();
    
})
function createPost(){
    console.log("create post is working..!")
    const imageURL = canvas.toDataURL();
    $.ajax({
        url:'/diary/write/',
        type : "POST",
        data : { // post request로 data 보내기
            title : $("#id_title").val(),
            content : $("#id_content").val(),
            imgURL: imageURL,
            mood: $("#id_mood").val(),
            
        },
        success : function(){
            window.location.href = '/diary/';
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error on js")
            console.log(err, errmsg, xhr)
        }
    })
}