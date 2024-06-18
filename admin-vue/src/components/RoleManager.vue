<template>
  <el-container>
    <el-header>
      <h1>Role Manager</h1>
    </el-header>
    <el-main>
      <el-card shadow="hover" class="box-card">
        <el-form :model="form" label-width="80px" @submit.prevent="addRole" class="form-container" inline>
          <el-form-item label="Role title" label-position="left">
            <el-input v-model="form.name" placeholder="Enter the role title" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addRole">Create Role</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      <el-divider></el-divider>
      <el-row :gutter="20" class="role-row">
        <el-col v-for="(role, index) in roles" :key="index" :span="8" class="role-col">
          <el-card class="role-card" shadow="hover" v-drop:role="handleDrop">
            <p>{{ role.title }}</p>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="user-row">
        <el-col v-for="(user, index) in trelloUsers" :key="index" :span="6" class="user-col">
          <div class="user-card" shadow="hover" v-drag:transfer="user" drag-data="user">
            <span>{{ user.fullName }}</span>
            <span class="split">|</span>
            <span>{{ user.username }}</span>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { directive as onDrag, directive as onDrop } from 'vue-drag-drop';

export default {
  name: 'RoleManager',
  directives: {
    onDrag,
    onDrop,
  },
  setup() {
    const trelloUsers = ref([]);
    const form = ref({
      name: '',
    });

    const roles = ref([]);

    const addRole = () => {
      if (form.value.name.trim()) {
        roles.value.push({ title: form.value.name });
        form.value.name = '';
      }
    };

    const fetchTrelloUsers = () => {
      const boardId = process.env.VUE_APP_BOARD_ID;
      const TRELLO_KEY = process.env.VUE_APP_TRELLO_KEY;
      const TRELLO_TOKEN = process.env.VUE_APP_TRELLO_TOKEN;
      axios.get(`/trello/boards/${boardId}/members?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}`)
        .then(response => {
          trelloUsers.value = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    };

    const handleDrop = (data, role) => {
      // Here you can handle what happens when a user is dropped into a role card
      console.log('Dropped user:', data, 'on role:', role);
      // For example, you can assign the user to the role
      // Assuming you want to add the user data to the role object
      role.users = role.users || [];
      role.users.push(data);
    };

    onMounted(() => {
      fetchTrelloUsers();
    });

    return {
      form,
      roles,
      addRole,
      trelloUsers,
      handleDrop,
    };
  },
};
</script>

<style scoped>
h1 {
  margin: 0;
  padding: 20px 0;
  text-align: center;
  color: #409EFF;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
}

.box-card {
  margin-bottom: 20px;
  padding: 20px;
}

.role-row {
  margin-top: 20px;
}

.role-col {
  display: flex;
  justify-content: center;
}

.role-card {
  width: 100%;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
}

.user-card {
  border-radius: 2rem;
  background-color: #409EFF;
  color: aliceblue;
  height: 2rem;
  line-height: 2rem;
  margin: 0.5rem;
  cursor: pointer;
}

.split {
  padding: 1rem;
}
</style>
