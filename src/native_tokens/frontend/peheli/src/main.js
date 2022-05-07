import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import 'vue-material/dist/theme/default.css'
import 'vue-material/dist/vue-material.min.css'
import VueMaterial from 'vue-material'

Vue.use(VueMaterial)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Object.defineProperty(Vue.prototype, 'cardano', { value: window.cardano.nami });


new Vue({
    render: h => h(App),
    methods:{}
}).$mount('#app')    

    


