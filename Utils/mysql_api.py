import logging

import numpy as np
import pymysql

logging.basicConfig(level=logging.INFO)


class MysqlConn:
    """创建数据库连接"""
    def __init__(self, host, port, user, password, database):
        self.conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database)
        self.c = self.conn.cursor()

    def close(self, save=True):
        if save:
            self.conn.commit()
        self.conn.close()

    def commit(self):
        self.conn.commit()


class MysqlOpt:
    """创建表连接"""
    def __init__(self, db, tbname):
        self.db = db
        self.tbname = tbname

    @staticmethod
    def tf_dict(kw):
        """将字典转换为SQL,where语句的条件"""
        term = []
        for k, v in kw.items():
            if isinstance(v, int):
                term.append(k+'='+str(v))
            else:
                term.append(k+'='+"'"+v+"'")
        return ' and '.join(term)

    def get_tags(self):
        self.db.c.execute("")

    def select(self, *tags, **kw):
        """返回查询结果，tags为查询的字段，kw为查询条件"""
        if not tags:
            tags = '*'
        if not kw:
            self.db.c.execute("select {0} from {1}".format(','.join(tags), self.tbname))
        else:
            cond = self.tf_dict(kw)
            self.db.c.execute(
                "select {0} from {1} where {2}".format(','.join(tags), self.tbname, cond))
        result = self.db.c.fetchall()
        return result

    def insert(self, *args, **kw):
        # 插入
        if args != ():
            tags = ''
            #logging.warning(tags)
            #logging.warning(args)
            if isinstance(args[0], (list, tuple)):
                values = str(tuple(args[0]))
            else:
                values = str(tuple(args))
        elif kw:
            tags = '('+','.join(kw.keys())+')'
            values = tuple(kw.values())
        else:
            raise Exception('No values!')
        try:
            #logging.info("insert into {0} {1} values {2}".format(self.tbname, tags, values))
            self.db.c.execute(
                "insert into {0} {1} values {2}".format(self.tbname, tags, values)
            )
            self.db.commit()
        except pymysql.err.ProgrammingError as e:
            logging.warning(e, values)
        except pymysql.err.IntegrityError as e:
            logging.warning(e, values)


if __name__ == '__main__':
    db = MysqlConn('localhost', 3306, 'yxd', '12345679', 'stock')
    tb = MysqlOpt(db, 'gsjj')
    a = tb.select()

