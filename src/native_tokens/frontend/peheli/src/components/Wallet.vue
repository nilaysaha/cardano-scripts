<template>
  <div>
    <h1> Wallet information </h1>
    <b-container>
      <div id="balance">
      <span>{{ balance.amount }}</span>
    </b-container>
  </div>
</template>

<script>
export default {
    name: 'Wallet',
    data: () => ({
	balance:{
	    amount: 0
	}
    }),
    methods:{
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
