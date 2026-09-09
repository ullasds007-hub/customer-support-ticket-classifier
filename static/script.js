const ticketInput = document.getElementById("ticketInput");

const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const resultCard = document.getElementById("resultCard");

const categoryResult =
    document.getElementById("categoryResult");

const priorityResult =
    document.getElementById("priorityResult");

const errorMessage =
    document.getElementById("errorMessage");

const loadingBox =
    document.getElementById("loadingBox");

const historyList =
    document.getElementById("historyList");

const sampleButtons =
    document.querySelectorAll(".sample-btn");


let predictionHistory = [];
let sessionStats = {
    total: 0,
    high: 0,
    medium: 0,
    low: 0
};


sampleButtons.forEach(button => {

    button.addEventListener("click", () => {

        ticketInput.value =
            button.dataset.ticket;

        ticketInput.focus();

    });

});


clearBtn.addEventListener("click", () => {

    ticketInput.value = "";

    errorMessage.textContent = "";

    resultCard.classList.add("hidden");

    ticketInput.focus();

});


analyzeBtn.addEventListener("click", async () => {

    const ticket = ticketInput.value.trim();

    errorMessage.textContent = "";

    if (!ticket) {

        errorMessage.textContent =
            "Please enter a support ticket.";

        resultCard.classList.add("hidden");

        return;
    }

    analyzeBtn.disabled = true;

    loadingBox.classList.remove("hidden");

    resultCard.classList.add("hidden");

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                ticket: ticket
            })

        });

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || "Unable to analyze ticket."
            );

        }

        categoryResult.textContent =
            data.category;

        priorityResult.textContent =
            data.priority;

        priorityResult.className =
            "priority-badge";

        if (data.priority === "High") {

            priorityResult.classList.add(
                "priority-high"
            );

        }

        else if (data.priority === "Medium") {

            priorityResult.classList.add(
                "priority-medium"
            );

        }

        else {

            priorityResult.classList.add(
                "priority-low"
            );

        }

        resultCard.classList.remove("hidden");

        addToHistory(
            ticket,
            data.category,
            data.priority
        );
        updateDashboardStats(
            data.priority
        );

    }

    catch (error) {

        errorMessage.textContent =
            error.message;

    }

    finally {

        loadingBox.classList.add("hidden");

        analyzeBtn.disabled = false;

    }

});


function addToHistory(ticket, category, priority) {

    predictionHistory.unshift({
        ticket,
        category,
        priority
    });

    predictionHistory =
        predictionHistory.slice(0, 5);

    renderHistory();

}


function renderHistory() {

    historyList.innerHTML = "";

    if (predictionHistory.length === 0) {

        historyList.innerHTML = `
            <div class="empty-history">
                No tickets analyzed yet.
            </div>
        `;

        return;
    }

    predictionHistory.forEach(item => {

        const row =
            document.createElement("div");

        row.className =
            "history-item";

        row.innerHTML = `
            <span class="history-text">
                ${escapeHtml(item.ticket)}
            </span>

            <span class="history-category">
                ${escapeHtml(item.category)}
            </span>

            <span class="history-priority">
                ${escapeHtml(item.priority)}
            </span>
        `;

        historyList.appendChild(row);

    });

}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}
const introScreen =
    document.getElementById("introScreen");

const introProgress =
    document.getElementById("introProgress");

const progressNumber =
    document.getElementById("progressNumber");

const loadingText =
    document.getElementById("loadingText");

const appShell =
    document.querySelector(".app-shell");


let introValue = 0;


const loadingStages = [

    {
        value: 20,
        text: "Loading classification model..."
    },

    {
        value: 45,
        text: "Initializing TF-IDF engine..."
    },

    {
        value: 68,
        text: "Connecting priority system..."
    },

    {
        value: 88,
        text: "Preparing SupportAI dashboard..."
    },

    {
        value: 100,
        text: "System ready."
    }

];


let stageIndex = 0;


