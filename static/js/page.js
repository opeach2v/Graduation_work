// 개인 알림장 열기
function openForm() {
    const container = document.getElementById('homeworkContainer');
    const formArea = document.getElementById('formArea');
    const formAreaAll = document.getElementById('formAreaAll');

    container.classList.add('open');
    formArea.style.width = '400px';
    formArea.style.padding = '1px';      // 보여줄 때만 padding 추가
    formArea.style.opacity = '1';
    formArea.style.pointerEvents = 'auto';

    formAreaAll.style.width = '0';
    formAreaAll.style.padding = '0';      // 안 보이게 padding 제거
    formAreaAll.style.opacity = '0';
    formAreaAll.style.pointerEvents = 'none';
};

// 공통 내용 알림장 열기
function openFormAll() {
    const container = document.getElementById('homeworkContainer');
    const formArea = document.getElementById('formArea');
    const formAreaAll = document.getElementById('formAreaAll');

    container.classList.add('open');
    container.classList.add('open');
    formAreaAll.style.width = '400px';
    formAreaAll.style.padding = '1px';
    formAreaAll.style.opacity = '1';
    formAreaAll.style.pointerEvents = 'auto';

    formArea.style.width = '0';
    formArea.style.padding = '0';
    formArea.style.opacity = '0';
    formArea.style.pointerEvents = 'none';
};

function closeForm() {
    const formArea = document.getElementById('formArea');
    const formAreaAll = document.getElementById('formAreaAll');
    const container = document.getElementById('homeworkContainer');

    formArea.style.width = '0';
    formArea.style.padding = '0';
    formArea.style.opacity = '0';
    formArea.style.pointerEvents = 'none';

    formAreaAll.style.width = '0';
    formAreaAll.style.padding = '0';
    formAreaAll.style.opacity = '0';
    formAreaAll.style.pointerEvents = 'none';

    container.classList.remove('open');
}

// 로그인 페이지 로그인 버튼 임시
function login() {
    const id = document.getElementById('id').value;
    const pw = document.getElementById('password').value;

    if (id == '' && pw == '') {
        alert('아이디와 비밀번호를 입력해주세요.');
        return;
    }
    if (id == 'aaa' && pw == 'bbb') {
        alert('아이디와 비밀번호가 틀렸습니다.');
        return;
    }

    window.location.href = 'teachers_page.html';
}