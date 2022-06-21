<template lang="pug">
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
        .flex.gap-2.items-center.text-lg.font-semibold.text-gray-600.mt-4
          div Bài tập mới
          v-select.ml-2(
            :label="'Kiểu'"
            :items="typeHomeWorks"
            item-text="key"
            item-value="value"
            v-model="typeHomeWork"
          )
        .flex.justify-between.items-center
          .text-lg Danh sách câu hỏi (Số câu hỏi đã làm đúng : {{corrected}})
        .mt-2(class='md:px-4')
          div(v-if="typeHomeWork === 1")
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
                    v-for="(question, index) in item.homeWork"
                    :key="question.id"
                  )
                    v-col.p-0(cols="12")
                      v-row.p-0
                        //span {{ question.questions. }}
                        h2 {{ index }}:
                        span {{ question.questions.answers.question }}
                      v-row.p-0(v-if="question.questions.type===0")
                        v-radio-group(v-model="check[question.questions.id]" row='')
                          v-radio(:label="question.questions.answers.a" :value="'A'")
                          v-radio(:label="question.questions.answers.b" :value="'B'")
                          v-radio(:label="question.questions.answers.c" :value="'C'")
                          v-radio(:label="question.questions.answers.d" :value="'D'")
                      v-row.p-0(v-if="question.questions.type===1")
                        v-text-field(v-model="check[question.questions.id]")

          div(v-if="typeHomeWork === 2")
            div(v-for="homeWorkFile in homeWorkFiles" :key="homeWorkFile.id")
              v-list-item
                span {{ homeWorkFile.title }}
                v-spacer
                span {{ homeWorkFile.date }}
                v-spacer
                span.text-click-able(@click="onDownload(homeWorkFile.fileQuestions.url)") download
              v-divider

        button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
          class="hover:bg-orange-300 focus:outline-none"
          @click="onSubmit()"
        )
          span.text-base Nộp

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'
import jwtDecode from 'jwt-decode'
import home from '../Home/index.vue'
import { HOME_WORK_STUDENT } from '../../utils/apiEndpoints'

const HomeWorkStudent = defineComponent({
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
  setup(props, { root }) {
    const { $toast } = root
    const homeWorks = ref<any[]>([])
    const check = ref<any>({})
    const student: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const corrected = ref(0)
    const typeHomeWorks = [
      { key: 'Bài Tập Thường', value: 1 },
      { key: 'Bài Tập Theo file', value: 2 }
    ]
    const typeHomeWork = ref(1)
    const homeWorkFiles = ref<any>([])

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(
            `${endpoints.HOME_WORK}group_by_units?classroom=${props.classroom.id}&student=${student.id}`
          ),
          api.get(
            `${endpoints.HOME_WORK_STUDENT}check_rate_correct?student_id=${student.id}&classroom_id=${props.classroom.id}`
          ),
          api.get(`${endpoints.HOME_WORK_FILE}?classroom_id=${props.classroom.id}`)
        ])
        const [{ data: homeWorksData }, { data: checkRateData }, { data: QTFIle }] = data
        homeWorkFiles.value = toCamelCase(QTFIle)
        corrected.value = checkRateData.correct
        homeWorks.value = toCamelCase(homeWorksData)
        const x = []
          .concat(
            ...homeWorks.value.map((homeWork: any) => {
              return homeWork.homeWork.map((e: any) => {
                return e.id
              })
            })
          )
          .map((id: number) => {
            check.value[id.toString()] = null
            return null
          })
      } catch (e) {
        $toast.error('Get data failed')
      }
      ;[].concat(...homeWorks.value.map((e: any) => e.homeWork)).forEach((e: any) => {
        check.value[e.id] = e.resultStudent
      })
    }

    const saveResultAPI = async (body: any) => {
      try {
        await api.post(`${endpoints.HOME_WORK_STUDENT}multiple_result`, body)
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const onSubmit = () => {
      const body: any[] = []
      Object.keys(check.value).forEach((key: string) => {
        if (check.value[key] !== null && check.value[key] !== '') {
          body.push({
            result: check.value[key],
            question: Number(key),
            student: student.id
          })
        }
      })
      saveResultAPI(toSnakeCase(body))
    }

    const onDownload = (url: string) => {
      window.open(url)
    }

    onMounted(async () => {
      await getData()
    })
    return {
      homeWorks,
      check,
      onSubmit,
      corrected,
      typeHomeWorks,
      typeHomeWork,
      homeWorkFiles,
      onDownload
    }
  }
})

export default HomeWorkStudent
</script>

<style lang="sass"></style>
