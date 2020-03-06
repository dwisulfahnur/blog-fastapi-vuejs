<template>
    <div>
        <div class="container">
        <div class="card">
            <div class="card-header">
                <h3>New User</h3>
            </div>
            <div class="card-body">
                <form v-on:submit.prevent="createUser">
                    <div class="form-group">
                        <label>Email:</label>
                        <input type="email" class="form-control" v-model="user.email"/>
                    </div>
                    <div class="form-group">
                        <label>First Name:</label>
                        <input type="text" class="form-control" v-model="user.first_name"/>
                    </div>
                    <div class="form-group">
                        <label>Last Name:</label>
                        <input type="text" class="form-control" v-model="user.last_name"/>
                    </div>
                    <div class="form-group">
                        <input type="submit" class="btn btn-primary" value="Create User"/>
                    </div>
                </form>
            </div>
        </div>
    </div>
    </div>
</template>
<script>
export default {
    // components: {
    //     name: 'CreateUser'
    // },
    data() {
        return {
            user: {}
        }
    },
    methods: {
        createUser(){
            let uri = 'http://localhost:8000/api/users'
            this.axios.post(uri, this.user).then((response)=>{
                console.log(response.data)
                this.$router.replace({name:'user-list'})
            })
        }
    }
}
</script>