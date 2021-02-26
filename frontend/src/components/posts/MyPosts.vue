<template>
    <div class="col-md-8">
        <h3>My Posts</h3>
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
                    <a class="btn btn-outline-primary btn-sm mr-2">Edit</a>
                    <a class="btn btn-outline-danger btn-sm">Delete</a>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    export default {
        name: "MyPosts",
        data: function () {
            return {
                posts: []
            }
        },
        mounted() {
            this.axios.get('/posts/me').then(response => {
                this.posts = response.data
            })
        }
    }
</script>

<style scoped>

</style>