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
          v-expansion-panels(
            flat
            multiple
            accordion
            style="overflow: hidden"
          )
            v-expansion-panel(v-for="(item, index) in homeWorks" :key="index")
              v-expansion-panel-header.px-0.py-1(expand-icon="")
                v-row.ma-0.p-0
                  v-col(cols="1")
                    v-icon(v-if="") mdi-chevron-down
                  v-col.title(cols="10")
                    span.pl-4.bold--text {{ item.title }}
                  v-col(cols="1")
                    v-icon mdi-dots-vertical
              v-expansion-panel-content(style="background-color: #deedfc; border-radius: 4px; padding: 0")
                v-list-item.ma-0.title(
                  v-for="question in item.homeWork"
                  :key="question.id"
                )
                  v-col.p-0(cols="12")
                    v-row.p-0
                      span {{ question.questions }}
                      //span {{ question.questions.answers.question }}
                    v-row.p-0(v-if="question.questions.type===0")
                      v-radio-group(v-model="check[question.questions.id]" row='')
                        v-radio(:label="question.questions.answers.a" :value="'A'")
                        v-radio(:label="question.questions.answers.b" :value="'B'")
                        v-radio(:label="question.questions.answers.c" :value="'C'")
                        v-radio(:label="question.questions.answers.d" :value="'D'")

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
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { QuestionDialog } from 'components'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'

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
  setup(props, { root }) {
    const { $toast } = root
    const isOpenAddQuestionDialog = ref(false)
    const openAddQuestionDialog = () => {
      isOpenAddQuestionDialog.value = true
    }
    const homeWorks = ref<any[]>([])
    const check = ref<any[]>([])

    const getData = async () => {
      try {
        const { data } = await api.get(
          `${endpoints.HOME_WORK}group_by_units?classroom=${props.classroom.id}`
        )
        homeWorks.value = toCamelCase(data)
        // console.log(homeWorks.value)
        const x = []
          .concat(
            ...homeWorks.value.map((homeWork: any) => {
              return homeWork.homeWork.map((e: any) => {
                return e.id
              })
            })
          )
          .map((id: number) => {
            check.value[id] = null
            return null
          })
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })

    return {
      isOpenAddQuestionDialog,
      openAddQuestionDialog,
      homeWorks,
      check
    }
  }
})

export default HomeWork
</script>

<style lang="sass">
.title
  text-align: left !important
</style>
