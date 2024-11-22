async function checkEligibility() {
    const studentID = document.getElementById('studentID').value;

    if (!studentID) {
        alert("Please enter a valid Student ID!");
        return;
    }

    try {
        // Fetch scholarship status
        const scholarshipResponse = await fetch(`http://localhost:3000/check_scholarship?student_id=${studentID}`);
        const scholarshipData = await scholarshipResponse.json();

        // Fetch exam permission status
        const examResponse = await fetch(`http://localhost:3000/check_exam_permission?student_id=${studentID}`);
        const examData = await examResponse.json();

        // Format statuses
        const scholarshipStatusText = scholarshipData.status === "not_eligible" ? "Not Eligible" : "Eligible";
        const scholarshipStatusClass = scholarshipData.status === "not_eligible" ? "negative" : "positive";

        const examStatusText = examData.status === "not_permitted" ? "Not Permitted" : "Permitted";
        const examStatusClass = examData.status === "not_permitted" ? "negative" : "positive";

        // Display scholarship status
        const scholarshipStatus = document.getElementById('scholarshipStatus');
        scholarshipStatus.innerText = `Scholarship Eligibility: ${scholarshipStatusText}`;
        scholarshipStatus.className = `status ${scholarshipStatusClass}`;

        // Display exam permission status
        const examPermissionStatus = document.getElementById('examPermissionStatus');
        examPermissionStatus.innerText = `Exam Permission: ${examStatusText}`;
        examPermissionStatus.className = `status ${examStatusClass}`;

        // Open modal
        document.getElementById('resultsModal').style.display = "flex";
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch eligibility data. Please ensure the server is running.");
    }
}

function closeModal() {
    document.getElementById('resultsModal').style.display = "none";
    document.getElementById('studentID').value = ""; // Reset input for next check
}
