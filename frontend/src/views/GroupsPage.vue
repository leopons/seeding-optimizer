<template>
  <div class="page-container">
    <div class="column-container">
      <h2>Players</h2>
      <div class="list-scroll">
        <div
          class="player"
          v-for="(player, playerIndex) in players"
          :key="playerIndex"
        >
          <b>{{ player }}</b>
          <div class="player-groups">
            <div
              class="player-groups__group"
              :style="
                isPlayerInGroup(playerIndex, groupName)
                  ? {
                      backgroundColor: '#2c3e50',
                      fontWeight: 'bold',
                      color: 'white',
                    }
                  : {}
              "
              v-for="groupName in allGroupsNames"
              @click="togglePlayerInGroup(playerIndex, groupName)"
              :key="groupName"
            >
              {{ groupName }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column-container">
      <h2>Groups</h2>
      <div class="list-scroll">
        <div
          class="group"
          v-for="(group, groupName) in groups"
          :key="groupName"
        >
          <div class="group__name">{{ groupName }}</div>
          <div>
            <div
              class="group__player"
              v-for="playerIndex in group"
              :key="playerIndex"
            >
              <span>{{ getPlayerByIndex(playerIndex) }}</span>
              <i
                @click="removePlayerFromGroup(playerIndex, groupName)"
                class="material-icons"
                >close</i
              >
            </div>
          </div>
        </div>
        <div class="add-group-form">
          <input type="text" v-model="newGroupName" />
          <button @click="addGroup">Create New Group</button>
        </div>
      </div>
    </div>
    <button class="cta" @click="$router.push('/results')">Go !</button>
  </div>
</template>

<script>
import { usePlayersStore } from "@/store/playersStore";

export default {
  setup() {
    const store = usePlayersStore();
    return { store };
  },
  data() {
    return {
      newGroupName: "",
    };
  },
  mounted() {
    if (this.store.getTotalNumberPlayers == 0) {
      this.$router.push("/");
    }
  },
  computed: {
    players() {
      return this.store.getPlayers;
    },
    groups() {
      return this.store.getGroups;
    },
    allGroupsNames() {
      return Object.keys(this.groups);
    },
    colors() {
      return ["red"];
    },
  },
  methods: {
    getPlayerByIndex(playerIndex) {
      return this.players[playerIndex];
    },
    isPlayerInGroup(playerIndex, groupName) {
      return this.groups[groupName].includes(playerIndex);
    },
    addPlayerToGroup(playerIndex, groupName) {
      this.store.addPlayerToGroup(playerIndex, groupName);
    },
    removePlayerFromGroup(playerIndex, groupName) {
      this.store.removePlayerFromGroup(playerIndex, groupName);
    },
    togglePlayerInGroup(playerIndex, groupName) {
      if (this.isPlayerInGroup(playerIndex, groupName)) {
        this.removePlayerFromGroup(playerIndex, groupName);
      } else {
        this.addPlayerToGroup(playerIndex, groupName);
      }
    },
    addGroup() {
      const groupName = this.newGroupName.trim();
      if (groupName !== "") {
        this.store.addGroup(groupName);
        this.newGroupName = "";
      }
    },
  },
};
</script>

<style scoped lang="scss">
.page-container {
  display: flex;
  justify-content: space-around;
  height: 100%;
}
.column-container {
  width: 48%;
  height: calc(100% - 40px);
  box-sizing: border-box;
  margin-top: 20px;
  padding: 20px;
  background-color: white;
  border-radius: 20px;

  h2 {
    margin-top: 0;
  }

  .nothing-selected {
    opacity: 0.8;
    font-style: italic;
    margin-top: calc(50vh - 50px);
  }
}

.list-scroll {
  overflow-y: scroll;
  height: calc(100% - 50px);

  &::-webkit-scrollbar {
    display: none;
  }
}

.player {
  margin: 6px 0;
  background-color: rgba(black, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 6px;
  border-radius: 4px;

  .player-groups {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 5px;

    .player-groups__group {
      background-color: rgba(black, 0.05);
      padding: 3px 7px;
      border-radius: 100px;
      margin: 0 2px;
      cursor: pointer;
    }
  }
}

.group {
  margin-bottom: 10px;
  .group__name {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 4px;
  }
  .group__player {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2px;

    .material-icons {
      font-size: 20px;
      margin-left: 3px;
      opacity: 0.3;
      cursor: pointer;

      &:hover {
        opacity: 1;
      }
    }
  }
}

.cta {
  background-color: #209f4a;
  border: none;
  color: white;
  box-shadow: #000000a1 4px 6px 16px;
  position: absolute;
  bottom: 35px;
  right: 35px;
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  height: 95px;
  width: 95px;
  border-radius: 100px;
  font-size: 1.2em;
  font-weight: bold;
  cursor: pointer;
}
</style>
