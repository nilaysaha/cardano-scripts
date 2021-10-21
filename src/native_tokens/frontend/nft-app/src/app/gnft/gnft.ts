export class NFT {
    public assetName: string;
    public assetAmount: number;
    public tags: string;
    public recvAddr: string;
    public url: string;


    constructor(name:string, amount:number,  tags:string, addr:string, url:string){
	console.log(`name:${name}, amount:${amount}, tags:${tags}, addr:${addr}, url:${url}`)
	this.assetName = name;
	this.assetAmount = amount
	this.tags = tags;
	this.recvAddr = addr;
	this.url = url;	
    }
}
