import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'
import axios from 'axios'
import NProgress from 'nprogress'

import App from './App.vue'
import CreateUser from './components/users/CreateUser'
import EditUser from './components/users/EditUser'
import ListUser from './components/users/ListUser'

import 'bootstrap/dist/css/bootstrap.css'


Vue.use(VueRouter)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false


const routes = [
  {
    name: 'user-list',
    path: '/users/',
    component: ListUser
  },
  {
    name: 'user-create',
    path: '/users/create',
    component: CreateUser
  },
  {
    name: 'user-edit',
    path: '/users/edit',
    component: EditUser
  }
]


const router = new VueRouter({ mode: 'history', routes: routes })

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