import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import { urlPath } from 'utils'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    ...urlPath.START,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Home/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.CLASSROOM,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.Login,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Login/index.vue')
  },
  {
    ...urlPath.Admin,
    component: () => import(/* webpackChunkName: "admin" */ '../pages/Admin/index.vue')
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
