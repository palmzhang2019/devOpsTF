<template>
  <div class="home">
    <h1>Welcome to Home Page</h1>
    <UserList />
  </div>
</template>

<script>
import UserList from '../components/UserList'


export default {
  name: 'HomePage',
  components: {
    UserList,
  },
}
</script>

<style scoped>
.home {
  text-align: center;
}
</style>
