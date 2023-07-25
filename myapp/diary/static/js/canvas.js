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


const pos = {
    drawable : false,
    x : -1,
    y : -1,
};
const canvas = document.getElementById('canvas');
const brushSize = document.getElementById('brush_size')
const ctx = canvas.getContext("2d");
const rect = canvas.getBoundingClientRect();  // 터치 스크린

// 전체 지우기
function clearAll(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// 스타일 추가
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

function colorChange(color){
    ctx.strokeStyle = color;
} 
canvas.addEventListener("mousedown", listener);
canvas.addEventListener("mousemove", listener);
canvas.addEventListener("mouseup", listener);
canvas.addEventListener("mouseout", listener);

/// 터치 스크린
canvas.addEventListener("touchstart", listener);
canvas.addEventListener("touchmove", listener);
canvas.addEventListener("touchend", listener);

// postFormBtn.addEventListener("onclick", savePost)
//브러쉬 사이즈 
brushSize.addEventListener("input",function(){
    ctx.lineWidth = brushSize.value;
})

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
            console.log("success")
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error on js")
            console.log(err, errmsg, xhr)
        }
    })
}

function listener(e){
    switch(e.type){
        case "mousedown":
            drawStart(e);
            break;
        case "mousemove":
            if(pos.drawable){
                draw(e);
            }
            break;
        case "mouseout":
        case "mouseup":
            drawEnd();
            break;
        case "touchstart":
            touchStart(e);
            break;
        case "touchmove":
            if(pos.drawable)
                touch(e);
            break;
        case "touchend":
            drawEnd();
            break;
        default:
    }
}

function drawStart(e){
    pos.drawable = true;
    ctx.beginPath();
    pos.x = e.offsetX;
    pos.y = e.offsetY;
    ctx.moveTo(pos.x, pos.y);
}
function touchStart(e){
    pos.drawable = true;
    ctx.beginPath();
    pos.x = e.touches[0].pageX - rect.left
    pos.y = e.touches[0].pageY - rect.top
    ctx.moveTo(pos.x, pos.y);
}
function draw(e){
    ctx.lineTo(e.offsetX, e.offsetY);
    pos.x = e.offsetX;
    pos.y = e.offsetY;
    ctx.stroke();
}
function touch(e){
    ctx.lineTo(e.touches[0].pageX - rect.left, e.touches[0].pageY - rect.top);
    pos.x = e.touches[0].pageX - rect.left;
    pos.y = e.touches[0].pageY - rect.top;
    ctx.stroke();
}
function drawEnd(){
    pos.drawable = false;
    pos.x = -1;
    pos.y = -1;
}