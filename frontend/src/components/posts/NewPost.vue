<template>
    <div class="col-md-8">
        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h3>New Post</h3>
                </div>
                <div class="card-body">
                    <form v-on:submit.prevent="createPost">
                        <div class="form-group">
                            <label>Title:</label>
                            <input :class="{'is-invalid': errors.title}" class="form-control" type="text"
                                   v-model="title"/>
                            <div class="invalid-feedback" v-if="errors.title">{{errors.title}}</div>
                        </div>
                        <div class="form-group">
                            <label>Body of Content:</label>
                            <textarea :class="{'is-invalid': errors.content}" class="form-control" rows="10"
                                      v-model="content"></textarea>
                            <div class="invalid-feedback" v-if="errors.content">{{errors.content}}</div>
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary" disabled type="button" v-if="loading">
                                <span aria-hidden="true" class="spinner-grow spinner-grow-sm" role="status"></span>
                                Save
                            </button>
                            <button class="btn btn-primary" type="submit" v-else>Save</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NewPost",
        data: function () {
            return {
                loading: false,
                title: '',
                content: '',
                errors: {
                    title: null,
                    content: null
                },
            }
        },
        methods: {
            createPost() {
                this.loading = true
                this.axios.post('/posts', {
                    title: this.title,
                    content: this.content
                }).then(() => {
                    this.loading = false
                    this.$router.replace({name: 'my-posts'})
                }).catch(err => {
                    const detail = err.response.data.detail
                    if (Array.isArray(detail)) {
                        detail.map(i => {
                            this.errors[i.loc[1]] = i.msg
                        })
                    } else {
                        this.error = detail
                    }
                    this.loading = false
                })
            }
        }
    }
</script>

<style scoped>

</style>