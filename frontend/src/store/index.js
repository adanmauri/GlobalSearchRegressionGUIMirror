import Vuex from 'vuex'
import Vue from 'vue'
import utils from '../utils'

Vue.use(Vuex)
const state = {
  navHidden: false,
  currentStep: 0,
  userToken: utils.userToken(),
  completeSteps: utils.createStepStatus(),
  setSteps: utils.createStepStatus(),
  paraprocs: 1,
  exportcsv: false,
  inputData: {
    datanames: ['y', 'x1', 'x2', 'x3', 'x4'],
    nobs: 35
  },
  server: {
    nworkers: 4
  },
  gsregOptions: {
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
    criteria: []
  }
}
const getters = {
  getInputDataDatanames (state) {
    return state.inputData.datanames
  },
  getInputDataNobs (state) {
    return state.inputData.nobs
  },
  getServerNworkers (state) {
    return state.server.nworkers
  },
  getGSRegOptionsDepvar (state) {
    return state.gsregOptions.depvar
  },
  getGSRegOptionsExpvars (state) {
    return state.gsregOptions.expvars
  },
  getGSRegOptionsIntercept (state) {
    return state.gsregOptions.intercept
  },
  getGSRegOptionsTime (state) {
    return state.gsregOptions.time
  },
  getGSRegOptionsResidualtest (state) {
    return state.gsregOptions.residualtest
  },
  getGSRegOptionsKeepwnoise (state) {
    return state.gsregOptions.keepwnoise
  },
  getGSRegOptionsTtest (state) {
    return state.gsregOptions.ttest
  },
  getGSRegOptionsOrderresults (state) {
    return state.gsregOptions.orderresults
  },
  getGSRegOptionsModelavg (state) {
    return state.gsregOptions.modelavg
  },
  getGSRegOptionsOutsample (state) {
    return state.gsregOptions.outsample
  },
  getGSRegOptionsCsv (state) {
    return state.gsregOptions.csv
  },
  getGSRegOptionsMethod (state) {
    return state.gsregOptions.method
  },
  getGSRegOptionsAddprocs (state) {
    return state.gsregOptions.addprocs
  },
  getGSRegOptionsCriteria (state) {
    return state.gsregOptions.criteria
  }
}

const actions = {
  setGSRegOptionsDepvar ({commit, state}, depvar) {
    commit('setGSRegOptionsDepvar', depvar)
  },
  setGSRegOptionsExpvars ({commit, state}, expvars) {
    commit('setGSRegOptionsExpvars', expvars)
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
  setnputDataDatanames (state, datanames) {
    state.inputData.datanames = datanames
  },
  setInputDataNobs (state, nobs) {
    state.inputData.nobs = nobs
  },
  setServerNworkers (state, nworkers) {
    state.server.nworkers = nworkers
  },
  setGSRegOptionsDepvar (state, depvar) {
    state.gsregOptions.depvar = depvar
  },
  setGSRegOptionsExpvars (state, expvars) {
    state.gsregOptions.expvars = expvars
  },
  setGSRegOptionsIntercept (state, intercept) {
    state.gsregOptions.intercept = intercept
  },
  setGSRegOptionsTime (state, time) {
    state.gsregOptions.time = time
  },
  setGSRegOptionsResidualtest (state, residualtest) {
    state.gsregOptions.residualtest = residualtest
  },
  setGSRegOptionsKeepwnoise (state, keepwnoise) {
    state.gsregOptions.keepwnoise = keepwnoise
  },
  setGSRegOptionsTtest (state, ttest) {
    state.gsregOptions.ttest = ttest
  },
  setGSRegOptionsOrderresults (state, orderresults) {
    state.gsregOptions.orderresults = orderresults
  },
  setGSRegOptionsModelavg (state, modelavg) {
    state.gsregOptions.modelavg = modelavg
  },
  setGSRegOptionsOutsample (state, outsample) {
    state.gsregOptions.outsample = outsample
  },
  setGSRegOptionsCsv (state, csv) {
    state.gsregOptions.csv = csv
  },
  setGSRegOptionsMethod (state, method) {
    state.gsregOptions.method = method
  },
  setGSRegOptionsAddprocs (state, addprocs) {
    state.gsregOptions.addprocs = addprocs
  },
  setGSRegOptionsCriteria (state, criteria) {
    state.gsregOptions.criteria = criteria
  },
  setNavHidden (state, navHidden) {
    state.navHidden = navHidden
  },
  setCurrentStep (state, step) {
    state.currentStep = step
  },
  filterExpvars (state, depvar) {
    state.gsregOptions.expvars = state.gsregOptions.expvars.filter(e => e !== depvar)
  },
  filterTime (state, depvar) {
    state.gsregOptions.time = (state.gsregOptions.time !== depvar) ? state.gsregOptions.time : null
  },
  filterCriteria (state, outsample) {
    if (parseInt(outsample) === 0) {
      state.gsregOptions.criteria = state.gsregOptions.criteria.filter(e => e !== 'rmseout')
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
