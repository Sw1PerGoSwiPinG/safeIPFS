from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource

import json
from umbral import SecretKey, keys


app = Flask(__name__)
api = Api(app, version='1.0', title='Generate Key', description='A simple API using flask_restx')


@api.route('/key')
class GenerateKey(Resource):
    def get(self):
        # 生成密钥
        secret_key = SecretKey.random()
        public_key = secret_key.public_key()

        key_pair_json = {
            'public_key': bytes(public_key).hex(),
            'secret_key': secret_key.to_secret_bytes().hex(),
        }

        # key_pair_json_str = json.dump(key_pair_json)
        return jsonify(key_pair_json)


if __name__ == '__main__':
    app.run(debug=True)
