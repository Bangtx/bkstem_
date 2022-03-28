<template lang="pug">
  .w-full.bg-white.shadow.py-3.px-4.flex.justify-between.items-center.z-20.fixed(class="md:px-8")
    div
      h1.text-red-500.text-5xl BK
    .flex.rounded-full.bg-gray-100
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
      button#dropdownButton.flex.items-center.gap-2(data-dropdown-toggle="dropdown")
        img.object-cover.w-6.h-6.rounded-full(src="https://images.unsplash.com/photo-1502378735452-bc7d86632805?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&s=aa3a807e1bbdfd4364d1f449eaa96d82" alt="" aria-hidden="true")
        h2.text-gray-800.font-medium.hidden(class="md:block") Hi, Nam
      #dropdown.hidden.z-10.w-44.text-base.list-none.bg-white.rounded.divide-y.divide-gray-100.shadow
        .py-1(aria-labelledby="dropdownButton")
          .py-2.mx-4.text-gray-700.border-b.border-b-gray-700 Nam
          h2.block.py-2.px-4.text-sm.text-gray-700(class="hover:bg-gray-100") Thông tin cá nhân
          h2.block.py-2.px-4.text-sm.text-gray-700(class="hover:bg-gray-100") Cài đặt
          h2.block.py-2.px-4.text-sm.text-gray-700(class="hover:bg-gray-100") Đăng xuất

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const HeaderBar = defineComponent({
  setup() {
    return {}
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
