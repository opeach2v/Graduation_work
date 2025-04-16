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
const sliderWrap = document.querySelector(".slider__wrap")
const sliderImg = sliderWrap.querySelector(".slider__img") //보여지는 영역
const sliderInner = sliderWrap.querySelector(".slider__inner")  //움직이는 영역
const slider = sliderWrap.querySelectorAll(".slider")     //개별 영역
const sliderDot = sliderWrap.querySelector(".slider__dot")
const sliderBtn = sliderWrap.querySelectorAll(".slider__btn a")

let currentIndex = 0;   //현재보이는 이미지
let sliderCount = slider.length;  //이미지 갯수
let sliderWidth = slider[0].offsetWidth;  //이미지 가로값
let sliderInterval = 1000; //이미지 변경 시간
let dotIndex = "";

function init(){
    //이미지 갯수만큼 닷 메뉴 생성
    slider.forEach(() => dotIndex += "<a href='#' class='dot'>이미지</a>");
    sliderDot.innerHTML = dotIndex;

    //첫번째 닷 메뉴에 활성화 표시
    sliderDot.firstChild.classList.add("active");
    
}
init();

function gotoSlider(num){
    sliderInner.style.transition = "all 400ms"
    sliderInner.style.transform = "translateX(" + -sliderWidth * num + "px)"
    currentIndex = num;

    let dotActive = document.querySelectorAll(".slider__dot .dot")
    dotActive.forEach((active)=>active.classList.remove("active"));
    dotActive[num].classList.add("active")

    //이미지에 맞는 닷 
}

//버튼을 클릭했을 때
sliderBtn.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        let prevIndex = (currentIndex + sliderCount - 1) % sliderCount
        let nextIndex = (currentIndex + 1) % sliderCount

        if (btn.classList.contains("prev")) {
            gotoSlider(prevIndex)
        } else {
            gotoSlider(nextIndex)
        }
    })
})