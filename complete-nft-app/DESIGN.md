# complete-nft-app
This project is a compilation of three other programs and my own Solidity
smart contract. Technically, this was implemented by adapting, modifying, and
adding to an NFT generator app, a Pinata uploader app, and a Hardhat smart
contract deployment app, as well as the development of my own
Solidity code. Ultimately, I built on top of three existing apps, developed
a single `package.json` file, and engineered a Solidity smart contract.

The original NFT generator app that I modified was built to generate NFTs comp-
atible for the either the Ethereum or Solana blockchain. Since I am only inter-
ested in deploying a smart contract to the Ethereum blockchain, I removed all
functions and variables which existed solely for deployment on the Solana 
blockchain. Additionally, I removed extraneous scripts which to decrease the
overall size of the program, keeping only the `set_metadata.js` script. In the
`config.js` file, I rearranged the code to make creation of NFTs in production
more intuitive. I also fixed a deprecated function (according to the Node.js
documentation, `rmSync` should now be used instead of `rmdirSync`). The orig-
inal program also had a function to generate GIFs, including an additional in-
stalled dependency, which I removed. Finally, I modified the program's initial
handling of the NFTs IPFS URI. Originally, users were expected to enter the
entire URI, which is usually a string that looks like
`ipfs://QmZPmyDfoj9Sw9gURfPcLz928B2zuqS33cTeDZuiTnzP2L`. This can be confusing,
for there are two URI's that exist when developing NFTs, they are each used
in a different stage of the development, and they each have different formatting
requirements. For context, the URI that is used in the generator is written
into the NFT's JSON file. Each NFT's JSON file will have the base URI followed
by a forward slash, the ID of the NFT, and then the extension of the file type
of the NFT (which is .png in my example). If you have an NFT in your wallet and
connect to OpenSea, the website will see ERC-721, a.k.a. NFT, tokens that you
have in your wallet (if you have any) as well as the associated smart contract.
The smart contract also has a URI, and each NFT token has its own URI similar
to the previous URI, except the URI's provided by the smart contract have a
different CID (the long hash) and end in `.JSON`. The URI from the smart contract
points to the NFTs JSON file on the IPFS, which in turn points to the image's
URI on the IPFS. This is how OpenSea shows an NFT's image and metadata.
However, the URI in the metadata must by formatted without the forward slash
at the end of the URI, while the URI in the smart contract must be programmed
with a forward slash at the end of the URI. Additionally, the URI provided by
OpenSea upon clicking on an NFT's ID looks like this:
opensea.mypinata.cloud/ipfs/QmZPmyDfoj9Sw9gURfPcLz928B2zuqS33cTeDZuiTnzP2L/1.png
while the Pinata provided URI looks like this:
gateway.pinata.cloud/ipfs/QmZPmyDfoj9Sw9gURfPcLz928B2zuqS33cTeDZuiTnzP2L/1.png
and the actual IPFS URI looks like this:
ipfs.io/ipfs/QmZPmyDfoj9Sw9gURfPcLz928B2zuqS33cTeDZuiTnzP2L/1.png
As a result of this there is a lot of room for error, so I added to the generator
app such that it only requires the CID of the of the IPFS URI, and then it gen-
erates the URI on its own. The files for this sub-program are `config.js`,
`main.js`, `blend-mode.js`, and `set_metadata.js`.

I did not do much to change the Pinata uploader app; in fact, I only used two
files from the original app, renamed them, and moved some variables around
for ease-of-use. This is a straightforward program that only requires a user’s
Pinata API key and the names that they wish their metadata and images folders
on Pinata's IPFS pinning service to be called. This app accomplishes this by
using the axios, fs-extra, recursive-fs, form-data, and base-path-converter
libraries. The files for this sub-program are `upload_metadata.js` and
`upload_images.js`.

For the Hardhat smart contract app, rather than accessing any repository or
code, I followed a tutorial on YouTube. The program is straightforward. In
`hardhat.config.js` a boilerplate dictionary containing info on the network to 
be deployed to, the user wallet's private key, a blockchain node provider API,
and Etherscan API key is created. This is exported. Hardhat accesses this file
to interact with blockchains. Next is `deploy.js`, which again uses boilerplate
code create an instance of the smart contract which the user developed and
compiled, and then uses the ethers library function `deploy()` to put the smart
contract on the blockchain. The contract is then verified on Etherscan using
the Etherscan library and the verify CLI command. Finally, I created a script 
called `update_uri.js` which uses the user's wallet as well as the node pro-
vider to interact with the blockchain. It creates an instance of the smart
contract, at which point it can call functions that are programmed within the
smart contract. I call the `setBaseURI()` and `baseURI()` functions that are
coded in my smart contract to tell ERC-721 token holders where the NFT lives on
the IPFS. The user enters contract's name, address, and the CID of the IPFS pin
to do this successfully.

