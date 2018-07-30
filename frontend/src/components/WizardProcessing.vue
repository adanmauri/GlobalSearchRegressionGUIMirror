<template>
  <div class="main">
    <div v-if="!processing">
      <h5>Input</h5>
      <p>Input file, input vars nobs.</p>
      <h5>gsreg options</h5>
      <p>criteria, etc</p>
      <button @click="solve()" class="btn btn-success">Solve</button>
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
        if (parsedMessage.hasOwnProperty('finish') && parsedMessage.finish === true) {
          // ir a otra pestaña y ofrecer resultados
        }
        this.messages.push(JSON.parse(msg.data))
      }
      this.sendMessage()
    },
    methods: {
      ...mapState(['options']),
      sendMessage (msg = {}) {
        msg['user-token'] = this.$store.state.userToken
        this.$socket.sendObj(msg)
      },
      solve () {
        this.processing = true
      }
    }
  }
</script>

<style>
  h1 {
    font-weight: normal;
    font-family: "Lato Regular";
    margin-bottom: 0;
  }

  p {
    max-width: 800px;
    margin: 10px auto;
  }
</style>
