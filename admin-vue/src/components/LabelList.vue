<template>
    <div>
        <div id="forgejoUsers" style="float: left; width: 50%;">
            <h2>Forgejo Labels</h2>
            <div v-for="label in forgejoLabels" :key="label.id" class="label"
                 :id="'forgejo-' + label.username"
                 :style="{ backgroundColor: getUserBgColor('forgejo', label.id) }"
                 @click="selectUser('forgejo', label.id)">
                {{ label.name }}
            </div>
        </div>
        <div id="trelloUsers" style="float: right; width: 50%;">
            <h2>Trello Labels</h2>
            <div v-for="label in trelloLabels" :key="label.id" class="label"
                 :id="'trello-' + label.username"
                 :style="{ backgroundColor: getUserBgColor('trello', label.id) }"
                 @click="selectUser('trello', label.id)">
                {{ label.name }}
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
            forgejoLabels: null,
            trelloLabels: null,
            selectedForgejoUserId: null,
            selectedTrelloUserId: null,
            matchedPairs: [],
            selectedUser: null, 
            colors: ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow', 'lightsalmon', 'lightgrey', 'lightcyan', 'lightpink', 'wheat', 'lavender']
        };
    },
    mounted() {
        this.fetchForgejoLabels();
        this.fetchTrelloLabels();
    },
    methods: {
        fetchForgejoLabels() {
            const owner = process.env.VUE_APP_OWNER;
            const token = process.env.VUE_APP_FORGEJO_TOKEN;
            axios.get(`/forgejo/v1/orgs/${owner}/labels`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => {
                    this.forgejoLabels = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        },
        fetchTrelloLabels() {
            const boardId = process.env.VUE_APP_BOARD_ID;
            const TRELLO_KEY = process.env.VUE_APP_TRELLO_KEY;
            const TRELLO_TOKEN = process.env.VUE_APP_TRELLO_TOKEN;
            axios.get(`/trello/boards/${boardId}/labels?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}`)
                .then(response => {
                    this.trelloLabels = response.data;
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
.label {
    height: 36px;
    line-height: 36px;
    border-radius: 0.4rem;
    border: 1px solid #ccc;
    margin: 10px;
    cursor: pointer;
}
</style>