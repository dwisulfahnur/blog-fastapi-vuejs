<template>
    <div class="row">
        <div :key="post.id" class="col-md-4" v-for="post in posts">
            <div class="card">
                <div class="card-body">
                    <h4 class="card-title">
                        {{post.title}}
                    </h4>
                    <span class="help text-muted" v-if="post.author_name">Author: {{ post.author_name }}</span>
                    <span class="help text-muted" v-else>Author: Unknown</span>
                    <hr/>
                    <p>{{post.content}}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "PublicPosts",
        data: function () {
            return {
                posts: []
            }
        },
        mounted() {
            this.axios.get('/posts').then(response => {
                this.posts = response.data
            })
        }
    }
</script>

<style scoped>

</style>