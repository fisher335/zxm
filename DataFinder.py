#!/usr/bin/python
# coding:utf-8
import json
import logging
# import inotify.adapters
import DataUtil
import sys
import os
import time
from urllib import parse, request

from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CLOSE_WRITE

log = logging.getLogger('file watch ---')
fp = logging.FileHandler('a.log', 'a+', encoding='utf-8')
fs = logging.StreamHandler()
log.addHandler(fs)
log.addHandler(fp)
log.setLevel(logging.DEBUG)

fileMask = IN_CLOSE_WRITE
FILE_DIR = r'/home/bjsasc/test/'


def notice(url, filename):
    data = {'filename': filename}
    post_data = parse.urlencode(data).encode()
    rest = request.Request(url, data=post_data)
    resp = request.urlopen(rest)
    log.info(resp.read())


class EventHandler(ProcessEvent):
    """事件处理"""

    def process_IN_CLOSE_WRITE(self, event):
        # logging.info("create file: %s " % os.path.join(event.path, event.name))
        file_path = os.path.join(event.path, event.name)
        time.sleep(2)
        # notice("http://www.baidu.com",event.name)
        log.info('write file finished ...%s' % (file_path))
        read_json_form_file(file_path)


def check_dir():
    if not FILE_DIR:
        log.info("The WATCH_PATH setting MUST be set.")
        sys.exit()
    else:
        if os.path.exists(FILE_DIR):
            log.info('Found watch path: path=%s.' % (FILE_DIR))
        else:
            log.info('The watch path NOT exists, watching stop now: path=%s.' % (FILE_DIR))
            sys.exit()


def main():
    check_dir()
    wm = WatchManager()
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(FILE_DIR, fileMask, rec=True, auto_add=True)
    log.info('Now starting monitor %s' % (FILE_DIR))
    notifier.loop()


def read_json_form_file(file_path):
    with open(file_path) as f:
        s = f.read()
        result = json.loads(s)
    for i in result:
        data_process(i)


def data_process(data: dict):
    file_path = data["file_path"]
    # 从文件名称获取文件信息
    name_info = DataUtil.parse_name(file_path)
    weixin_info = name_info[0]
    zaihe_info = name_info[1]
    # 打开文件检查
    checknum = DataUtil.check_file(file_path)
    # 构造保存数据库的dict
    result = {}
    result['type'] = '1'
    result['name'] = file_path
    result['suffix'] = 'fits'
    result['sourcepath'] = file_path
    result['checknum'] = checknum
    result['status'] = '1'
    # 保存数据到数据库
    DataUtil.save_data(result)
    # 拷贝文件
    DataUtil.copy_file(file_path, file_path)
    # 更新数据
    DataUtil.update_date()
    # 调用远程接口
    notice()


if __name__ == '__main__':
    main()
