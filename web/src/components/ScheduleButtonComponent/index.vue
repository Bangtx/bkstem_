<template lang="pug">
  .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
    .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
      svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
        path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
    div
      p.mb-2.text-sm.font-medium.text-gray-600
        | Thứ 2
      p.text-lg.text-gray-500
        | 17h00p - 19h00p
      p.text-lg.text-gray-500
        | Địa điểm: phòng 701 - A2
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const ScheduleButtonComponent = defineComponent({
  setup() {
    return {}
  }
})

export default ScheduleButtonComponent
</script>
