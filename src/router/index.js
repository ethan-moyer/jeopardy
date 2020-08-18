import Vue from 'vue'
import VueRouter from 'vue-router'
import Player from "../views/Player.vue"
import Host from "../views/Host.vue"
import About from "../views/About.vue"

Vue.use(VueRouter)

  const routes = [
  {
    path: "/",
    name: "Player",
    component: Player
  },
  {
    path: "/host",
    name: "Host",
    component: Host
  },
  {
    path: "/about",
    name: "About",
    component: About
  }
]

const router = new VueRouter({
  mode: "history",
  routes
})

export default router
