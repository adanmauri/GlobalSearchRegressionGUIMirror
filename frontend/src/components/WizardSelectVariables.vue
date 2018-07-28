<template>
  <div class="main">
    <h2>Select variables</h2>
    <div class="row">
      <div class="col">
        <md-field>
          <label for="dependent" title="Select dependent variables">Dependent variables</label>
          <md-select v-model="dependent" placeholder="Dependent variables" required>
            <md-option v-for="(dataname, index) in datanames" :key="index" :value="dataname">{{ dataname }}</md-option>
          </md-select>
        </md-field>
      </div>
      <div class="col">
        <div class="md-layout-item">
          <md-field>
            <label for="explanatory" title="Select explanatory variables">Explanatory variables</label>
            <md-select v-model="explanatory" placeholder="Explanatory variables" multiple required>
              <md-option v-for="(dataname, index) in datanames" :key="index" :value="dataname" :disabled="dependent==dataname">{{ dataname }}</md-option>
            </md-select>
          </md-field>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <md-checkbox class="intercept" v-model="intercept" :checked="intercept" title="Include intercept">Include intercept</md-checkbox>
      </div>
      <div class="col">
        <div class="md-layout-item">
          <md-field>
            <label for="time" title="Select time variable">Time variable</label>
            <md-select v-model="time" placeholder="Time variable">
              <md-option v-for="(dataname, index) in datanames" :key="index" :value="dataname" :disabled="dependent==dataname">{{ dataname }}</md-option>
            </md-select>
          </md-field>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import utils from '../utils'

export default {
  components: { },
  name: 'SelectVariables',
  data () {
    return {}
  },
  watch: {
    dependent: function (depvar) {
      this.$store.commit('filterExpvars', depvar)
      this.$store.commit('filterTime', depvar)
      this.validate()
    },
    explanatory: function (expvars) {
      this.validate()
      this.updateOutsample()
    },
    intercept: function (intercept) {
      this.updateOutsample()
    }
  },
  methods: {
    validate () {
      this.$store.commit('updateCompleteStep', { step: this.$store.state.currentStep, complete: this.$store.state.depvar !== null && this.$store.state.expvars.length > 1 })
    },
    updateOutsample () {
      var outsampleMax = utils.outsampleMax(this.$store.state.nobs, this.$constants.INSAMPLE_MIN_SIZE, this.$store.state.expvars, this.$store.state.intercept)
      if (outsampleMax < this.$store.state.outsample) {
        this.$store.commit('setOutsample', outsampleMax)
      }
    },
    updateSetStep () {
      this.$store.commit('updateSetStep', { step: this.$store.state.currentStep, set: true })
    }
  },
  computed: {
    ...mapState(['datanames']),
    dependent: {
      get () {
        return this.$store.state.depvar
      },
      set (value) {
        this.$store.commit('setDepvar', value)
        this.updateSetStep()
      }
    },
    explanatory: {
      get () {
        return this.$store.state.expvars
      },
      set (value) {
        this.$store.commit('setExpvars', value)
        this.updateSetStep()
      }
    },
    intercept: {
      get () {
        return this.$store.state.intercept
      },
      set (value) {
        this.$store.commit('setIntercept', value)
        this.updateSetStep()
      }
    },
    time: {
      get () {
        return this.$store.state.time
      },
      set (value) {
        this.$store.commit('setTime', value)
        this.updateSetStep()
      }
    }
  }
}
</script>

<style>
.intercept {
  margin-top: 27px;
  margin-bottom: 5px;
}

.md-checkbox.md-theme-default.md-checked .md-ripple {
  color: #60ad51;
}
.md-checkbox.md-theme-default.md-checked .md-checkbox-container {
  background: #60ad51;
  border-color: #60ad51;
}
</style>
