<template>
<div id="app">
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand  class="ml-auto">
      <form>
	<b-button type="submit" v-on:click="connect" variant="primary">{{ button_text }}</b-button>
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
    data: () => {
        return {
	    button_text: "Sign In",
            chandle: window.cardano["nami"],
            API: null
        }
    },
    methods:{
	async connect(e){
	    e.preventDefault();
	    try{	
		console.log("Pressed connect wallet")                                

                this.API = await this.chandle.enable()
                
		if (await this.$chandle.isEnabled())
                {
		    this.button_text = "SignOut"
                    console.log("Attached Wallet")

                    console.log(this.chandle)
                    console.log(this.API)
                    
		}
                else
                {
                    console.log("retry")
                    this.API = await this.$chandle.enable()
                    throw new Error("Failed this.$chandle.isEnabled()")
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
