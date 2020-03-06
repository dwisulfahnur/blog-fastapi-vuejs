<template>
  <div>
    <h1>User List</h1>

    <table class="table table-hover">
      <thead>
        <tr>
          <td>ID</td>
          <td>Full Name</td>
          <td>Email</td>
          <td>Actions</td>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.first_name }} {{ user.last_name }}</td>
          <td>{{ user.email }}</td>
          <td>
            <router-link
              :to="{name: 'EditUser', params: { id: user.id }}"
              class="btn btn-primary mr-2"
            >Edit</router-link>

            <button class="btn btn-danger" v-on:click="deleteUser(user.id)">Delete</button>
          
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      users: []
    };
  },

  created: function(){
      this.fetchUsers();
  },

  methods: {
      fetchUsers() {
          let uri = 'http://localhost:8000/api/users'
          this.axios.get(uri).then((response)=>{
              this.users = response.data
          })
      },
      deleteUser(id) {
          let uri = `http://localhost:8000/api/users/${id}`
          let index = this.users.map((x)=>{return x.id}).indexOf(id)
          this.axios.delete(uri).then(
              this.users.splice(index, 1)
          )
      }
  }
};
</script>