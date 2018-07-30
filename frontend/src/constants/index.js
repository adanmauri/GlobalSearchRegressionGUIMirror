export default {
  'API': {
    'host': '//192.168.0.22:8000',
    'paths': {
      'load_database': '/upload'
    }
  },
  'WS': {
    'url': 'ws://192.168.0.22:8000'
  },
  'INSAMPLE_MIN_SIZE': 20,
  'STEPS': [
    {
      'label': 'Load database',
      'icon': 'database',
      'component': 'WizardLoadDatabase'
    },
    {
      'label': 'Select variables',
      'icon': 'flask',
      'component': 'WizardSelectVariables'
    },
    {
      'label': 'Settings',
      'icon': 'cog',
      'component': 'WizardSettings'
    },
    {
      'label': 'Processing',
      'icon': 'spinner',
      'component': 'WizardProcessing'
    },
    {
      'label': 'Results',
      'icon': 'clipboard-list',
      'component': 'WizardResults'
    }
  ],
  'CRITERIA': [
    {
      'name': 'r2adj',
      'label': 'Adjusted R²'
    },
    {
      'name': 'bic',
      'label': 'BIC'
    },
    {
      'name': 'aic',
      'label': 'AIC'
    },
    {
      'name': 'aicc',
      'label': 'AIC Corrected'
    },
    {
      'name': 'cp',
      'label': 'Mallows\'s Cp'
    },
    {
      'name': 'rmse',
      'label': 'RMSE'
    },
    {
      'name': 'rmseout',
      'label': 'RMSE OUT'
    },
    {
      'name': 'sse',
      'label': 'SSE'
    }
  ],
  'METHODS': [
    {
      'name': 'fast',
      'label': 'Fast'
    },
    {
      'name': 'precise',
      'label': 'Precise'
    }
  ]
}
