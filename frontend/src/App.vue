<template>
  <div id="app">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
      <span class="navbar-brand">
        <img id="gsreg-logotype" src="@/assets/img/gsreg_logotype_white.png" alt="GSReg" />
      </span>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a href="https://github.com/ParallelGSReg/GSReg.jl" class="nav-link" target="_blank" >About GSReg</a>
          </li>
        </ul>
        <div class="mt-2 mt-md-0">
          <a href="https://julialang.org/" title="The Julia Language" target="_blank" ><img id="julia-logotype" src="@/assets/img/julia_logotype_white.png" alt="Julia" /></a>
        </div>
      </div>
    </nav>
    <main role="main">
      <div class="container">
        <header>
          <h1>Global Search Regression GUI</h1>
        </header>
      </div>
    </main>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      progress: 0
    }
  },
  mounted () {
  },
  computed: {},
  methods: {},
  created () {}
}
</script>

<style lang="scss">
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 800px,
  xl: 810px
);
@import "../node_modules/bootstrap/scss/bootstrap.scss";
@import "../node_modules/bootstrap-vue/dist/bootstrap-vue.css";
@import "../node_modules/bootstrap-vue/dist/bootstrap-vue.css";
@import "../node_modules/vue-material/dist/vue-material.min.css";

@font-face {
  font-family: "Lato Black";
  src: url("./assets/fonts/lato/lato-black.ttf") format("truetype");
}
@font-face {
  font-family: "Lato Regular";
  src: url("./assets/fonts/lato/lato-regular.ttf") format("truetype");
}
@font-face {
  font-family: "Lato Light";
  src: url("./assets/fonts/lato/lato-light.ttf") format("truetype");
}
@font-face {
  font-family: "Roboto Regular";
  src: url("./assets/fonts/roboto/Roboto-Regular.ttf") format("truetype");
}
@font-face {
  font-family: "Tamil MN Bold";
  src: url("./assets/fonts/tamilmn/TamilMN-Bold.ttf") format("truetype");
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding-bottom: 20px;
}

nav.navbar {
  line-height: 0.5;
  font-size: 14px;
}

nav.navbar .navbar-brand {
  line-height: 0.5;
  font-size: 14px;
}

nav.navbar #gsreg-logotype,
nav.navbar #julia-logotype {
  height: 32px;
}

.bg-julia {
  background-color: #5b38da !important;
}

h1 {
  font-size: 24px;
  font-family: "Lato Regular";
  text-align: center;
}

.md-button.md-theme-default.md-raised:not([disabled]) {
  color: #666666;
  background: #e9ecef;
}

@include media-breakpoint-down(sm) {
  #main {
    padding-top: 10px;
  }

  #gsreg-logotype {
    width: 200px;
  }

  #julia-logotype {
    width: 83px;
  }
}


</style>
