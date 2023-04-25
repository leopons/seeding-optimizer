import { defineStore } from "pinia";

export const usePlayersStore = defineStore("players", {
  state: () => ({
    players: [],
    groups: {},
  }),
  actions: {
    initPlayersAndGroups(players, groups) {
      this.players = players;
      this.groups = groups;
    },
    addGroup(groupName) {
      this.groups[groupName] = [];
    },
    removeGroup(groupName) {
      delete this.groups[groupName];
    },
    addPlayerToGroup(playerIndex, groupName) {
      this.groups[groupName].push(playerIndex);
    },
    removePlayerFromGroup(playerIndex, groupName) {
      const playerIndexInGroup = this.groups[groupName].indexOf(playerIndex);
      if (playerIndexInGroup !== -1) {
        this.groups[groupName].splice(playerIndexInGroup, 1);
      }
      if (this.groups[groupName].length === 0) {
        delete this.groups[groupName];
      }
    },
  },
  getters: {
    getPlayers: (state) => {
      return state.players;
    },
    getPlayerByIndex: (state) => (index) => {
      return state.players[index];
    },
    getTotalNumberPlayers: (state) => {
      return state.players.length;
    },
    getGroups: (state) => {
      return state.groups;
    },
  },
});
