<template>
    <div class="col-md-8">
        <div class="card">
            <div class="card-body" v-if="loading">
                <div class="spinner-grow text-primary" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
            <div class="card-body" v-else-if="posts.length > 0">
                <h3 class="card-title">
                    My Posts
                </h3>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Title</th>
                        <th>Actions</th>
                    </tr>
                    </thead>

                    <tbody>
                    <tr :key="post.id" v-for="(post, index) in posts">
                        <th style="width: 10px">{{ index + 1 }}</th>
                        <td>{{ post.title }}</td>
                        <td>
                            <router-link :to="{name:'edit-post',params: {id: post.id}}"
                                         class="btn btn-outline-primary btn-sm mr-2">Edit
                            </router-link>
                            <a @click="deleteItem(post.id)" class="btn btn-outline-danger btn-sm">Delete</a>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div class="card-body text-center" v-else>
                <h3>You don't have any post</h3>
                <router-link :to="{name:'new-post'}" class="btn btn-outline-primary">Create a new one</router-link>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "MyPosts",
        data: function () {
            return {
                loading: false,
                posts: []
            }
        },
        mounted() {
            this.loadPosts()
        },
        methods: {
            loadPosts() {
                this.loading = true
                this.axios.get('/posts/me').then(response => {
                    this.posts = response.data
                    this.loading = false
                })
            },
            deleteItem(id) {
                if (confirm('Are you sure to delete the post?')) {
                    this.axios.delete(`/posts/${id}`).then(() => {
                        this.loadPosts()
                    })
                }
            }
        }
    }
</script>

<style scoped>

</style>