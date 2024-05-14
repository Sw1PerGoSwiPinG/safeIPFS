const CryptoService = {
  // Generates a random 256-bit AES key and returns it
  async generateAESKey() {
    try {
      const key = await window.crypto.subtle.generateKey(
        {
          name: "AES-CBC",
          length: 256, // Can be 128, 192, or 256
        },
        true, // Whether the key is extractable (i.e., can be used in exportKey)
        ["encrypt", "decrypt"] // Can be "encrypt", "decrypt", "wrapKey", or "unwrapKey"
      );
      return key;
    } catch (err) {
      console.error('Error generating AES key:', err);
      throw err;
    }
  },

  // Encrypts a file using AES-256 in CBC mode
  async encryptFile(fileBlob, key) {
    const data = await fileBlob.arrayBuffer();
    const IVString = 'safeipfssafeipfs';
    const iv = new Uint8Array(IVString.length);

    for (let i = 0; i < IVString.length; i++) {
      iv[i] = IVString.charCodeAt(i);
    }

    // const iv = crypto.getRandomValues(new Uint8Array(16)); // IV size for AES-CBC is 16 bytes
    try {
      const encryptedData = await window.crypto.subtle.encrypt(
        {
          name: "AES-CBC",
          iv: iv
        },
        key,
        data
      );
      return new Blob([iv, new Uint8Array(encryptedData)], { type: fileBlob.type });
    } catch (err) {
      console.error('Error encrypting file:', err);
      throw err;
    }
  },

  // Decrypts a file using AES-256 in CBC mode
  async decryptFile(encryptedBlob, key) {
    const encryptedData = await encryptedBlob.arrayBuffer();
    const iv = new Uint8Array(encryptedData.slice(0, 16));
    const data = encryptedData.slice(16);
    try {
      const decryptedData = await window.crypto.subtle.decrypt(
        {
          name: "AES-CBC",
          iv: iv
        },
        key,
        data
      );
      return new Blob([decryptedData], { type: 'application/octet-stream' });
    } catch (err) {
      console.error('Error decrypting file:', err);
      throw err;
    }
  }
};

export default CryptoService;
