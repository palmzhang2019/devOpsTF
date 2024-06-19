<template>
  <div>
    <h2>Drag and Drop Demo with Element Plus</h2>
    <el-row :gutter="20">
      <el-col v-for="(items, area) in dropAreas" :key="area" :span="4">
        <div
          class="drop-area"
          @dragover="onDragOver"
          @drop="onDrop($event, area)"
        >
          <template v-if="items.length">
            <div
              v-for="(item, index) in items"
              :key="index"
              class="draggable-item"
              draggable="true"
              @dragstart="onDragStart($event, item)"
            >
              {{ item }}
            </div>
          </template>
        </div>
        <p>{{ area }}</p>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'TestPage',
  setup() {
    const item1 = 'Item1';
    const item2 = 'Item2';
    const item3 = 'Item3';

    // 使用对象来存储多个区域的状态
    const dropAreas = ref({
      a: [item1],
      b: [item2],
      c: [item3],
      d: [],
      e: [],
    });

    const onDragStart = (event, data) => {
      event.dataTransfer.setData('text/plain', data);
      event.dataTransfer.effectAllowed = 'move';
    };

    const onDragOver = (event) => {
      event.preventDefault();
    };

    const onDrop = (event, target) => {
      event.preventDefault();
      const data = event.dataTransfer.getData('text/plain');

      // 移动数据到目标区域
      for (let area in dropAreas.value) {
        dropAreas.value[area] = dropAreas.value[area].filter(item => item !== data);
      }
      if (!dropAreas.value[target].includes(data)) {
        dropAreas.value[target].push(data);
      }
    };

    return {
      dropAreas,
      onDragStart,
      onDragOver,
      onDrop,
    };
  },
};
</script>

<style scoped>
.draggable-item {
  width: 100px;
  padding: 10px;
  margin: 10px;
  background-color: #409EFF;
  color: white;
  cursor: grab;
  text-align: center;
}

.drop-area {
  width: 200px;
  height: 200px;
  margin: 10px;
  background-color: #F5F5F5;
  border: 2px dashed #409EFF;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