const introInterval =
    setInterval(() => {

        introValue += 1;

        introProgress.style.width =
            introValue + "%";

        progressNumber.textContent =
            introValue + "%";


        if (
            stageIndex < loadingStages.length &&
            introValue >=
                loadingStages[stageIndex].value
        ) {

            loadingText.textContent =
                loadingStages[stageIndex].text;

            stageIndex++;

        }


        if (introValue >= 100) {

            clearInterval(introInterval);

            setTimeout(() => {

                introScreen.classList.add(
                    "hide-intro"
                );

                appShell.classList.add(
                    "dashboard-entry"
                );

            }, 500);

        }

    }, 28);
    /* ==================================================
   SIDEBAR NAVIGATION
================================================== */

const navItems =
    document.querySelectorAll(".nav-item");

const pageSections =
    document.querySelectorAll(".page-section");


navItems.forEach(item => {

    item.addEventListener("click", () => {

        const sectionId =
            item.dataset.section;

        navItems.forEach(nav => {
            nav.classList.remove("active");
        });

        pageSections.forEach(section => {
            section.classList.remove(
                "active-section"
            );
        });

        item.classList.add("active");

        document
            .getElementById(sectionId)
            .classList.add("active-section");

    });

});


/* ==================================================
   CURSOR TRACKING
================================================== */

const cursorGlow =
    document.getElementById("cursorGlow");

const cursorDot =
    document.getElementById("cursorDot");


let mouseX = 0;
let mouseY = 0;

let glowX = 0;
let glowY = 0;


document.addEventListener(
    "mousemove",
    event => {

        mouseX = event.clientX;
        mouseY = event.clientY;

        cursorDot.style.left =
            mouseX + "px";

        cursorDot.style.top =
            mouseY + "px";

    }
);


function animateCursorGlow() {

    glowX +=
        (mouseX - glowX) * 0.09;

    glowY +=
        (mouseY - glowY) * 0.09;

    cursorGlow.style.left =
        glowX + "px";

    cursorGlow.style.top =
        glowY + "px";

    requestAnimationFrame(
        animateCursorGlow
    );

}


animateCursorGlow();


/* ==================================================
   3D CARD CURSOR TILT
================================================== */

const tiltCards =
    document.querySelectorAll(".tilt-card");


tiltCards.forEach(card => {

    card.addEventListener(
        "mousemove",
        event => {

            const rect =
                card.getBoundingClientRect();

            const x =
                event.clientX -
                rect.left;

            const y =
                event.clientY -
                rect.top;

            const centerX =
                rect.width / 2;

            const centerY =
                rect.height / 2;

            const rotateX =
                ((y - centerY) /
                    centerY) * -4;

            const rotateY =
                ((x - centerX) /
                    centerX) * 4;

            card.style.transform =
                `
                perspective(900px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                translateY(-3px)
                `;

            card.style.setProperty(
                "--mx",
                (x / rect.width) * 100 + "%"
            );

            card.style.setProperty(
                "--my",
                (y / rect.height) * 100 + "%"
            );

        }
    );


    card.addEventListener(
        "mouseleave",
        () => {

            card.style.transform =
                `
                perspective(900px)
                rotateX(0deg)
                rotateY(0deg)
                translateY(0)
                `;

        }
    );

});


/* ==================================================
   LIVE DASHBOARD COUNTERS
================================================== */

  


function updateDashboardStats(priority) {

    sessionStats.total++;

    if (priority === "High") {
        sessionStats.high++;
    }

    else if (priority === "Medium") {
        sessionStats.medium++;
    }

    else {
        sessionStats.low++;
    }


    document.getElementById(
        "totalTickets"
    ).textContent =
        sessionStats.total;


    document.getElementById(
        "highCount"
    ).textContent =
        sessionStats.high;


    document.getElementById(
        "highValue"
    ).textContent =
        sessionStats.high;

    document.getElementById(
        "mediumValue"
    ).textContent =
        sessionStats.medium;

    document.getElementById(
        "lowValue"
    ).textContent =
        sessionStats.low;


    const total =
        sessionStats.total || 1;


    document.getElementById(
        "highBar"
    ).style.width =
        (
            sessionStats.high /
            total * 100
        ) + "%";


    document.getElementById(
        "mediumBar"
    ).style.width =
        (
            sessionStats.medium /
            total * 100
        ) + "%";


    document.getElementById(
        "lowBar"
    ).style.width =
        (
            sessionStats.low /
            total * 100
        ) + "%";

}