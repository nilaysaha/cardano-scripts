export class NFT {

  constructor(
      public assetName: string,
      public assetAmount: number,
      public mintingCost: number,
      public tags: string,
      public recvAddress: string,
      public url: string
  ) {  }

}
