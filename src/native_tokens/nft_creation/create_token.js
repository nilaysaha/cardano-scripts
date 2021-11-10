const CardanocliJs = require("cardanocli-js");
const shelleyGenesisPath = "../../tconfig/testnet-shelley-genesis.json"


class CreateToken{
    constructor(token_name="REITNFT"){
	const options={
	    "shelleyGenesisPath": shelleyGenesisPath,
	    "network": "testnet-magic 1097911063"
	}	
	this.token_name = token_name
	this.ccjs = new CardanocliJs(options);
    }
    
    prepare_wallet(account){
	try{
	    let paymentKeys = this.ccjs.addressKeyGen(account);
	    let stakeKeys   = this.ccjs.stakeAddressKeyGen(account);
	    let stakeAddr   = this.ccjs.stakeAddressBuild(account);
	    let paymentAddr = this.ccjs.addressBuild(account,{
		"paymentVkey": paymentKeys.vkey,
		"stakeVkey": stakeKeys.vkey 
	    });
	    return this.ccjs.wallet(account);
	}
	catch(e){
	    console.log(`Failed to create payment address for wallet:${account}`, e)
	}
    }

    prepare_policy(policy_account){
	try{
	    let protocolParams = this.ccjs.queryProtocolParameters()
	    let policyKey = this.ccjs.addressKeyGen(policy_account)
	    let policyKeyHash = this.ccjs.addressKeyHash(policy_account)
	    let policy_script = {
		"keyHash": policyKeyHash,
		"type": "sig"
	    }
	    return {
		"protocolParams": protocolParams,
		"policy_script": policy_script
	    }
	}
	catch(e){
	    console.log(e)
	}
    }    
    
}

if (require.main === module){
    a = new CreateToken()
    let wallet = a.prepare_wallet("nsaha")
    let policy = a.prepare_policy("tada")

    console.log(wallet.paymentAddr)
    console.log(policy.protocolParams)
}
