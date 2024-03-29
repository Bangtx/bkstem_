<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Điểm danh
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      v-card-text
        v-text-field(readonly :value="data.date")
        v-select(
          label="Diem danh"
          :items="items"
          item-value="value"
          item-text="key"
          v-model="data.absentType"
        )
      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu
</template>

<script lang="ts">
import { defineComponent, watch, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'

const EditRollCallDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      required: true
    },
    absentTypes: {
      type: Array,
      required: true
    },
    isSelfLearning: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const items = ref<any>([])
    const itemSelected = ref(0)

    const getBodySelfLearning = () => {
      return {
        classroom: props.data.classroom,
        student: props.data.student,
        absent_type: props.data.absentType,
        dates: [props.data.date],
        id: props.data.id
      }
    }

    const onSave = async () => {
      try {
        if (!props.isSelfLearning) await api.put(`${endpoints.ROLLCALL}`, toSnakeCase(props.data))
        else await api.put(`${endpoints.SELF_LEARNING}${props.data.id}`, getBodySelfLearning())
        emit('reload')
        emit('on-close')
        $toast.success('Delete data successful')
      } catch {
        $toast.error('Delete data failed')
      }
    }

    watch(
      () => props.value,
      () => {
        items.value = props.absentTypes.map((e: any) => {
          return { key: e.type, value: e.id }
        })
      }
    )

    return {
      onSave,
      items,
      itemSelected
    }
  }
})

export default EditRollCallDialog
</script>
