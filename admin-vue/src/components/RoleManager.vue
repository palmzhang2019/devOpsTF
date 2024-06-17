<template>
    <el-container>
      <el-header>
        <h1>Role Manager</h1>
      </el-header>
      <el-main>
        <el-card shadow="hover" class="box-card">
          <el-form :model="form" label-width="80px" @submit.prevent="addRole" class="form-container" inline>
            <el-form-item label="Role title" label-position="left" >
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
            <el-card class="role-card" shadow="hover">
              <p>{{ role.title }}</p>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'RoleManager',
    setup() {
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
  
      return {
        form,
        roles,
        addRole,
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
  </style>
  