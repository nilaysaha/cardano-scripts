<template>
  <div class="container">
    <form>
      <b-button type="submit" @click="connect" variant="primary">{{ button.text }}</b-button>
      <span>{{ balance.amount }}</span>
    </form>
  </div>
</template>

<script>
export default {
    name: 'Card',
    data: () => ({
	button:{
	    text: "Connect Wallet"
	},
	balance:{
	    amount: 0
	}
    }),
    methods:{
	async connect(e){
	    e.preventDefault();
	    if (cardano.isEnabled()){
		console.log("cardano wallet is enabled")
		this.button.text = "Connected"
		await this.fetchBalance()
	    }
	    else
	    {
		console.log("Pressed connect wallet")
		cardano.enable()
		connect(e)
	    }	    
	},
	isEnabled(){
	    console.log("Now checking if cardano wallet is connected")
	},
	async fetchBalance(){
	    this.balance.amount = await cardano.getBalance()
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
