<template>
  <div id="app">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
      <span class="navbar-brand"><img id="gsreg-logotype" src="@/assets/img/gsreg_icon.svg" alt="GSReg"/></span>
      <span class="navbar-brand"><h1>Global Search Regression</h1></span>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a href="https://github.com/ParallelGSReg/GSReg.jl" class="nav-link" target="_blank">About GSReg</a>
          </li>
        </ul>
        <div class="mt-2 mt-md-0">
          <a href="https://julialang.org/" title="The Julia Language" target="_blank">
            <img id="julia-logotype" src="@/assets/img/julia_logotype_white.png" alt="Julia"/></a>
        </div>
      </div>
    </nav>
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
    created () {
      this.$http.get(this.$constants.API.host + this.$constants.API.paths.server_info).then(response => {
        this.$store.commit('setServerNworkers', response.body.nworkers)
        this.$store.commit('setServerNcores', response.body.ncores)
        this.$store.commit('setServerJuliaVersion', response.body.julia_version)
        this.$store.commit('setServerGsregVersion', response.body.gsreg_version)
        this.$store.commit('setServerJobQueueLength', response.body.job_queue.length)
      })
    }
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
  }
</style>
