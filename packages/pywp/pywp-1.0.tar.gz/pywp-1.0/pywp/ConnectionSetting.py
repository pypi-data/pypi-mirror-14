class ConnectionSetting(object):
    host='localhost'
    port=3306
    user=''
    passwd=''
    db=''


    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
