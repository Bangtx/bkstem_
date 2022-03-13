import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

import { urlPath } from 'utils'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    ...urlPath.START,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Home/index.vue')
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

// router.beforeEach(authGuard)
// router.beforeEach(navGuard)

export default router
