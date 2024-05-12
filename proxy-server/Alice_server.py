from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS

# from flask_session import Session
import requests
from umbral import (
    SecretKey,
    Signer,
    encrypt,
    Capsule,
    generate_kfrags,
    VerifiedCapsuleFrag,
    PublicKey,
    decrypt_reencrypted,
)
import sqlite3
import hashlib
import socket
import json

app = Flask(__name__)
CORS(app)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
port = 5000
proxy_address = "10.122.236.111"
# conn = sqlite3.connect("owner.db")

import sqlite3


def get_db_connection():
    conn = sqlite3.connect("owner.db")
    conn.row_factory = sqlite3.Row
    return conn


# 登录路由
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    # 计算密码的SHA-256哈希值
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    ip_address = socket.gethostbyname(socket.gethostname())

    # 构造数据包发送给代理
    data = {
        "username": username,
        "password_hash": password_hash,
        "address": f"{ip_address}:{port}",
    }

    # 发送数据到代理并等待响应
    response = requests.post(f"http://{proxy_address}:5000/validate_login", json=data)
    if response.status_code == 200:
        print("Login successful")
        # session["user_id"] = username
        # print(session["user_id"])
        return jsonify({"message": "Login successful", "user_id": username})
        # return redirect(url_for('dashboard'))
    else:
        print("Login failed")
        return jsonify({"message": "Login failed"}), 400


@app.route("/register", methods=["POST"])
def register():
    print(request.json)

    username = request.json["username"]
    password = request.json["password"]

    # print("here!", username)
    # password = "12345"
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    ip_address = socket.gethostbyname(socket.gethostname())

    # 构造数据包发送给代理
    data = {
        "username": username,
        "password_hash": password_hash,
        "address": f"{ip_address}:{port}",
    }

    # 发送数据到代理并等待响应
    response = requests.post(f"http://{proxy_address}:5000/register", json=data)
    if response.status_code == 200:
        print("Register successful")
        return jsonify({"message": "Register successful", "user_id": username})
    else:
        print("Register failed")
        return jsonify({"message": "Register failed"}), 400


@app.route("/create_group", methods=["POST"])
def create_group():
    user_id = request.json.get("user_id")
    file_key = request.json.get("file_key")
    group_name = request.json.get("group_name")
    group_description = request.json.get("group_description")
    owner_secret_key = SecretKey.random()
    owner_public_key = owner_secret_key.public_key()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS KeyTable (
            group_id INTEGER PRIMARY KEY,
            file_key TEXT,
            public_key TEXT,
            private_key TEXT
        )
    """
    )
    conn.commit()
    conn.close()
    capsule, encrypted_file_key = encrypt(owner_public_key, file_key.encode())
    data = {
        "user_id": user_id,
        "owner_public_key": bytes(owner_public_key).hex(),
        "encrypted_file_key": encrypted_file_key.hex(),
        "capsule": bytes(capsule).hex(),
        "group_name": group_name,
        "group_description": group_description,
    }
    response = requests.post(f"http://{proxy_address}:5000/receive", json=data)
    group_id = response.text
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO KeyTable (group_id, file_key, public_key, private_key) VALUES (?, ?, ?, ?)",
        (
            group_id,
            file_key,
            bytes(owner_public_key).hex(),
            owner_secret_key.to_secret_bytes().hex(),
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Data saved", "group_id": group_id})


@app.route("/request_access", methods=["POST"])
def request_access():
    group_id = request.json.get("group_id")
    user_id = request.json.get("user_id")
    current_time = request.json.get("current_time")
    requester_secret_key = SecretKey.random()
    requester_public_key = requester_secret_key.public_key()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS KeyTable (
            group_id INTEGER PRIMARY KEY,
            file_key TEXT,
            public_key TEXT,
            private_key TEXT
        )
    """
    )
    conn.commit()
    conn.close()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM KeyTable WHERE group_id = ?", (group_id,))
    result = c.fetchone()
    conn.close()
    if result is None:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO KeyTable (group_id, file_key, public_key, private_key) VALUES (?, ?, ?, ?)",
            (
                group_id,
                None,
                bytes(requester_public_key).hex(),
                requester_secret_key.to_secret_bytes().hex(),
            ),
        )
        conn.commit()
        conn.close()
        data = {
            "requester_id": user_id,
            "requester_public_key": bytes(requester_public_key).hex(),
            "group_id": group_id,
        }
    else:
        data = {
            "requester_id": user_id,
            "requester_public_key": result["public_key"],
            "group_id": group_id,
            "current_time": current_time,
        }
    response = requests.post(f"http://{proxy_address}:5000/get_address", json=data)
    if response.status_code == 200:
        return (
            jsonify({"message": "Access request submitted for group ID: " + group_id}),
            200,
        )
    else:
        return jsonify({"message": "Access request failed"}), 400


