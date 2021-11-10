#!/usr/bin/env node


const CardanocliJs = require("cardanocli-js");
const shelleyGenesisPath = "../../tconfig/testnet-shelley-genesis.json"

class Transaction{
    constructor(){
	const options={
	    "shelleyGenesisPath": shelleyGenesisPath,
	    "network": "testnet-magic 1097911063"
	}	
	this.ccjs = new CardanocliJs(options);
    }

    nft_options(uuid, name, amount, metadata={}){
	return {
	    "uuid": uuid,
	    "name": name,
	    "amount": amount,
	    "metadata": metadata
	}
    }

    _construct_tx_in(payment_addr=[]){
	let output = []
	for(let t in payment_addr){
	    output.push(this.ccjs.queryUtxo(payment_addr[t]))
	}
	return output
    }

    _construct_tx_out(output=[]){
	let tx_output = []
	for(let i in output){
	    let obj = {}
	    obj['address'] = i["address"]
	    obj["value"] = {}
	    obj['value'][i["coinname"]]   = i["amount"] 
	    tx_output.push(obj)
	}
	return tx_output
    }

    
    _construct_mint(){
	
    }

    //output = [{}] each entry should be of form: {"coinname":"lovelace", "amount":10000, "address":"b1dd...."}
    create_raw_transactions(input_addr=[],output=[]){
	let tx = {
	    txIn: this._construct_tx_in(input_addr)
	    txOut: this._construct_tx_out(output),
	    certs: [{ cert: stakeCert }],
	    witnessCount: 2,
	    invalidBefore:0,
	    invalidAfter:0,
	    fee:0,
	    metadata:{}
	};
	
    }
    
    calculate_min_fees(){
	
    }
        

    sign_transactions(){
	
    }

    submit_transaction(){
	
    }
}
