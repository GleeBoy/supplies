import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Material from '@/components/Material'
import Kind from '@/components/Kind'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/home',
      // path: '',
      name: 'HelloWorld',
      component: HelloWorld,
      children: [
        // {
        //   path: '',
        //   component: Material
        // },
        {
          path: 'material',
          name: 'Material',
          component: Material
        },
        {
          path: 'kind',
          name: 'Kind',
          component: Kind
        }
      ]
    },
    {
      path: '',
      name: 'Login',
      component: Login
    }
    // {
    //   path: '/kind',
    //   name: 'Kind',
    //   component: Kind
    // }
  ]
})
