const quizData = [
  {
    question:
      "Bạn nhận được email từ IT yêu cầu cập nhật mật khẩu trong 2 giờ tới qua một đường dẫn lạ. Bạn nên làm gì?",
    scenario:
      "From: it-admin@company-security.test\nSubject: [URGENT] Yêu cầu cập nhật mật khẩu",
    options: [
      {
        text: "A. Nhấp vào liên kết và cập nhật ngay.",
        correct: false,
      },
      {
        text: "B. Kiểm tra tên miền, xác minh qua IT và báo cáo email đáng ngờ.",
        correct: true,
      },
      {
        text: "C. Chuyển tiếp email cho đồng nghiệp thực hiện.",
        correct: false,
      },
    ],
    explanation:
      "Email tạo áp lực thời gian và sử dụng tên miền lạ. Cần xác minh thông tin qua kênh IT chính thức.",
  },
  {
    question:
      "Trong email thông báo giao hàng, những yếu tố nào sau đây đáng nghi?",
    scenario:
      "From: delivery-service@post-express-notice.com\nSubject: Thông báo giao kiện hàng PL-9982",
    options: [
      {
        text: "A. Bạn không chờ nhận kiện hàng nào.",
        correct: false,
      },
      {
        text: "B. Địa chỉ người gửi không được xác minh là thuộc đơn vị vận chuyển.",
        correct: false,
      },
      {
        text: "C. Cả A và B đều là dấu hiệu đáng nghi.",
        correct: true,
      },
    ],
    explanation:
      "Thông báo bất ngờ và địa chỉ người gửi không đáng tin cậy đều là dấu hiệu cần kiểm tra.",
  },
  {
    question: "Phương pháp nào an toàn nhất khi nhận được email đáng ngờ?",
    scenario: "Tình huống xử lý email phishing.",
    options: [
      {
        text: "A. Trả lời email để hỏi người gửi.",
        correct: false,
      },
      {
        text: "B. Không nhấp liên kết, xác minh qua kênh chính thức và báo cáo email.",
        correct: true,
      },
      {
        text: "C. Tải file đính kèm về máy để kiểm tra.",
        correct: false,
      },
    ],
    explanation:
      "Không tương tác với liên kết hoặc tệp đáng ngờ. Hãy xác minh độc lập và báo cáo cho bộ phận phụ trách.",
  },
  {
    question:
      "Bạn nhận được đường dẫn https://portal.phishlab.test.verify.example/update. Dấu hiệu nào cần chú ý?",
    scenario: "URL trong tình huống: portal.phishlab.test.verify.example",
    options: [
      {
        text: "A. Có chữ phishlab nên chắc chắn là website chính thức.",
        correct: false,
      },
      {
        text: "B. Tên miền thực tế cần kiểm tra là verify.example, không phải phishlab.test.",
        correct: true,
      },
      {
        text: "C. Có HTTPS nên chắc chắn an toàn.",
        correct: false,
      },
    ],
    explanation:
      "Tên thương hiệu có thể xuất hiện trong phần tên miền phụ. Cần kiểm tra hostname và tên miền thực tế, không chỉ nhìn một phần URL.",
  },
  {
    question:
      "Một website có biểu tượng ổ khóa và sử dụng HTTPS. Bạn có thể kết luận website đó đáng tin cậy không?",
    scenario: "Tình huống kiểm tra chứng chỉ HTTPS.",
    options: [
      {
        text: "A. Có, vì HTTPS chứng minh website chính thức.",
        correct: false,
      },
      {
        text: "B. Không. Cần kiểm tra chính xác tên miền và xác minh website qua nguồn chính thức.",
        correct: true,
      },
      {
        text: "C. Có, miễn là website hiển thị giao diện đẹp.",
        correct: false,
      },
    ],
    explanation:
      "HTTPS giúp mã hóa kết nối, nhưng không chứng minh website thuộc tổ chức mà bạn mong đợi.",
  },
];

let currentQuestionIndex = 0;
let score = 0;
let answered = false;

const questionNumberEl = document.getElementById("question-number");
const questionTextEl = document.getElementById("question-text");
const scenarioBoxEl = document.getElementById("scenario-box");
const optionsGroupEl = document.getElementById("options-group");
const explanationBoxEl = document.getElementById("explanation-box");
const btnNext = document.getElementById("btn-next");
const progressBar = document.getElementById("progress-bar");

