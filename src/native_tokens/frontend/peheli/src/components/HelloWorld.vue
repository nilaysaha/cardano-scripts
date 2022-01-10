<template>
<div>
  <b-container>
    Welcome to this NFT minting platform on Cardano. Hosted by the folks at <a href="https://lkbh-pools.org">LKBH Stake Pool.</a> For the community, by the community. Currently being run on testnet of Cardano.<p style="color:red;"><b>Beta Version</b></p>
    <md-divider></md-divider>
    <form>
      <md-divider></md-divider>
      <!-- <b-button type="submit" v-on:click="connect" variant="primary">{{ button_text }}</b-button> -->
      <!-- <br/> -->
      <!-- <br/> -->
      <!-- <b-button type="submit" v-on:click="fetchBalance" variant="primary">{{ balance }}</b-button> -->
      <!-- <br/> -->
      <!-- <br/> -->
      <!-- <b-button type="submit" v-on:click="fetchAddress" variant="primary">{{ address }}</b-button> -->
      <!-- <br/> -->
      <!-- <br/> -->
      <!-- <b-button type="submit" v-on:click="fetchRewardAddress" variant="primary">{{ rewardAddress }}</b-button> -->
      <!-- <br/> -->
      <!-- <br/> -->
      <!-- <b-button type="submit" v-on:click="fetchNetwork" variant="primary">{{ network }}</b-button> -->
      <!-- <br/> -->
      <!-- <br/>     -->
      <md-divider></md-divider>
      <md-steppers md-vertical>
	<md-step id="first" md-label="Provide info for minting NFT">
	  <div class="image-holder">
	    <b-img-lazy	 :src="previewImage" class="image-holder" alt="Image Preview"></b-img-lazy>
	  </div>
	  <md-field>
	    <label>Upload files</label>
	    <md-file  @change=mediaUpload placeholder="A nice input placeholder" />
	  </md-field>
	  
	  <md-field>
	    <label>"Name of the NFT"</label>
	    <md-input v-model="nft_name"></md-input>
	  </md-field>
	  
	  <md-field>
	    <label>Number of NFT to mint</label>
	    <md-input v-model="nft_number" type="number"></md-input>
	  </md-field>
	  
	  <md-chips v-model="nft_tags" md-placeholder="Add nft tags..."></md-chips>
	  
	  <md-field>
	    <label>"recvAddr:Login to link your Nami wallet to this app"</label>
	    <md-input v-on:click="fetchAddress" v-model="nft_recv_addr"></md-input>
	  </md-field>
	  
	  <md-field>
	    <label>Unique ID for this  transaction</label>
	    <md-input v-model="uuid" readonly></md-input>
	  </md-field>

	  <md-field>
	    <label>balance in wallet Address</label>
	    <md-input v-on:click="fetchBalance" v-model="balance" readonly></md-input>
	  </md-field>

	  <md-field>
	    <label>utxo</label>
	    <md-input v-on:click="fetchUtxo" v-model="utxo" readonly></md-input>
	  </md-field>
	  
	  <br/>
	  <br/>	   
	  <b-form @submit="onSubmit" @reset="onReset">
	    <b-container class="bv-example-row">
	      <b-row>
		<b-col>
		  <b-button type="submit" variant="danger">Cancel</b-button>
		</b-col>
		<b-col></b-col>
		<b-col>
		  <b-button type="reset" variant="primary">Submit</b-button>
		</b-col>
	      </b-row>
	    </b-container>
	  </b-form>
	</md-step>
	
	<md-step id="second" md-label="Transfer Funds for Minting">
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
  </b-container>
</div>
</template>

<script>
const uniqueId = require('uuid')


export default {
    name: 'Intro',
    data: () => (
	{
	    nft_tags: [
		"unique"
	    ],
	    uuid:"",
	    button_text: "Sign In",
	    balance: 1,
	    network: "",
	    address: "",
	    rewardAddress: "",
	    nft_name: "test nft",
	    nft_number:1,
	    nft_recv_addr: "",
	    nft_uuid: "",
	    nft_minting_cost: "",
	    nft_cost_payment_addr: "",
	    previewImage: "",
	    utxo:[],
	    mainProps: {
		center: true,
		fluidGrow: true,
		blank: true,
		blankColor: '#bbb',
		width: 600,
		height: 400,
		class: 'my-5'
	    }
	}
    ),
    beforeMount(){
	this.previewImage = this.getImageUrl(80)
	this.uuid = uniqueId.v4()
    },
    methods:{
	onSubmit(event) {
	    event.preventDefault()
	},
	onReset(event) {
	    event.preventDefault()
	},
	getImageUrl(imageId) {
	    const { width, height } = this.mainProps
	    return `https://picsum.photos/${width}/${height}/?image=${imageId}`
	},
	mediaUpload(e){
	    const image = e.target.files[0];
	    const reader = new FileReader();
	    reader.readAsDataURL(image);	    
	    reader.onload = e =>{
		this.previewImage = e.target.result;
		console.log(this.previewImage);
	    };
	},
	decodeHex(t){
	    let cb = require('cborg')
	    return cb["decode"](Buffer.from(t,'hex'))
	},
	async fetchBalance(e){
	    console.log("Now fetching balance")
	    e.preventDefault();
	    try{
		if (cardano.isEnabled()){
		    var t = await cardano.getBalance()	
		    this.balance = this.decodeHex(t)
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
	    catch(error){
		console.log("Failed to fetch network id", error)
	    }
	},
	async fetchAddress(e){
	    const S = await import('@emurgo/cardano-serialization-lib-browser/cardano_serialization_lib.js')
	    const _Buffer = (await import('buffer/')).Buffer

	    e.preventDefault()
	    try{
		if (cardano.isEnabled()){
		    var t  = await cardano.getChangeAddress()
		    this.nft_recv_addr = S.Address.from_bytes(_Buffer.from(t, 'hex')).to_bech32()
		    console.log("Address associated with the wallet is:",this.nft_recv_addr )
		}
	    }
	    catch(error){
		console.log("Failed to fetch address", error)
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
	    catch(error){
		console.log("Failed to fetch of Reward address", e)
	    }
	},
	async fetchUtxo(e){
	    const S = await import('@emurgo/cardano-serialization-lib-browser/cardano_serialization_lib.js')
	    const _Buffer = (await import('buffer/')).Buffer

	    let utxo = {}
	    e.preventDefault()
	    try{
		if (cardano.isEnabled()){
		    let rawUtxo = await cardano.getUtxos()
		    console.log(rawUtxo)
		    const utxos = rawUtxo.map(u => S.TransactionUnspentOutput.from_bytes(_Buffer.from(u, 'hex')))
		    console.log(utxos)
		    for (let i = 0; i < utxos.length; i++) {
			const utxo = utxos[i];
			console.log(utxo.output().address())
			console.log(utxo.input())
			console.log(utxo.output().amount())
		    }
		}		    
	    }
	    catch(error){
		console.log("failed to fetch utxo",error)
	    }		
		
	}

	
    }
}
</script>

<style scoped>
image-holder {
  width: 600px;
  height: 400px;
  border: 5px dashed #f7a239;
}
</style>
