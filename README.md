# ERC721 Airdrop Contract Input Formatter
A simple python script to check Ethereum addresses &amp; duplicates before formatting for ERC721 Airdrops using Thirdweb's airdrop contract.

It uses no dependencies on purpose to be simple and quick. 

Thirdweb's contract can be found here: https://thirdweb.com/thirdweb.eth/AirdropERC721

Output format:

```
[
   {
       recipient: "0x123...",
       tokenId: 1 
   },
   {
       recipient: "0xabc...",
       tokenId: 2
   }
]
```
