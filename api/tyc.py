# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime

from flask import request, jsonify
from flask.json import jsonify
from pymongo import MongoClient

from scrapyd_api import ScrapydAPI

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app


def get_data_from_db(search):
    client = MongoClient()
    db = client.crawl.corp_info
    cursor = db.find({'search': search})

    documents = sorted(cursor, key=lambda _doc: _doc['upt'], reverse=True)
    doc = documents[0] if documents else {}

    doc.pop('_id', None)
    doc.pop('upt', None)
    doc.pop('typ', None)

    client.close()

    return doc


def interval_seconds(from_typ='tianyancha'):
    """ 企查查， 启信宝， 天眼查
        每次调用至少满足最少间隔时间，连续调用则限制一定时间;
        rg: 天眼查每分钟最多4次
    """

    schedule_list = []
    interval_dict = {'tianyancha': 15}

    client = MongoClient()
    db = client.crawl.corp_schedule
    cursor = db.find({'typ': from_typ}).sort([('upt', -1)]).limit(20)

    for index, doc in enumerate(cursor):
        doc.pop('_id', None)
        schedule_list.append(doc)

    client.close()

    if not schedule_list:
        return True, 0

    diff_seconds = (datetime.now() - schedule_list[0]['upt']).total_seconds()
    remaining_seconds = diff_seconds - interval_dict[from_typ]
    if remaining_seconds > 0:
        return True, 0

    return False,  -remaining_seconds


@app.route(r'/api/corp/search', methods=['GET'])
def get_corp_info():
    project = 'company'
    scrapyd = ScrapydAPI()
    word = request.args.get('word')
    resp = {'result': {}, 'is_success': False, 'message': ''}

    if word is None:
        resp['message'] = u'调用失败: 没有关键字!'
        return jsonify(resp)

    result = get_data_from_db(word)
    if result:
        resp['message'] = u'调用成功!'
        resp['result'].update(result)
        return jsonify(resp)

    interval = interval_seconds()
    if not interval[0]:
        resp['message'] = u'调用频繁: {}s 后再调用!'.format(interval[1])
        return jsonify(resp)

    start_time = time.time()
    jobid = scrapyd.schedule(project, spider='tianyancha', search=word.encode('u8'))

    while (time.time() - start_time) <= 15:
        time.sleep(1)
        state = scrapyd.job_status(project, job_id=jobid)
        crawled_result = get_data_from_db(word)

        if state == 'finished':
            resp['is_success'] = True
            resp['result'] = crawled_result

            if crawled_result:
                resp['message'] = u'爬虫完成：获取数据成功!'
            else:
                resp['message'] = u'爬虫完成: 未获取数据!'

            break

    return jsonify(resp)


if __name__ == '__main__':
    # Run this file, must comment of `import tyc` line in api/__init__.py file
    app.run(host='0.0.0.0', port=8880, debug=True)

