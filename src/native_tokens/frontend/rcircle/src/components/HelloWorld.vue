<template>
<div>
  <b-container>
    Welcome to this NFT minting platform on Cardano. Hosted by the folks at <a href="https://lkbh-pools.org">LKBH Stake Pool.</a> For the community, by the community. Currently being run on testnet of Cardano.<p style="color:red;"><b>Beta Version</b></p>
    <md-divider></md-divider>
    <form>
      <md-divider></md-divider>
      <b-button type="submit" v-on:click="connect" variant="primary">{{ button_text }}</b-button>
      <br/>
      <br/>
      <b-button type="submit" v-on:click="fetchBalance" variant="primary">{{ balance }}</b-button>
      <br/>
      <br/>
      <b-button type="submit" v-on:click="fetchAddress" variant="primary">{{ address }}</b-button>
      <br/>
      <br/>
      <b-button type="submit" v-on:click="fetchRewardAddress" variant="primary">{{ rewardAddress }}</b-button>
      <br/>
      <br/>
      <b-button type="submit" v-on:click="fetchNetwork" variant="primary">{{ network }}</b-button>
      <br/>
      <br/>    
      <md-divider></md-divider>
      <md-steppers md-vertical>
	<md-step id="first" md-label="Step 1: Provide info for minting NFT">
	  <md-field>
	    <label>Upload files</label>
	    <md-file v-model="placeholder" placeholder="A nice input placeholder" />
	  </md-field>

	  <md-field>
	    <label>"Name of the NFT"</label>
	    <md-input v-model="nft_name"></md-input>
	  </md-field>

	  <md-field>
	    <label>Number of NFT to mint</label>
	    <md-input v-model="nft_number" type="number"></md-input>
	  </md-field>

	  <md-field>
	    <label>"Tags"</label>
	    <md-input v-model="nft_tags"></md-input>
	  </md-field>

	  <md-field>
	    <label>"recvAddr"</label>
	    <md-input v-model="nft_recv_addr"></md-input>
	  </md-field>	  
	</md-step>
	
	<md-step id="second" md-label="Step 2: Transfer Funds for Minting">
	  <md-field>
	    <label>"Unique ID for this transaction"</label>
	    <md-input v-model="nft_uuid"></md-input>
	  </md-field>	  
	  <md-field>
	    <label>"NFT Minting Cost"</label>
	    <md-input v-model="nft_minting_cost" type="number"></md-input>
	  </md-field>	  
	  <md-field>
	    <label>"Unique Payment Address"</label>
	    <md-input v-model="nft_cost_payment_addr"></md-input>
	  </md-field>	  
	</md-step>
      </md-steppers>	  
    </form>
    <br/>
    <br/>    
    <b-form @submit="onSubmit" @reset="onReset">
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-container>
</div>
</template>

<script>
export default {
    name: 'Intro',
    data: () => ({
	button_text: "Sign In",
	balance: 0,
	network: "",
	address:"",
	rewardAddress:""
    }),
    methods:{
	onSubmit(event) {
	    event.preventDefault()
	},
	onReset(event) {
	    event.preventDefault()
	},
	async connect(e){
	    e.preventDefault();
	    try{	
		console.log("Pressed connect wallet")
		await cardano.enable()
		if (await cardano.isEnabled()){
		    this.button_text = "SignOut"
		}
	    }			
	    catch(e){
		console.log("Failed to connect to wallet", e)
	    }
	},
	async fetchBalance(e){
	    console.log("Now fetching balance")
	    e.preventDefault();
	    try{
		if (cardano.isEnabled()){
		    var t = await cardano.getBalance()
		    let cb = require('cborg')
		    this.balance = cb["decode"](Buffer.from(t,'hex'))
		    console.log("decoded wallet amount", this.balance)
		    // const S = await import('@emurgo/cardano-serialization-lib-browser/cardano_serialization_lib.js')
		    // this.balance =  S.BigNum.from_str(await cardano.getBalance())
		}
		else
		{
		    console.log("Wallet is not connected hence cannot fetch balance")
		    this.balance = "unknown"
		}		
	    }
	    catch(e) {
		console.log("Failed to fetch balance", e)		
	    }

	},
	async fetchNetwork(e){
	    e.preventDefault()
	    try{
		if (cardano.isEnabled()){
		    var id = await cardano.getNetworkId()
		    if( id == 0){
			this.network = "Testnet"
		    }
		    else if(id == 1){
			this.network = "Mainnet"
		    }else {
			this.network = "Custom"
		    }
		}
	    }
	    catch(e){
		console.log("Failed to fetch network id", e)
	    }
	},
	async fetchAddress(e){
	    e.preventDefault()
	    try{
		if (cardano.isEnabled()){
		    var t  = await cardano.getUsedAddresses()
		    this.address = t[0]
		    this.nft_recv_addr = t[0]
		    console.log("Address associated with the wallet is:", this.address)
		}
	    }
	    catch(e){
		console.log("Failed to fetch address", e)
	    }
	},
	async fetchRewardAddress(e){
	    e.preventDefault()
	    try{
		if (cardano.isEnabled()){
		    var t  = await cardano.getRewardAddress()
		    this.rewardAddress = t
		    console.log("Reward Address associated with the wallet is:", this.rewardAddress)
		}
	    }
	    catch(e){
		console.log("Failed to fetch of Reward address", e)
	    }
	}
    }
}
</script>

