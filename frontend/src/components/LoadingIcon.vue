<template>
  <div :style="containerStyle">
    <div :style="outerStyle"></div>
    <div :style="innerStyle"></div>
  </div>
</template>

<script>
export default {
  name: "LoadingIcon",
  props: {
    size: Number,
  },
  computed: {
    margin() {
      if (this.size < 30) {
        return 1;
      } else {
        return 2;
      }
    },
    border() {
      if (this.size < 30) {
        return Math.ceil(this.size / 7);
      } else {
        return 5;
      }
    },
    innerSize() {
      return this.size - 2 * (this.border + this.margin);
    },
    innerTop() {
      return this.border + this.margin - this.size;
    },
    innerLeft() {
      return this.border + this.margin;
    },
    containerStyle() {
      var that = this;
      return `
        width: ${that.size + "px"};
        height: ${that.size + "px"};
      `;
    },
    outerStyle() {
      var that = this;
      return `
        box-sizing: border-box;
        height: ${that.size + "px"};
        width: ${that.size + "px"};
        border: ${that.border + "px"} solid red;
        border-radius: 50%;
        border-color: #2c3e50 transparent #2c3e50 transparent;
        animation: rotateIndirect 1.2s linear infinite;
      `;
    },
    innerStyle() {
      var that = this;
      return `
        box-sizing: border-box;
        height: ${that.innerSize + "px"};
        width: ${that.innerSize + "px"};
        border: ${that.border + "px"} solid red;
        border-radius: 50%;
        border-color: #2c3e50 transparent #2c3e50 transparent;
        position: relative;
        top: ${that.innerTop + "px"};
        left: ${that.innerLeft + "px"};
        animation: rotateDirect 1.2s linear infinite;
      `;
    },
  },
};
</script>

<style lang="scss">
@keyframes rotateIndirect {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes rotateDirect {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}
</style>
