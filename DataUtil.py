# -*- coding:utf-8 -*-
import os
import subprocess
import time

import pymysql
from DBClient import DBClient

def save_data(m: dict):

    sql = """INSERT INTO `g_divcoverdata` (`type`, `name`, `suffix`, `sourcepath`, `checknum`, `status`, `dtime`)\
            VALUES ( {type}, {name}, {suffix}, {sourcepath},  {checknum}, {status}, {datetime}""" \
        .format(m['type'], m[''], m['suffix'], m['sourcepath'], m['checknum'], m['status'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    with DBClient() as db:
        db.execute(sql)


def update_data():
    # 打开数据库连接（请根据自己的用户名、密码及数据库名称进行修改）
    sql = "select 1"
    with DBClient() as db:
        db.execute(sql)


def get_data():
    sql = "select * from g_divcoverdata"
    cnn = pymysql.connector.connect(host = "127.0.0.1",user='root', passwd='root', database='testdb')
    try:
        cursor = cnn.cursor()
        cursor.execute(sql)
        field_list = []
        for field in cursor.description:
            field_list.append(field[0])
        results = cursor.fetchall()
        list = []
        for row in results:
            dict_row = {}
            i = 0
            while i < len(field_list):
                # print(field_list[i], type(row[i]), str(row[i]))
                if type(row[i]) == bytes:
                    dict_row[field_list[i]] = bytes.decode(row[i])
                else:
                    dict_row[field_list[i]] = row[i]
                i += 1
            list.append(dict_row)
        cursor.close()
        return list
    except Exception as e:
        print("数据库操作失败", e)
    finally:
        # 关闭数据库连接
        cnn.close()


def parse_name(filepath: str):
    """
    根据文件路径，返回文件有效信息，
    :rtype: list，文件相关信息
    """
    filename = filepath.rsplit("/")[1]
    name_info = filename.split("_")
    return name_info


def check_file(file_path):
    """
    用来检查文件，但是不知道具体干啥用的
    :rtype: object
    """
    try:
        # print(filePath)
        f = open(file_path, 'r')
        result = list()
        for line in open(file_path):
            line = f.readline()
            # print(line)
            result.append(line)
            # print(result)
    except Exception as e:
        print("文件打开失败", file_path, e)
        return 1
    finally:
        f.close()
    return 0


def copy_file(from_path, to_path):
    user = "",
    ip = ""
    password = ""
    port = 22
    SCP_CMD_BASE = r"""
          expect -c "
          set timeout 300 ;
          spawn scp -P {port} -r {from_path} {username}@{host}:{to_path} ;
          expect *assword* {{{{ send {password}\r }}}} ;
          expect *\r ;
          expect \r ;
          expect eof
          "
        """.format(username=user, password=password, host=ip, remotedest=to_path, port=port)
    SCP_CMD = SCP_CMD_BASE.format(localsource=from_path)
    print("execute SCP_CMD: ", SCP_CMD)
    p = subprocess.Popen(SCP_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    os.system(SCP_CMD)
