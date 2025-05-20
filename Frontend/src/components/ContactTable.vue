<template>
  <div>
    <table id="contacts-table" class="display" style="width:100%"></table>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import $ from 'jquery'
import 'datatables.net'
import 'datatables.net-dt/css/jquery.dataTables.css'

export default {
  name: 'ContactTable',
  setup() {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/contactos/');
        const data = await response.json();

        // Inicializar DataTable con columnas definidas
        $('#contacts-table').DataTable({
          data: data,
          destroy: true, // Por si se reinicializa
          columns: [
            { data: 'nombre', title: 'Nombre' },
            { data: 'apellido', title: 'Apellido' },
            { data: 'numero_celular', title: 'Celular' },
            { data: 'correo', title: 'Correo' },
            {
              data: null,
              title: 'Acciones',
              orderable: false,
              render: function (data, type, row) {
                return `<button class="eliminar-btn" data-id="${row.id}">Eliminar</button>`;
              }
            }
          ]
        });

        // Escuchar evento eliminar (delegado)
        $('#contacts-table tbody').on('click', '.eliminar-btn', async function () {
          const id = $(this).data('id');
          if (confirm('¿Estás seguro de que deseas eliminar este contacto?')) {
            await fetch(`http://127.0.0.1:8000/api/contactos/${id}/`, {
              method: 'DELETE'
            });
            location.reload(); // Recargar para reflejar cambios
          }
        });
      } catch (error) {
        console.error('Error al cargar contactos:', error);
      }
    };

    onMounted(fetchData);
  }
}
</script>

<style>
/* Puedes personalizar aquí */
</style>