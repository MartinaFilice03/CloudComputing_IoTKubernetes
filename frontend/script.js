async function loadTemps() {

  const response =
    await fetch("/temperatures");

  const data = await response.json();

  const list = document.getElementById("temps");
  list.innerHTML = "";

  data.forEach(t => {
    const li = document.createElement("li");
    li.textContent = t.value ?? JSON.stringify(t);
    list.appendChild(li);
  });
}