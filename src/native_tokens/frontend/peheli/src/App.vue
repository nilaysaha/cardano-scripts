<template>
<div id="app">
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand  class="ml-auto">
      <form>
	<b-button type="submit" v-on:click="switchStatus" variant="primary">{{ button_text }}</b-button>
      </form>
    </b-navbar-brand>
  </b-navbar>
  <HelloWorld v-bind:API="API"/>
</div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
    name: 'App',
    async created() {
        console.log(this.$el);
    },
    async mounted() {
        console.log(this.$el);
        this.connected = await this.$chandle.isEnabled()
        alert(`Wallet status on mount:${this.connected}`)
        this.button_text = (this.connected)?"Disconnect":"Connect"
        if (this.connected){
            console.log("now getting handle")
            this.API = await this.$chandle.enable()
            console.log(this.API)
        }
    },
    data() {
        return {
            button_text: this.connect_string,
            chandle: window.cardano["nami"],
            API: null
        };
    },
    methods:{
        async disconnect(e){
            e.preventDefault();
            console.log("disconnecting wallet")
            this.button_text = "Connect"
            this.API = null
            this.connected = false
        },
        async connect(e){
            e.preventDefault();
            console.log("Connecting")
            this.button_text = "Disconnect"

            this.API = await this.$chandle.enable()
            this.connected = await this.$chandle.isEnabled()  

            console.log(this.API)
        },
	async switchStatus(e){
	    e.preventDefault();
            
	    try{                
                console.log(`Current connect status:${this.connected}`)

		if (this.connected)
                {
                    this.disconnect(e)                    
		}
                else //wallet is not connected
                {
                    this.connect(e)
                }
	    }			
	    catch(e){
		console.log("Failed to connect to wallet", e)
	    }
	},	
    },
    components: {
	HelloWorld
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
