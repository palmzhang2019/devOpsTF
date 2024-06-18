<template>
    <div>
      <h2>Drag and Drop Demo with Element Plus</h2>
      <el-row :gutter="20">
        <el-col :span="6">
          <div
            class="drop-area"
            @dragover="onDragOver"
            @drop="onDrop($event, 'left')"
          >
            <template v-if="leftItems.length">
              <div
                v-for="(item, index) in leftItems"
                :key="index"
                class="draggable-item"
                draggable="true"
                @dragstart="onDragStart($event, item)"
              >
                {{ item }}
              </div>
            </template>
          </div>
        </el-col>
        <el-col :span="6">
          <div
            class="drop-area"
            @dragover="onDragOver"
            @drop="onDrop($event, 'right')"
          >
            <template v-if="rightItems.length">
              <div
                v-for="(item, index) in rightItems"
                :key="index"
                class="draggable-item"
                draggable="true"
                @dragstart="onDragStart($event, item)"
              >
                {{ item }}
              </div>
            </template>
          </div>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'TestPage',
    setup() {
      const item1 = 'This is a draggable item';
      const leftItems = ref([item1]);
      const rightItems = ref([]);
  
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
  
        if (target === 'left') {
          if (!leftItems.value.includes(data)) {
            leftItems.value.push(data);
          }
          rightItems.value = rightItems.value.filter(item => item !== data);
        } else {
          if (!rightItems.value.includes(data)) {
            rightItems.value.push(data);
          }
          leftItems.value = leftItems.value.filter(item => item !== data);
        }
      };
  
      return {
        leftItems,
        rightItems,
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
  