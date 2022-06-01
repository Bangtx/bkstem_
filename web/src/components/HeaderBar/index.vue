<template lang="pug">
  .w-full.bg-white.shadow.py-3.px-4.flex.justify-between.items-center.z-20.fixed(class="md:px-8")
    div(@click="goToHomePage")
      //h1.text-red-500.text-5xl BK
      v-img(:src="`/img/icons/android-chrome-192x192.png`" width="40")
    .hidden.text-3xl.font-bold(v-if="isAdmin" class='md:block')
      h1 Trang quản lí dành cho Admin
    .flex.rounded-full.bg-gray-100(v-if="!isAdmin")
      input.px-4.py-2.w-32.text-gray-600.rounded-full.bg-gray-100(type="text" class="md:w-80 lg:w-96 focus:outline-none" placeholder="Tìm kiếm ...")
      button.flex.items-center.justify-center.px-4.text-orange-500
        svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
          path(stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z")
    .flex.items-center.gap-4.text-orange-400(class="md:gap-6")
      button.relative.align-middle.rounded-md(class="focus:outline-none")
        svg.w-5.h-5(aria-hidden="true" fill="currentColor" viewBox="0 0 20 20")
          path(d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z")
        // Notification badge
        span.absolute.top-0.right-0.inline-block.w-3.h-3.transform.translate-x-1.-translate-y-1.bg-red-600.border-2.border-white.rounded-full(aria-hidden="true")

      v-menu(offset-y='')
        template(v-slot:activator='{ on, attrs }')
          button.flex.items-center.gap-2(v-bind='attrs' v-on='on')
            img.object-cover.w-6.h-6.rounded-full(src="https://media.istockphoto.com/vectors/user-icon-flat-isolated-on-white-background-user-symbol-vector-vector-id1300845620?k=20&m=1300845620&s=612x612&w=0&h=f4XTZDAv7NPuZbG0habSpU0sNgECM0X7nbKzTUta3n8=" alt="" aria-hidden="true")
            h2.text-gray-800.font-medium.hidden(class="md:block") {{ member.name }}
        v-list
          v-list-item.logout(@click="logout()") Đắng xuất

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { toCamelCase, urlPath } from 'utils'
import jwtDecode from 'jwt-decode'

const HeaderBar = defineComponent({
  props: {
    isAdmin: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup(props, { root }) {
    const { $router } = root
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    console.log(member)
    const goToHomePage = () => {
      $router.push({ name: urlPath.START.name })
    }

    const logout = () => {
      localStorage.removeItem('token')
      $router.push({ name: urlPath.Login.name })
    }

    return {
      goToHomePage,
      logout,
      member
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
.logout
  cursor: pointer
.flex
  flex: none !important
  max-width: 100% !important
</style>
