import pymysql


# MySql连接
def connectDB():
    conn = pymysql.connect(host='localhost',
                           port=3306, user='root',
                           passwd='root',
                           db="scholar",
                           charset='utf8')  # 可以指定返回的类型，指定为queryset的字典类型，比较方便
    return conn