function loadQuestion() {
  const currentQuiz = quizData[currentQuestionIndex];

  answered = false;

  questionNumberEl.innerText = `Câu hỏi ${currentQuestionIndex + 1} / ${quizData.length}`;

  progressBar.style.width = `${((currentQuestionIndex + 1) / quizData.length) * 100}%`;

  questionTextEl.innerText = currentQuiz.question;
  scenarioBoxEl.innerText = currentQuiz.scenario;

  optionsGroupEl.innerHTML = "";

  explanationBoxEl.className = "explanation-box";
  explanationBoxEl.innerText = "";

  btnNext.disabled = true;

  btnNext.innerText =
    currentQuestionIndex === quizData.length - 1
      ? "Xem kết quả"
      : "Câu tiếp theo";

  currentQuiz.options.forEach((opt, index) => {
    const btn = document.createElement("button");

    btn.className = "option-btn";
    btn.innerText = opt.text;

    btn.addEventListener("click", () => {
      selectOption(btn, index, currentQuiz);
    });

    optionsGroupEl.appendChild(btn);
  });
}

function selectOption(selectedBtn, selectedIndex, currentQuiz) {
  if (answered) {
    return;
  }

  answered = true;

  const allBtns = optionsGroupEl.querySelectorAll(".option-btn");

  const correctIndex = currentQuiz.options.findIndex(
    (option) => option.correct,
  );

  allBtns.forEach((btn, index) => {
    btn.disabled = true;

    if (index === correctIndex) {
      btn.classList.add("correct");
    }
  });

  const isCorrect = currentQuiz.options[selectedIndex].correct;

  if (isCorrect) {
    score++;
  } else {
    selectedBtn.classList.add("wrong");
  }

  if (isCorrect) {
    explanationBoxEl.style.backgroundColor = "rgba(16, 185, 129, 0.15)";

    explanationBoxEl.style.border = "1px solid #10b981";

    explanationBoxEl.style.color = "#34d399";

    explanationBoxEl.innerText = "Chính xác! " + currentQuiz.explanation;
  } else {
    explanationBoxEl.style.backgroundColor = "rgba(239, 68, 68, 0.15)";

    explanationBoxEl.style.border = "1px solid #ef4444";

    explanationBoxEl.style.color = "#fca5a5";

    explanationBoxEl.innerText =
      "Chưa chính xác. Đáp án đúng: " +
      currentQuiz.options[correctIndex].text +
      " " +
      currentQuiz.explanation;
  }

  explanationBoxEl.classList.add("show");

  btnNext.disabled = false;
}

btnNext.addEventListener("click", () => {
  if (currentQuestionIndex < quizData.length - 1) {
    currentQuestionIndex++;
    loadQuestion();
  } else {
    showResult();
  }
});

function showResult() {
  document.getElementById("quiz-screen").classList.add("hidden");

  const resultScreen = document.getElementById("result-screen");

  resultScreen.classList.remove("hidden");

  const percentage = Math.round((score / quizData.length) * 100);

  document.getElementById("score-text").innerText =
    `${score}/${quizData.length}`;

  const resultTitle = document.getElementById("result-title");
  const resultDesc = document.getElementById("result-desc");

  if (percentage === 100) {
    resultTitle.innerText = "Xuất sắc!";
  } else if (percentage >= 60) {
    resultTitle.innerText = "Khá tốt!";
  } else {
    resultTitle.innerText = "Cần cải thiện!";
  }

  resultDesc.innerText = `Bạn trả lời đúng ${score}/${quizData.length} câu, đạt ${percentage}%.`;

  const result = {
    score: score,
    total: quizData.length,
    percentage: percentage,
    completed: true,
    completedAt: new Date().toISOString(),
  };

  window.dispatchEvent(
    new CustomEvent("phishlab:quiz-completed", {
      detail: result,
    }),
  );
}

function restartQuiz() {
  currentQuestionIndex = 0;
  score = 0;

  document.getElementById("result-screen").classList.add("hidden");

  document.getElementById("quiz-screen").classList.remove("hidden");

  loadQuestion();
}

loadQuestion();
