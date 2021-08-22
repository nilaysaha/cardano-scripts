export class NFTPay {
    public assetID: string;
    public mintingCost: number;
    public currency: string;  //for paying the mintingCost
    public payAddr: string;

    constructor(assetID:string, mintingCost:number, currency:string,  payAddr:string){
	console.log(`assetID:${assetID}, mintingCost:${mintingCost}, payaddr:${payAddr}`)
	this.assetID = assetID;
	this.mintingCost = mintingCost;
	this.currency = currency;
	this.payAddr = payAddr;
    }
}
