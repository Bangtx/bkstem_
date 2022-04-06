<template lang="pug">
  div
    #main.main-content.flex-1.py-20(class="md:pb-5")
      .px-4.text-gray-700(class="md:px-8")
        .px-4.text-gray-700(class="md:px-8")
          .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(d="M12 14l9-5-9-5-9 5 9 5z")
              path(d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222")
            div Tình hình học tập
          .items-center.mt-4.gap-36(class="md:flex")
            h1.py-2
              | Tên lớp:
              span Toán cao cấp
            h1.py-2
              | Sĩ số:
              span 32
          div
            .w-full.overflow-auto.mt-8(style="max-height: 500px;")
              table.w-full.whitespace-nowrap
                thead
                  tr.text-xs.bg-white.font-semibold.tracking-wide.text-left.text-gray-500.uppercase.border-b
                    th.px-4.py-3.px-6 Mã học sinh
                    th.px-4.py-3.px-6 Tên học sinh
                    th.px-4.py-3.px-6.text-center Điểm trung bình
                    th.px-4.py-3.px-6.text-center Nhận xét giáo viên
                tbody.bg-white.divide-y
                  tr.text-gray-700
                    td.px-4.py-3.text-sm 123
                    td.px-4.py-3.text-sm Nguyễn minh khôi
                    td.px-4.py-3.text-sm.text-center 6.7
                    td.px-4.py-3.text-xs.text-center.flex.items-center.justify-center.gap-2
                      button.bg-orange-400.w-14.text-white.py-1.px-2.rounded-full(@click="openNotiDialog('see')") Xem
                      button.bg-green-500.w-14.text-white.py-1.px-2.rounded-full(@click="openNotiDialog('add')") Nhập

    notification-dialog(
      :value="isOpenNotiDialog"
      :mode="modeOpen"
      @on-close="isOpenNotiDialog = false"
    )

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { NotificationDialog } from 'components'

const Learn = defineComponent({
  components: {
    NotificationDialog
  },
  setup() {
    const isOpenNotiDialog = ref(false)
    const modeOpen = ref('')
    const openNotiDialog = (mode: string) => {
      isOpenNotiDialog.value = true
      modeOpen.value = mode
      console.log(mode, isOpenNotiDialog.value)
    }
    return {
      openNotiDialog,
      isOpenNotiDialog,
      modeOpen
    }
  }
})

export default Learn
</script>
