from umbral import SecretKey, Signer

# Alice 的密钥
alice_secret_key = SecretKey.random()
alice_public_key = alice_secret_key.public_key()
print(type(alice_public_key))
print(type(alice_secret_key))


# Bob 的密钥
bob_secret_key = SecretKey.random()
bob_public_key = bob_secret_key.public_key()

from umbral import encrypt

plaintext = '这是一个重要的消息!'.encode()
capsule, ciphertext = encrypt(alice_public_key, plaintext)

print(type(capsule), type(ciphertext))
print(str(capsule))

from umbral import generate_kfrags

kfrags = generate_kfrags(delegating_sk=alice_secret_key, receiving_pk=bob_public_key,
                          signer=Signer(alice_secret_key), threshold=10, shares=20)

from umbral import reencrypt

cfrags = [reencrypt(capsule=capsule, kfrag=kfrag) for kfrag in kfrags[:10]]

from umbral import decrypt_reencrypted

decrypted_data = decrypt_reencrypted(receiving_sk=bob_secret_key, delegating_pk=alice_public_key,
                                      capsule=capsule, verified_cfrags=cfrags, ciphertext=ciphertext)

if decrypted_data == plaintext:
    print("Success!")
