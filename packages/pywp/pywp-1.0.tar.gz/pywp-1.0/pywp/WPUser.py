from pywp.Connectable import Connectable


class WPUser(Connectable):
    
    
    ID = 0
    caps = []
    cap_key = ''
    roles = []
    allcaps = []
    first_name = ''
    last_name = ''

    
    def __init__(self,
            ID=0,
            caps=[],
            cap_key='',
            roles=[],
            allcaps=[],
            first_name='',
            last_name=''
            ):
        
        self.ID = ID
        self.caps = caps
        self.cap_key = cap_key
        self.roles = roles
        self.allcaps = allcaps
        self.first_name = first_name
        self.last_name = last_name


    def get(self, key):
        cur = self.mysql.cursor()

        sql = """
              SELECT meta_value FROM wp_usermeta WHERE meta_key='{}'
              """.format(key)
        
        cur.execute(sql)
        value = cur.fetchone()
        if value is not None:
            value = value[0]

        if value is None or value == '':
            sql = """
                  SELECT {} FROM wp_users
                  """.format(key)
        
        cur.execute(sql)
        value = cur.fetchone()[0]

        cur.close()

        return value
