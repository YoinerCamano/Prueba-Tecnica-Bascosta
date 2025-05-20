<template>
  <div class="container mt-4">
    <h1>Libreta de Contactos</h1>
    <form @submit.prevent="submitForm" class="mb-4">
      <div class="row g-3 align-items-end">
        <div class="col">
          <label>Nombre</label>
          <input v-model="newContact.nombre" class="form-control" required />
        </div>
        <div class="col">
          <label>Apellido</label>
          <input v-model="newContact.apellido" class="form-control" required />
        </div>
        <div class="col">
          <label>Celular</label>
          <input v-model="newContact.numero_celular" class="form-control" required />
        </div>
        <div class="col">
          <label>Correo</label>
          <input v-model="newContact.correo" type="email" class="form-control" required />
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-primary">
            {{ editingId ? 'Actualizar' : 'Agregar' }}
          </button>
          <button v-if="editingId" @click="cancelEdit" type="button" class="btn btn-secondary ms-2">
            Cancelar
          </button>
        </div>
      </div>
    </form>

    <table id="contacts-table" class="table table-striped" style="width:100%">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Celular</th>
          <th>Correo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <!-- DataTables genera las filas -->
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import 'datatables.net-bs5'

export default {
  data() {
    return {
      contactos: [],
      newContact: {
        nombre: '',
        apellido: '',
        numero_celular: '',
        correo: ''
      },
      editingId: null,
      dataTable: null,
      traducciones: {
        "contacto with this correo already exists.": "El correo ya está registrado.",
        "contacto with this numero celular already exists.": "El número celular ya está registrado.",
        "Este número de celular ya está registrado.": "El número celular ya está registrado."
      }
    }
  },
  methods: {
    async fetchContacts() {
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/contactos/')
        this.contactos = res.data
        this.$nextTick(() => {
          if (this.dataTable) {
            this.dataTable.clear()
            this.dataTable.rows.add(this.contactos)
            this.dataTable.draw()
          } else {
            this.dataTable = $('#contacts-table').DataTable({
              data: this.contactos,
              columns: [
                { data: 'nombre' },
                { data: 'apellido' },
                { data: 'numero_celular' },
                { data: 'correo' },
                {
                  data: null,
                  render: (data, type, row) => {
                    return `
                      <button class="btn btn-sm btn-warning me-1" data-edit-id="${row.id}">Editar</button>
                      <button class="btn btn-sm btn-danger" data-id="${row.id}">Eliminar</button>`
                  },
                  orderable: false
                }
              ]
            })

            $('#contacts-table tbody').off('click').on('click', 'button', (event) => {
              const $btn = $(event.currentTarget)
              const id = $btn.data('id')
              const editId = $btn.data('edit-id')

              if (editId) {
                this.editContact(editId)
              } else {
                this.deleteContact(id)
              }
            })
          }
        })
      } catch (error) {
        console.error('Error al cargar contactos:', error)
      }
    },

    async submitForm() {
      const digitsOnly = this.newContact.numero_celular.replace(/\D/g, '')
      if (digitsOnly.length !== 10) {
        alert('El número celular debe tener exactamente 10 dígitos (puede contener espacios para legibilidad).')
        return
      }

      const payload = {
        ...this.newContact,
        numero_celular: digitsOnly
      }

      try {
        if (this.editingId) {
          await axios.put(`http://127.0.0.1:8000/api/contactos/${this.editingId}/`, payload)
        } else {
          await axios.post('http://127.0.0.1:8000/api/contactos/', payload)
        }

        this.cancelEdit()
        await this.fetchContacts()
      } catch (error) {
        if (error.response && error.response.data) {
          const data = error.response.data
          for (const campo in data) {
            if (Array.isArray(data[campo]) && data[campo].length > 0) {
              const original = data[campo][0]
              const traducido = this.traducciones[original] || original
              alert(`${traducido}`)
              return
            }
          }
        }
        alert('No se pudo guardar el contacto. Revisa la consola.')
        console.error('Error al guardar contacto:', error)
      }
    },

    async deleteContact(id) {
      if (!confirm('¿Seguro que deseas eliminar este contacto?')) return
      try {
        await axios.delete(`http://127.0.0.1:8000/api/contactos/${id}/`)
        await this.fetchContacts()
      } catch (error) {
        console.error('Error al eliminar contacto:', error)
        alert('No se pudo eliminar el contacto.')
      }
    },

    editContact(id) {
      const contacto = this.contactos.find(c => c.id === id)
      if (contacto) {
        this.newContact = {
          nombre: contacto.nombre,
          apellido: contacto.apellido,
          numero_celular: contacto.numero_celular,
          correo: contacto.correo
        }
        this.editingId = id
      }
    },

    cancelEdit() {
      this.editingId = null
      this.newContact = {
        nombre: '',
        apellido: '',
        numero_celular: '',
        correo: ''
      }
    }
  },

  mounted() {
    this.fetchContacts()
  }
}
</script>