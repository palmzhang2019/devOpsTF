<template>
  <div class="home">
    <h1>Welcome to Home Page</h1>
    <ItemList />
  </div>
</template>

<script>
import ItemList from '../components/ItemList'


export default {
  name: 'HomePage',
  components: {
    ItemList,
  },
}
</script>

<style scoped>
.home {
  text-align: center;
}
</style>
