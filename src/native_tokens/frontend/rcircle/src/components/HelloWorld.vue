<template>
  <div class="container">
    <form>
      <b-button type="submit" @click="connect" variant="primary">{{ button.text }}</b-button>
    </form>
  </div>
</template>

<script>
export default {
    name: 'Card',
    data: () => ({
	button:{
	    text: "Connect Wallet"
	}	
    }),
    methods:{
	connect(e){
	    e.preventDefault();
	    console.log("Pressed connect wallet")
	    cardano.enable()
	    if (cardano.isEnabled()){
		console.log("cardano wallet is enabled")
		this.button.text = "Connected"
	    }	    
	},
	isEnabled(){
	    console.log("Now checking if cardano wallet is connected")
	}
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #fffff;
}
</style>
