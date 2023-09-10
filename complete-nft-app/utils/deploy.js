// Enter contract name
const contract_name = "IceCreamFrens";

// Do not change anything below this line
const { ethers } = require("hardhat");

async function main() {
    const contract = await ethers.getContractFactory(contract_name);

    // Instance of contract
    const instance = await contract.deploy(); 
    console.log("Contract was deployed to address: ", instance.address); 
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
