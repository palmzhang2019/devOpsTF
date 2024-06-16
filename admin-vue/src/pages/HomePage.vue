<template>
  <div class="home">
    <h1>Welcome to Home Page</h1>
    <div class="tabs">
      <div
        v-for="tab in tabs"
        :key="tab.name"
        :class="['tab', { active: activeTab === tab.name }]"
        @click="activeTab = tab.name"
      >
        {{ tab.label }}
      </div>
    </div>
    <div class="tab-content">
      <UserList v-if="activeTab === 'userlist'" />
      <LabelList v-if="activeTab === 'labellist'" />
    </div>
  </div>
</template>

<script>
import UserList from '../components/UserList';
import LabelList from '../components/LabelList';

export default {
  name: 'HomePage',
  components: {
    UserList,
    LabelList,
  },
  data() {
    return {
      activeTab: 'userlist',
      tabs: [
        { label: 'User List', name: 'userlist' },
        { label: 'Label List', name: 'labellist' },
      ],
    };
  },
}
</script>

<style scoped>
.home {
  text-align: center;
}
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.tab {
  padding: 10px 20px;
  cursor: pointer;
  margin-right: 20px;
  background-color: #f1f1f1;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.tab.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
.tab-content {
  margin-top: 20px;
}
</style>
