<template>
  <div class="home">
    <h1>Welcome to Home Page</h1>
    <el-tabs v-model="activeTab" @tab-click="handleClick">
      <el-tab-pane label="User List" name="userlist">
        <UserList v-if="activeTab === 'userlist'" />
      </el-tab-pane>
      <el-tab-pane label="Label List" name="labellist">
        <LabelList v-if="activeTab === 'labellist'" />
      </el-tab-pane>
      <el-tab-pane label="Role Manager" name="rolemanager">
        <RoleManager v-if="activeTab === 'rolemanager'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import UserList from '../components/UserList';
import LabelList from '../components/LabelList';
import RoleManager from '../components/RoleManager.vue';

export default {
  name: 'HomePage',
  components: {
    UserList,
    LabelList,
    RoleManager,
  },
  data() {
    return {
      activeTab: 'userlist',
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log('Tab clicked:', tab, event);
    },
  },
}
</script>

<style scoped>
.home {
  text-align: center;
}
</style>
