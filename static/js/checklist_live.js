// Guarda el checklist de la admisión vía AJAX y refleja las alertas nuevas sin recargar la página.
(function () {
  const form = document.getElementById('checklist-form');
  if (!form) return;

  const statusEl = document.getElementById('checklist-status');
  const alertasContainer = document.getElementById('alertas-container');
  let guardando = false;

  function nivelABootstrap(nivel) {
    if (nivel === 'CRITICA') return 'danger';
    if (nivel === 'ADVERTENCIA') return 'warning';
    return 'info';
  }

  function renderAlerta(alerta) {
    const div = document.createElement('div');
    div.className = `alert alert-${nivelABootstrap(alerta.nivel)}`;
    div.setAttribute('data-alerta-id', alerta.id);
    div.innerHTML = `<strong>${alerta.titulo}</strong><div>${alerta.mensaje}</div><div class="small fst-italic">${alerta.sugerencia}</div>`;
    return div;
  }

  async function guardarChecklist(event) {
    event.preventDefault();
    if (guardando) return;
    guardando = true;
    statusEl.textContent = 'Guardando...';

    try {
      const response = await fetch(form.dataset.url, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(form),
      });
      const data = await response.json();

      if (!response.ok || !data.ok) {
        statusEl.textContent = 'Error al guardar. Revise los datos.';
        statusEl.classList.replace('text-success', 'text-danger');
        return;
      }

      statusEl.textContent = 'Checklist guardado.';
      statusEl.classList.replace('text-danger', 'text-success');

      const sinAlertas = document.getElementById('sin-alertas');
      if (data.alertas_nuevas.length && sinAlertas) {
        sinAlertas.remove();
      }
      data.alertas_nuevas.forEach((alerta) => {
        alertasContainer.prepend(renderAlerta(alerta));
      });
    } catch (error) {
      statusEl.textContent = 'No se pudo conectar con el servidor.';
      statusEl.classList.replace('text-success', 'text-danger');
    } finally {
      guardando = false;
    }
  }

  form.addEventListener('submit', guardarChecklist);
})();
