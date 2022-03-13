<template lang="pug">
  div
    nav.navbar.navbar-expand-md.navbar-ligh.bg-light.sticky-top.pa-0
      div.container-fluid.my-header
        a.navbar-branch(:href="'#'")
          img.ml-3(src="http://bksteam.edu.vn/wp-content/uploads/2021/03/logobksteam.png" height="50")
        button.navbar-toggler(
          data-toggle="collapse"
          data-target="#navbarResponsive"
        )
          v-icon(large color="#FFF" ) mdi-format-list-bulleted
        div.collapse.navbar-collapse#navbarResponsive
          ul.navbar-nav.ml-auto
            li.nav-item.pa-2
              v-avatar(size="40" color="#7F91F5")
                span.white--text H
              span(v-if="showHeaderText").white--text.ml-4 Ho so ca nhan
            li.nav-item.pa-2
              v-avatar(size="40" color="#7F91F5")
                v-icon(color="#FFF") mdi-wechat
              span(v-if="showHeaderText").white--text.ml-4 Tin nhan
            li.nav-item.pa-2
              v-avatar(size="40" color="#7F91F5")
                v-icon(color="#FFF") mdi-email
              span(v-if="showHeaderText").white--text.ml-4 Hop thu
            li.nav-item.pa-2
              v-avatar(size="40" color="#7F91F5")
                v-icon(color="#FFF") mdi-bell-ring
              span(v-if="showHeaderText").white--text.ml-4 Thong bao
            li.nav-item.pa-2
              v-menu(
                v-model="menu"
                :close-on-content-click="false"
                :nudge-width="200"
                offset-x
              )
                template(v-slot:activator="{ on, attrs }")
                  v-avatar(size="40" color="#7F91F5" v-bind="attrs" v-on="on")
                    v-icon(color="#FFF") mdi-playlist-plus
                v-card(width="650px")
                  v-card-title
                    v-avatar(size="40" color="#7F91F5")
                      span.white--text H
                    span.ml-2 Phạm Việt Hưng
                  div.pa-5
                    v-list-item Mail: hungphamaep@gmail.com
                    v-list-item Giáo viên - trợ giảng

    div.dropdown.pa-1
      div.dropdown-toggle.pa-2(
        id="dropdownMenu"
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      )
        v-icon mdi-chart-line
        span Tổng quan
      div.dropdown-toggle.pa-2(
        id="dropdownMenuTraining"
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      )
        v-icon mdi-calendar
        span Đào tạo
      div.dropdown-menu(aria-labelledby="dropdownMenu")
        a.dropdown-item Action
        a.dropdown-item Another action
        a.dropdown-item Something else here
      div.dropdown-menu(aria-labelledby="dropdownMenuTraining")
        a.dropdown-item Action
        a.dropdown-item Another action

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'

const HeaderBar = defineComponent({
  setup() {
    const menu = ref(false)
    const fav = ref(false)
    const showHeaderText = ref(false)
    showHeaderText.value = window.innerWidth < 700
    window.addEventListener('resize', () => {
      showHeaderText.value = window.innerWidth < 700
    })
    const value = ref('hhi')
    return {
      value,
      showHeaderText,
      menu
    }
  }
})
export default HeaderBar
</script>

<style lang="sass">
.my-header
  background-color: #3F51B5
.carousel-caption
  color: #0E5A84
@media (min-width: 700px)
  .carousel-item img
    height: 450px
@media (min-width: 350px)
  .carousel-item img
    height: 300px
.dropdown
  display: inline-block
.dropdown-toggle
  float: left
.dropdown-toggle:hover
  cursor: pointer
</style>
