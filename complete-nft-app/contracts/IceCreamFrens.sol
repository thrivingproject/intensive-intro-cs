// SPDX-License-Identifier: UNLICENSED

// Version of Solidity
pragma solidity ^0.8.13;

// These are Ethereum standardized contracts that are built on top of
import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/access/Ownable.sol';

// Defining the smart contract which follows ERC-721 standards and can be owned
contract IceCreamFrens is ERC721, Ownable {
    string public baseURI;
    uint public mintPrice = 0.01 ether;
    uint public totalSupply;

    // Creation of the smart contract
    // The word payable is not required
    constructor() payable ERC721('IceCreamFrens', 'CONE') {}

    // Function to set the base URI which will point to the NFTs IPFS location
    function setBaseURI(string calldata _baseURI) external onlyOwner {
        baseURI = _baseURI;
    }

    // Function to get the URI of a specific NFT
    function tokenURI(uint tokenId) public view override returns (string memory) {
        require(_exists(tokenId), 'Nonexistent');

        return string(abi.encodePacked(baseURI, Strings.toString(tokenId), ".json"));
    }

    // Function to withdraw Ethereum payed by minters from smart contract
    function withdraw() external onlyOwner {
        (bool success, ) = payable(msg.sender).call{value: address(this).balance}('');
        require(success, 'Failed');
    }


    function mint(uint _qty) public payable {
        require(msg.value == _qty * mintPrice, 'Wrong mint value');
        require(totalSupply + _qty <= 10, 'Sold out');  // 10 is the max supply
        
        for (uint i = 0; i < _qty; i++) {
            uint newTokenId = totalSupply + 1;
            totalSupply++;
            _safeMint(msg.sender, newTokenId);
        }
    }
}