<template>
  <div class="main">
    <div v-if="!processing">
      <h2>Request details</h2>
      <p>Please confirm that the selected options are correct before starting.
      <h3>Selected variables</h3>
      <hr/>
      <div class="row">
        <div class="col">
          <ul>
            <li><b>Dependent variable: </b>{{ gsregOptions.depvar }}</li>
            <li><b>Explanatory variables: </b><span v-for="(expvar, index) in gsregOptions.expvars" :key="index">{{ expvar }} </span></li>
            <li><b>Time variable: </b><span v-if="gsregOptions.time">{{ gsregOptions.time }}</span><span v-else>No selected</span></li>
            <li><b>Include intercept: </b><span v-if="gsregOptions.intercept">Yes</span><span v-else>No</span></li>
          </ul>
        </div>
      </div>
      <h3>Settings</h3>
      <hr />
      <div class="row">
        <div class="col">
          <ul>
            <li><b>Out-of-sample observations: </b>{{ gsregOptions.outsample }}</li>
            <li><b>Ordering criteria: </b><span v-for="(criteria, index) in gsregOptions.criteria" :key="index">{{ criteria }} </span></li>
            <li><b>Estimate residuals tests: </b><span v-if="gsregOptions.residualtest">Yes</span><span v-else>No</span></li>
            <li v-if="gsregOptions.residualtest"><b>Just white noise residuals: </b><span v-if="gsregOptions.keepwnoise">Yes</span><span v-else>No</span></li>
            <li><b>Estimate t-test: </b><span v-if="gsregOptions.ttest">Yes</span><span v-else>No</span></li>
          </ul>
        </div>
        <div class="col">
          <ul>
            <li><b>Number of parallel workers: </b>{{ paraprocs }}</li>
            <li><b>Calculation precision: </b>{{ gsregOptions.method }}</li>
            <li><b>Display model averaging results: </b><span v-if="gsregOptions.modelavg">Yes</span><span v-else>No</span></li>
          </ul>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <ul>
            <li><b>Sort all models: </b><span v-if="gsregOptions.orderresults">Yes</span><span v-else>No</span></li>
            <li><b>Export to CSV: </b><span v-if="gsregOptions.exportcsv">Yes</span><span v-else>No</span></li>
            <li v-if="gsregOptions.exportcsv"><b>Output filename: </b>{{ gsregOptions.csv }}</li>
          </ul>
        </div>
      </div>
      <div class="text-right">
        <md-button class="md-raised md-primary start-solve" @click.native="solve()">Start to solve</md-button>
      </div>
    </div>
    <div v-else>
      <p>Server console</p>
      <div class="websocket-console">
        <ul>
          <li v-for="msg in messages">{{ msg }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex'
  // TODO: Create a better view
  export default {
    components: {},
    name: 'WizardProcessing',
    data () {
      return {
        messages: [],
        processing: false
      }
    },
    created () {
      this.$options.sockets.onmessage = function (msg) {
        let parsedMessage = JSON.parse(msg.data)
        if (parsedMessage.hasOwnProperty('done') && parsedMessage.done === true) {
          // ir a otra pestaña y ofrecer resultados
        }
        this.messages.push(JSON.parse(msg.data))
      }
      this.sendMessage()
    },
    methods: {
      sendMessage (msg = {}) {
        msg['user-token'] = this.$store.state.userToken
        this.$socket.sendObj(msg)
      },
      solve () {
        this.$store.commit('setNavBlocked', true)
        this.$store.commit('setNavHidden', true)
        this.processing = true
      }
    },
    computed: {
      ...mapState(['gsregOptions', 'paraprocs', 'exportcsv'])
    }
  }
</script>

<style>
  button.start-solve {
    background: #6682e0!important;
  }

  h1 {
    font-weight: normal;
    font-family: "Lato Regular";
    margin-bottom: 0;
  }

  p {
    max-width: 800px;
    margin: 10px auto;
  }

  ul {
    list-style: none;
    padding-left: 0;
    margin-top: 10px;
    font-size: 14px;
  }

  h4 {
    font-size: 16px;
  }
</style>
