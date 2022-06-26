<template lang="pug">
  div
    v-dialog(:value="value" max-width="500" persistent)
      v-card
        v-card-title.text-h5.title-color.lighten-2
          span Bài Tập
          v-spacer
          v-btn(icon @click="$emit('on-close')")
            v-icon mdi-close
        v-card-text
          v-select(
            :items="homeWorkFiles"
            item-text="title"
            item-value="id"
            v-model="studentFileProps.homeWorkFile"
          )
          v-text-field(label="msg" v-model="studentFileProps.msg" )
          v-row
            v-file-input(
              v-if="!studentFileProps.id || isEditFile"
              accept="pdf/*, doc/*"
              v-model="file"
            )
          v-row
            v-col
              span.text-click-able(
                v-if="studentFileProps.id"
                @click="openFile(studentFileProps.url)"
              ) xem file
            v-col
              v-btn(
                v-if="studentFileProps.id"
                @click="isEditFile = true"
              ) edit file

        v-card-actions
          v-btn.relative-btn(
            :large="!$vuetify.breakpoint.xsOnly"
            block
            @click="onSave()"
          )
            span Lưu
</template>

<script lang="ts">
import { defineComponent, watch, ref, toRefs } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, readFile, toSnakeCase } from 'utils'

const UploadFileAnswerDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    homeWorkFiles: {
      type: Array,
      required: false,
      default: () => []
    },
    studentFileProps: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const file = ref<any>()
    const isEditFile = ref(false)
    const { studentFileProps } = toRefs(props)

    const uploadFile = async () => {
      const payload = await readFile(file.value)
      const body = {
        payload,
        name: file.value.name,
        type: file.value.type,
        size: file.value.size
      }
      try {
        const { data } = await api.post(endpoints.FILE_QUESTION, body)
        studentFileProps.value.name = data.name
        studentFileProps.value.url = data.url
      } catch {
        $toast.error('Save data failed')
      }
    }

    const onSave = async () => {
      console.log(studentFileProps.value)
      try {
        if (studentFileProps.value.id) {
          await api.put(
            `${endpoints.FILE_RESULT_STUDENT}${studentFileProps.value.id}`,
            toSnakeCase(studentFileProps.value)
          )
        } else {
          await api.post(`${endpoints.FILE_RESULT_STUDENT}`, toSnakeCase(studentFileProps.value))
        }
        $toast.success('Save data successful')
        emit('reload')
        emit('on-close')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const openFile = (url: string) => {
      window.open(url)
    }

    watch(
      () => file.value,
      () => {
        uploadFile()
      }
    )

    return {
      onSave,
      file,
      isEditFile,
      openFile
    }
  }
})

export default UploadFileAnswerDialog
</script>

<style lang="sass"></style>
