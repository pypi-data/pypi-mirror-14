import pymysql


class Connectable(object):


    def connect(self, connectionsetting):
        self.connectionsetting = connectionsetting

        self.mysql = pymysql.connect(
                host=connectionsetting.host,
                port=int(connectionsetting.port),
                user=connectionsetting.user,
                passwd=connectionsetting.passwd,
                db=connectionsetting.db)
