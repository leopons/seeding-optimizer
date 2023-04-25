<template>
  <div class="header-bar">
    <div class="header-bar__left">
      <router-link class="header-bar__link" to="/">Restart</router-link>
      <a
        class="header-bar__link"
        href="https://twitter.com/UnCalinSSB"
        target="_blank"
        >Contact</a
      >
    </div>
    <div class="header-bar__right">Beta</div>
  </div>
  <div class="app-container">
    <router-view />
  </div>
  <div class="no-responsive">Please get on a wider screen to use this app.</div>
</template>

<style lang="scss">
body {
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: grey;
  margin: 0;
}

.header-bar {
  height: 30px;
  background-color: black;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  padding: 0 10px;
}

.header-bar__left {
  display: flex;
  align-items: center;
}

a.header-bar__link {
  margin-right: 10px;
  text-transform: uppercase;
  font-weight: bold;
  cursor: pointer;
  color: white;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.header-bar__right {
  font-style: italic;
}

.app-container {
  height: calc(100vh - 30px);
}

.no-responsive {
  position: absolute;
  width: 100vw;
  height: 100vh;
  background-color: white;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
  box-sizing: border-box;
}

@media (min-width: 920px) {
  .no-responsive {
    display: none;
  }
}
</style>
