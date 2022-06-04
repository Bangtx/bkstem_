<template lang="pug">
  div
    v-dialog(:value="value" max-width="500" persistent)
      v-card
        v-card-title.text-h5.title-color.lighten-2
          span Bài Tập
          v-spacer
          v-btn(icon @click="$emit('on-close')")
            v-icon mdi-close

        .p-4
          h1 Câu Hỏi
          v-textarea.question-input(outlined v-model="question")
          span Ảnh (nếu có)
          v-text-field(outlined v-model="linkImage")
          span Câu trả lời
          v-select(
            :label="'loại câu hỏi'"
            :items="typeQuestions"
            v-model="typeQuestion"
            max-width="300"
          )
          v-select(
            :label="'unit'"
            :items="units.map(e => e.title)"
            v-model="unit"
            max-width="300"
          )
          span.pt-4 Đáp án
          div(v-if="typeQuestion==='trắc nghiệm'")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="ans.correct === 'A'"
                  color="primary" @click="clickCheckBox('A')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="ans.correct !== 'A'" color="#0000003d" @click="clickCheckBox('A')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da A
              v-col(cols="2")
                v-text-field(outlined, v-model="ans.a")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="ans.correct === 'B'"
                  color="#0000003d" @click.stop="clickCheckBox('B')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="ans.correct !== 'B'" color="#0000003d" @click="clickCheckBox('B')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da B
              v-col(cols="2")
                v-text-field(outlined, v-model="ans.b")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="ans.correct === 'C'"
                  color="#0000003d" @click.stop="clickCheckBox('C')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="ans.correct !== 'C'" color="#0000003d" @click="clickCheckBox('C')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da C
              v-col(cols="2")
                v-text-field(outlined, v-model="ans.c")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="ans.correct === 'D'"
                  color="#0000003d" @click.stop="clickCheckBox('D')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="ans.correct !== 'D'" color="#0000003d" @click="clickCheckBox('D')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da D
              v-col(cols="2")
                v-text-field(outlined, v-model="ans.d")
          div(v-if="typeQuestion==='tự luận'")
            v-text-field(outlined, v-model="ansLongResponse")

        v-card-actions
          v-btn.relative-btn(
            :large="!$vuetify.breakpoint.xsOnly"
            block
            @click="onSave()"
          )
            span Lưu
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints } from 'utils'

const QuestionDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    units: {
      type: Array,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const unit = ref('')
    const linkImage = ref('')
    const ans = ref({ a: '', b: '', c: '', d: '', correct: '' })
    const question = ref('')
    const typeQuestions = ['trắc nghiệm', 'tự luận']
    const typeQuestion = ref('trắc nghiệm')
    const ansLongResponse = ref('')

    const clickCheckBox = (value: string) => {
      ans.value.correct = value
    }

    const onSave = async () => {
      const bodyQuestion = {
        answers:
          typeQuestion.value === typeQuestions[0]
            ? {
                question: question.value,
                a: ans.value.b,
                b: ans.value.b,
                c: ans.value.c,
                d: ans.value.d
              }
            : { question: question.value },
        result: typeQuestion.value === typeQuestions[0] ? ans.value.correct : ansLongResponse.value,
        type: typeQuestion.value === typeQuestions[0] ? 0 : 1,
        image: linkImage.value === '' ? null : linkImage.value
      }
      if (bodyQuestion.result === '') {
        $toast.error('Chưa chọn đán án đúng')
        return
      }
      try {
        let check = false
        if (typeQuestion.value === typeQuestions[0]) {
          check =
            ans.value.correct !== '' &&
            ans.value.a !== '' &&
            ans.value.b !== '' &&
            ans.value.c !== '' &&
            ans.value.d !== '' &&
            question.value !== ''
        } else {
          check = ansLongResponse.value !== ''
        }
        if (check) {
          const questionPost = (await api.post(`${endpoints.QUESTION}`, bodyQuestion)).data
          const schedule: any = props.units.find((e: any) => e.title === unit.value)
          const bodyHomeWork = {
            classroom: props.classroom.id,
            question: questionPost.id,
            schedule: schedule.id
          }
          await api.post(endpoints.HOME_WORK, bodyHomeWork)
          $toast.success('Save data successful')
          emit('re-load')
        } else {
          $toast.error('Save data failed')
        }
      } catch {
        $toast.error('Save data failed')
      }
    }

    return {
      question,
      typeQuestions,
      ans,
      typeQuestion,
      clickCheckBox,
      ansLongResponse,
      onSave,
      unit,
      linkImage
    }
  }
})

export default QuestionDialog
</script>

<style lang="sass">
.da
  margin-top: 2px
.v-input__control > .v-input__slot
  min-height: 30px !important
  min-width: 200px
.theme--light.v-icon
  color: #1f68e1 !important
.question-input
  .v-input__control
    .v-input__slot
      width: 300px
</style>
