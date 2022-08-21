<template>
<div id="app">
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand  class="ml-auto">
      <form>
	<b-button type="submit" v-on:click="connect" variant="primary">{{ button_text }}</b-button>
      </form>
    </b-navbar-brand>
  </b-navbar>
  <HelloWorld name="Beautiful card"/>
</div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
    name: 'App',
    data: () => ({
	button_text: "Sign In",
    }),
    methods:{
	async connect(e){
	    e.preventDefault();
	    try{	
		console.log("Pressed connect wallet")
		await cardano.enable()
		if (await cardano.isEnabled()){
		    this.button_text = "SignOut"
                    console.log("Attached Wallet")
		}
                else{
                    throw new Error("Could not enable wallet")
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
