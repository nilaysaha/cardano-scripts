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
	},
	state: {
	    networkId: undefined,
	    walletHandle: undefined,
            selectedTabId: "1",
            whichWalletSelected: "nami",
            walletFound: false,
            walletIsEnabled: false,
            walletName: undefined,
            walletIcon: undefined,
            walletAPIVersion: undefined,
            networkId: undefined,
            Utxos: undefined,
            CollatUtxos: undefined,
            balance: undefined,
            changeAddress: undefined,
            rewardAddress: undefined,
            usedAddress: undefined,
            txBody: undefined,
            txBodyCborHex_unsigned: "",
            txBodyCborHex_signed: "",
            submittedTxHash: "",
            addressBech32SendADA: "addr_test1qrt7j04dtk4hfjq036r2nfewt59q8zpa69ax88utyr6es2ar72l7vd6evxct69wcje5cs25ze4qeshejy828h30zkydsu4yrmm",
            lovelaceToSend: 3000000,
            assetNameHex: "4c494645",
            assetPolicyIdHex: "ae02017105527c6c0c9840397a39cc5ca39fabe5b9998ba70fda5f2f",
            assetAmountToSend: 5,
            addressScriptBech32: "addr_test1wpnlxv2xv9a9ucvnvzqakwepzl9ltx7jzgm53av2e9ncv4sysemm8",
            datumStr: "12345678",
            plutusScriptCborHex: "4e4d01000033222220051200120011",
            transactionIdLocked: "",
            transactionIndxLocked: 0,
            lovelaceLocked: 3000000,
            manualFee: 900000,
        },
	protocolParams: {
            linearFee: {
                minFeeA: "44",
                minFeeB: "155381",
            },
            minUtxo: "34482",
            poolDeposit: "500000000",
            keyDeposit: "2000000",
            maxValSize: 5000,
            maxTxSize: 16384,
            priceMem: 0.0577,
            priceStep: 0.0000721,
            coinsPerUtxoWord: "34482",
        }	
    }),
    methods:{
	async fetchBalance(){
	    this.balance.amount = await cardano.getBalance()
	},
	async checkIfWalletFound(wallet_name){
	    let walletfound = true
	    	    
	},
	async checkIfWalletEnabled(){
	    try{
		return await window.cardano.nami.isEnabled();
	    }
	    catch(err){
		console.log(err)
	    }
	},
	async generateScriptAddress() {
	    
	},
	async enableWallet(wallet_name){
	    try{
		this.state.walletHandle =  await window.cardano.nami.enable()
		this.checkIfWalletEnabled()
	    }
	    catch(err){
		console.log(err)
	    }
	},
	async getWalletHandleVersion(){
	    
	},
	async getWalletName(){
	    return window.cardano.nami.name
	},
	/*
	 * Gets the UTXOs from the user's wallet and then
	 * stores in an object in the state
	 * @returns {Promise<void>}
	 */
	async getUtxos() {
	    try{
		const rawUtxos = await this.API.getUtxos();
		console.log(rawUtxos)
	    }
	    catch(err){
		console.log(err)
	    }
	},
	async getCollateral() {
	    
	},
	async getBalance() {
	    this.state.balance = await cardano.getBalance()
	},
	async getChangeAddress(){
	    
	},
	async getRewardAddresses() {
	    
	},
	async getUsedAddresses(){
	    
	},
	async getNetworkId(){
	    try {
		const networkId = await this.walletHandle.getNetworkId();
		this.state.networkId = networkId		
            } catch (err) {
		console.log(err)
            }
	},  
	async refreshData() => {
            this.generateScriptAddress()

            try{
		const walletFound = this.checkIfWalletFound(wallet_selected);
		if (walletFound) {
                    await this.enableWallet();
                    await this.getAPIVersion();
                    await this.getWalletName();
                    await this.getUtxos();
                    await this.getCollateral();
                    await this.getBalance();
                    await this.getChangeAddress();
                    await this.getRewardAddresses();
                    await this.getUsedAddresses();
		}
            } catch (err) {
		console.log(err)
            }
	},
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
