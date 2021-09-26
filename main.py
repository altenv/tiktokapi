import logging
from gevent import monkey, pywsgi
monkey.patch_all()

from flask import Flask, request, make_response, jsonify
from datetime import datetime

from tiktoklib.tiktok import TikTokApi

app = Flask(__name__)
#api = TikTokApi.get_instance(use_test_endpoints=True, proxy="http://139.99.99.165:3128", custom_verifyFp="verify_kmb8g7cy_BhbVe9ke_35MR_46Um_BDs0_n2h103kiD5cP")
#api = TikTokApi.get_instance(use_test_endpoints=True, proxy="http://122.3.41.154:8090") #active
#api = TikTokApi.get_instance(use_test_endpoints=True, proxy="http://116.80.45.7:80")
api = TikTokApi.get_instance(use_test_endpoints=True)
@app.route("/public/by-hashtag")
def get_by_hashtag():
    try:
        hashtag = request.args.get('hashtag')
        if hashtag is None or not hashtag:
            return make_response(jsonify({ "message": "please specify hashtag" }), 400)

        count = request.args.get('target_count')
        if count is None or not count.isnumeric():
            return make_response(jsonify({ "message": "please specify target_count" }), 400)

        cursor = request.args.get('cursor')
        if cursor is None or not cursor.isnumeric():
            cursor = '0'

        verify_fp = request.args.get('verification_key')
        
        api = TikTokApi.get_instance(use_test_endpoints=True)

        tiktoks = api.by_hashtag(hashtag, count=int(count), offset=int(cursor))
        
        result = "[" + str(datetime.now()) + "] get tiktoks by hashtag: " + hashtag + ", total count: " + str(len(tiktoks)), ", offset: " + cursor
        logging.info(result)

        return make_response(jsonify({ "data": tiktoks }), 200)
    except Exception as e:
        logging.exception(e)
        return make_response(jsonify({ "message": str(e) }), 500)

@app.route("/public/by-username")
def get_by_username():
    try:
        username = request.args.get('username')
        if username is None or not username:
            return make_response(jsonify({ "message": "please specify hashtag" }), 400)

        verify_fp = request.args.get('verification_key')

        tiktoks = api.get_user(username)
        
        result = "[" + str(datetime.now()) + "] get tiktoks by username: " + username
        logging.info(result)

        return make_response(jsonify({ "data": tiktoks }), 200)
    except Exception as e:
        logging.exception(e)
        return make_response(jsonify({ "message": str(e) }), 500)

if __name__ == '__main__':
    port = 5002
    http_server = pywsgi.WSGIServer(("0.0.0.0", port), app)
    print("[" + str(datetime.now()) + "] start server at " + str(port))
    http_server.serve_forever()