import requests


def get_msg(url):
    data = {
        'userId': user_id,
        'orderUse': KqoeOrderConfig.orderUse,
        'sourceExtend': {
            'appId': KqoeOrderConfig.appId
        },
        'source': 3,  # openapi订单
        'products': [
            {
                "num": 1,
                "billType": KqoeOrderConfig.DaybillType,
                "duration": 1,
                "items": products,
                "productType": product_type,
                "productUse": 1,
                "productWhat": 1,
                "region": "Default-CN",
                "userId": user_id
            }
        ],

    }
    resp = requests.post(url, json=data)
    if resp.status_code != 200:
        error_msg = resp.json()['message']
        return {'data': None, 'error_msg': error_msg}
    else:
        data = resp.json()
        return {'data': data, 'error_msg': ''}
