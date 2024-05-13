use safeipfs;
CREATE TABLE request_complete_cache (
    owner_id VARCHAR(255),
    requester_id VARCHAR(255),
    group_id INT,
    cfrag TEXT,
    PRIMARY KEY (owner_id, requester_id, group_id)
);
CREATE TABLE users (
    user_id VARCHAR(255),
    password_hash VARCHAR(255),
    is_online BOOLEAN,
    user_address VARCHAR(255),
    PRIMARY KEY (user_id)
);
CREATE TABLE user_groups (
    group_id INT AUTO_INCREMENT,
    group_name VARCHAR(255) NOT NULL,
    group_description TEXT,
    owner_id VARCHAR(255),
    requesters_id TEXT,
    encrypted_file_key TEXT,
    owner_public_key TEXT,
    capsule TEXT,
    PRIMARY KEY (group_id)
);
CREATE TABLE files (
    group_id INT,
    file_name VARCHAR(255),
    ipfs_hash VARCHAR(255),
    file_size VARCHAR(255),
    upload_date VARCHAR(255),
    PRIMARY KEY (group_id, ipfs_hash)
);
CREATE TABLE request_cache (
    owner_id VARCHAR(255),
    requester_id VARCHAR(255),
    requester_public_key TEXT,
    group_id INT,
    PRIMARY KEY (owner_id, requester_id, group_id)
);