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
          <el-card class="role-card" shadow="hover" @dragover="onDragOver" @drop="onDrop($event, role, 'role')">
            <p>{{ role.title }}</p>
            <div v-if="role.users && role.users.length">
              <div v-for="(user, userIndex) in role.users" :key="userIndex" class="user-card" draggable="true" @dragstart="onDragStart($event, user, role.title)">
                <span>{{ user.fullName }}</span>
                <span class="split">|</span>
                <span>{{ user.username }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row :gutter="20" class="user-row" @dragover="onDragOver" @drop="onDrop($event, null, 'user')">
        <el-col v-for="(user, index) in trelloUsers" :key="index" :span="6" class="user-col">
          <div class="user-card" shadow="hover" draggable="true" @dragstart="onDragStart($event, user, 'user')">
            <span>{{ user.fullName }}</span>
            <span class="split">|</span>
            <span>{{ user.username }}</span>
          </div>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-button type="primary" @click="getRolesWithUsers">Get Roles and Users</el-button>
    </el-main>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'RoleManager',
  setup() {
    const trelloUsers = ref([]);
    const roleUsers = ref(null);
    const form = ref({
      name: '',
    });

    const roles = ref([]);

    const addRole = () => {
      if (form.value.name.trim()) {
        roles.value.push({ title: form.value.name, users: [] });
        form.value.name = '';
      }
    };

    const fetchTrelloUsers = () => {
      const boardId = process.env.VUE_APP_BOARD_ID;
      const TRELLO_KEY = process.env.VUE_APP_TRELLO_KEY;
      const TRELLO_TOKEN = process.env.VUE_APP_TRELLO_TOKEN;
      return axios.get(`/trello/boards/${boardId}/members?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}`)
        .then(response => {
          trelloUsers.value = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    };

    const fetchRolesUsers = () => {
      axios.get(`/local/role-users`)
        .then(response => {
          roleUsers.value = response.data;
          initializeRolesAndUsers();
        })
        .catch(error => {
          console.error(error);
        });
    };

    const initializeRolesAndUsers = () => {
      const roleMap = {};
      const usersSet = new Set();

      roleUsers.value.forEach(roleUser => {
        const { title, users } = roleUser;
        roleMap[title] = users.map(user => {
          usersSet.add(user.username);
          return user;
        });
      });

      roles.value = Object.keys(roleMap).map(roleTitle => ({
        title: roleTitle,
        users: roleMap[roleTitle]
      }));

      const allUsers = trelloUsers.value.filter(user => !usersSet.has(user.username));
      trelloUsers.value = allUsers;
    };

    const onDragStart = (event, user, source) => {
      event.dataTransfer.setData('user', JSON.stringify(user));
      event.dataTransfer.setData('source', source);
      event.dataTransfer.effectAllowed = 'move';
    };

    const onDragOver = (event) => {
      event.preventDefault();
    };

    const onDrop = (event, targetRole, targetType) => {
      event.preventDefault();
      const userData = event.dataTransfer.getData('user');
      const source = event.dataTransfer.getData('source');
      if (userData) {
        const user = JSON.parse(userData);

        // 移除用户从原来的位置
        if (source === 'user') {
          trelloUsers.value = trelloUsers.value.filter(u => u.username !== user.username);
        } else {
          const sourceRole = roles.value.find(role => role.title === source);
          if (sourceRole) {
            sourceRole.users = sourceRole.users.filter(u => u.username !== user.username);
          }
        }

        // 添加用户到新的位置
        if (targetType === 'role') {
          if (!targetRole.users.find(u => u.username === user.username)) {
            targetRole.users.push(user);
          }
        } else if (targetType === 'user') {
          if (!trelloUsers.value.find(u => u.username === user.username)) {
            trelloUsers.value.push(user);
          }
        }
      }
    };

    const getRolesWithUsers = async () => {
      const rolesWithUsers = roles.value.map(role => ({
        title: role.title,
        users: role.users.map(user => ({ id: user.id, fullName: user.fullName, username: user.username }))
      }));
      try {
        const response = await axios.post('/local/role-users', rolesWithUsers);
        console.log(response.data);
        // Handle the response as needed
      } catch (error) {
        console.error('Error updating roles and users:', error);
        // Handle the error as needed
      }
    };

    onMounted(() => {
      fetchTrelloUsers().then(fetchRolesUsers);
    });

    return {
      form,
      roles,
      addRole,
      trelloUsers,
      onDragStart,
      onDragOver,
      onDrop,
      getRolesWithUsers,
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
  text-align: center;
  padding: 20px;
  border-radius: 10px;
}

.user-row {
  margin-top: 20px;
}

.user-col {
  display: flex;
  justify-content: center;
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
