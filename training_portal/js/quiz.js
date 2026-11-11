const quizData = [
    {
        question: "Bạn nhận được email từ IT thông báo cần cập nhật lại mật khẩu trong 2 giờ tới, đường dẫn nhận được là: 'http://security-update-it.test/login'. Bạn sẽ xử lý thế nào?",
        scenario: "From: it-admin@company-security.test\nSubject: [URGENT] Yêu cầu cập nhật mật khẩu gấp",
        options: [
            { text: "A. Nhấp vào đường dẫn ngay lập tức và nhập thông tin vì từ phòng IT.", correct: false },
            { text: "B. Kiểm tra lại tên miền người gửi/đường dẫn, không nhập thông tin và báo cáo bộ phận IT.", correct: true },
            { text: "C. Chuyển tiếp email này cho đồng nghiệp cùng thực hiện.", correct: false }
        ],
        explanation: "Chính xác! Email có tính chất hối thúc thời gian khẩn cấp và tên miền lạ là những dấu hiệu điển hình của Phishing. Luôn xác minh lại qua kênh nội bộ."
    },
    {
        question: "Kiện hàng của bạn bị tạm giữ do sai thông tin giao nhận, email yêu cầu nhấp liên kết để cập nhật lại thông tin cá nhân. Dấu hiệu nào đáng nghi nhất?",
        scenario: "From: delivery-service@post-express-notice.com\nSubject: Thông báo giao kiện hàng #PL-9982",
        options: [
            { text: "A. Bạn không chủ động chờ nhận bất kỳ kiện hàng nào từ người gửi này.", correct: false },
            { text: "B. Địa chỉ email không khớp với đơn vị vận chuyển chính thức.", correct: false },
            { text: "C. Tất cả các phương án trên.", correct: true }
        ],
        explanation: "Đúng rồi! Cả việc nhận thông báo kiện hàng bất ngờ lẫn địa chỉ email giả mạo đơn vị vận chuyển đều là dấu hiệu lừa đảo phổ biến."
    },
    {
        question: "Phương pháp nào sau đây là an toàn nhất khi nhận được email có dấu hiệu nghi ngờ?",
        scenario: "Hành vi an toàn trong môi trường làm việc kỹ thuật số.",
        options: [
            { text: "A. Trả lời trực tiếp email đó để hỏi xem có phải lừa đảo không.", correct: false },
            { text: "B. Không nhấp vào bất kỳ liên kết/file đính kèm nào, xác minh qua kênh liên lạc độc lập.", correct: true },
            { text: "C. Tải file đính kèm về máy để kiểm tra xem có virus không.", correct: false }
        ],
        explanation: "Chính xác! Đừng bao giờ trả lời email lừa đảo hoặc tải file đính kèm. Hãy dùng kênh liên lạc chính thức (điện thoại/chat nội bộ) để xác minh."
    }
];

let currentQuestionIndex = 0;
let score = 0;

const questionNumberEl = document.getElementById('question-number');
const questionTextEl = document.getElementById('question-text');
const scenarioBoxEl = document.getElementById('scenario-box');
const optionsGroupEl = document.getElementById('options-group');
const explanationBoxEl = document.getElementById('explanation-box');
const btnNext = document.getElementById('btn-next');
const progressBar = document.getElementById('progress-bar');

function loadQuestion() {
    const currentQuiz = quizData[currentQuestionIndex];
    questionNumberEl.innerText = `Câu hỏi ${currentQuestionIndex + 1} / ${quizData.length}`;
    progressBar.style.width = `${((currentQuestionIndex + 1) / quizData.length) * 100}%`;
    questionTextEl.innerText = currentQuiz.question;
    scenarioBoxEl.innerText = currentQuiz.scenario;
    optionsGroupEl.innerHTML = '';
    explanationBoxEl.className = 'explanation-box';
    explanationBoxEl.innerText = '';
    btnNext.disabled = true;

    currentQuiz.options.forEach((opt) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = opt.text;
        btn.onclick = () => selectOption(btn, opt.correct, currentQuiz.explanation);
        optionsGroupEl.appendChild(btn);
    });
}

function selectOption(selectedBtn, isCorrect, explanation) {
    const allBtns = optionsGroupEl.querySelectorAll('.option-btn');
    allBtns.forEach(btn => btn.disabled = true);

    if (isCorrect) {
        selectedBtn.classList.add('correct');
        score++;
        explanationBoxEl.style.backgroundColor = 'rgba(16, 185, 129, 0.15)';
        explanationBoxEl.style.border = '1px solid #10b981';
        explanationBoxEl.style.color = '#34d399';
    } else {
        selectedBtn.classList.add('wrong');
        explanationBoxEl.style.backgroundColor = 'rgba(239, 68, 68, 0.15)';
        explanationBoxEl.style.border = '1px solid #ef4444';
        explanationBoxEl.style.color = '#fca5a5';
    }

    explanationBoxEl.innerText = explanation;
    explanationBoxEl.classList.add('show');
    btnNext.disabled = false;
}

btnNext.addEventListener('click', () => {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizData.length) {
        loadQuestion();
    } else {
        showResult();
    }
});

function showResult() {
    document.getElementById('quiz-screen').classList.add('hidden');
    const resultScreen = document.getElementById('result-screen');
    resultScreen.classList.remove('hidden');

    document.getElementById('score-text').innerText = `${score}/${quizData.length}`;
    const resultTitle = document.getElementById('result-title');
    const resultDesc = document.getElementById('result-desc');

    if (score === quizData.length) {
        resultTitle.innerText = "Xuất Sắc!";
        resultDesc.innerText = "Bạn có khả năng nhận diện các cuộc tấn công Phishing rất tốt.";
    } else if (score >= 1) {
        resultTitle.innerText = "Khá Tốt!";
        resultDesc.innerText = "Bạn đã nhận biết được một số dấu hiệu, nhưng hãy cẩn trọng hơn với các kịch bản tinh vi.";
    } else {
        resultTitle.innerText = "Cần Cải Thiện!";
        resultDesc.innerText = "Hãy ôn lại 5 dấu hiệu nhận biết phishing trên trang Landing Page để bảo vệ tài khoản tốt hơn.";
    }
}

function restartQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    document.getElementById('result-screen').classList.add('hidden');
    document.getElementById('quiz-screen').classList.remove('hidden');
    loadQuestion();
}

loadQuestion();