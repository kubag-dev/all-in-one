document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("todo-tasks-list");
  const createBtn = document.getElementById("create-btn");
  const todoFileId = document.getElementById("todo-root").dataset.todoFileId;

  createBtn.addEventListener("click", async () => {
    const text = prompt("Enter a name for a todo task:");
    if (!text) return;

    try {
      const res = await fetch(`/todo/${todoFileId}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        alert("Failed to create task.");
        return;
      }

      await loadTodos();

    } catch (err) {
      console.error(err);
      alert("Network error while creating task.");
    }
  });

  async function loadTodos() {
    try {
      const res = await fetch(`/todo/${todoFileId}/tasks`);
      const todos = await res.json();

      list.innerHTML = "";

      todos.forEach(t => {
        const li = document.createElement("li");

        const del = document.createElement("a");
        del.textContent = "🗑️";
        del.href = "#";
        del.style.marginRight = "8px";
        del.title = "Delete this item";

        del.addEventListener("click", async (e) => {
          e.preventDefault();
          if (!confirm(`Delete "${t.text}"?`)) return;

          try {1
            const resp = await fetch(`/todo/${todoFileId}/tasks/${t.id}`, { method: "DELETE" });
            if (resp.ok) li.remove();
            else alert("Failed to delete item.");
          } catch (err) {
            console.error(err);
            alert("Network error while deleting item.");
          }
        });

        const title = document.createElement("a");
        title.textContent = t.text;

        li.appendChild(del);
        li.appendChild(title);
        list.appendChild(li);
      });
    } catch (e) {
      list.innerHTML = "<li>Failed to load todo files</li>";
      console.error(e);
    }
  }

  loadTodos();
});
