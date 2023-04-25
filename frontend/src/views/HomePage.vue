<template>
  <div class="page-container">
    <div class="column-container">
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
  components: { CsvLoader },
  methods: {
    handleData(data) {
      // Should be already sorted but just to be sure
      data.sort((a, b) => a['"Pool Seed"'] - b['"Pool Seed"']);
      let players = data.map((el) => el['"Entrant"']);
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
    },
  },
};
</script>

<style scoped lang="scss">
.page-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100vh;
}
.column-container {
  width: 400px;
  height: 300px;
  background-color: white;
  border-radius: 20px;
}
.csv-uploader {
  margin: 20px;
  height: calc(100% - 40px);
  border-radius: 20px;
}
</style>
