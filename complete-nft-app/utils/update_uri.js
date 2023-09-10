// Update the following three lines
const CID = "QmNngaeRyxEDouKRSJz1iFtkWMSU2EcMqVorURU3M8TdXe"  // Paste
const contract_address = "0x282A6b350B41EA62d62F331887c094CFF3479341"  // Paste contract address
const contract_name = "IceCreamFrens" // Enter contract name

// Don't change anything below here
const artifact = require("../artifacts/contracts/" + contract_name + ".sol/"
                          + contract_name + ".json");

// Hidden environment info
const { PRIVATE_KEY, RINKEBY_KEY } = process.env;

// Provider - Alchemy
const alchemyProvider = new ethers.providers.AlchemyProvider(network="rinkeby", RINKEBY_KEY);

// Wallet to pay for transactions
const signer = new ethers.Wallet(PRIVATE_KEY, alchemyProvider);

// Contract instance
const contractInstance = new ethers.Contract(contract_address, artifact.abi, signer);

async function main() {
    
    console.log("Updating the base URI...");
    const tx = await contractInstance.setBaseURI("ipfs://" + CID + "/");
    await tx.wait();
    
    const baseTokenUri = await contractInstance.baseURI();
    console.log("New Base Token URI: " + baseTokenUri);

}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });