<template>
    <div class="col-md-5">
        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h3>Login</h3>
                </div>
                <div class="card-body">
                    <div class="alert alert-danger" role="alert" v-if="invalidLogin">
                        Invalid Email or Password
                    </div>
                    <form v-on:submit.prevent="login">
                        <div class="form-group">
                            <label>Email:</label>
                            <input class="form-control" type="email" v-model="email"/>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input class="form-control" type="password" v-model="password"/>
                        </div>
                        <div class="form-group">
                            <input class="btn btn-primary w-100" type="submit" value="Login"/>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                email: '',
                password: '',
                invalidLogin: false,
            }
        },
        methods: {
            login() {
                let data = new FormData()
                data.append('grant_type', 'password')
                data.append('username', this.email)
                data.append('password', this.password)
                let uri = '/oauth/token'
                this.axios.post(uri, data).then((response) => {
                    console.log(response)
                    localStorage.setItem('actoken', response.data.access_token)
                    localStorage.setItem('loggedIn', true)
                    this.axios.get('/users/me', {
                            headers: {Authorization: `Bearer ${response.data.access_token}`}
                        }
                    ).then(response => {
                        localStorage.setItem('email', response.data.email)
                        this.$router.replace({name: 'my-posts'})
                        window.location.reload()
                    })
                }).catch(() => {
                    console.log("INVALID LOGIN")
                    this.invalidLogin = true
                })
            }
        }
    }
</script>

<style scoped>
</style>