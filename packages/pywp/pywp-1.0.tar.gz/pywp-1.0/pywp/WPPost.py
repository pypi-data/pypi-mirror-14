from pywp.Connectable import Connectable


class WPPost(Connectable):
    
    
    ID = 0
    post_author = 0
    post_name = ''
    post_type = ''
    post_title = ''
    post_date = ''
    post_date_gmt = ''
    post_content = ''
    post_excerpt = ''
    post_status	= ''
    comment_status = ''
    ping_status	= ''
    post_password = ''
    post_parent	= 0
    post_modified = ''
    post_modified_gmt = ''
    comment_count = 0
    menu_order = 0

    
    def __init__(self,
            ID=0,
            post_author=0,
            post_name='',
            post_type='post',
            post_title='',
            post_date='0000-00-00 00:00:00',
            post_date_gmt='0000-00-00 00:00:00',
            post_content='',
            post_excerpt='',
            post_status='publish',
            comment_status='',
            ping_status='',
            post_password='',
            post_parent=0,
            post_modified='0000-00-00 00:00:00',
            post_modified_gmt='0000-00-00 00:00:00',
            comment_count=0,
            menu_order=0,
            ):

        self.ID = ID
        self.post_author = post_author
        self.post_name = post_name
        self.post_type = post_type
        self.post_title = post_title
        self.post_date = post_date
        self.post_date_gmt = post_date_gmt
        self.post_content = post_content
        self.post_excerpt = post_excerpt
        self.post_status = post_status
        self.comment_status = comment_status
        self.ping_status = ping_status
        self.post_password = post_password
        self.post_parent = post_parent
        self.post_modified = post_modified
        self.post_modified_gmt = post_modified_gmt
        self.comment_count = comment_count
        self.menu_order = menu_order


    def get(self, key):
        cur = self.mysql.cursor()

        sql = """
              SELECT meta_value FROM wp_postmeta WHERE meta_key='{}'
              """.format(key)
        
        cur.execute(sql)
        value = cur.fetchone()
        if value is not None:
            value = value[0]

        if value is None or value == '':
            sql = """
                  SELECT {} FROM wp_posts
                  """.format(key)
        
        cur.execute(sql)
        value = cur.fetchone()[0]

        cur.close()

        return value


    def commit(self):
        if self.ID is not None and self.ID is not 0:
            sql = """
                  UPDATE wp_posts SET

                  post_author={},
                  post_name='{}',
                  post_type='{}',
                  post_title='{}',
                  post_date='{}',
                  post_date_gmt='{}',
                  post_content='{}',
                  post_excerpt='{}',
                  post_status='{}',
                  comment_status='{}',
                  ping_status='{}',
                  post_password='{}',
                  post_parent={},
                  post_modified='{}',
                  post_modified_gmt='{}',
                  comment_count={},
                  menu_order={}
                  
                  WHERE ID={}
                  """.format(
                            self.post_author,
                            self.post_name,
                            self.post_type,
                            self.post_title,
                            self.post_date,
                            self.post_date_gmt,
                            self.post_content,
                            self.post_excerpt,
                            self.post_status,
                            self.comment_status,
                            self.ping_status,
                            self.post_password,
                            self.post_parent,
                            self.post_modified,
                            self.post_modified_gmt,
                            self.comment_count,
                            self.menu_order,
                            self.ID
                          )
        else:
            sql = """
                  INSERT INTO wp_posts

                  (
                  post_author,
                  post_name,
                  post_type,
                  post_title,
                  post_date,
                  post_date_gmt,
                  post_content,
                  post_excerpt,
                  post_status,
                  comment_status,
                  ping_status,
                  post_password,
                  post_parent,
                  post_modified,
                  post_modified_gmt,
                  comment_count,
                  menu_order,
                  post_content_filtered,
                  to_ping,
                  pinged
                  )
                
                  VALUES
                  (
                  {},
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  '{}',
                  {},
                  '{}',
                  '{}',
                  {},
                  {},
                  '',
                  '',
                  ''
                  )
                  """.format(
                            self.post_author,
                            self.post_name,
                            self.post_type,
                            self.post_title,
                            self.post_date,
                            self.post_date_gmt,
                            self.post_content,
                            self.post_excerpt,
                            self.post_status,
                            self.comment_status,
                            self.ping_status,
                            self.post_password,
                            self.post_parent,
                            self.post_modified,
                            self.post_modified_gmt,
                            self.comment_count,
                            self.menu_order
                          )


        cur = self.mysql.cursor()
        cur.execute(sql)
        self.mysql.commit()
        insertid = cur.lastrowid
        cur.close()

        if self.ID is None or self.ID is 0:
            self.ID = insertid
            return insertid
        else:
            return self.ID
