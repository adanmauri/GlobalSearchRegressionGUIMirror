<template>
  <div id="app">
    <main role="main" class="role-main">
      <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
        <span class="navbar-brand"><img id="gsreg-logotype" src="@/assets/img/gsreg_icon.svg" alt="GSReg"/></span>
        <span class="navbar-brand"><h1>Global Search Regression</h1></span>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
          </ul>
          <div class="mt-2 mt-md-0">
            <a href="https://julialang.org/" title="The Julia Language" target="_blank">
              <img id="julia-logotype" src="@/assets/img/julia_logotype_white.png" alt="Julia"/></a>
          </div>
        </div>
      </nav>
      <router-view></router-view>
    </main>
    <footer class="footer text-muted">

      <div class="footer-links-container container-fluid">
        <ul class="footer-links">
          <li><a href="https://parallelgsreg.github.io/GSReg.jl/">About</a></li>
          <li><a href="https://github.com/ParallelGSReg/GSReg.jl">GitHub</a></li>
          <li><a href="https://julialang.org/">Julia</a></li>
        </ul>
        <p><b>Global Regression Search</b> is licensed under the <a href="https://github.com/ParallelGSReg/GSReg.jl/blob/master/LICENSE.md" target="_blank" rel="license noopener">MIT License</a>.</p>
      </div>

    </footer>
    <div class="server-status-container container-fluid">
      <ul class="server-status">
        <li><b>Server status:</b> <span v-if="server" class="online">Online</span><span v-else-if="server === false"
                                                                                        class="offline">Offline</span><span
          v-else class="offline">...</span></li>
        <li v-if="server"><b>Julia version:</b> <span>{{ server.julia_version }}</span></li>
        <li v-if="server"><b>GSReg version:</b> <span>{{ server.gsreg_ersion }}</span></li>
        <li v-if="server"><b>Number of cores:</b> <span>{{ server.ncores }}</span></li>
      </ul>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  export default {
    name: 'app',
    data () {
      return {
        progress: 0
      }
    },
    mounted () {
    },
    computed: {
      ...mapState(['server'])
    },
    methods: {},
    created () {
      this.$http.get(this.$constants.API.host + this.$constants.API.paths.server_info).then(response => {
        this.$store.commit('setServer', response.body)
      }).catch(() => {
        this.$store.commit('setServer', false)
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

  /* Sticky footer styles
  -------------------------------------------------- */
  html {
    position: relative;
    min-height: 100%;
  }

  .role-main {
    margin-bottom: 126px; /* Margin bottom by footer height */
  }

  .footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 106px; /* Set the fixed height of the footer here */
    background-color: #f5f5f5;
    font-size: 85%;
    text-align: center;
    background-color: #f7f7f7;
  }

  .server-status-container {
    padding: 0 5em;
    line-height: 30px;
    background: #333;
    color: #ddd;
    position: fixed;
    bottom: 0;
    font-size: 12px;
    z-index: 99;
  }

  .footer .footer-links-container {
    padding: 10px 5em 10px 5em;
  }

  .server-status {
    padding-left: 0;
    margin-bottom: 0 !important;
  }

  .server-status li {
    display: inline-block;
  }

  .server-status li + li {
    margin-left: 1rem;
  }

  .footer-links {
    padding-left: 0;
    margin-bottom: 1rem;
  }

  .footer a {
    font-weight: bold !important;
    color: #495057 !important;
  }

  .footer-links li {
    display: inline-block;
  }

  .footer-links li + li {
    margin-left: 1rem;
  }

  .footer p {
    margin-bottom: 0;
    max-width: inherit;
    margin: 0;
  }

  #app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    padding-bottom: 20px;
  }

  .online {
    color: #00ff00;
  }

  .offline {
    color: #ff0000;
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

  @include media-breakpoint-up(sm) {
    .footer {
      text-align: left;
    }
  }

  @include media-breakpoint-down(sm) {
    #main {
      padding-top: 10px;
    }
  }
</style>
