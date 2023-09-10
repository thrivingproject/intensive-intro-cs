// Enter name of directory as you want it to appear on Pinata (inconsequential)
const FOLDER_NAME = 'Demo';

// Don't change anything below here
const cid = null;
const { post } = require('axios');
const { createReadStream, outputJsonSync } = require('fs-extra');
const { read } = require('recursive-fs');
const FormData = require('form-data');
const basePathConverter = require('base-path-converter');

require('dotenv').config();

const { PINATA_API_KEY, PINATA_API_SECRET } = process.env;

const { log, error } = console;

const PINATA_API_PINFILETOIPFS = 'https://api.pinata.cloud/pinning/pinFileToIPFS';

(async () => {
  try {
    const OUTPUT_PATH = './output/images-folder-cid.json';
    
    const FOLDER_PATH = './build/images';
    const { files } = await read(FOLDER_PATH);
    if ((files && files.length) <= 0) {
      log(`No files were found in folder '${FOLDER_PATH}'`);
      return;
    }
    log(`'${FOLDER_PATH}' upload started`);
    const formData = new FormData();
    files.forEach((filePath) => {
      log(`Adding file: ${filePath}`);
      formData.append('file', createReadStream(filePath), {
        filepath: basePathConverter(FOLDER_PATH, filePath),
      });
    });
    formData.append(
      'pinataMetadata',
      JSON.stringify({
        name: FOLDER_NAME,
      }),
    );
    const {
      data: { IpfsHash: cid },
    } = await post(PINATA_API_PINFILETOIPFS, formData, {
      maxBodyLength: 'Infinity',
      headers: {
        // eslint-disable-next-line no-underscore-dangle
        'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
        pinata_api_key: PINATA_API_KEY,
        pinata_secret_api_key: PINATA_API_SECRET,
      },
    });
    log(`'${FOLDER_PATH}' upload complete; CID: ${cid}`);
    outputJsonSync(OUTPUT_PATH, { [FOLDER_NAME]: cid });
  } catch (err) {
    error(err);
    process.exit(1);
  }
})();
