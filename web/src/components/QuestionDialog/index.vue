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
          v-textarea.question-input(
            v-if="questionProps"
            outlined
            v-model="questionProps.answers.question"
          )
          span Ảnh (nếu có)
          v-text-field(outlined v-model="questionProps.image")
          span Câu trả lời
          v-select(
            :label="'loại câu hỏi'"
            :items="typeQuestions"
            item-text="key"
            item-value="value"
            v-model="questionProps.type"
            max-width="300"
          )
          v-select(
            :label="'unit'"
            :items="unitShows"
            item-text="key"
            item-value="value"
            v-model="questionProps.unit"
            max-width="300"
          )
          span.pt-4 Đáp án
          div(v-if="questionProps.type===0")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="questionProps.result === 'A'"
                  color="primary" @click="clickCheckBox('A')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="questionProps.result !== 'A'" color="#0000003d" @click="clickCheckBox('A')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da A
              v-col(cols="2")
                v-text-field(outlined, v-model="questionProps.answers.a")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="questionProps.result === 'B'"
                  color="#0000003d" @click.stop="clickCheckBox('B')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="questionProps.result !== 'B'" color="#0000003d" @click="clickCheckBox('B')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da B
              v-col(cols="2")
                v-text-field(outlined, v-model="questionProps.answers.b")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="questionProps.result === 'C'"
                  color="#0000003d" @click.stop="clickCheckBox('C')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="questionProps.result !== 'C'" color="#0000003d" @click="clickCheckBox('C')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da C
              v-col(cols="2")
                v-text-field(outlined, v-model="questionProps.answers.c")
            v-row
              v-col(cols="1")
                v-icon.ml-2(
                  v-if="questionProps.result === 'D'"
                  color="#0000003d" @click.stop="clickCheckBox('D')"
                ) mdi-check-circle
                v-icon.ml-2(
                  v-if="questionProps.result !== 'D'" color="#0000003d" @click="clickCheckBox('D')"
                ) mdi-checkbox-blank-circle-outline
              v-col(cols="1")
                span.da D
              v-col(cols="2")
                v-text-field(outlined, v-model="questionProps.answers.d")
          div(v-if="questionProps.type===1")
            v-text-field(outlined, v-model="questionProps.result")

        v-card-actions
          v-btn.relative-btn(
            :large="!$vuetify.breakpoint.xsOnly"
            block
            @click="onSave()"
          )
            span Lưu
</template>

<script lang="ts">
import { defineComponent, ref, toRefs, onMounted } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toSnakeCase } from 'utils'

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
    },
    questionProps: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const unitShows = ref<any[]>([])
    const ans = ref({ a: '', b: '', c: '', d: '', correct: '' })
    const typeQuestions = [
      { key: 'trắc nghiệm', value: 0 },
      { key: 'tự luận', value: 1 }
    ]
    const { questionProps } = toRefs(props)

    const clickCheckBox = (value: string) => {
      ans.value.correct = value
      questionProps.value.result = value
    }

    const onSave = async () => {
      console.log(questionProps.value)
      // const bodyQuestion = {
      //   answers:
      //     typeQuestion.value === typeQuestions[0]
      //       ? {
      //           question: question.value,
      //           a: ans.value.b,
      //           b: ans.value.b,
      //           c: ans.value.c,
      //           d: ans.value.d
      //         }
      //       : { question: question.value },
      //   result: typeQuestion.value === typeQuestions[0] ? ans.value.correct : ansLongResponse.value,
      //   type: typeQuestion.value === typeQuestions[0] ? 0 : 1,
      //   image: linkImage.value === '' ? null : linkImage.value
      // }
      questionProps.value.answers =
        questionProps.value.type === 0
          ? {
              question: questionProps.value.answers.question,
              a: questionProps.value.answers.a,
              b: questionProps.value.answers.b,
              c: questionProps.value.answers.c,
              d: questionProps.value.answers.d
            }
          : { question: questionProps.value.answers.question }
      if (questionProps.value.result === '') {
        $toast.error('Chưa chọn đán án đúng')
        return
      }
      try {
        let check = false
        if (questionProps.value.type === 0) {
          check =
            questionProps.value.answers.correct !== '' &&
            questionProps.value.answers.a !== '' &&
            questionProps.value.answers.b !== '' &&
            questionProps.value.answers.c !== '' &&
            questionProps.value.answers.d !== '' &&
            questionProps.value.answers !== ''
        } else {
          check = questionProps.value.result !== ''
        }
        if (check) {
          if (questionProps.value.id) {
            await api.put(
              `${endpoints.QUESTION}${questionProps.value.id}`,
              toSnakeCase(questionProps.value)
            )
          } else {
            const questionPost = (
              await api.post(`${endpoints.QUESTION}`, toSnakeCase(questionProps.value))
            ).data
            const bodyHomeWork = {
              classroom: props.classroom.id,
              question: questionPost.id,
              schedule: questionProps.value.unit
            }
            await api.post(endpoints.HOME_WORK, bodyHomeWork)
          }
          $toast.success('Save data successful')
          emit('re-load')
        } else {
          $toast.error('Save data failed')
        }
      } catch {
        $toast.error('Save data failed')
      }
    }

    onMounted(() => {
      unitShows.value = props.units.map((unit: any) => {
        return { key: unit.title, value: unit.id }
      })
    })

    return {
      typeQuestions,
      ans,
      clickCheckBox,
      onSave,
      unitShows
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
