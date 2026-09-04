const API_URL = "http://127.0.0.1:8000";


// ==========================================
// ELEMENTS
// ==========================================

const fileInput = document.getElementById("csvFile");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");


// ==========================================
// NAVIGATION
// ==========================================

const navItems = document.querySelectorAll(".nav-item");
const sections = document.querySelectorAll(".section");


navItems.forEach(item => {

    item.addEventListener("click", () => {

        const target = item.dataset.section;

        navItems.forEach(nav => {
            nav.classList.remove("active");
        });

        item.classList.add("active");


        sections.forEach(section => {

            section.classList.remove("active");

            if (section.id === target) {
                section.classList.add("active");
            }

        });

    });

});


// ==========================================
// FILE SELECTION
// ==========================================

fileInput.addEventListener("change", () => {

    if (fileInput.files.length === 0) {
        fileName.textContent = "Choose Network Traffic CSV";
        return;
    }

    fileName.textContent = fileInput.files[0].name;

});


// ==========================================
// CHART
// ==========================================

let threatChart = null;


function createChart(benign, ddos, portscan) {

    const canvas = document.getElementById("threatChart");

    if (threatChart) {
        threatChart.destroy();
    }


    threatChart = new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: [
                "BENIGN",
                "DDoS",
                "PortScan"
            ],

            datasets: [{

                data: [
                    benign,
                    ddos,
                    portscan
                ],

                backgroundColor: [
                    "#35a8e0",
                    "#ff5f78",
                    "#ff9d3d"
                ],

                borderColor: "#101a2b",

                borderWidth: 4

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "55%",

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    });

}


// ==========================================
// NUMBER FORMAT
// ==========================================

function formatNumber(number) {

    return Number(number).toLocaleString("en-IN");

}


// ==========================================
// SEVERITY STYLE
// ==========================================

function updateSeverity(severity) {

    const element = document.getElementById("severity");

    element.textContent = severity;

    if (severity === "CRITICAL") {

        element.style.color = "#ff4545";

    } else if (severity === "HIGH") {

        element.style.color = "#ff7b45";

    } else if (severity === "MEDIUM") {

        element.style.color = "#ffbd45";

    } else {

        element.style.color = "#32d978";

    }

}


// ==========================================
// ANALYZE CSV
// ==========================================

analyzeBtn.addEventListener("click", async () => {

    if (fileInput.files.length === 0) {

        showError(
            "Please choose a network traffic CSV file first."
        );

        return;
    }


    const file = fileInput.files[0];


    if (!file.name.toLowerCase().endsWith(".csv")) {

        showError(
            "Only CSV files are supported."
        );

        return;
    }


    // Form data

    const formData = new FormData();

    formData.append(
        "file",
        file
    );


    // UI state

    analyzeBtn.disabled = true;

    loading.classList.remove("hidden");

    errorMessage.classList.add("hidden");


    try {

        const response = await fetch(
            `${API_URL}/analyze`,
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            throw new Error(
                "AI server returned an error."
            );

        }


        const result = await response.json();


        if (result.error) {

            throw new Error(
                result.error
            );

        }


        updateDashboard(result);


    } catch (error) {

        console.error(error);

        showError(
            "Could not connect to AI server. Make sure FastAPI is running."
        );

    } finally {

        analyzeBtn.disabled = false;

        loading.classList.add("hidden");

    }

});


// ==========================================
// UPDATE DASHBOARD
// ==========================================

function updateDashboard(result) {

    const total = result.total_flows || 0;

    const benign = result.benign || 0;

    const ddos = result.ddos || 0;

    const portscan = result.portscan || 0;

    const threats = result.threats || 0;
    // ======================================
// AI INVESTIGATION
// ======================================

const benignPercent =
    total > 0
        ? ((benign / total) * 100).toFixed(2)
        : 0;

const ddosPercent =
    total > 0
        ? ((ddos / total) * 100).toFixed(2)
        : 0;

const portscanPercent =
    total > 0
        ? ((portscan / total) * 100).toFixed(2)
        : 0;


// DDoS

document.getElementById(
    "investigationDdos"
).textContent = formatNumber(ddos);

document.getElementById(
    "investigationDdosPercent"
).textContent =
    `${ddosPercent}% of traffic`;


// PortScan

document.getElementById(
    "investigationPort"
).textContent = formatNumber(portscan);

document.getElementById(
    "investigationPortPercent"
).textContent =
    `${portscanPercent}% of traffic`;


// Benign

document.getElementById(
    "investigationBenign"
).textContent = formatNumber(benign);

document.getElementById(
    "investigationBenignPercent"
).textContent =
    `${benignPercent}% of traffic`;


// AI Confidence

document.getElementById(
    "investigationConfidence"
).textContent =
    `${result.confidence}%`;


    // ======================================
    // STAT CARDS
    // ======================================

    document.getElementById(
        "totalFlows"
    ).textContent = formatNumber(total);


    document.getElementById(
        "benignFlows"
    ).textContent = formatNumber(benign);


    document.getElementById(
        "threatFlows"
    ).textContent = formatNumber(threats);


    document.getElementById(
        "threatRate"
    ).textContent =
        `${result.threat_percentage}%`;


    // ======================================
    // THREAT DETAILS
    // ======================================

    document.getElementById(
        "ddosCount"
    ).textContent = formatNumber(ddos);


    document.getElementById(
        "portscanCount"
    ).textContent = formatNumber(portscan);


    document.getElementById(
        "benignCount"
    ).textContent = formatNumber(benign);


    // ======================================
    // LATEST RESULT
    // ======================================

    document.getElementById(
        "emptyResult"
    ).classList.add("hidden");


    document.getElementById(
        "analysisResult"
    ).classList.remove("hidden");


    document.getElementById(
        "resultThreats"
    ).textContent = formatNumber(threats);


    document.getElementById(
        "riskScore"
    ).textContent =
        `${result.risk_score}/100`;


    document.getElementById(
        "confidence"
    ).textContent =
        `${result.confidence}%`;


    updateSeverity(result.severity);


    // ======================================
    // CHART
    // ======================================

    createChart(
        benign,
        ddos,
        portscan
    );


    // ======================================
    // THREAT PAGE
    // ======================================

    document.getElementById(
        "threatOverview"
    ).textContent = formatNumber(threats);


    document.getElementById(
        "ddosOverview"
    ).textContent = formatNumber(ddos);


    document.getElementById(
        "portOverview"
    ).textContent = formatNumber(portscan);


    // ======================================
    // RESULT TITLE
    // ======================================

    const title =
        document.getElementById("resultTitle");


    if (threats === 0) {

        title.textContent =
            "No Threats Detected";

    } else {

        title.textContent =
            "Potential Threats Detected";

    }

}


// ==========================================
// ERROR
// ==========================================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

}