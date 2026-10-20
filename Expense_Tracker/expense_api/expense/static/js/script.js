// =========================
// 1. CONFIGURATION
// =========================
const apiUrl = "/api/expenses/";

// =========================
// 2. DOM ELEMENTS
// =========================
const form = document.getElementById("expenseForm");
const expenseList = document.getElementById("expenses");
const message = document.getElementById("message");
const submitBtn = document.getElementById("submitBtn");
const dateInput = document.getElementById("date");
const cancelBtn = document.getElementById("cancelBtn");

const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const clearFilters = document.getElementById("clearFilters");

const totalElement = document.getElementById("total");
const countElement = document.getElementById("count");

// =========================
// 3. VARIABLES
// =========================
let editingExpenseId = null;
let allExpenses = [];

// =========================
// 4. SET TODAY'S DATE
// =========================
function setTodayDate() {
    const today = new Date();

    dateInput.value = new Date(
        today.getTime() - today.getTimezoneOffset() * 60000
    ).toISOString().slice(0, 10);
}

// =========================
// 5. SHOW MESSAGE
// =========================
function showMessage(text, success = true) {
    message.textContent = text;
    message.style.color = success ? "#15803d" : "#dc2626";
}

// =========================
// 6. CHECK ACTIVE FILTERS
// =========================
function updateClearFiltersButton() {
    const isFilterApplied =
        searchInput.value.trim() !== "" ||
        categoryFilter.value !== "" ||
        startDate.value !== "" ||
        endDate.value !== "";

    clearFilters.hidden = !isFilterApplied;
}

// =========================
// 7. LOAD EXPENSES
// =========================
async function loadExpenses() {
    expenseList.innerHTML = "<p>Loading expenses...</p>";

    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(
                `Failed to load expenses. Status: ${response.status}`
            );
        }

        const data = await response.json();

        if (Array.isArray(data)) {
            allExpenses = data;
        } else if (data && Array.isArray(data.results)) {
            allExpenses = data.results;
        } else {
            throw new Error("Unexpected API response format.");
        }

        displayExpenses();

    } catch (error) {
        console.error("Loading error:", error);

        expenseList.replaceChildren();

        const errorText = document.createElement("p");
        errorText.textContent =
            "Unable to load expenses. Check your Django server and API.";

        expenseList.appendChild(errorText);

        totalElement.textContent = "₹0.00";
        countElement.textContent = "0";
    }
}

// =========================
// 8. DISPLAY AND FILTER EXPENSES
// =========================
function displayExpenses() {
    // Update Clear Filters button visibility
    updateClearFiltersButton();

    const searchText = searchInput.value.trim().toLowerCase();
    const selectedCategory = categoryFilter.value;
    const fromDate = startDate.value;
    const toDate = endDate.value;

    const filteredExpenses = allExpenses.filter((expense) => {
        const title = (expense.title || "").toLowerCase();
        const description = (expense.description || "").toLowerCase();

        const matchesSearch =
            title.includes(searchText) ||
            description.includes(searchText);

        const matchesCategory =
            !selectedCategory ||
            expense.category === selectedCategory;

        const matchesFromDate =
            !fromDate || expense.date >= fromDate;

        const matchesToDate =
            !toDate || expense.date <= toDate;

        return (
            matchesSearch &&
            matchesCategory &&
            matchesFromDate &&
            matchesToDate
        );
    });

    expenseList.replaceChildren();

    // Calculate total of filtered expenses
    const total = filteredExpenses.reduce(
        (sum, expense) => sum + Number(expense.amount || 0),
        0
    );

    totalElement.textContent = `₹${total.toFixed(2)}`;
    countElement.textContent = String(filteredExpenses.length);

    // Empty state
    if (filteredExpenses.length === 0) {
        const emptyMessage = document.createElement("p");

        emptyMessage.textContent = allExpenses.length === 0
            ? "No expenses added yet."
            : "No matching expenses found.";

        expenseList.appendChild(emptyMessage);
        return;
    }

    // Create expense cards
    filteredExpenses.forEach((expense) => {
        const item = document.createElement("div");
        item.className = "expense";

        const title = document.createElement("h3");
        title.textContent = expense.title || "Untitled Expense";

        const details = document.createElement("p");
        details.textContent =
            `${expense.category || "Other"} | ${expense.date || ""}`;

        const amount = document.createElement("p");
        amount.className = "amount";
        amount.textContent =
            `₹${Number(expense.amount || 0).toFixed(2)}`;

        const description = document.createElement("p");
        description.textContent =
            expense.description || "No description";

        // Edit button
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.className = "edit-btn";
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => {
            editExpense(expense);
        });

        // Delete button
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteExpense(expense.id);
        });

        item.append(
            title,
            details,
            amount,
            description,
            editButton,
            deleteButton
        );

        expenseList.appendChild(item);
    });
}

