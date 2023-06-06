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
            <label>Network ID</label>
            <md-input v-on:click="fetchNetwork" v-model="network" readonly></md-input>
          </md-field>

          <md-field>
            <label>utxo</label>
            <md-input v-on:click="fetchUtxo" v-model="utxo" readonly></md-input>
          </md-field>

          <div>
            <small>Flat</small>
            <b-button class="md-primary padd" v-on:click="getCollateral">Collateral</b-button> &nbsp;&nbsp
            <b-button class="md-primary padd" v-on:click="getRewardAddresses">RewardAddress</b-button>  &nbsp;&nbsp
            <b-button class="md-accent padd" v-on:click="getChangeAddress">ChangeAddress</b-button> &nbsp;&nbsp
            <b-button class="md-accent padd" v-on:click="genJWTtoken">genJWTtoken</b-button> &nbsp;&nbsp 
            <b-button class="md-accent padd" v-on:click="buildSendADATransaction">BuildTransaction</b-button> &nbsp;&nbsp
            <b-button class="md-accent padd" v-on:click="MeshNFT">meshBuild</b-button> &nbsp;&nbsp
          </div>
          
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
import * as S from "@emurgo/cardano-serialization-lib-asmjs";
import Web3Token from 'web3-cardano-token-cportal/dist/browser';
//import * as M from "@meshsdk/core"

