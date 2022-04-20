<template lang="pug">
  div
    v-dialog(:value="value" max-width="700" persistent)
      v-card
        v-card-title.text-h5.title-color.lighten-2
          span Bài Tập
          v-spacer
          v-btn(icon @click="$emit('on-close')")
            v-icon mdi-close

        .p-4
          h1 Câu Hỏi
          v-textarea(outlined v-model="question")
          span Câu trả lời
          v-select(
            :label="'loại câu hỏi'"
            :items="typeQuestions"
            v-model="typeQuestion"
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
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const ans = ref({ a: '', b: '', c: '', d: '', correct: '' })
    const question = ref('')
    const typeQuestions = ['trắc nghiệm', 'tự luận']
    const typeQuestion = ref('trắc nghiệm')
    const ansLongResponse = ref('')

    const clickCheckBox = (value: string) => {
      ans.value.correct = value
    }

    const onSave = async () => {
      try {
        console.log(111)
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
      onSave
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
</style>
