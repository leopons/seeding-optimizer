<template>
  <div class="page-container">
    <div class="column-container">
      <h2>Alternatives</h2>
      <div class="list-scroll">
        <div
          :class="
            'alternative' +
            (alternative.loading ? ' --loading' : '') +
            (alternative.error ? ' --error' : '')
          "
          v-for="(alternative, power) in alternatives"
          :key="power"
          @click="selectAlternative(power)"
        >
          <div v-if="alternative.loading"><LoadingIcon :size="40" /></div>
          <div v-else-if="alternative.error">
            <span class="alternative__error">Unexpected Error</span><br />
            <span
              class="alternative__try-again"
              @click="getCollides(Number(power))"
              >Try again</span
            >
          </div>
          <div v-else>
            <div>
              <b v-if="power == 0">Original Seeding</b>
              <b v-else>Alternative #{{ power }}</b>
            </div>
            <div class="alternative__grade-scores">
              <i>Collides:</i>
              <div v-if="Object.keys(alternative.collide_stats).length !== 0">
                <span
                  v-for="(amount, grade) in alternative.collide_stats"
                  :key="grade"
                  :class="`alternative__grade-score --${grade}`"
                >
                  <b>{{ amount }}&nbsp;</b>{{ capitalize(grade)
                  }}<span>{{ " " }}</span>
                </span>
              </div>
              <div v-else>No possible collides.</div>
            </div>
            <div class="alternative__deviation-score" v-if="power != 0">
              Seeding deviation:
              <b>{{ Math.round(alternative.deviation_score / 10) }}%</b>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column-container">
      <h2>Players</h2>
      <div v-if="selected_alternative" class="list-scroll">
        <div
          v-for="(player, index) in alternative_data['players']"
          :key="index"
          :class="
            'player' +
            (player.seeding_difference > 0
              ? ' --positive'
              : player.seeding_difference < 0
              ? ' --negative'
              : '')
          "
        >
          <span>{{ player.new_seeding + 1 }}</span>
          <span>{{
            this.store.getPlayerByIndex(player.original_seeding)
          }}</span>
          <span
            v-if="player.seeding_difference != 0"
            :class="
              'seeding-difference' +
              (player.seeding_difference > 0 ? ' --positive' : ' --negative')
            "
            ><span v-if="player.seeding_difference > 0">+</span
            >{{ player.seeding_difference }}</span
          ><span v-else>&nbsp;</span>
        </div>
      </div>
      <div v-else class="nothing-selected">
        Please select a seeding alternative
      </div>
    </div>
    <div class="column-container">
      <h2>Collides</h2>
      <div v-if="selected_alternative" class="list-scroll">
        <div
          v-for="(collide, index) in alternative_data['collides']"
          :key="index"
          :class="`collide --${collide.grade}`"
        >
          <div class="collide__recap">
            <div
              class="collide__group-tag"
              v-for="group in collide.groups"
              :key="group"
            >
              {{ group }}
            </div>
            <div>
              {{ Math.round(collide.prob * 100) }}% -
              <span class="collide__grade">{{
                capitalize(collide.grade)
              }}</span>
            </div>
          </div>
          <div class="collide__players">
            {{ getPlayerByAlternativeSeeding(collide.players[0]) }}
            <b><i>vs</i></b>
            {{ getPlayerByAlternativeSeeding(collide.players[1]) }}
          </div>
          <div class="collide__encounters">
            <div v-for="encounter in collide.encounters" :key="encounter.match">
              Match <b>{{ encounter.match }}</b> -
              {{ Math.round(encounter.prob * 100) }}%
            </div>
          </div>
        </div>
      </div>
      <div v-else class="nothing-selected">
        Please select a seeding alternative
      </div>
    </div>
  </div>
</template>

<script>
import LoadingIcon from "@/components/LoadingIcon.vue";
import { usePlayersStore } from "@/store/playersStore";

