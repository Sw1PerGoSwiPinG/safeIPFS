import json
from umbral import SecretKey, Signer

# 生成密钥
secret_key = SecretKey.random()
public_key = secret_key.public_key()

print(type(public_key))
print(type(secret_key))

# key = public_key.bytes().hex()

key_pair_json = {
    'public_key': bytes(public_key),
    'secret_key': secret_key.to_secret_bytes(),
}

# key_pair_json_str = json.dump(key_pair_json)
# print(key_pair_json_str)
print(key_pair_json)

# return jsonify({
#     'public_key': ,
#     'secret_key': 'Hello, world!',
# })
