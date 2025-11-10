document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("todo-list");
  try {
    const res = await fetch("/todo/");
    const todos = await res.json();

    list.innerHTML = "";
    todos.forEach(t => {
      const li = document.createElement("li");
      li.textContent = t.title;
      list.appendChild(li);
    });
  } catch (e) {
    list.innerHTML = "<li>Failed to load todo files</li>";
    console.error(e);
  }
});
