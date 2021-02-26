<template>
    <div class="col-md-8">
        <div class="container">
            <div class="card" v-if="!isNotFound">
                <div class="card-header">
                    <h3>{{post.title}}</h3>
                </div>
                <div class="card-body">
                    <form v-on:submit.prevent="savePost">
                        <div class="form-group">
                            <label>Title:</label>
                            <input :class="{'is-invalid': errors.title}" class="form-control" type="text"
                                   v-model="post.title"/>
                            <div class="invalid-feedback" v-if="errors.title">{{errors.title}}</div>
                        </div>
                        <div class="form-group">
                            <label>Body of Content:</label>
                            <textarea :class="{'is-invalid': errors.content}" class="form-control" rows="10"
                                      v-model="post.content"></textarea>
                            <div class="invalid-feedback" v-if="errors.content">{{errors.content}}</div>
                        </div>
                        <div class="alert alert-success" role="alert" v-if="saved">
                            Post has been updated. Go to
                            <router-link :to="{name:'my-posts'}">My Posts</router-link>
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
            <div class="card" v-else>
                <div class="card-body text-center">
                    <h3>Not Found</h3>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "EditPost",
        data: function () {
            return {
                loading: false,
                post: {
                    title: null,
                    content: null
                },
                saved: false,
                isNotFound: false,
                errors: {
                    title: null,
                    content: null
                },
            }
        },
        mounted() {
            this.axios.get(`/posts/${this.$route.params.id}`).then(res => {
                this.post = res.data
            }).catch(() => {
                this.isNotFound = true
            })
        },
        methods: {
            savePost() {
                this.loading = true
                this.axios.patch(`/posts/${this.$route.params.id}`, {
                    title: this.post.title,
                    content: this.post.content,
                }).then(res => {
                    this.post = res.data
                    this.saved = true
                    this.loading = false
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