<template>
    <div class="host">
        <div class="header">
            <h1>Host</h1>
            <p v-if="isConnected">Connected to server.</p>
        </div>

        <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="J-Archive ID" v-model="gameId">
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="button" v-on:click="startGame()">Start Game</button>
            </div>
        </div>

        <table class="table table-bordered w-25" id="scores">
            <thead>
                <tr>
                    <th colspan="3" style="text-align:center">Scores</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>P1: {{ scores[0] }}</td>
                    <td>P2: {{ scores[1] }}</td>
                    <td>P3: {{ scores[2] }}</td>
                </tr>   
            </tbody> 
        </table>
        <hr/>

        <table class="table table-bordered" id="game-board">
            <thead>
                <tr>
                    <th v-for="category in gameCategories" :key="category" id="game-cell">{{ category }}</th>
                </tr>
            </thead>
            <tbody v-if="gameQuestions.length !== 1">
                <tr v-for="(row, indexR) in gameQuestions" :key="row">
                    <td v-for="(col, indexC) in row" :key="col" id="game-cell">
                        <a v-if="col !== null" href="#" v-on:click="showQuestion(indexR, indexC)" data-toggle="modal" data-target="#questionModal">{{ 1000*(indexR+1)/5 }}</a>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="modal fade" id="questionModal" tabindex="-1" role="dialog" data-backdrop="true" v-if="gameQuestions.length !== 1">
            <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="questionModalTitle">Question for ${{ 1000*(pos.row+1)/5 }}</h3>
                    </div>
                    <div class="modal-body">
                        <h4>{{ gameQuestions[pos.row][pos.col] }}</h4>
                        <br/>
                        <p style="color: red">{{ gameAnswers[pos.row][pos.col] }}</p>
                    </div>
                    <div class="modal-footer">
                        <select class="custom-select" v-model="selectedPlayer">
                            <option selected>Player</option>
                            <option value="0">One</option>
                            <option value="1">Two</option>
                            <option value="2">Three</option>
                            <option value="-1">Nobody</option>
                        </select>
                        <button type="button" class="btn btn-success" v-on:click="correct()" data-dismiss="modal">Correct</button>
                        <button type="button" class="btn btn-danger" v-on:click="incorrect()">Incorrect</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import "bootstrap"

export default {
    name: "Host",
    data() {
        return {
            isConnected: false,
            gameId: "",
            scores: [0, 0, 0],
            gameCategories: Array,
            gameQuestions: [[]],
            gameAnswers: [[]],
            pos: { row: 0, col: 0 },
            selectedPlayer: String
        }
    },
    methods: {
        startGame() {
            this.$socket.client.emit("load_data", this.gameId, 1);
        },
        showQuestion(row, col) {
            this.pos.row = row;
            this.pos.col = col;
            this.$socket.client.emit("open_question", row, col);
        },
        correct() {
            if (this.selectedPlayer && this.selectedPlayer !== "-1") {
                let points = 1000 * (this.pos.row + 1) / 5;
                this.$socket.client.emit("change_score", this.selectedPlayer, points);
            } else if (this.selectedPlayer === "-1") {
                this.$socket.client.emit("change_score", 0, 0);
            }
            this.$socket.client.emit("remove_question", this.pos.row, this.pos.col);
        },
        incorrect() {
            if (this.selectedPlayer) {
                let points = 1000 * (this.pos.row + 1) / 5;
                this.$socket.client.emit("change_score", this.selectedPlayer, -points);
            }
        }
    },
    sockets: {
        connect() {
            this.isConnected = true;
            //this.$socket.client.emit("get_data_host");
        },
        receive_data_host(gameData, scores) {
            this.scores = scores;
            this.gameCategories = gameData.categories;
            this.gameQuestions = gameData.questions;
            this.gameAnswers = gameData.answers;
        }
    }
}
</script>

<style lang="scss" scoped>
    @import "../../node_modules/bootstrap/scss/bootstrap.scss";

    .host {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        
        flex-grow: 1;
        height: 100%;
    }

    .header {
        background: mediumseagreen;
        text-align: center;
    }
    
    .input-group {
        padding-left: 50px;
        padding-right: 50px;
    }

    #scores {
        margin: auto;
        table-layout: fixed; 
    }
    
    #game-board {
        flex-grow: 1;
        table-layout: fixed;
        padding-left: 50px;
        padding-right: 50px;
        height: 100%;
    }

    #game-cell {
        height: 100px;
    }
</style>