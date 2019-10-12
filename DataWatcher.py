# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 11:21
# @Author  : bjsasc
import json
import logging
import os
import sys
import time
import DataUtil
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CLOSE_WRITE

# 设置日志输出两个handle，屏幕和文件
log = logging.getLogger('file watch ---')
fp = logging.FileHandler('a.log', 'a+', encoding='utf-8')
fs = logging.StreamHandler()
log.addHandler(fs)
log.addHandler(fp)
log.setLevel(logging.DEBUG)

FILE_DIR = r'/home/bjsasc/test/' # 监听文件目录


def check_dir_exist():
    """
        检查文件目录是否存在
    """
    if not FILE_DIR:
        log.info("The WATCH_PATH setting MUST be set.")
        sys.exit()
    else:
        if os.path.exists(FILE_DIR):
            log.info('Found watch path: path=%s.' % (FILE_DIR))
        else:
            log.info('The watch path NOT exists, watching stop now: path=%s.' % (FILE_DIR))
            sys.exit()


def read_json_from_file(file_path):
    """
    从文件中读取json数据
    :param file_path:
    """
    with open(file_path) as f:
        s = f.read()
        result = json.loads(s)
    # 处理数据
    for i in result:
        data_process(i)


def data_process(data: dict):
    """
    处理从json中读取到的数据
    :param data:
    """
    file_path = data["file_path"]
    # 从文件名称获取文件信息
    name_info = DataUtil.parse_name(file_path)
    weixing_info = name_info[0]
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
    DataUtil.notice(file_path)


class EventHandler(ProcessEvent):

    def process_IN_CLOSE_WRITE(self, event):
        """
        监听文件传输完成时间，只实现了传输完成监听
        :param event:
        """
        # logging.info("create file: %s " % os.path.join(event.path, event.name))
        file_path = os.path.join(event.path, event.name)
        time.sleep(2)
        log.info('write file finished ...%s' % (file_path))
        read_json_from_file(file_path)


def main():
    """
    文件监听的入口程序
    """
    check_dir_exist()
    wm = WatchManager()
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(FILE_DIR, IN_CLOSE_WRITE, rec=True, auto_add=True)
    log.info('Now starting monitor %s' % (FILE_DIR))
    notifier.loop()


if __name__ == '__main__':
    main()
