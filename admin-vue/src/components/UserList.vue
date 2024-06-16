<template>
    <div>
        <div id="forgejoUsers" style="float: left; width: 50%;">
            <h2>Forgejo Users</h2>
            <div v-for="user in forgejoUsers" :key="user.id" class="user"
                 :id="'forgejo-' + user.username"
                 :style="{ backgroundColor: getUserBgColor('forgejo', user.id) }"
                 @click="selectUser('forgejo', user.id)">
                {{ user.username }} ({{ user.email }})
            </div>
        </div>
        <div id="trelloUsers" style="float: right; width: 50%;">
            <h2>Trello Users</h2>
            <div v-for="user in trelloUsers" :key="user.id" class="user"
                 :id="'trello-' + user.username"
                 :style="{ backgroundColor: getUserBgColor('trello', user.id) }"
                 @click="selectUser('trello', user.id)">
                {{ user.username }} ({{ user.fullName }})
            </div>
        </div>
        <div style="clear: both;"></div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserList',
    data() {
        return {
            forgejoUsers: null,
            trelloUsers: null,
            selectedForgejoUserId: null,
            selectedTrelloUserId: null,
            matchedPairs: [],
            selectedUser: null,  // Stores the currently selected user details
            colors: ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow', 'lightsalmon', 'lightgrey', 'lightcyan', 'lightpink', 'wheat', 'lavender']
        };
    },
    mounted() {
        this.fetchForgejoUsers();
        this.fetchTrelloUsers();
    },
    methods: {
        fetchForgejoUsers() {
            const owner = process.env.VUE_APP_OWNER;
            const token = process.env.VUE_APP_FORGEJO_TOKEN;
            axios.get(`/forgejo/v1/orgs/${owner}/members`, {
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
        fetchTrelloUsers() {
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
        },
        selectUser(type, userId) {
            if (type === 'forgejo') {
                if (this.matchedPairs.some(pair => pair.forgejo === userId)) {
                    this.removeMatch(userId);
                } else {
                    this.selectedForgejoUserId = userId;
                    this.checkForMatch();
                }
            } else {
                if (this.matchedPairs.some(pair => pair.trello === userId)) {
                    this.removeMatch(userId);
                } else {
                    this.selectedTrelloUserId = userId;
                    this.checkForMatch();
                }
            }
        },
        checkForMatch() {
            if (this.selectedForgejoUserId && this.selectedTrelloUserId) {
                this.matchedPairs.push({
                    forgejo: this.selectedForgejoUserId,
                    trello: this.selectedTrelloUserId
                });
                this.selectedForgejoUserId = null;
                this.selectedTrelloUserId = null;
            }
        },
        getUserBgColor(type, userId) {
            const index = this.matchedPairs.findIndex(pair => pair[type] === userId);
            if (index !== -1) {
                return this.colors[index % this.colors.length];  // Cycle through the colors array
            } 
            return '';  // Default, no color
        },
        removeMatch(userId) {
            this.matchedPairs = this.matchedPairs.filter(pair => pair.forgejo !== userId && pair.trello !== userId);
        }
    },
};
</script>

<style scoped>
.user {
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    border-radius: 0.4rem;
    border: 1px solid #ccc;
    margin: 10px;
    cursor: pointer;
}
</style>