@app.route("/logout", methods=["POST"])
def logout():
    request_data = request.json
    data = {
        "user_id": request_data["user_id"],
    }
    response = requests.post(f"http://{proxy_address}:5000/logout", json=data)
    return jsonify({"message": json.loads(response.text)["message"]})


@app.route("/get_requests", methods=["POST"])
def get_requests():
    user_id = request.json.get("user_id")
    data = {"user_id": user_id}
    response = requests.post(f"http://{proxy_address}:5000/get_requests", json=data)
    return jsonify({"requests": json.loads(response.text)["requests"]})


@app.route("/get_public_key", methods=["POST"])
def get_public_key():
    owner_id = request.json.get("owner_id")
    requester_id = request.json.get("requester_id")
    group_id = request.json.get("group_id")
    data = {"owner_id": owner_id, "requester_id": requester_id, "group_id": group_id}
    response = requests.post(f"http://{proxy_address}:5000/get_public_key", json=data)
    requester_public_key_bytes = json.loads(response.text)["requester_public_key"]
    requester_public_key = PublicKey.from_bytes(
        bytes.fromhex(requester_public_key_bytes)
    )
    group_id = data["group_id"]
    requester_id = data["requester_id"]
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT private_key FROM KeyTable WHERE group_id = ?", (group_id,))
    owner_secret_key_bytes = c.fetchone()[0]
    owner_secret_key = SecretKey._from_exact_bytes(
        bytes.fromhex(owner_secret_key_bytes)
    )
    conn.close()
    kfrags = generate_kfrags(
        delegating_sk=owner_secret_key,
        receiving_pk=requester_public_key,
        signer=Signer(owner_secret_key),
        threshold=1,
        shares=1,
    )
    kfrag = kfrags[0]
    kfrag_bytes = bytes(kfrag).hex()
    print(kfrag_bytes)
    data_ = {
        "kfrag": kfrag_bytes,
        "requester_id": requester_id,
        "group_id": group_id,
        "owner_id": owner_id,
    }
    response_ = requests.post(
        f"http://{proxy_address}:5000/calculate_cfrag", json=data_
    )
    if response_.status_code == 200:
        return jsonify({"message": "Success!"}), 200
    else:
        return jsonify({"message": "Failed!"}), 400


@app.route("/get_approved_requests", methods=["POST"])
def get_approved_requests():
    requester_id = request.json.get("requester_id")
    data = {"requester_id": requester_id}
    response = requests.post(
        f"http://{proxy_address}:5000/get_approved_requests", json=data
    )
    return jsonify({"requests": json.loads(response.text)["requests"]})


@app.route("/process_approved_request", methods=["POST"])
def process_approved_request():
    requester_id = request.json.get("user_id")
    owner_id = request.json.get("owner_id")
    group_id = request.json.get("group_id")
    data_ = {"requester_id": requester_id, "owner_id": owner_id, "group_id": group_id}
    response = requests.post(
        f"http://{proxy_address}:5000/process_approved_request", json=data_
    )
    data = json.loads(response.text)
    cfrag_bytes = data["cfrag"]
    capsule_bytes = data["capsule"]
    owner_public_key_bytes = data["owner_public_key"]
    encrypted_file_key_hex = data["encrypted_file_key"]
    encrypted_file_key = bytes.fromhex(encrypted_file_key_hex)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM KeyTable WHERE group_id = ?", (group_id,))
    result = c.fetchone()
    conn.close()
    requester_secret_key_bytes = result["private_key"]
    cfrag = VerifiedCapsuleFrag.from_verified_bytes(bytes.fromhex(cfrag_bytes))
    capsule = Capsule.from_bytes(bytes.fromhex(capsule_bytes))
    owner_public_key = PublicKey.from_bytes(bytes.fromhex(owner_public_key_bytes))
    requester_secret_key = SecretKey._from_exact_bytes(
        bytes.fromhex(requester_secret_key_bytes)
    )
    file_key = decrypt_reencrypted(
        receiving_sk=requester_secret_key,
        delegating_pk=owner_public_key,
        capsule=capsule,
        verified_cfrags=[cfrag],
        ciphertext=encrypted_file_key,
    )
    file_key = file_key.decode()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE KeyTable SET file_key = ? WHERE group_id = ?",
        (
            file_key,
            group_id,
        ),
    )
    conn.commit()
    conn.close()
    return (
        jsonify(
            {
                "message": "Request processed successfully!",
                "decrypted_file_key": file_key,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, port=port)
