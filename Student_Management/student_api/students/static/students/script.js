const form = document.getElementById("studentForm");
const studentTable = document.getElementById("studentTable");
const studentId = document.getElementById("studentId");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");

const nameInput = document.getElementById("name");
const classInput = document.getElementById("class_name");
const branchInput = document.getElementById("branch");
const rollInput = document.getElementById("roll");
const cityInput = document.getElementById("city");

const apiUrl = "/api/students/";

loadStudents();

function loadStudents() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            studentTable.innerHTML = "";

            data.forEach(student => {
                studentTable.innerHTML += `
                    <tr>
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.class_name}</td>
                        <td>${student.branch}</td>
                        <td>${student.roll}</td>
                        <td>${student.city}</td>
                        <td>
                            <button class="edit-btn" onclick="editStudent(${student.id})">Edit</button>
                            <button class="delete-btn" onclick="deleteStudent(${student.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
        })
        .catch(error => {
            console.log("Error:", error);
        });
}

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const studentData = {
        name: nameInput.value,
        class_name: classInput.value,
        branch: branchInput.value,
        roll: rollInput.value,
        city: cityInput.value
    };

    let url = apiUrl;
    let method = "POST";

    if (studentId.value) {
        url = apiUrl + studentId.value + "/";
        method = "PUT";
    }

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(studentData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to save student");
            }

            return response.json();
        })
        .then(data => {
            if (studentId.value) {
                alert("Student updated successfully");
            } else {
                alert("Student added successfully");
            }

            form.reset();
            studentId.value = "";
            submitBtn.textContent = "Add Student";

            loadStudents();
        })
        .catch(error => {
            alert("Error: " + error.message);
        });
});

function editStudent(id) {
    fetch(apiUrl + id + "/")
        .then(response => response.json())
        .then(student => {
            studentId.value = student.id;
            nameInput.value = student.name;
            classInput.value = student.class_name;
            branchInput.value = student.branch;
            rollInput.value = student.roll;
            cityInput.value = student.city;

            submitBtn.textContent = "Update Student";
        })
        .catch(error => {
            alert("Error loading student");
        });
}

function deleteStudent(id) {
    if (confirm("Are you sure you want to delete this student?")) {
        fetch(apiUrl + id + "/", {
            method: "DELETE"
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to delete student");
                }

                alert("Student deleted successfully");
                loadStudents();
            })
            .catch(error => {
                alert("Error: " + error.message);
            });
    }
}

cancelBtn.addEventListener("click", function () {
    form.reset();
    studentId.value = "";
    submitBtn.textContent = "Add Student";
});