async function loadTemps() {

  console.log("CLICK");

  const response =
    await fetch("http://localhost:5000/temperatures");

  const data = await response.json();

  console.log("DATA:", data);

  const list = document.getElementById("temps");

  if (!list) {
    console.log("ERRORE: elemento temps non trovato");
    return;
  }

  list.innerHTML = "";

  data.forEach(row => {

    const li = document.createElement("li");

    li.innerText =
      "ID: " + row[0] +
      " | Device: " + row[1] +
      " | Temp: " + row[2] +
      " | Time: " + row[3];

    list.appendChild(li);
  });

  console.log("FINITO");
}