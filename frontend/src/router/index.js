import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import GroupsPage from "../views/GroupsPage.vue";
import ResultsPage from "../views/ResultsPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/groups",
    name: "groups",
    component: GroupsPage,
  },
  {
    path: "/results",
    name: "results",
    component: ResultsPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
