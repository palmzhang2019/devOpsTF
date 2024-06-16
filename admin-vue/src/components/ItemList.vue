<template>
    <div>
        <el-table :data="items" style="width: 100%">
            <el-table-column prop="id" label="ID" width="50"></el-table-column>
            <el-table-column prop="name" label="Name"></el-table-column>
            <el-table-column prop="age" label="Age" width="100"></el-table-column>
        </el-table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'ItemList',
    data() {
        return {
            forgejoUsers: null,
            trelloUsers: null
        };
    },
    mounted() {
        this.fetchForgejo();
        this.fetchTrello();
    },
    methods: {
        fetchForgejo() {
            const token = process.env.VUE_APP_FORGEJO_TOKEN;
            axios.get('/forgejo/v1/orgs/devPalmOps/members', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => {
                    this.forgejoUsers = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        },
        fetchTrello() {
            const boardId = process.env.VUE_APP_BOARD_ID;
            const TRELLO_KEY = process.env.VUE_APP_TRELLO_KEY;
            const TRELLO_TOKEN = process.env.VUE_APP_TRELLO_TOKEN;
            axios.get(`/trello/boards/${boardId}/members?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}`)
                .then(response => {
                    this.trelloUsers = response.data;
                })
                .catch(error => {
                    console.error(error);
            });
        }
    },
};
</script>

<style scoped>
/* 添加一些样式以使表格看起来更好 */
</style>