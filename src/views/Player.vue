<template>
    <div class="player">
        <div class="container">
            <div class="category" v-for="c in categories" :key="c">
                <span class="category-text">
                    {{ c }}
                </span>
            </div>
            <div class="question" v-for="(q, i) in questions" :key="q">
                <span class="question-text" v-if="q !== false && i < 6">
                    ${{ 200 }}
                </span>
                <span class="question-text" v-if="q !== false && i > 5 && i < 12">
                    ${{ 400 }}
                </span>
                <span class="question-text" v-if="q !== false && i > 11 && i < 18">
                    ${{ 600 }}
                </span>
                <span class="question-text" v-if="q !== false && i > 17 && i < 21">
                    ${{ 800 }}
                </span>
                <span class="question-text" v-if="q !== false && i > 20">
                    ${{ 1000 }}
                </span>
            </div>
        </div>

        <div class="modal">
            <h1 class="modal-text">{{ currentQuestion }}</h1>
        </div>
    </div>
</template>

<script>

export default {
    name: "Player",
    components: {
    },
    data() {
        return {
            isConnected: false,
            categories: ["C0", "C0", "C0", "C0", "C0", "C0"],
            questions: ["1"],
            currentQuestion: ""
        }
    },
    sockets: {
        connect() {
            this.isConnected = true;
            this.$socket.client.emit("get_data");
        },
        receive_data(gameData) {
            if (Object.keys(gameData).length === 0 && gameData.constructor === Object) {
                return;
            } else {
                this.categories = gameData.categories;
                this.questions = gameData.questions;
            }
        },
        open_question(question) {
            this.currentQuestion = question;
            let modal = document.getElementsByClassName("modal");
            modal[0].style.display = "block";
        },
        close_question() {
            let modal = document.getElementsByClassName("modal");
            modal[0].style.display = "none";
        }
    }
}
//background: #100373;
</script>

<style scoped>
    @import url("https://fonts.googleapis.com/css2?family=Teko:wght@600&display=swap");
    @import url("https://fonts.googleapis.com/css2?family=Noto+Serif&display=swap");

    .container {
        display: grid;
        height: 100vh;
        grid-template-rows: repeat(6, 1fr);
        grid-template-columns: repeat(6, 1fr);
        background: #170a7f;
    }

    .category {
        display: flex;
        justify-content: center;
        align-items: center;

        border: 1px solid black;
    }
    
    .category-text {
        font-family: "Teko", sans-serif;
        font-size: 30px;
        color: #ffffff;
    }

    .question {
        display: flex;
        justify-content: center;
        align-items: center;

        border: 1px solid black;
    }

    .question-text {
        font-family: "Teko", sans-serif;
        font-size: 45px;
        color: #ca983f;
    }

    .modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: #170a7f;
    }

    .modal-text {
        text-align: center;
        padding-top: 12.5%;
        font-family: 'Noto Serif', serif;
        font-size: 80px;
        color: white;
    }
</style>