import Vuex from 'vuex'
import Vue from 'vue'
import utils from '../utils'

Vue.use(Vuex)
const state = {
  navBlocked: false,
  currentStep: 0,
  userToken: utils.userToken(),
  completeSteps: utils.createStepStatus(),
  setSteps: utils.createStepStatus(),
  nworkers: 4,
  datanames: ['y', 'x1', 'x2', 'x3', 'x4'],
  nobs: 35,
  depvar: null,
  expvars: [],
  intercept: false,
  time: null,
  residualtest: null,
  keepwnoise: null,
  ttest: null,
  orderresults: null,
  modelavg: null,
  outsample: 0,
  csv: null,
  method: 'fast',
  addprocs: 0,
  criteria: [],
  paraprocs: 1,
  exportcsv: false
}
const getters = {}
const actions = {
  setDepvar ({commit, state}, depvar) {
    commit('setDepvar', depvar)
  },
  setExpvars ({commit, state}, expvars) {
    commit('setExpvars', expvars)
  },
  setStep ({commit, state}, step) {
    commit('setCurrentStep', step)
  },
  prevStep ({commit, state}) {
    commit('setCurrentStep', state.currentStep - 1)
  },
  nextStep ({commit, state}) {
    commit('setCurrentStep', state.currentStep + 1)
  },
  updateCompleteStep ({commit, payload}) {
    commit('updateCompleteStep', payload)
  },
  updateSetStep ({commit, payload}) {
    commit('updateSetStep', payload)
  }
}
const mutations = {
  setNavBlocked (state, navBlocked) {
    state.navBlocked = navBlocked
  },
  setCurrentStep (state, step) {
    state.currentStep = step
  },
  setDepvar (state, depvar) {
    state.depvar = depvar
  },
  setExpvars (state, expvars) {
    state.expvars = expvars
  },
  setIntercept (state, intercept) {
    state.intercept = intercept
  },
  setTime (state, time) {
    state.time = time
  },
  setResidualtest (state, residualtest) {
    state.residualtest = residualtest
  },
  setKeepwnoise (state, keepwnoise) {
    state.keepwnoise = keepwnoise
  },
  setTtest (state, ttest) {
    state.ttest = ttest
  },
  setOrderresults (state, orderresults) {
    state.orderresults = orderresults
  },
  setModelavg (state, modelavg) {
    state.modelavg = modelavg
  },
  setOutsample (state, outsample) {
    state.outsample = outsample
  },
  setCsv (state, csv) {
    state.csv = csv
  },
  setMethod (state, method) {
    state.method = method
  },
  setAddprocs (state, addprocs) {
    state.addprocs = addprocs
  },
  setCriteria (state, criteria) {
    state.criteria = criteria
  },
  filterExpvars (state, depvar) {
    state.expvars = state.expvars.filter(e => e !== depvar)
  },
  filterTime (state, depvar) {
    state.time = (state.time !== depvar) ? state.time : null
  },
  filterCriteria (state, outsample) {
    if (parseInt(outsample) === 0) {
      state.criteria = state.criteria.filter(e => e !== 'rmseout')
    }
  },
  updateCompleteStep (state, payload) {
    state.completeSteps[payload.step] = payload.complete
    var currentStep = state.currentStep
    state.currentStep = -1
    state.currentStep = currentStep
  },
  updateSetStep (state, payload) {
    state.setSteps[payload.step] = payload.set
    var currentStep = state.currentStep
    state.currentStep = -1
    state.currentStep = currentStep
  },
  setParaprocs (state, paraprocs) {
    state.paraprocs = paraprocs
    state.addprocs = paraprocs - 1
  },
  setExportcsv (state, exportcsv) {
    state.exportcsv = exportcsv
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  strict: false
})
