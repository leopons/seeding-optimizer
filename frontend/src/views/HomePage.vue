<template>
  <div class="page-container">
    <div class="column-container">
      <div class="title">
        Automatically minimize collides on your start.gg bracket!
      </div>
      <div class="subtitle">
        This currently supports Double Elimination brackets from 8 to 64
        players.
      </div>
      <div v-if="errorNumberPlayers" class="error">
        Error: You gave a file with {{ errorNumberPlayers }} players.
      </div>
      <div v-if="unexpectedError" class="error">
        Unexpected Error: Please ensure the file is valid.
      </div>
      <CsvLoader
        class="csv-uploader"
        :handleData="handleData"
        text="Drag and drop your start.gg seeding here, or click to select a file."
      />
    </div>
  </div>
</template>

<script>
import CsvLoader from "@/components/CsvLoader.vue";
import { usePlayersStore } from "@/store/playersStore";

export default {
  setup() {
    const store = usePlayersStore();
    return { store };
  },
  data() {
    return {
      errorNumberPlayers: null,
      unexpectedError: false,
    };
  },
  components: { CsvLoader },
  methods: {
    handleData(data) {
      try {
        this.errorNumberPlayers = null;
        this.unexpectedError = false;
        if (!('"Pool Seed"' in data[0])) {
          this.unexpectedError = true;
          return;
        }
        // Should be already sorted but just to be sure
        data.sort((a, b) => a['"Pool Seed"'] - b['"Pool Seed"']);
        let players = data.map((el) => el['"Entrant"']);
        if (players.length < 8 || players.length > 64) {
          this.errorNumberPlayers = players.length;
          return;
        }
        let groups = {};
        players.forEach((str, index) => {
          let pipeIndex = str.indexOf("|");
          // If the '|' character is found, extract the tag
          let tag = null;
          if (pipeIndex !== -1) {
            tag = str.substr(0, pipeIndex).trim();
          }
          if (tag) {
            if (tag in groups) {
              groups[tag].push(index);
            } else {
              groups[tag] = [index];
            }
          }
        });
        // Remove singleton groups
        for (let key in groups) {
          if (groups[key].length == 1) {
            delete groups[key];
          }
        }
        this.store.initPlayersAndGroups(players, groups);
        this.$router.push("/groups");
      } catch {
        this.unexpectedError = true;
      }
    },
  },
};
</script>

<style scoped lang="scss">
.page-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
}
.column-container {
  width: 400px;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
}
.title {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}
.subtitle {
  font-style: italic;
  margin-bottom: 10px;
}
.error {
  font-style: italic;
  margin-bottom: 10px;
  color: orange;
}
.csv-uploader {
  height: 200px;
  border-radius: 20px;
}
</style>
