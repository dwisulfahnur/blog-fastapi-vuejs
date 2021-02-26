<template>
    <div class="col-md-5">
        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h3>Register</h3>
                </div>
                <div class="card-body">
                    <form v-on:submit.prevent="createUser">
                        <div class="form-group">
                            <label>Full Name:</label>
                            <input :class="{'is-invalid': errors.full_name}" class="form-control" type="text"
                                   v-model="user.full_name"/>
                            <div class="invalid-feedback" v-if="errors.full_name">{{errors.full_name}}</div>
                        </div>
                        <div class="form-group">
                            <label>Email:</label>
                            <input :class="{'is-invalid': errors.email}" class="form-control" type="text"
                                   v-model="user.email"/>
                            <div class="invalid-feedback" v-if="errors.email">{{errors.email}}</div>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input :class="{'is-invalid': errors.password}" class="form-control" type="password"
                                   v-model="user.password"/>
                            <div class="invalid-feedback" v-if="errors.password">{{errors.password}}</div>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary w-100" disabled type="button" v-if="loading">
                                <span aria-hidden="true" class="spinner-grow spinner-grow-sm" role="status"></span>
                                Register
                            </button>
                            <button class="btn btn-primary w-100" type="submit" v-else>Register</button>
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
                loading: false,
                user: {
                    full_name: '',
                    email: '',
                    password: '',
                },
                errors: {
                    full_name: null,
                    email: null,
                    password: null,
                },
                error: null
            }
        },
        methods: {
            createUser() {
                this.loading = true
                this.axios.post('/users', this.user)
                    .then(() => {
                        this.loading = false
                        this.$router.replace({name: 'login'})
                    })
                    .catch(err => {
                        const detail = err.response.data.detail
                        if (Array.isArray(detail)) {
                            detail.map(i => {
                                this.errors[i.loc[1]] = i.msg
                            })
                        } else {
                            this.error = detail
                        }

                        this.user.password = ''
                        this.loading = false
                    })
            }
        }
    }
</script>