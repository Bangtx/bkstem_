<template lang="pug">
  div
    portal(to="header-action")
      v-icon.nav-icon(@click="openMenuList()") mdi-format-align-justify

    .mt-16(v-if="isResponsive && isOpenMenu")
      div(v-if="isAdmin && isResponsive && isOpenMenu" v-for="item in menuAdmins")
        v-list-item(@click="$emit('on-click', item.event)")
          span {{ item.text }}
        v-divider
      div(v-if="member.typeMember === 'teacher' && !isAdmin && isResponsive && isOpenMenu" v-for="item in menuTeachers")
        v-list-item(@click="$emit('on-click', item.event)")
          span {{ item.text }}
        v-divider
      div(v-if="member.typeMember === 'student' && !isAdmin && isResponsive && isOpenMenu" v-for="item in menuStudents")
        v-list-item(@click="$emit('on-click', item.event)")
          span {{ item.text }}
        v-divider

    .bg-white.border-r.pb-2.fixed.bottom-0.z-10.w-full.content-center(class="md:bg-gray-50 md:relative md:h-screen md:w-60")
      .text-sm.content-center.text-left.justify-between(class="md:mt-12 md:w-60 md:fixed md:left-0 md:top-0 md:content-start")
        .list-reset.flex.justify-between.flex-row.pt-3.px-2.text-center.text-gray-600(class="md:flex-col md:py-3 md:px-2 md:text-left")
          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="isAdmin" v-for="item in menuAdmins"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', item.event)")
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="member.typeMember === 'teacher' && !isAdmin" v-for="item in menuTeachers"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', item.event)")
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

          .relative(
            class="md:block md:px-6 md:py-3 md:pt-6"
            v-if="member.typeMember === 'student' && !isAdmin" v-for="item in menuStudents"
          )
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', item.event)")
              span.hidden(class="md:ml-4 md:block") {{ item.text }}

</template>

<script lang="ts">
import { defineComponent, ref, watch } from '@vue/composition-api'
import { toCamelCase } from 'utils'
import jwtDecode from 'jwt-decode'

const MenuComponent = defineComponent({
  props: {
    isAdmin: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup(props, { root }) {
    const { $store } = root
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const isResponsive = ref(window.screen.width < 750)
    const isOpenMenu = ref(false)

    const menuTeachers = [
      { text: 'Trang chủ', event: 'index' },
      { text: 'Điểm danh', event: 'rollcall' },
      { text: 'Điểm số', event: 'score' },
      { text: 'Tình hình học tập', event: 'learn' },
      { text: 'Giao Bài Tập', event: 'home_work' }
    ]

    const menuAdmins = [
      { text: 'Quản lí môn học', event: 'class_management' },
      { text: 'Quản lí học viên', event: 'teacher_management' },
      { text: 'Quản lí giáo viên', event: 'student_management' }
    ]

    const menuStudents = [
      { text: 'Trang chủ', event: 'index' },
      { text: 'Điểm danh', event: 'rollcall' },
      { text: 'Điểm số', event: 'score' },
      { text: 'Thông báo', event: 'noti' },
      { text: 'Bài tập', event: 'home_work_student' }
    ]

    if (!localStorage.getItem('token')) member.value = { typeMember: 'teacher' }
    else member.value = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))

    window.addEventListener('resize', (event) => {
      isResponsive.value = document.body.clientWidth < 750
    })

    const openMenuList = () => {
      isOpenMenu.value = !isOpenMenu.value
    }

    return {
      member,
      isResponsive,
      menuTeachers,
      menuAdmins,
      menuStudents,
      openMenuList,
      isOpenMenu
    }
  }
})

export default MenuComponent
</script>

<style lang="sass">
.relative a:hover
  cursor: pointer
@media (min-width: 850px)
  .nav-icon
    display: none !important
</style>