// =========================
// 9. ADD OR UPDATE EXPENSE
// =========================
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("");

    const expenseData = {
        title: document.getElementById("title").value.trim(),
        amount: document.getElementById("amount").value,
        category: document.getElementById("category").value,
        date: dateInput.value,
        description: document.getElementById("description").value.trim()
    };

    if (
        !expenseData.title ||
        !expenseData.amount ||
        !expenseData.category ||
        !expenseData.date
    ) {
        showMessage("Please fill in all required fields.", false);
        return;
    }

    const isEditing = editingExpenseId !== null;

    const url = isEditing
        ? `${apiUrl}${editingExpenseId}/`
        : apiUrl;

    submitBtn.disabled = true;

    try {
        const response = await fetch(url, {
            method: isEditing ? "PUT" : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(expenseData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error("Validation error:", errorData);

            showMessage(
                "Unable to save expense. Please check the entered data.",
                false
            );
            return;
        }

        resetEditForm();

        showMessage(
            isEditing
                ? "Expense updated successfully!"
                : "Expense added successfully!"
        );

        await loadExpenses();

    } catch (error) {
        console.error("Save error:", error);

        showMessage(
            "Unable to save expense. Check your Django server.",
            false
        );
    } finally {
        submitBtn.disabled = false;
    }
});

// =========================
// 10. EDIT EXPENSE
// =========================
function editExpense(expense) {
    editingExpenseId = expense.id;

    document.getElementById("title").value = expense.title || "";
    document.getElementById("amount").value = expense.amount || "";
    document.getElementById("category").value = expense.category || "";
    dateInput.value = expense.date || "";
    document.getElementById("description").value =
        expense.description || "";

    submitBtn.textContent = "Update Expense";
    cancelBtn.hidden = false;

    showMessage("Edit the details and click Update Expense.");

    form.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

// =========================
// 11. RESET FORM
// =========================
function resetEditForm() {
    editingExpenseId = null;

    form.reset();
    setTodayDate();

    submitBtn.textContent = "Add Expense";
    cancelBtn.hidden = true;
}

// Cancel editing
cancelBtn.addEventListener("click", () => {
    resetEditForm();
    showMessage("Edit cancelled.");
});

// =========================
// 12. DELETE EXPENSE
// =========================
async function deleteExpense(id) {
    const confirmed = confirm(
        "Are you sure you want to delete this expense?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${apiUrl}${id}/`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Unable to delete expense.");
        }

        if (String(editingExpenseId) === String(id)) {
            resetEditForm();
        }

        showMessage("Expense deleted successfully!");

        await loadExpenses();

    } catch (error) {
        console.error("Delete error:", error);
        showMessage("Unable to delete expense.", false);
    }
}

// =========================
// 13. SEARCH AND FILTER EVENTS
// =========================
searchInput.addEventListener("input", displayExpenses);
categoryFilter.addEventListener("change", displayExpenses);
startDate.addEventListener("change", displayExpenses);
endDate.addEventListener("change", displayExpenses);

// =========================
// 14. CLEAR FILTERS
// =========================
clearFilters.addEventListener("click", () => {
    searchInput.value = "";
    categoryFilter.value = "";
    startDate.value = "";
    endDate.value = "";

    displayExpenses();
});

// =========================
// 15. INITIALIZE APPLICATION
// =========================
clearFilters.hidden = true;

setTodayDate();
loadExpenses();