Lastly, and most importantly, is the Solidity smart contract. This turns the
PNG and JSON files into an NFT. The first comment is required, or else the con-
tract will not compile, and it sets the license. I have chosen `UNLICENSED`
because I plan to launch this Solidity program on the Ethereum mainnet and to
earn a profit and do not want others to take my away my idea and opportunity
to earn an income. Next, I specify that the source code is written for Solidity
version 0.8.13, as newer versions of solidity may break this contract. Next, I 
import openzeppelin smart contract templates, which are like libraries in the 
smart contract world. They allow me to omit a lot of the boilerplate code 
required to make an NFT function. The documentation for these templates is 
available on openzeppelin's website. The next line, `contract` is like 
classes in OOP languages. It contains functions and data in state variables. My
contract inherets the `ERC721` contract and the `Ownable` contract. ERC721 
ensures that the tokens minted via the contract are non-fungible; this is in-
tentional, for each token represents a unique NFT (image and metadata). This is
similar to art, for the Mona Lisa can not be subsistuted with Starry Starry 
Night, even though both are extremely valuable and beautiful. Ownable allows 
the contract to have an owner and have exclusive rights to the contract, like 
setting the base URI and withdrawing funds from the contract. Next I define 
state variables which are initialized upon contract creation such as the mint 
price (variables without values are initialized to the default values, which
are `""` for string and `0` for uint). After that comes the `constructor()` keyword
which is executed upon contract creation and creates the contract, setting the
contract name and token symbol. The remainder of the code is functions that
people interacting with the smart contract can call, and each function is mod-
ified using particular modifiers. A function's visability is determined by the
keywords `external`, `public`, or `internal`. External and public functions can 
be accessed outside of the contract (meaning anyone in the world can call the 
function and execute the code, with the exection of functions that have the 
`onlyOwner` modifier which can only be called by the owner of the con-ract. The
`payable` modifier requires ETH to be sent (in addition to gas fees) to be sent
when calling the function. Thus the `mint` function has the payable modifier
because the NFTs have an expense. The `view` modifier does not cost gas for the
function caller and simply return a state variable's value; these functions
use the keyword `return` to indicate that a value is returned when the function
is called, and the values type is specified (`memory` is a place that data can
be temporarily stored in order to call a function). The `override` modifier 
overridese a function (and modifies it) which is written in a contract
which this contract inherits. The functions in my smart contract are essential
for the NFT. The mint function uses the `require()` function to ensure that the
minter is sending the approprate amount of ETH, as well as that no more than
the maximum supply of tokens can be minted. Then, a for loop is used to deter-
mine the current ID number of the token, the total supply is updated, and the
`_safeMint()` function (from the ERC721 openzeppelin contract) is called with
the address of the sender and the token ID as arguments. When OpenSea detects
an NFT in someone's wallet, it gets the token ID. It then uses the `tokenURI`
function in my smart contract to get the JSON file for the NFT. The `tokenURI`
function uses the `baseURI` and the `tokenID` to generate a string which ends 
in `.json`, and this allows OpenSea to get the JSON file from the IPFS. The
JSON file includes the image's IPFS location which allows OpenSea to display
the image. My `setBaseURI` function allows me (the contract owner) to set the
`baseURI`, which is the IPFS base URI, so that `tokenURI` can append the 
`tokenId` and `.json` extension. Finally, the withdraw function allows me (the
contract owner) to withrdaw the balance of the smart contract to my wallet add-
ress (`payable(msg.sender)` is the Ethereum Virtual Machine message sender
which is of the payable address type), and this function requires the tran-
saction to succeed or else be reverted (so that funds cannot be lost).

Works cited:
Generator - https://github.com/HashLips/hashlips_art_engine
Pinata IPFS uploader - https://github.com/Coderrob/pinata-ipfs-scripts-for-nft-projects
Hardhat contract deployer - https://www.youtube.com/watch?v=g73EGNKatDw&list=PLUOW4dxqiJaVu-L5O_ZdIeX7GOA57Ybnc


