[Link to video](https://youtu.be/Aj40_2tCPQ0)

# complete-nft-app
 This app will take image layers designed by an artist and generate unique
 PNG images. These images are then indexed on the Inter-Planetary File System
 (IPFS) by uploading them to Pinata via Pinata's API. Next, a metadata file is
 created for each image, and then they are also uploaded to Pinata. Afterward,
 this program will take an NFT smart contract and compile it using the HardHat
 development environment. The smart contract can then be verified on Etherscan
 so that it can be interacted with. Finally, the program calls a function on
 the smart contract which sets the base Uniform Resource Identifier (URI) of
 each NFT. Now a smart contract lives on the blockchain that points to a URI
 on the IPFS, and when the mint function on the smart contract is called
 an NFT is sent to your wallet; the NFT can be viewed on OpeaSea (an NFT
 marketplace) where it can also be bought or sold; the NFT's characteristics,
 rarity, id number, URI, IPFS location, and smart contract can all be viewed via 
 the markeplace as well; additionally, funds sent to the smart contract (the 
 mint price) can be withdrawn by the contract owner.

 In order to run this program, you must have the following: (1) a free [MetaMask](https://metamask.io/)
 wallet set to Rinkeby Test Network, (2) a free [Etherscan](https://etherscan.io) account and API key,
 (3) a free [Alchemy](https://www.alchemy.com/) account and API key, (4) a free [Pinata](https://www.pinata.cloud/) account and API key,
 (5) Node.js and npm installed.

 No personally identifiable information is required for any of the aforementioned requirements. You can obtain free Rinkeby test Ethereum via a faucet
 such as [Chainlink Faucet](https://faucets.chain.link/rinkeby) or [Rinkeby Fauct](https://rinkebyfaucet.com/).
 Welcome to blockchain!

For security you must run `code .env` and enter your own credentials using the
following variable names (note the value of the variables are randomized and you
must enter your own values for this program to run):
```
PINATA_API_KEY = "ds5a64f56as4df65sad5"
PINATA_API_SECRET = "a5sd4f65a4sdf564as56df465asd4f564asd1v98sad1v56f156fd1h561fdfs5g"
RINKEBY_URL = "https://eth-rinkeby.alchemyapi.io/v2/465fg4h56f465fd4g5hs165df1sd6f5g"
RINKEBY_KEY = "65sd4f56g4sd56f1b56dfs6g4sd56fg4"
PRIVATE_KEY = "s56df4gh56sdf1g56dsf1g561sdf651g56sd1f651h56sfdf1561s5df65f4gs5f"
ETHERSCAN_API_KEY = '56SD4F564SDF5G4DS56F4G8FFS9D7FG4F5'
```

## Usage
**Run `npm install` in the terminal.**

Add your own image layer directories to `layers` directory or use the images
that are already included in the layers directory. These directories should be
the traits of your NFT and should contain inside images of uniform dimensions.

**Run `code src/config.js` and read first comment; follow its instructions.**

**Run `npm run build` in the terminal.**

**Run `code utils/upload_images.js` and adjust directory name per comment.**

**Run `npm run upload-images`.**
Copy the CID from the terminal.

**Run `code src/config.js`.**
Paste the CID into the variable called `imagesCID`. Now is also a good time to
update the rest of the description. Give your NFT collection a name and
description. This will appear on [OpenSea](https://opensea.io) (marketplace).

**Run `code utils/upload_metadata.js`.**
Adjust directory name per comment.

**Run `npm run set-metadata`.**

**Run `npm run upload-metadata`.**
Again, copy the CID from the terminal.

**Run `code utils/update_uri.js`.**
Paste the CID into the CID variable.

## The smart contract
The following instructions refer to my own smart contract. If you are using
artwork that you created then you will want to cnage the name *IceCreamFrens*
to a name that resembles your own collection. Also, you must delete
IceCreamFrens.Sol if you are going to create your own smart contract.

**Run `code IceCreamFrens.sol`.**
Review the contract. Modify it if you would like
to add functions that you think are critical to the success of the smart
contract, and you may also delete it and create your own if you would like;
however, be aware of the fact that the blockchain is immutable, and you will
to be able to fix the contract if it is broken.

**Run `npx hardhat compile`.**

*If you created your own smart contract or changed the name of the default
contract run `code utils/deploy.js` and change `contract_name` to reflect your
contract.*

**Run `npx hardhat run utils/deploy.js`**
Paste the contract address in the `contract_address` variable. Also, the pre-
ceding instruction applies to this file as well.

## Interacting with the smart contract
Please note the following steps depend on the blockchain network's traffic.
After the contract is deployed, you can go to [Etherscan](https://etherscan.io) and paste the address
in the search bar. If you see "There are no matching entries" under tran-
sactions then the network is congested. In this case, take a break, and then
back later to refresh the page. Once you see the deployment transaction you may
continue.

**Run `npx hardhat verify` with your pasted contract addresss.**

**Run `code utils/update_uri.js`.**
Paste the contract address in the `contract_address` variables and change
`contract_name` to the name of your contract if you made your own.

**Run `npx hardhat run utils/update_uri.js`**

Congratulations! You have created NFTs, developed a smart contract, and 
deployed them on the blockchain. Now you should mint one and check it out on
OpenSea! To do so, grab some free test Ethereum, and then head to Etherscan.io.
Navigate to the smart contract's page. You can do this by opening the MetaMask
wallet extension in the browser, clicking the hamburger menu, clicking on "View
Account on [Etherscan](https://etherscan.io), and then clicking on the transaction "Create: Contract"
in the "To" column. Alternatively, you can go to one of the files in which you
pasted the contract address, copying it, and then pasting it in the search bar
in Etherscan. Next, navigate to the "Contract" tab. Click on the button that
says "Write Contract". Now, click the button that says "Connect to Web3" and
approve the transactions that your MetaMask extension pops up. Click "2. mint"
on the webpage, enter a quanitity of NFTs to mint in the "_qty" field, and then
enter a value in the "mint" field equal to 0.01 * _qty (this is the amount of
test network Ethereum you are paying for the entire transaction at a rate of 
0.01 ETH per NFT). Lastly, go to [OpenSea Testnets](https://testnets.opensea.io), connect your wallet, and
then go to your profile. Look at your beauiful NFT!
