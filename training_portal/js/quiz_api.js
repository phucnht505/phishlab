
const QUIZ_API_URL = "http://127.0.0.1:8000/quiz-event";
const QUIZ_SESSION_KEY = "phishlab_quiz_session_id";

function getQuizSessionId() {
  let sessionId = sessionStorage.getItem(QUIZ_SESSION_KEY);

  if (!sessionId) {
    sessionId = crypto.randomUUID
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(16).slice(2)}`;

    sessionStorage.setItem(QUIZ_SESSION_KEY, sessionId);
  }

  return sessionId;
}

const quizSessionId = getQuizSessionId();

async function sendQuizEvent(eventType, extraData = {}) {
  try {
    const response = await fetch(QUIZ_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: quizSessionId,
        event: eventType,
        ...extraData,
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    console.log("Quiz event sent:", eventType);
  } catch (error) {
    console.error("Cannot send quiz event:", error);
  }
}

sendQuizEvent("started");

window.addEventListener("phishlab:quiz-completed", (event) => {
  const percentage = event.detail?.percentage;

  if (
    typeof percentage !== "number" ||
    percentage < 0 ||
    percentage > 100
  ) {
    console.error("Invalid quiz percentage");
    return;
  }

  sendQuizEvent("completed", {
    percentage: percentage,
  });
});
