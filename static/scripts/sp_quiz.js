const quiz = {
    1: {
        'question': 'を向上させる',
        'answers': ['import', 'core', 'force', 'improve'],
        'correct': 'improve'
    },
    2: {
        'question': 'を関連づける',
        'answers': ['mental', 'relate', 'preoccupation', 'display'],
        'correct': 'relate'
    },
    3: {
        'question': 'を供給する',
        'answers': ['patch', 'forecast', 'surplus', 'provide'],
        'correct': 'provide'
    },
    4: {
        'question': '見なす',
        'answers': ['hesitate', 'sibling', 'hostage', 'consider'],
        'correct': 'consider'
    },
    5: {
        'question': 'を含む',
        'answers': ['signature', 'vessel', 'panic', 'include'],
        'correct': 'include'
    }
};


const $window = window;
const $doc = document;
const $question = $doc.getElementById('js-question');
const $buttons = $doc.querySelectorAll('.btn');

const quizLen = Object.keys(quiz).length;
let quizCount = 1;
let score = 0;

const init = () => {
    console.log(quizLen)
    $question.textContent = "(" + quizCount + ") " + quiz[quizCount].question;

    const buttonLen = $buttons.length;
    let btnIndex = 0;

    while (btnIndex < buttonLen) {
        $buttons[btnIndex].textContent = quiz[quizCount].answers[btnIndex];
        btnIndex++;
    }
};

const goToNext = () => {
    quizCount++;
    if (quizCount < quizLen + 1) {
        init(quizCount);
    } else {
        // $window.alert('クイズ終了！');
        showEnd();
    }
};

const judge = (elm) => {
    if (elm.textContent === quiz[quizCount].correct) {
        $window.alert('正解!');
        score++;
    } else {
        $window.alert('不正解!');
    }
    goToNext();
};

const showEnd = () => {
    $question.textContent = '終了！あなたのスコアは' + score + '/' + quizLen + 'です';

    const $items = $doc.getElementById('js-items');
    $items.style.visibility = 'hidden';
};

init();

function post() {
    xhr = new XMLHttpRequest();
    xhr.open('POST', 'calc.php', true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    // フォームに入力した値をリクエストとして設定
    var request = "arg1=" + arg1.value + "&arg2=" + arg2.value;
    xhr.send(request);
}

let answersIndex = 0;
let answersLen = quiz[quizCount].answers.length;

while (answersIndex < answersLen) {
    $buttons[answersIndex].addEventListener('click', (e) => {
        judge(e.target);
    });
    answersIndex++;
}
