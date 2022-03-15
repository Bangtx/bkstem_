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
      console.log(from.fullPath)
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
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
