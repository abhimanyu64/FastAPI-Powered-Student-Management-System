const API = "http://127.0.0.1:5500";
const form = document.querySelector("#studentForm");
const rows = document.querySelector("#studentRows");
const search = document.querySelector("#search");
const apiStatus = document.querySelector("#apiStatus");
const formMessage = document.querySelector("#formMessage");
const listMessage = document.querySelector("#listMessage");
let students = [];

function showMessage(element, text, error = false) {
  element.textContent = text;
  element.classList.toggle("error", error);
}
async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) }
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
  return body;
}
async function checkApi() {
  try {
    await api("/health");
    apiStatus.textContent = "API connected";
    apiStatus.className = "status ok";
  } catch {
    apiStatus.textContent = "API offline";
    apiStatus.className = "status bad";
  }
}
function updateStats(data) {
  document.querySelector("#totalCount").textContent = data.length;
  document.querySelector("#courseCount").textContent = new Set(data.map(s => s.course)).size;
  document.querySelector("#yearCount").textContent = new Set(data.map(s => s.year)).size;
}
function renderStudents(data) {
  updateStats(data);
  if (!data.length) {
    rows.innerHTML = '<tr><td colspan="6" class="empty">No student records found.</td></tr>';
    return;
  }
  
rows.innerHTML = data.map(s => `
  <tr>
    <td>${s.id}</td>
    <td>${escapeHtml(s.name)}</td>
    <td>${escapeHtml(s.email)}</td>
    <td>${escapeHtml(s.course)}</td>
    <td>Year ${s.year}</td>
    <td>
      <div class="actions">
        <button class="action edit" data-edit="${s.id}">Edit</button>
        <button class="action delete" data-delete="${s.id}">Delete</button>
      </div>
    </td>
  </tr>
`).join("");

}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
}
async function loadStudents() {
  try {
    const q = search.value.trim();
    students = await api(`/students${q ? `?search=${encodeURIComponent(q)}` : ""}`);
    renderStudents(students);
    showMessage(listMessage, "");
  } catch (error) {
    rows.innerHTML = '<tr><td colspan="6" class="empty">Could not load records. Is the backend running?</td></tr>';
    showMessage(listMessage, error.message, true);
  }
}
function resetForm() {
  form.reset();
  document.querySelector("#studentId").value = "";
  document.querySelector("#formTitle").textContent = "Add a student";
  document.querySelector("#saveButton").textContent = "Add student";
  document.querySelector("#cancelButton").classList.add("hidden");
  showMessage(formMessage, "");
}
form.addEventListener("submit", async event => {
  event.preventDefault();
  const id = document.querySelector("#studentId").value;
  const payload = {
    name: document.querySelector("#name").value.trim(),
    email: document.querySelector("#email").value.trim(),
    course: document.querySelector("#course").value.trim(),
    year: Number(document.querySelector("#year").value)
  };
  try {
    await api(id ? `/students/${id}` : "/students", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(payload)
    });
    showMessage(formMessage, id ? "Student updated successfully." : "Student added successfully.");
    resetForm();
    await loadStudents();
    await checkApi();
  } catch (error) {
    showMessage(formMessage, error.message, true);
  }
});
document.querySelector("#cancelButton").addEventListener("click", resetForm);
rows.addEventListener("click", async event => {
  const editButton = event.target.closest("[data-edit]");
  const deleteButton = event.target.closest("[data-delete]");
  if (editButton) {
    const student = students.find(s => s.id === Number(editButton.dataset.edit));
    if (!student) return;
    document.querySelector("#studentId").value = student.id;
    document.querySelector("#name").value = student.name;
    document.querySelector("#email").value = student.email;
    document.querySelector("#course").value = student.course;
    document.querySelector("#year").value = student.year;
    document.querySelector("#formTitle").textContent = "Edit student";
    document.querySelector("#saveButton").textContent = "Save changes";
    document.querySelector("#cancelButton").classList.remove("hidden");
    form.scrollIntoView({behavior:"smooth", block:"start"});
  } else if (deleteButton) {
    const id = Number(deleteButton.dataset.delete);
    const student = students.find(s => s.id === id);
    if (!confirm(`Delete ${student?.name || "this student"}? This cannot be undone.`)) return;
    try {
      await api(`/students/${id}`, {method:"DELETE"});
      showMessage(listMessage, "Student deleted successfully.");
      await loadStudents();
    } catch (error) {
      showMessage(listMessage, error.message, true);
    }
  }
});
let searchTimer;
search.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadStudents, 200);
});
checkApi();
loadStudents();
