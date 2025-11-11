document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("todo-list");
  const createBtn = document.getElementById("create-btn");

  createBtn.addEventListener("click", async () => {
    const title = prompt("Enter a name for the new todo file:");
    if (!title) return;

    try {
      const res = await fetch("/todo/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });

      if (!res.ok) {
        alert("Failed to create file.");
        return;
      }

      await loadTodos();

    } catch (err) {
      console.error(err);
      alert("Network error while creating file.");
    }
  });

  async function loadTodos() {
    try {
      const res = await fetch("/todo/");
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
          if (!confirm(`Delete "${t.title}"?`)) return;

          try {
            const resp = await fetch(`/todo/${t.id}`, { method: "DELETE" });
            if (resp.ok) li.remove();
            else alert("Failed to delete item.");
          } catch (err) {
            console.error(err);
            alert("Network error while deleting item.");
          }
        });

        const title = document.createElement("a");
        title.textContent = t.title;
        title.href = `/gui/todo/${t.id}`;

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