export default {
    name: 'Intro',
    props: ['API'],
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
            DEFAULT_SESSION_LENGTH_IN_DAYS: 365,
            mainProps: {
                center: true,
                fluidGrow: true,
                blank: true,
                blankColor: '#bbb',
                width: 600,
                height: 400,
                class: 'my-5'
            },
            txBuilder: undefined,
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
                rewardAddredss: undefined,
                usedAddress: undefined,
                txBody: undefined,
                txBodyCborHex_unsigned: "",
                txBodyCborHex_signed: "",
                submittedTxHash: "",
                addressBech32SendADA: "addr_test1qr0pjr2nu5qmf2szd0gqqpdlk3hrv7vh4ty2m9fapm4npqdsqj43gyduezd0crpju8l9ps4fuu94z0rp86t00c4m3nzsguzzhc",
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
                var t = await this.API.getBalance()  
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
                var id = await this.API.getNetworkId()
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
                console.log(this.API)
                var t  = await this.API.getChangeAddress()
                console.log(t)
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
                const networkId = await this.API.getNetworkId() ;
                this.networkId = networkId                
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
            
            try {                
                this.state.walletIsEnabled = await window.this.API.nami.isEnabled();                
                return this.state.walletIsEnabled
            } catch (err) {
                console.log(err)
            }            
        },
        
        async enableWallet(e){
            try {                                
                await this.checkIfWalletEnabled();
                if (! this.state.walletIsEnabled){
                    await this.API.nami.enable();
                    this.state.walletIsEnabled = true
                }
                await this.getNetworkId();
                console.log(this.networkId)
            }
            catch (err) {
                console.log(err)
            }
        },
        
        isHex(h){
            var re = /[0-9A-Fa-f]{6}/g;
            if(re.test(h)) {
                alert('valid hex');
                return true
            } else {
                alert('invalid');
                return false
            }
        },
        
        async addrToPubKeyHash(bech32Addr) {
            const _Buffer = (await import('buffer/')).Buffer
            
            const addr_bytes = await S.Address.from_bech32(bech32Addr)
            const addr_hbytes  = await S.BaseAddress.from_address(addr_bytes).payment_cred().to_keyhash().to_bytes()
            const pkh = _Buffer.from(addr_hbytes).toString("hex")
            return pkh
        },
        
        async fetchUtxo(e){
            const _Buffer = (await import('buffer/')).Buffer
            
            let wallet_utxos = []
            e.preventDefault()
            
            const pkh = await this.addrToPubKeyHash(this.nft_recv_addr)
            console.log(`Public key hash of ${this.nft_recv_addr} is ${pkh}`)
            
            try{
                let rawUtxo = await this.API.getUtxos()
                console.log(rawUtxo)
                
                rawUtxo.map(async (u) => {
                    
                    //console.log(`checking if ${u} is hexadecimal value: ${this.isHex(u)}`)
                    
                    const utxo = S.TransactionUnspentOutput.from_bytes(_Buffer.from(u, 'hex'))
                    
                    const input = utxo.input();
                    const txid = _Buffer.from(input.transaction_id().to_bytes(), "utf8").toString("hex");
                    const txindx = input.index();
                    
                    const output = utxo.output();
                    
                    console.log("output utxo")
                    console.log(output)
                    
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
                        TransactionUnspentOutput: utxo,
                        txid: txid,
                        txindx: txindx,
                        amount: amount,
                        str: `${txid} #${txindx} = ${amount}`,
                        multiAssetStr: multiAssetStr   
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
        async getCollateral(e){
            
            let CollatUtxos = [];
            
            try {
                
                let collateral = [];                
                collateral = await this.API.getCollateral();
                
                for (const x of collateral) {
                    const utxo = S.TransactionUnspentOutput.from_bytes(Buffer.from(x, "hex"));
                    CollatUtxos.push(utxo)
                    console.log(utxo)
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
                const raw = await this.API.getChangeAddress();
                const changeAddress = S.Address.from_bytes(Buffer.from(raw, "hex")).to_bech32()
                this.state.changeAddress = changeAddress
                return changeAddress
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
                const raw = await this.API.getRewardAddresses();
                const rawFirst = raw[0];
                const rewardAddress = S.Address.from_bytes(Buffer.from(rawFirst, "hex")).to_bech32()
                console.log(rewardAddress)
                
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
                const raw = await this.API.getUsedAddresses();
                const rawFirst = raw[0];
                const usedAddress = S.Address.from_bytes(Buffer.from(rawFirst, "hex")).to_bech32()
                this.usedAddress = usedAddress
                console.log(usedAddress)
            } catch (err) {
                console.log(err)
            }
        },
        
        async generateMessagingKeys(e){
            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "ECDH",
                    namedCurve: "P-256",
                },
                true,
                ["deriveKey", "deriveBits"]
            );
            
            const publicKeyJwk = await window.crypto.subtle.exportKey(
                "jwk",
                keyPair.publicKey
            );
            
            const privateKeyJwk = await window.crypto.subtle.exportKey(
                "jwk",
                keyPair.privateKey
            );
            
            return { publicKeyJwk, privateKeyJwk };
        },
        
        /*
          Localstorage of items required for storage.
          where method: 'get', 'set', 'del'
        */
        async lstore(key,value,method){
            
            try{
                switch (method) {
                case 'get':
                    localStorage.getItem(key)
                    break;
                case 'set':
                    localStorage.setItem(key, value)
                    break
                case 'del':
                    localStorage.removeItem(key)
                    break;
                default:
                    console.log('did not find proper method get, set, del for localstorage')
                    throw new Error(`Method:${method} not found.`)
                    
                }
            }
            catch(err){
                console.error('Could not process localstorage data',err)
                throw new Error('Could not process localstorage data',err)
            }
            
        },
        
        async genJWTtoken(e){
            try{
                const Buffer = (await import('buffer/')).Buffer
                
                const saddress = await this.API.getRewardAddresses()
                
                const paddress = await this.getChangeAddress(e)
                
                const expiry_date = Math.floor(Date.now() / 1000) + 60 * 60 * 24 * this.DEFAULT_SESSION_LENGTH_IN_DAYS
                
                //The "type" of message can be: "walletLogin", "DaoCreation", "DaoMembership", "HouseFractionalise" etc.
                
                const msgKPairs = await this.generateMessagingKeys()
                
                const msg = {
                    'type': "walletLogin",
                    'chainID': (await this.API.getNetworkId()).toString(),
                    'msgPublicKey': JSON.stringify(msgKPairs.publicKeyJwk)
                };
                
                //store the key pairs.
                await this.lstore('ecdh_private_key', msgKPairs.privateKeyJwk, 'set')
                await this.lstore('ecdh_public_key', msgKPairs.publicKeyJwk, 'set')
                
                const wallet_signing_function = async (msg) => {
                    const Buffer = (await import('buffer/')).Buffer
                    
                    const paddress = await this.API.getRewardAddresses();
                    const msg_hex = Buffer.from(JSON.stringify(msg), 'utf-8').toString("hex")
                    
                    const signdata = await this.API.signData(saddress[0], msg_hex)
                    console.log(signdata)
                    return signdata
                }
                
                // const signed_data = await this.API.signData(saddress[0], msg_hex)                
                // console.log(signed_data)                
                //const token = await Web3Token.sign(m => this.API.signData(saddress[0], msg_hex), '1d', )
                
                const nonce = 123 //to be finally obtained via api using the wallet address
                const token = await Web3Token.sign(wallet_signing_function, '365d', msg, nonce )
                console.log(token)
            }
            catch(err){
                console.error(err)
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
        },
        
        
        
        async initTransactionBuilder(e){
            console.log(S)
            
            this.txBuilder = S.TransactionBuilder.new(
                S.TransactionBuilderConfigBuilder.new()
                    .fee_algo(S.LinearFee.new(S.BigNum.from_str(this.protocolParams.linearFee.minFeeA), S.BigNum.from_str(this.protocolParams.linearFee.minFeeB)))
                    .pool_deposit(S.BigNum.from_str(this.protocolParams.poolDeposit))
                    .key_deposit(S.BigNum.from_str(this.protocolParams.keyDeposit))
                    .coins_per_utxo_word(S.BigNum.from_str(this.protocolParams.coinsPerUtxoWord))
                    .max_value_size(this.protocolParams.maxValSize)
                    .max_tx_size(this.protocolParams.maxTxSize)
                    .prefer_pure_change(true)
                    .build()
            );
            
        },
        
        /**
         * Builds an object with all the UTXOs from the user's wallet
         * @returns {Promise<TransactionUnspentOutputs>}
         */
        async getTxUnspentOutputs(){
            
            // create TransactionUnspentOutputs for 'add_inputs_from' function
            const utxoOutputs = await S.TransactionUnspentOutputs.new();            
            const rawUtxo = await this.API.getUtxos()
            
            
            const utxosFromWalletConnector = rawUtxo.map(utxo => {
                
                let t = S.TransactionUnspentOutput.from_bytes(Buffer.from(utxo, 'hex'))
                utxoOutputs.add(t);
                
            })
            
            return utxoOutputs;
        },
        
        async generate_timelockScript(){
            const result = await fetch('https://api.koios.rest/api/v0/tip');
            console.log(result);
            const nslot = result.abs_slot+10000
            const timelock = this.API.TimelockExpiry.new(nslot);
            const timelockScript = this.API.NativeScript.new_timelock_expiry(timelock);
            
            return timelockScript
        },
        
        async getWalletWasmAddr(){
            const Buffer = (await import('buffer/')).Buffer
            
            const changeAddress = await this.API.getChangeAddress();
            console.log(`raw change address is:${changeAddress}`)
            const wasmChangeAddress = await S.Address.from_bytes(Buffer.from(changeAddress, 'hex'))
            
            return wasmChangeAddress
        },
        
        async generate_pubkeyscript(){
            
            const wasmChangeAddress = await this.getWalletWasmAddr()
            const baseAddress = await S.BaseAddress.from_address(wasmChangeAddress);            
            const scriptPubKey = await S.ScriptPubkey.new(baseAddress.payment_cred().to_keyhash());            
            
            const pubKeyScript = await S.NativeScript.new_script_pubkey(scriptPubKey);
            
            console.log(`pubkeyscript is`)
            console.log(pubKeyScript)
            
            return pubKeyScript
        },
        
        async txBuilder_add_nft_tx(pubKeyScript, metadataObj, NFTIndex){
            
            const wasmChangeAddress = await this.getWalletWasmAddr()

            this.txBuilder.add_mint_asset_and_output_min_required_coin(
                pubKeyScript,
                await S.AssetName.new(Buffer.from('NFT' + NFTIndex.toString(), 'utf8')),
                await S.Int.new_i32(1),
                S.TransactionOutputBuilder.new().with_address(wasmChangeAddress).next()
            );
            
            this.txBuilder.add_json_metadatum(S.BigNum.from_str('721'), JSON.stringify(metadataObj));
        },
        
        async tx_Nft_Prepare(NFTIndex){
            
            //TO DO: ALSO ADD REITCIRCLES BACKEND SCRIPT PUBLIC KEY, SO THAT ISSUANCE OF NFT CAN BE PROVEN.
            // const appScript = Loader.Cardano.ScriptPubkey.new(appKeyHash);
            // const appNativeScript = Loader.Cardano.NativeScript.new_script_pubkey(appScript);                        
            
            // const timelockScript = generate_timelockScript()
            const pubKeyScript = await this.generate_pubkeyscript()            
            
            const policyScripts = await S.NativeScripts.new();
            policyScripts.add(pubKeyScript);
            //policyScripts.add(timelockScript);
            
            console.log('policyScripts :>> ', policyScripts);
            
            const policyId = Buffer.from(pubKeyScript.hash(0).to_bytes()).toString('hex');
            console.log('policyId :>> ', policyId);
            
            const metadataObj = {
                [policyId]: {
                    ['NFT' + NFTIndex.toString()]: {
                        description: 'Test2',
                        name: 'Test token2',
                        id: NFTIndex.toString(),
                        image: 'ipfs://QmUb8fW7qm1zCLhiKLcFH9yTCZ3hpsuKdkTgKmC8iFhxV8',
                    },
                },
            };
            
            console.log(metadataObj)
            
            await this.txBuilder_add_nft_tx(pubKeyScript, metadataObj, NFTIndex)
        },
        
        // THIS FUNCTION NEEDS TO BE REPLICATED IN THE BACKEND.
        // async tx_create_clean_witness_backend_sample(txBuilder, prvKey){
        
        //     // create empty witness array
        //     const witnesses = await S.TransactionWitnessSet.new();
        //     const vkeyWitnesses = await S.Vkeywitnesses.new();
        
        //     // once the transaction is ready, we build it to get the tx body without witnesses
        //     const txBody = txBuilder.build();
        //     const txHash = await S.hash_transaction(txBody);
        
        //     // add keyhash witnesses
        //     const vkeyWitness = CardanoWasm.make_vkey_witness(txHash, prvKey);
        //     vkeyWitnesses.add(vkeyWitness);
        //     witnesses.set_vkeys(vkeyWitnesses);
        
        //     return witnesses
        // },

        async tx_prepare_witness_set_v1(policy){

            const txBody = this.txBuilder.build();
            const txHash = await S.hash_transaction(txBody);
            
            // sign the tx using the policy key and main key
            const witnesses = await S.TransactionWitnessSet.new();
            const vkeyWitnesses = await S.Vkeywitnesses.new();

            const policy_hash = await S.make_vkey_witness(txHash, policy.privateKey) 
            
            vkeyWitnesses.add();
            vkeyWitnesses.add(CardanoWasm.make_vkey_witness(txHash, privateKey));
            witnesses.set_vkeys(vkeyWitnesses);
            witnesses.set_native_scripts;
            const witnessScripts = CardanoWasm.NativeScripts.new();
            witnessScripts.add(mintScript);
            witnesses.set_native_scripts(witnessScripts);
            
        },
        
        async tx_prepare_witness_Set(){
            
            // Tx witness
            const txWitnessSet = await S.TransactionWitnessSet.new();
            
            const unsignedTxHex = Buffer.from(this.txBuilder.build_tx().to_bytes()).toString("hex")
            const encodedTxVkeyWitnesses = await this.API.signTx(unsignedTxHex, true)
            console.log('witnessSetHex :>> ', encodedTxVkeyWitnesses);
                        
            // decode witness-set produced by signature
            const txVkeyWitnesses = await S.TransactionWitnessSet.from_bytes(
                Buffer.from(encodedTxVkeyWitnesses, "hex")
            );
            
            txWitnessSet.set_vkeys(txVkeyWitnesses.vkeys());
            
            return txWitnessSet
        },
        
        /**
         * The transaction is build in 3 stages:
         * 1 - initialize the Transaction Builder
         * 2 - Add inputs and outputs
         * 3 - Calculate the fee and how much change needs to be given
         * 4 - Build the transaction body
         * 5 - Sign it (at this point the user will be prompted for
         * a password in his wallet)
         * 6 - Send the transaction
         * @returns {Promise<void>}
         */
        
        async buildSendADATransaction(e){

            const Buffer = (await import('buffer/')).Buffer
            
            //Step 1: Initialise the transaction
            this.initTransactionBuilder(e);          
            const shelleyOutputAddress = await S.Address.from_bech32(this.state.addressBech32SendADA);
            const shelleyChangeAddress = await S.Address.from_bech32(this.nft_recv_addr);
            
            
            //Step 1: Add output of the transaction fee to the platform wallet.
            this.txBuilder.add_output(
                S.TransactionOutput.new(
                    shelleyOutputAddress,
                    S.Value.new(S.BigNum.from_str(this.state.lovelaceToSend.toString()))
                ),
            );
            
            //Step 2: Add nft creation transaction and transfer of same to user wallet
            // await this.tx_Nft_Prepare(1)                                   
            // console.log(this.txBuilder)
            
            //Step 3: Add input utxos
            const txUnspentOutputs = await this.getTxUnspentOutputs();
            this.txBuilder.add_inputs_from(txUnspentOutputs, 2)
            
            
            // Step 4: calculate the min fee required and send any change to an address
            this.txBuilder.add_change_if_needed(shelleyChangeAddress)
            
            
            //Step 5: create witness set.
            const txWitnessSet = await this.tx_prepare_witness_Set()
            
            //Step 6: Sign the transaction            
            const signedTx = await S.Transaction.new(
                this.txBuilder.build_tx().body(),
                txWitnessSet
            );

            console.log(signedTx)
            
            // Step 6: Submit transaction
            const submittedTxHash = await this.API.submitTx(Buffer.from(signedTx.to_bytes(), "utf8").toString("hex"));
            console.log(`submitted transaction hash:${submittedTxHash}`)
            
            //this.setState({submittedTxHash});
            
        },
        
        async meshNFT(e){
            // const blockchainProvider = new M.BlockfrostProvider(process.env.VUE_APP_BLOCKFROST_PROJECT_ID);

            // const walletAddress = await this.API.getChangeAddress();
            // const forgingScript = M.ForgeScript.withOneSignature(walletAddress);

            // console.log(`obtained payment address wallet:${walletAddress}`)
            
            // const assetMetadata1 = {
            //     name: 'Mesh Token',
            //     image: 'ipfs://QmRzicpReutwCkM6aotuKjErFCUD213DpwPq6ByuzMJaua',
            //     mediaType: 'image/jpg',
            //     description: 'This NFT is minted by Mesh (https://meshjs.dev/).',
            // };
            // const asset1 = {
            //     assetName: 'MeshToken',
            //     assetQuantity: '1',
            //     metadata: assetMetadata1,
            //     label: '721',
            //     recipient: 'addr_test1vpvx0sacufuypa2k4sngk7q40zc5c4npl337uusdh64kv0c7e4cxr'
            // };
            
            // const tx = new Transaction({ initiator: wallet });
            // tx.mintAsset(forgingScript, asset1);
            
            const unsignedTx = await tx.build();
            // const signedTx = await wallet.signTx(unsignedTx);
            // const txHash = await wallet.submitTx(signedTx);
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
