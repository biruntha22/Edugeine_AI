const task =
    document.getElementById("task");

const input =
    document.getElementById("input");

const level =
    document.getElementById("level");

const levelWrap =
    document.getElementById("levelWrap");

const run =
    document.getElementById("run");

const result =
    document.getElementById("result");

const status =
    document.getElementById("status");

const copy =
    document.getElementById("copy");


// --------------------------------------------------
// Task change
// --------------------------------------------------

task.addEventListener(
    "change",
    function () {

        if (task.value === "learn") {

            levelWrap.classList.remove(
                "hidden"
            );

            input.placeholder =
                "Example: Python Programming";

        }

        else {

            levelWrap.classList.add(
                "hidden"
            );

            input.placeholder =
                "Type your question, concept, topic or text...";

        }

    }
);


// --------------------------------------------------
// Escape HTML
// --------------------------------------------------

function escapeHtml(value) {

    return String(value)
        .replace(
            /[&<>'"]/g,
            function (character) {

                const map = {

                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    "'": "&#39;",
                    '"': "&quot;"

                };

                return map[character];

            }
        );

}


// --------------------------------------------------
// Render result
// --------------------------------------------------

function renderResult(data) {

    if (task.value === "quiz") {

        result.classList.remove(
            "empty"
        );

        result.innerHTML =
            data.questions
                .map(
                    function (question, index) {

                        return `
                            <div class="quiz-q">

                                <strong>
                                    ${index + 1}.
                                    ${escapeHtml(
                                        question.question
                                    )}
                                </strong>

                                ${question.options
                                    .map(
                                        function (option) {

                                            return `
                                                <div class="option">
                                                    ${escapeHtml(option)}
                                                </div>
                                            `;

                                        }
                                    )
                                    .join("")
                                }

                                <p>
                                    <b>Answer:</b>
                                    ${escapeHtml(
                                        question.answer
                                    )}
                                </p>

                                <small>
                                    ${escapeHtml(
                                        question.explanation || ""
                                    )}
                                </small>

                            </div>
                        `;

                    }
                )
                .join("");

        return;
    }


    const text =
        data.answer ||
        data.explanation ||
        data.summary ||
        data.recommendations ||
        "No result returned.";

    result.textContent = text;

    result.classList.remove(
        "empty"
    );
}


// --------------------------------------------------
// Run API
// --------------------------------------------------

run.addEventListener(
    "click",
    async function () {

        const value =
            input.value.trim();


        if (!value) {

            status.textContent =
                "Please enter something first.";

            return;

        }


        run.disabled = true;

        status.textContent =
            "EduGenie is working...";

        result.textContent = "";


        const routes = {

            qa:
                "/api/qa",

            explain:
                "/api/explain",

            quiz:
                "/api/quiz",

            summarize:
                "/api/summarize",

            learn:
                "/api/learn/recommendations"

        };


        let body;


        if (task.value === "learn") {

            body = {

                topic: value,

                level: level.value

            };

        }

        else {

            body = {

                text: value

            };

        }


        try {

            const response =
                await fetch(
                    routes[task.value],
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Request failed."
                );

            }


            renderResult(data);


            status.textContent =
                "Completed • Source: " +
                (
                    data.source ||
                    "unknown"
                );

        }

        catch (error) {

            result.textContent =
                error.message;

            status.textContent =
                "Something went wrong.";

        }

        finally {

            run.disabled = false;

        }

    }
);


// --------------------------------------------------
// Copy button
// --------------------------------------------------

copy.addEventListener(
    "click",
    async function () {

        const text =
            result.innerText.trim();


        if (!text) {

            return;

        }


        try {

            await navigator.clipboard
                .writeText(text);

            status.textContent =
                "Result copied.";

        }

        catch {

            status.textContent =
                "Copy failed.";

        }

    }
);