// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import Cookies from 'js-cookie'

const djangoAPI = axios.create({
  timeout: 10000
})
djangoAPI.interceptors.response.use(
  resp => {
    return resp.data
  },
  err => {
    return Promise.reject((err))
  }
)
djangoAPI.get('/api/login/').then(res => {
  djangoAPI.interceptors.request.use((config) => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest'
    config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
    return config
  })
})
Vue.prototype.$djangoAPI = djangoAPI

Vue.use(ElementUI)
Vue.config.productionTip = false

Vue.filter('fileName', function (value) {
  if (!value) return ''
  if (value instanceof Object) {
    return ''
  } else {
    return decodeURIComponent(value.substring(value.lastIndexOf('/') + 1))
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
