import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.prototype.cardano = window.cardano

new Vue({
    render: h => h(App),
    methods:{
	connect(){
	    alert("Pressed connect wallet")
	}
    }
}).$mount('#app')
