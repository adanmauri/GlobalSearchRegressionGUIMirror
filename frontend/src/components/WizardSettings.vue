<template>
  <div class="main">
    <h2>Settings</h2>
    <md-card>
      <md-card-header>
        <div class="md-title">Ordering criteria and additional tests</div>
      </md-card-header>
      <hr>
      <md-card-content>
        <div class="row">
          <div class="col">
            <div class="md-layout-item">
              <md-field>
                <label for="outsample" title="Number of out-of-sample observations">Out-of-sample observations</label>
                <md-input v-model="outsample" type="number" min="0" :max="outsampleMax" placeholder="Out-of-sample observations"></md-input>
              </md-field>
            </div>
          </div>
          <div class="col">
            <div class="md-layout-item">
              <md-field>
                <label for="criteria" title="Ordering criteria">Ordering criteria</label>
                <md-select v-model="criteria" placeholder="Ordering criteria" multiple>
                  <md-option v-for="(criteria, index) in $constants.CRITERIA" :key="index" :value="criteria.name" :disabled="criteria.name==='rmseout' && parseInt(outsample)===0" >{{ criteria.label }}</md-option>
                </md-select>
              </md-field>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <md-checkbox class="residualtest" v-model="residualtest" :checked="residualtest" title="Estimate residuals tests">Estimate residuals tests</md-checkbox>
          </div>
          <div class="col">
            <md-checkbox class="keepwnoise" v-model="keepwnoise" :checked="keepwnoise" :disabled="!residualtest" :hidden="!residualtest" title="Discard models without white noise residuals">Just white noise residuals</md-checkbox>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <md-checkbox class="ttest" v-model="ttest" :checked="ttest" title="Estimate t-test">Estimate t-test</md-checkbox>
          </div>
        </div>
      </md-card-content>
    </md-card>
    <md-card>
      <md-card-header>
        <div class="md-title">Processing options</div>
      </md-card-header>
      <hr>
      <md-card-content>
        <div class="row">
          <div class="col">
            <div class="md-layout-item">
              <md-field>
                <label for="paraprocs" title="Number of parallel workers">Number of parallel workers</label>
                <md-input v-model="paraprocs" type="number" min="1" :max="nworkers" placeholder="Number of parallel workers"></md-input>
              </md-field>
            </div>
          </div>
          <div class="col">
            <div class="md-layout-item">
              <md-field>
                <label for="method" title="Calculation precision (Float32/Float64)">Calculation precision</label>
                <md-select v-model="method" placeholder="Calculation precision">
                  <md-option v-for="(method, index) in $constants.METHODS" :key="index" :value="method.name">{{ method.label }}</md-option>
                </md-select>
              </md-field>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <md-checkbox class="modelavg" v-model="modelavg" :checked="modelavg" title="Display weighted model averaging results">Display model averaging results</md-checkbox>
          </div>
        </div>
      </md-card-content>
    </md-card>
    <md-card>
      <md-card-header>
        <div class="md-title">Output options</div>
      </md-card-header>
      <hr>
      <md-card-content>
        <div class="row">
          <div class="col">
            <md-checkbox class="orderresults" v-model="orderresults" :checked="orderresults" title="Sort full result database by selected criteria">Sort all models</md-checkbox>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <md-checkbox class="exportcsv" v-model="exportcsv" :checked="exportcsv" title="Export to CSV">Export to CSV</md-checkbox>
          </div>
          <div class="col">
            <div class="md-layout-item">
              <md-field>
                <label for="csv" title="Define output CSV filename">Output filename</label>
                <md-input v-model="csv" type="text" placeholder="Output filename" :disabled="!exportcsv" :hidden="!exportcsv"></md-input>
              </md-field>
            </div>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import utils from '../utils'

export default {
  components: { },
  name: 'Settings',
  data () {
    return {}
  },
  watch: {
    criteria: function (depvar) {
      this.validate()
    }
  },
  methods: {
    validate () {
      this.$store.commit('updateCompleteStep', { step: this.$store.state.currentStep, complete: this.$store.state.criteria.length > 0 })
    },
    updateSetStep () {
      this.$store.commit('updateSetStep', { step: this.$store.state.currentStep, set: true })
    }
  },
  computed: {
    ...mapState(['datanames']),
    outsampleMax () {
      return utils.outsampleMax(this.$store.state.nobs, this.$constants.INSAMPLE_MIN_SIZE, this.$store.state.expvars, this.$store.state.intercept)
    },
    navBlocked: {
      get () {
        return this.$store.state.navBlocked
      }
    },
    nworkers: {
      get () {
        return this.$store.state.nworkers
      }
    },
    residualtest: {
      get () {
        return this.$store.state.residualtest
      },
      set (value) {
        this.$store.commit('setResidualtest', value)
        if (value !== true) {
          this.$store.commit('setKeepwnoise', false)
        }
        this.updateSetStep()
      }
    },
    keepwnoise: {
      get () {
        return this.$store.state.keepwnoise
      },
      set (value) {
        this.$store.commit('setKeepwnoise', value)
        this.updateSetStep()
      }
    },
    ttest: {
      get () {
        return this.$store.state.ttest
      },
      set (value) {
        this.$store.commit('setTtest', value)
        this.updateSetStep()
      }
    },
    orderresults: {
      get () {
        return this.$store.state.orderresults
      },
      set (value) {
        this.$store.commit('setOrderresults', value)
        this.updateSetStep()
      }
    },
    modelavg: {
      get () {
        return this.$store.state.modelavg
      },
      set (value) {
        this.$store.commit('setModelavg', value)
        this.updateSetStep()
      }
    },
    outsample: {
      get () {
        return this.$store.state.outsample
      },
      set (value) {
        this.$store.commit('setOutsample', value)
        this.$store.commit('filterCriteria', value)
        this.updateSetStep()
      }
    },
    csv: {
      get () {
        return this.$store.state.csv
      },
      set (value) {
        this.$store.commit('setCsv', value)
        this.updateSetStep()
      }
    },
    exportcsv: {
      get () {
        return this.$store.state.exportcsv
      },
      set (value) {
        this.$store.commit('setExportcsv', value)
        this.updateSetStep()
      }
    },
    method: {
      get () {
        return this.$store.state.method
      },
      set (value) {
        this.$store.commit('setMethod', value)
        this.updateSetStep()
      }
    },
    paraprocs: {
      get () {
        return this.$store.state.paraprocs
      },
      set (value) {
        this.$store.commit('setParaprocs', value)
        this.updateSetStep()
      }
    },
    criteria: {
      get () {
        return this.$store.state.criteria
      },
      set (value) {
        this.$store.commit('setCriteria', value)
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

.md-card-header {
  padding-top: 0;
  padding-bottom: 0;
}

h2 {
  margin-bottom: 20px;
}

.md-title {
  font-size: 18px!important;
}

hr {
  margin-bottom: 0;
}

</style>

