from flask import Flask

app = Flask(__name__)
from flask import Flask, request, jsonify

wx_lst = [
    'xiajiehaoyun1986'
    'xyyy2201',
    'bohaikunge',
    'qinlaodagongmei',
    'legelege1975',
    'TjFt996',
]
import json
from ie.log import logger


@app.route('/', methods=['POST'])
def index():
    req_body = request.get_json(force=True)
    if req_body['action'] != 'report_new_msg':
        return ''
    # print(req_body['data'])

    wxid = req_body['wxid']
    wxid_from = req_body['data']['msg']['wxid_from']
    raw_msg = req_body['data']['msg']['raw_msg']
    print(raw_msg)
    print(wxid_from)
    print(wxid)
    data = {'raw_msg': raw_msg, 'wxid_from': wxid_from, 'wxid': wxid}
    logger.error(data)

    for i in wx_lst:
        if wxid_from == i or wxid == i:
            print('######################')
    return 'Index Page'


@app.route('/', methods=['GET'])
def hello():
    print('GET')
    args = request.args
    print(args)
    return 'Hello, World'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )
