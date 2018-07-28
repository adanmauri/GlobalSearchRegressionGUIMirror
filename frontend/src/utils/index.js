import constants from '../constants'

const uuidv4 = require('uuid/v4')
export default {
  userToken () {
    return localStorage.getItem('user-token') || localStorage.setItem('user-token', uuidv4())
  },
  createStepStatus () {
    var steps = new Array(constants.STEPS.length).fill(false)
    steps[0] = true
    return steps
  },
  outsampleMax (nobs, insampleMinSize, expvars, intercept) {
    var max = nobs - insampleMinSize - expvars.length - ((intercept) ? 1 : 0)
    return (max >= 0) ? max : 0
  }
}
