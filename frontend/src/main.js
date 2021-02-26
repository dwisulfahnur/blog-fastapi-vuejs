import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'
import axios from 'axios'
import NProgress from 'nprogress'

import App from './App.vue'
import CreateUser from './components/users/Register'
import EditUser from './components/users/EditUser'
import Login from './components/auth/Login'
import 'bootstrap/dist/css/bootstrap.css'
import MyPosts from "./components/posts/MyPosts";
import PublicPosts from "./components/posts/PublicPosts";
import NewPost from "./components/posts/NewPost";
import EditPost from "./components/posts/EditPost";
// import ListUser from './components/users/ListUser'


Vue.use(VueRouter)
Vue.use(VueAxios, axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        Authorization: `Bearer ${localStorage.getItem('actoken')}`
    }
}))

Vue.config.productionTip = false


const routes = [
    // {
    //   name: 'user-list',
    //   path: '/users/',
    //   component: ListUser
    // },
    {
        name: 'Home',
        path: '/',
        component: PublicPosts
    },
    {
        name: 'login',
        path: '/login',
        component: Login
    },
    {
        name: 'register',
        path: '/register',
        component: CreateUser
    },
    {
        name: 'user-edit',
        path: '/users/edit',
        component: EditUser
    },
    {
        name: 'new-post',
        path: '/post/new',
        component: NewPost
    },
    {
        name: 'my-posts',
        path: '/post/me',
        component: MyPosts,
    },
    {
        name: 'edit-post',
        path: '/post/:id',
        component: EditPost
    }
]


const router = new VueRouter({mode: 'history', routes: routes})

router.beforeResolve((to, from, next) => {
    if (to.name) {
        NProgress.start()
    }
    next()
})

router.afterEach(() => {
    NProgress.done()
})

new Vue({
    render: h => h(App),
    router
}).$mount('#app')