export default {
  setup() {
    const store = usePlayersStore();
    return { store };
  },
  components: { LoadingIcon },
  data() {
    return {
      alternatives: {},
      selected_alternative: null,
    };
  },
  mounted() {
    if (this.store.getTotalNumberPlayers == 0) {
      this.$router.push("/");
    } else {
      this.getCollides(0);
      this.getCollides(1);
      this.getCollides(2);
      this.getCollides(3);
    }
  },
  computed: {
    players() {
      return this.store.getPlayers;
    },
    groups() {
      return this.store.getGroups;
    },
    alternative_data() {
      return this.alternatives[this.selected_alternative];
    },
  },
  methods: {
    selectAlternative(power) {
      if (this.alternatives[power].players) {
        this.selected_alternative = power;
      }
    },
    capitalize(myString) {
      return myString.charAt(0).toUpperCase() + myString.slice(1);
    },
    getPlayerByAlternativeSeeding(seeding) {
      return this.store.getPlayerByIndex(
        this.alternative_data.players.find((p) => p.new_seeding == seeding)
          .original_seeding
      );
    },
    getCollides(power) {
      this.alternatives[power] = { loading: true, error: false };
      fetch(
        "https://europe-west1-smash-upset-distance.cloudfunctions.net/get-bracket-collides",
        {
          headers: {
            "Content-Type": "application/json;charset=UTF-8",
          },
          method: "POST",
          body: JSON.stringify({
            nb_players: this.store.getTotalNumberPlayers,
            groups: this.store.getGroups,
            minimization_power: power,
          }),
        }
      )
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            this.alternatives[power] = { loading: false, error: true };
          }
        })
        .then((json) => {
          const seeding = json["seeding_alternative"];
          // Players processing
          let players = [];
          if (seeding == null) {
            players = this.store.getPlayers.map((player, index) => {
              return {
                original_seeding: index,
                new_seeding: index,
                seeding_difference: 0,
              };
            });
          } else {
            for (let key in seeding) {
              players.push({
                original_seeding: key,
                new_seeding: seeding[key],
                seeding_difference: key - seeding[key],
              });
            }
          }
          players.sort((a, b) => a.new_seeding - b.new_seeding);
          // Collides processing
          const prob_mapping = [
            { threshold: 0.2, grade: "possible" },
            { threshold: 0.6, grade: "expected" },
            { threshold: 1, grade: "guaranteed" },
          ];
          let collides = json["collides"].map((collide) => {
            let grade = "unlikely";
            prob_mapping.forEach((el) => {
              if (collide.prob >= el.threshold) {
                grade = el.grade;
              }
            });
            let encounters = Object.keys(collide.encounters).map((match) => {
              return { match, prob: collide.encounters[match] };
            });
            console.log(encounters);
            encounters.sort((a, b) => b.prob - a.prob);
            return { ...collide, grade, encounters };
          });
          // Collides stats
          let collide_stats = {};
          collides.forEach((collide) => {
            if (collide.grade in collide_stats) {
              collide_stats[collide.grade] += 1;
            } else {
              collide_stats[collide.grade] = 1;
            }
          });
          // Return data
          this.alternatives[power] = {
            loading: false,
            error: false,
            ...json,
            players,
            collides,
            collide_stats,
          };
          if (this.selected_alternative == null && power == 0) {
            this.selected_alternative = 0;
          }
        })
        .catch(() => {
          this.alternatives[power] = { loading: false, error: true };
        });
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
  width: 30%;
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

.alternative {
  background-color: rgba(black, 0.05);
  border-radius: 20px;
  height: 150px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  &:not(.--loading, .--error) {
    cursor: pointer;
    &:hover {
      background-color: rgba(black, 0.1);
    }
  }

  .alternative__error {
    color: orange;
    font-style: italic;
  }

  .alternative__try-again {
    cursor: pointer;
    text-decoration: underline;
  }

  .alternative__grade-scores {
    margin-top: 10px;
  }

  .alternative__grade-score {
    margin: 0 7px;

    &.--guaranteed {
      color: red;
    }
    &.--expected {
      color: orange;
    }
    &.--possible {
      color: #e8d438;
    }
    &.--unlikely {
      opacity: 0.6;
    }
  }

  .alternative__deviation-score {
    margin-top: 7px;
  }
}

.player {
  margin: 6px 0;
  background-color: rgba(black, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px;
  border-radius: 4px;

  &.--positive {
    background-color: rgba(green, 0.05);
  }

  &.--negative {
    background-color: rgba(red, 0.05);
  }

  .seeding-difference {
    font-weight: bold;

    &.--positive {
      color: green;
    }

    &.--negative {
      color: red;
    }
  }
}

.collide {
  margin: 6px 0;
  background-color: rgba(black, 0.05);
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 6px;
  border-radius: 4px;

  .collide__recap {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .collide__group-tag {
    background-color: grey;
    color: white;
    font-weight: bold;
    border-radius: 100px;
    padding: 1px 6px;
    margin-right: 5px;
  }

  .collide__grade {
    font-weight: bold;
  }

  .collide__encounters {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 0.9em;
    opacity: 0.7;
  }

  .collide__players {
    margin: 6px 0;
  }

  &.--guaranteed {
    background-color: rgba(red, 0.05);
    .collide__grade {
      color: red;
    }
  }

  &.--expected {
    background-color: rgba(orange, 0.05);
    .collide__grade {
      color: orange;
    }
  }

  &.--possible {
    background-color: rgba(yellow, 0.05);
    .collide__grade {
      color: #e8d438;
    }
  }

  &.--unlikely {
    opacity: 0.6;
  }
}
</style>
