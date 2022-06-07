<template lang="pug">
  v-dialog(:value="value" max-width="700" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Unit
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      .p-4
        v-text-field(
          v-model="unitProps.title"
          :label="'Unit'"
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
import { defineComponent, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toSnakeCase } from 'utils'

interface Unit {
  id: number
  title: string
}

const UnitDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    },
    unitProps: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit, root }) {
    const { $toast } = root

    const onSave = async () => {
      const body = {
        classroom: props.classroom.id,
        title: props.unitProps.title
      }

      try {
        if (props.unitProps.id)
          await api.put(`${endpoints.SCHEDULE}${props.unitProps.id}`, toSnakeCase(body))
        else await api.post(`${endpoints.SCHEDULE}`, toSnakeCase(body))
        emit('re-load')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    return {
      onSave
    }
  }
})

export default UnitDialog
</script>
