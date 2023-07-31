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