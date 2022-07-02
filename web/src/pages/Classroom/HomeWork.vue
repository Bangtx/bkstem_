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

          v-select.ml-2(
            :label="'Kiểu'"
            :items="typeHomeWorks"
            item-text="key"
            item-value="value"
            v-model="typeHomeWork"
          )

        .flex.justify-between.items-center
          .text-lg Danh sách câu hỏi
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
            v-if="typeHomeWork === 1"
            @click="openAddQuestionDialog()"
            class='hover:bg-orange-300 focus:outline-none'
          )
            svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M12 6v6m0 0v6m0-6h6m-6 0H6')
            span.text-base Thêm câu hỏi

          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
            v-if="typeHomeWork === 2"
            @click="openAddQuestionFileDialog()"
            class='hover:bg-orange-300 focus:outline-none'
          )
            svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M12 6v6m0 0v6m0-6h6m-6 0H6')
            span.text-base Thêm File

        .mt-2(class='md:px-4')
          div(v-if="typeHomeWork === 1")
            div(v-for="unit in units" :key="unit.id")
              v-list-item
                v-icon(
                  v-if="unitRequired.indexOf(unit.id) === -1" @click="requireThisUnit(unit.id, true)"
                  ) mdi-checkbox-blank-circle-outline
                v-icon(
                  v-if="unitRequired.indexOf(unit.id) !== -1" @click="requireThisUnit(unit.id, false)"
                ) mdi-checkbox-marked-circle
                span.ml-2 {{ unit.title }}
              v-divider

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
                      v-icon mdi-chevron-down
                    v-col.title(cols="10")
                      span.pl-4.bold--text {{ item.title }}
                    //v-col(cols="1")
                    //  v-icon mdi-dots-vertical
                v-expansion-panel-content(style="background-color: #deedfc; border-radius: 4px; padding: 0")
                  v-list-item.pa-0.ma-0.title(
                    v-for="(question, index) in item.homeWork"
                    :key="question.id"
                  )
                    v-col.p-0(cols="12")
                      v-row.p-0
                        v-col.p-0(cols="12")
                          v-row.p-0
                            v-col.p-0(cols="11")
                              span {{ index }}: {{ question.questions.answers.question }}
                            v-col.p-0(cols="1")
                              v-icon(@click="openBottomSheet(question)") mdi-dots-vertical
                        v-img(
                          v-if="question.questions.image !== null && question.questions.image !== ''"
                          :src="question.questions.image" max-width="360"
                        )
                        vuetify-audio(
                          v-if="question.questions.audio"
                          :file="question.questions.audio"
                          color="success"
                        )
                        //span {{ question }}
                      v-row.p-0(v-if="question.questions.type===0")
                        v-radio-group(v-model="question.result" row='')
                          v-radio(:label="question.questions.answers.a" :value="'A'")
                          v-radio(:label="question.questions.answers.b" :value="'B'")
                          v-radio(:label="question.questions.answers.c" :value="'C'")
                          v-radio(:label="question.questions.answers.d" :value="'D'")
                      v-row.p-0(v-if="question.questions.type===1")
                        v-text-field(v-model="question.result")

          //button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class='hover:bg-orange-300 focus:outline-none')
          //  span.text-base Giao bài
          div(v-if="typeHomeWork === 2")
            div(v-for="homeWorkFile in homeWorkFiles" :key="homeWorkFile.id")
              v-list-item
                span {{ homeWorkFile.title }}
                v-spacer
                span {{ homeWorkFile.date }}
                v-spacer
                span.text-click-able(@click="onDownload(homeWorkFile.fileQuestions.url)") download
                v-spacer
                v-icon(@click="openBottomSheet(homeWorkFile)") mdi-dots-vertical
              v-divider

    v-bottom-sheet(
        v-model="showBottomSheet"
        persistent
      )
        div.ma-0.pa-0
          v-row.ma-0.py-0.px-1(align='center' justify='center')
            v-btn.mb-1.rounded-lg(
              block
              height="50"
              elevation="0"
              color="white"
              @click="typeHomeWork === 1 ? editQuestion() : editQuestionFile()"
            )
              span Sửa
            v-btn.mb-1.rounded-lg(
              v-if="typeHomeWork === 2"
              block
              height="50"
              elevation="0"
              color="white"
              @click="openStudentFiles()"
            )
              span Ds Bài Làm
          v-row.ma-0.py-0.px-1(align='center' justify='center')
            v-btn.mb-1.rounded-lg(
              block
              height="50"
              elevation="0"
              color="white"
              @click="showBottomSheet = false"
            )
              span Thoát

    question-dialog(
      v-if="isOpenAddQuestionDialog"
      :value="isOpenAddQuestionDialog"
      :units="units"
      :question-props="questionProps"
      :classroom="classroom"
      @on-close="isOpenAddQuestionDialog = false"
      @re-load="getData"
    )

    question-file-dialog(
      :value="isOpenAddQuestionFileDialog"
      :question-file-props="questionFileProps"
      :classroom="classroom"
      @on-close="isOpenAddQuestionFileDialog = false"
      @re-load="getData"
    )

    file-submit-of-student(
      :value="isOpenFileSubmitOfStudent"
      :question-file-id="questionFileOpenId"
      :classroom="classroom"
      @on-close="isOpenFileSubmitOfStudent = false"
    )
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { QuestionDialog, QuestionFileDialog, FileSubmitOfStudent } from 'components'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'
import jwtDecode from 'jwt-decode'
import VuetifyAudio from 'vuetify-audio/src/vuetifyaudio.vue'

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
    QuestionDialog,
    VuetifyAudio,
    QuestionFileDialog,
    FileSubmitOfStudent
  },
  setup(props, { root }) {
    const { $toast } = root
    const isOpenAddQuestionDialog = ref(false)
    const homeWorks = ref<any[]>([])
    const check = ref<any[]>([])
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const showBottomSheet = ref(false)
    const questionProps = ref<any>({})
    const currentQuestion = ref<any>()
    const currentQuestionFile = ref<any>()
    const isOpenAddQuestionFileDialog = ref(false)
    const isOpenFileSubmitOfStudent = ref(false)
    const questionFileOpenId = ref(0)
    const unitRequired = ref([])
    const questionFileProps = ref<any>({
      id: null,
      date: null,
      title: null,
      fileQuestions: {
        name: null,
        url: null
      }
    })
    const typeHomeWorks = [
      { key: 'Bài Tập Thường', value: 1 },
      { key: 'Bài Tập Theo file', value: 2 }
    ]
    const typeHomeWork = ref(1)
    const homeWorkFiles = ref<any>([])

    const getData = async () => {
      const url =
        member.typeMember === 'teacher'
          ? `${endpoints.HOME_WORK}group_by_units?classroom=${props.classroom.id}&result=true`
          : `${endpoints.HOME_WORK}group_by_units?classroom=${props.classroom.id}`
      try {
        const data = await Promise.all([
          api.get(url),
          api.get(`${endpoints.HOME_WORK_FILE}?classroom_id=${props.classroom.id}`),
          api.get(`${endpoints.HOME_WORK}get_unit_must_exactly?classroom_id=${props.classroom.id}`)
        ])
        const [{ data: QTData }, { data: QTFIle }, { data: UnitR }] = data

        homeWorkFiles.value = toCamelCase(QTFIle)
        homeWorks.value = toCamelCase(QTData)
        unitRequired.value = toCamelCase(UnitR)
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

    const openBottomSheet = (ques: any) => {
      showBottomSheet.value = true
      if (typeHomeWork.value === 1) currentQuestion.value = ques
      if (typeHomeWork.value === 2) currentQuestionFile.value = ques
    }

    const openStudentFiles = () => {
      isOpenFileSubmitOfStudent.value = true
      questionFileOpenId.value = currentQuestionFile.value.id
    }

    const openAddQuestionFileDialog = () => {
      questionFileProps.value = {
        id: null,
        date: null,
        title: null,
        fileQuestions: {
          id: null,
          name: null,
          url: null
        }
      }
      isOpenAddQuestionFileDialog.value = true
    }

    const openAddQuestionDialog = () => {
      isOpenAddQuestionDialog.value = true
      questionProps.value = {
        id: null,
        answers: { a: '', b: '', c: '', d: '' },
        result: '',
        type: 0,
        image: null,
        audio: null,
        unit: null
      }
    }

    const editQuestion = () => {
      isOpenAddQuestionDialog.value = true
      let unit = null
      homeWorks.value.forEach((homeWork: any) => {
        const questionIds = homeWork.homeWork.map((e: any) => e.id)
        if (questionIds.indexOf(currentQuestion.value.id) > -1) {
          unit = homeWork.id
        }
      })
      questionProps.value = {
        id: currentQuestion.value.questions.id,
        answers:
          currentQuestion.value.questions.type === 0
            ? {
                a: currentQuestion.value.questions.answers.a,
                b: currentQuestion.value.questions.answers.b,
                c: currentQuestion.value.questions.answers.c,
                d: currentQuestion.value.questions.answers.d,
                question: currentQuestion.value.questions.answers.question
              }
            : {
                question: currentQuestion.value.questions.answers.question
              },
        result: currentQuestion.value.result,
        type: currentQuestion.value.questions.type,
        image: currentQuestion.value.questions.image,
        audio: currentQuestion.value.questions.audio,
        unit
      }
    }

    const requireThisUnit = async (unitId: number, value: boolean) => {
      try {
        const { data } = await api.post(`${endpoints.HOME_WORK}update_unit_require`, {
          unit: unitId,
          value
        })
        unitRequired.value = data
        $toast.success('Save successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const editQuestionFile = () => {
      questionFileProps.value = {
        id: currentQuestionFile.value.id,
        date: null,
        title: currentQuestionFile.value.title,
        fileQuestions: currentQuestionFile.value.fileQuestions
      }

      isOpenAddQuestionFileDialog.value = true
    }

    const onDownload = (url: string) => {
      window.open(url)
    }

    onMounted(async () => {
      await getData()
    })

    return {
      isOpenAddQuestionDialog,
      openAddQuestionDialog,
      homeWorks,
      check,
      getData,
      showBottomSheet,
      editQuestion,
      openBottomSheet,
      questionProps,
      typeHomeWork,
      typeHomeWorks,
      openAddQuestionFileDialog,
      isOpenAddQuestionFileDialog,
      questionFileProps,
      homeWorkFiles,
      onDownload,
      currentQuestionFile,
      editQuestionFile,
      openStudentFiles,
      isOpenFileSubmitOfStudent,
      questionFileOpenId,
      unitRequired,
      requireThisUnit
    }
  }
})

export default HomeWork
</script>

<style lang="sass">
.title
  text-align: left !important
.v-input
  max-width: 100% !important
.v-expansion-panel-content__wrap
  padding: 3px !important
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
</style>
