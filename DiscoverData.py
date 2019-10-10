#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql

#GECAM-01_GRD_0D_ENG_BTIME_20190926T092412_011.fits
class Parse_file:
    file_path = ""
    file_name = ""
    source_path = ""
    archive_path = ""
    def __init__(self,file_path):
       self.file_path = file_path

    def parse_name(self):
        strs = self.file_path.split("\\")
        print(strs[strs.size])
        #"".__contains__("01")

def check_file(file_path):
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


def connect():
    host = "localhost"
    user = "adp"
    password = "adp"
    database = "gns"
    return pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')

# 执行查询sql，返回的是字典数据
def run_select(sql):
    try:
        db = connect()
        cursor = db.cursor()
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
        db.close()

# 数据库操作工具
def db_util(execSql):
    # 打开数据库连接
    db = connect()
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 更新语句
    #sql = "UPDATE g_activity SET output = 'log_json',rate=50 WHERE id = 25 "
    try:
        # 执行SQL语句
        cursor.execute(execSql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        db.rollback()
        print("数据库操作失败", e)
    finally:
        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    file = "D:\\filework\\target\python_db.py";
    result1 = check_file(file)
    print(result1)
    #execSql = "INSERT INTO g_divcoverdata ( `type`, `name`, `suffix`, `sourcepath`, `archivepath`, `checknum`, `status`, `dtime`) VALUES ('1', 'GECAM-01_GRD_0D_EVT_BTIME_20190926T092412_013.fits', 'fits', 'D:\\filework\\source\\GECAM-01_GRD_0D_EVT_BTIME_20190926T092412_013.fits', 'D:\\filework\\target\\GECAM-01_GRD_0D_EVT_BTIME_20190926T092412_013.fits', '1', '4', '2019-09-26 16:38:37')";
    #db_util(execSql);
    #list = run_select("select * from g_divcoverdata")
    #dict_row = list[0]
    #print(dict_row["id"])
    x = Parse_file(file)
    x.parse_name()
