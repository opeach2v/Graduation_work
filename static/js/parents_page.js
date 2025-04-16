// 알림장 팝업 띄우기
function openPop() {
    document.getElementById("popup_layer").style.display = "block";
}
// 알림장 팝업 닫기
function closePop() {
    document.getElementById("popup_layer").style.display = "none";
}

// 오늘의 하루 팝업 띄우기
function openTodayPop() {
    document.getElementById("today_popup_layer").style.display = "block";
}
// 오늘의 하루 팝업 닫기
function closeTodayPop() {
    document.getElementById("today_popup_layer").style.display = "none";
}

// 사진/영상 슬라이드
const prev = document.querySelector('.prev');
const next = document.querySelector('.next');
const slideBox = document.querySelector('.slide_box')
const slide = document.querySelectorAll('.slide_item img')
const slideLangth = slide.length
let currentIndex = 0;

const moveSlide = function(num){
    slideBox.style.transform = `translateX(${-num * 400}px)`;
    currentIndex = num;
}

prev.addEventListener('click', ()=>{
    if(currentIndex !== 0){
        moveSlide(currentIndex -1)
    }
})

next.addEventListener('click', ()=>{
    if(currentIndex !== slideLangth -1){
        moveSlide(currentIndex +1)
    }
})