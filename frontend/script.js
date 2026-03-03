async function loadTemps() {
  try {
      const response = await fetch('/api/temperatures');
      const data = await response.json();
      
      const tbody = document.getElementById('temps-body');
      tbody.innerHTML = ''; 

      data.forEach(item => {
          // Ho aggiunto le classi specifiche a ogni <td> per allinearli ai <th>
          const row = `
              <tr>
                  <td class="col-id">${item.id}</td>
                  <td class="col-dev">${item.device}</td>
                  <td class="col-temp" style="font-weight: bold; color: #2c3e50;">${item.value}</td>
                  <td class="col-time">${item.timestamp}</td>
              </tr>
          `;
          tbody.innerHTML += row;
      });
  } catch (error) {
      console.error("Errore nel caricamento dati:", error);
  }
}

// Avvio automatico
loadTemps();
setInterval(loadTemps, 5000);