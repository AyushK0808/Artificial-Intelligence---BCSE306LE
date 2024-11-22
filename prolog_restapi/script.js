async function checkEligibility(type) {
    const studentId = document.getElementById("student_id").value;
    if (!studentId) {
        document.getElementById("result").textContent = "Please enter a Student ID.";
        return;
    }

    const endpoint = type === "scholarship" ? "/scholarship" : "/exam_permission";
    try {
        const response = await fetch(`http://localhost:8000${endpoint}?student_id=${studentId}`);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        document.getElementById("result").textContent = `Result: ${data.status}`;
    } catch (error) {
        document.getElementById("result").textContent = "Error fetching data. Please try again.";
        console.error("Error:", error);
    }
}