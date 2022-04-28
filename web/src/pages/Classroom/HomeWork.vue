<template lang="pug" xmlns="">
  div
    #main.main-content.flex-1.py-20(class='md:pb-5')
      .px-4.text-gray-700(class='md:px-8')
        .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
          svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
          div Trang chủ
          svg.h-5.w-5(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M9 5l7 7-7 7')
          svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z')
          div Giao bài tập
        .flex.gap-2.items-center.text-lg.font-semibold.text-gray-600.mt-2
          div Bài tập đã giao
        .flex.gap-2.items-center.text-lg.font-semibold.text-gray-600.mt-4
          div Bài tập mới
        .flex.justify-between.items-center
          .text-lg Danh sách câu hỏi
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
            @click="openAddQuestionDialog()"
            class='hover:bg-orange-300 focus:outline-none'
          )
            svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M12 6v6m0 0v6m0-6h6m-6 0H6')
            span.text-base Thêm câu hỏi
        .mt-2(class='md:px-4')
          div
            | 1. aksjdklajsldkjals olaiksjdklajsdlkjaslkd lksdlkjasljdajssd kjdlkjalsjdla ................ skjadkjsaldkljlkklj
          div
            | 2. aksjdklajsldkjals olaiksjdklajsdlkjaslkd lksdlkjasljdajssd kjdlkjalsjdla ................ skjadkjsaldkljlkklj
        button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class='hover:bg-orange-300 focus:outline-none')
          span.text-base Giao bài

    question-dialog(
      :value="isOpenAddQuestionDialog"
      :units="units"
      :classroom="classroom"
      @on-close="isOpenAddQuestionDialog = false"
    )
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { QuestionDialog } from 'components'

const HomeWork = defineComponent({
  props: {
    units: {
      type: Array,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  components: {
    QuestionDialog
  },
  setup() {
    const isOpenAddQuestionDialog = ref(false)
    const openAddQuestionDialog = () => {
      isOpenAddQuestionDialog.value = true
    }
    return {
      isOpenAddQuestionDialog,
      openAddQuestionDialog
    }
  }
})

export default HomeWork
</script>
