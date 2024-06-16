import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/HomePage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  }
  // 其他路由配置
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;