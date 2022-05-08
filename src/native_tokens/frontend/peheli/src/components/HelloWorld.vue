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
            <b-img-lazy          :src="previewImage" class="image-holder" alt="Image Preview"></b-img-lazy>
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
import * as S from "@emurgo/cardano-serialization-lib-asmjs"


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
            },
            state: {
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
        async decodeHex(t){
            const Buffer = (await import('buffer/')).Buffer
            
            let cb = require('cborg')
            return cb["decode"](Buffer.from(t,'hex'))
        },
        async fetchBalance(e){
            console.log("Now fetching balance")
            e.preventDefault();
            try{
                var t = await cardano.getBalance()  
                this.balance = await this.decodeHex(t)
                console.log("decoded wallet amount", this.balance)
            }
            catch(e) {
                console.log("Failed to fetch balance", e)               
            }

        },
        async fetchNetwork(e){
            e.preventDefault()
            try{
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
            catch(error){
                console.log("Failed to fetch network id", error)
            }
        },
        async fetchAddress(e){
            const _Buffer = (await import('buffer/')).Buffer
            e.preventDefault()
            try{
                var t  = await cardano.getChangeAddress()
                this.nft_recv_addr = await S.Address.from_bytes(_Buffer.from(t, 'hex')).to_bech32()
                console.log("Address associated with the wallet is:",this.nft_recv_addr )
            }
            catch(error){
                console.log("Failed to fetch address", error)
            }
        },

        /**
         * Gets the Network ID to which the wallet is connected
         * 0 = testnet
         * 1 = mainnet
         * Then writes either 0 or 1 to state
         * @returns {Promise<void>}
         */
        async getNetworkId(e){
            try {
                const networkId = await this.API.getNetworkId();
                this.setState({networkId})
                
            } catch (err) {
                console.log(err)
            }
        },       

        /**
         * Checks if a connection has been established with
         * the wallet
         * @returns {Promise<boolean>}
         */
        async checkIfWalletEnabled(e){
            
            let walletIsEnabled = false;
            
            try {                
                this.state.walletIsEnabled = await window.cardano.nami.isEnabled();                
            } catch (err) {
                console.log(err)
            }
            
            return walletIsEnabled
        },
        
        async enableWallet(e){
            try {                                
                await this.checkIfWalletEnabled();
                await cardano.nami.enable();
                await this.getNetworkId();
                this.walletIsEnabled = true
            }
            catch (err) {
                console.log(err)
            }
        },
        
        
        async fetchUtxo(e){
            const _Buffer = (await import('buffer/')).Buffer

            let wallet_utxos = []
            e.preventDefault()
            try{
                let rawUtxo = await cardano.getUtxos()
                console.log(rawUtxo)
                rawUtxo.map(u => {
                    const utxo = S.TransactionUnspentOutput.from_bytes(_Buffer.from(u, 'hex'))
                    const input = utxo.input();
                    const txid = _Buffer.from(input.transaction_id().to_bytes(), "utf8").toString("hex");
                    const txindx = input.index();
                    const output = utxo.output();
                    const amount = output.amount().coin().to_str(); // ADA amount in lovelace
                    const multiasset = output.amount().multiasset();
                    let multiAssetStr = "";

                    if (multiasset) {
                        const keys = multiasset.keys() // policy Ids of thee multiasset
                        console.log(keys)
                        // keys.map(policyId => {
                        //     const policyIdHex = _Buffer.from(policyId.to_bytes(), "utf8").toString("hex");
                        //     const assets = multiasset.get(policyId)
                        //     const assetNames = assets.keys();

                        //     assetNames.map(assetName => {
                        //         const assetNameString = Buffer.from(assetName.name(),"utf8").toString();
                        //         const assetNameHex = Buffer.from(assetName.name(),"utf8").toString("hex")
                        //         const multiassetAmt = multiasset.get_asset(policyId, assetName)
                        //         multiAssetStr += `+ ${multiassetAmt.to_str()} + ${policyIdHex}.${assetNameHex} (${assetNameString})`
                        //     })
                        // })
                    }

                    const obj = {
                        txid: txid,
                        txindx: txindx,
                        amount: amount,
                        str: `${txid} #${txindx} = ${amount}`,
                        multiAssetStr: multiAssetStr,
                        TransactionUnspentOutput: utxo
                    }

                    console.log(obj)
                    wallet_utxos.push(obj)
                })
                this.state.Utxos = wallet_utxos
            }
            catch(error){
                console.log("failed to fetch utxo",error)
            }           
                
        },

        /**
         * The collateral is need for working with Plutus Scripts
         * Essentially you need to provide collateral to pay for fees if the
         * script execution fails after the script has been validated...
         * this should be an uncommon occurrence and would suggest the smart contract
         * would have been incorrectly written.
         * The amount of collateral to use is set in the wallet
         * @returns {Promise<void>}
         */
        async getCollatera(e){
            
            let CollatUtxos = [];
            
            try {
                
                let collateral = [];                
                collateral = await cardano.getCollateral();
                
                for (const x of collateral) {
                    const utxo = TransactionUnspentOutput.from_bytes(Buffer.from(x, "hex"));
                    CollatUtxos.push(utxo)
                // console.log(utxo)
                }
                this.state.CollatUtxos = CollatUtxos
                
            } catch (err) {
                console.log(err)
            }            
        },

        /**
         * Get the address from the wallet into which any spare UTXO should be sent
         * as change when building transactions.
         * @returns {Promise<void>}
         */
        async getChangeAddress(e){
            try {
                const raw = await cardano.getChangeAddress();
                const changeAddress = Address.from_bytes(Buffer.from(raw, "hex")).to_bech32()
                this.state.changeAddress = changeAddress
            }
            catch (err)
            {
                console.log(err)
            }
        },

        /**
         * This is the Staking address into which rewards from staking get paid into
         * @returns {Promise<void>}
         */
        async getRewardAddresses(e){
            
            try {
                const raw = await cardano.getRewardAddresses();
                const rawFirst = raw[0];
                const rewardAddress = Address.from_bytes(Buffer.from(rawFirst, "hex")).to_bech32()
                // console.log(rewardAddress)
                this.state.rewardAddress = rewardAddress                
            } catch (err) {
                console.log(err)
            }
        },

        /**
         * Gets previsouly used addresses
         * @returns {Promise<void>}
         */
        async getUsedAddresses(e){
            
            try {
                const raw = await cardano.getUsedAddresses();
                const rawFirst = raw[0];
                const usedAddress = Address.from_bytes(Buffer.from(rawFirst, "hex")).to_bech32()
                this.usedAddress = usedAddress                
            } catch (err) {
                console.log(err)
            }
        },


        /**
         * Refresh all the data from the user's wallet
         * @returns {Promise<void>}
         */
        async refreshData(e){
            
            //this.generateScriptAddress()
            
            try{
                const walletFound = this.checkIfWalletFound();
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
