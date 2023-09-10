/* 
 * Adjust height and width to match the dimensions of the images in layers;
 * also adjust growEditionSizeTo to desired collection size. Finally, adjust 
 * layersOrder by adding the names of the directories in the `layers` folder 
 * as they are to be stacked in the final image. 
 */

const format = {
    width: 500,  // Desired NFT width in pixels (match layer image width)
    height: 500,  // Desired NFT height in pixels (match layer image height)
    smoothing: false,
  };
  
  const layerConfigurations = [
    {
      growEditionSizeTo: 10,  // Enter desired number of NFTs 
      layersOrder: [
      { name: "Background" },
      { name: "Eyeball" },
      { name: "Eye color" },
      { name: "Iris" },
      { name: "Shine" },
      { name: "Bottom lid" },
      { name: "Top lid" },
      ],
    },
  ];
  
  // Edit this metadata
  const namePrefix = "";  // Project Name
  const description = "";  // Project description
  const imagesCID = "";  // Paste from terminal (after running upload_images)

  // Don't change anything below this
  const protocol = "ipfs://"
  const baseUri = protocol + imagesCID;
  
  const basePath = process.cwd();
  const { MODE } = require(`${basePath}/constants/blend-mode.js`);
  
  const network = "eth";
  
  const shuffleLayerConfigurations = false;
  
  const debugLogs = false;
  
  const text = {
    only: false,
    color: "#ffffff",
    size: 20,
    xGap: 40,
    yGap: 40,
    align: "left",
    baseline: "top",
    weight: "regular",
    family: "Courier",
    spacer: " => ",
  };
  
  const pixelFormat = {
    ratio: 2 / 128,
  };
  
  const background = {
    generate: true,
    brightness: "80%",
    static: false,
    default: "#000000",
  };
  
  const extraMetadata = {};
  
  const rarityDelimiter = "#";
  
  const uniqueDnaTorrance = 10000;
  
  const preview = {
    thumbPerRow: 5,
    thumbWidth: 50,
    imageRatio: format.height / format.width,
    imageName: "preview.png",
  };
  
  module.exports = {
    format,
    baseUri,
    description,
    background,
    uniqueDnaTorrance,
    layerConfigurations,
    rarityDelimiter,
    preview,
    shuffleLayerConfigurations,
    debugLogs,
    extraMetadata,
    pixelFormat,
    text,
    namePrefix,
    network,
  };
  