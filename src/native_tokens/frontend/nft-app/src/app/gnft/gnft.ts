export class NFT {
    public assetName: string;
    public assetAmount: number;
    public mintingCost: number;
    public tags: string;
    public recvAddress: string;
    public url: string;


    constructor(name:string, amount:number, mcost:number, tags:string, addr:string, url:string){
	console.log(`name:${name}, amount:${amount}, mcost:${mcost}, tags:${tags}, addr:${addr}, url:${url}`)
	this.assetName = name;
	this.assetAmount = amount
	this.mintingCost = mcost
	this.tags = tags;
	this.recvAddress = addr;
	this.url = url;	
    }
}
