import pymysql
from pywp.Connectable import Connectable

from pywp.WPUser import WPUser
from pywp.WPPost import WPPost


class Wordpress(Connectable):

    def __init__(self, email):
        self.email = email


    def get_user(self):
        cur = self.mysql.cursor(pymysql.cursors.DictCursor)
        sql = """
              SELECT * FROM wp_users WHERE user_email='{}'
              """.format(self.email)

        cur.execute(sql)
        user_dict = cur.fetchone()
        cur.close()

        cur = self.mysql.cursor(pymysql.cursors.DictCursor)
        sql = """
              SELECT * FROM wp_usermeta WHERE user_id={}
              """.format(user_dict['ID'])

        cur.execute(sql)
        user_meta = cur.fetchall()
        cur.close()
        user_meta_dict = {}
        for meta in user_meta:
            k = meta['meta_key']
            v = meta['meta_value']
            m = {k:v}
            user_meta_dict.update(m)


        user = WPUser(
                ID=user_dict['ID'],
                caps=user_meta_dict['wp_capabilities'],
                cap_key=user_meta_dict['wp_user_level'],
                roles=user_meta_dict['wp_user_level'],
                allcaps=user_meta_dict['wp_capabilities'],
                first_name=user_meta_dict['first_name'],
                last_name=user_meta_dict['last_name'],
                )
        user.connect(self.connectionsetting)

        return user


    def get_post(self, ID):
        cur = self.mysql.cursor(pymysql.cursors.DictCursor)
        sql = """
              SELECT * FROM wp_posts WHERE ID={}
              """.format(ID)

        cur.execute(sql)
        post_dict = cur.fetchone()
        cur.close()


        post = WPPost(
                ID=post_dict['ID'],
                post_author=post_dict['post_author'],
                post_name=post_dict['post_name'],
                post_type=post_dict['post_name'],
                post_title=post_dict['post_title'],
                post_date=post_dict['post_date'],
                post_date_gmt=post_dict['post_date'],
                post_content=post_dict['post_content'],
                post_excerpt=post_dict['post_excerpt'],
                post_status=post_dict['post_status'],
                comment_status=post_dict['comment_status'],
                ping_status=post_dict['ping_status'],
                post_password=post_dict['post_password'],
                post_parent=post_dict['post_parent'],
                post_modified=post_dict['post_modified'],
                post_modified_gmt=post_dict['post_modified_gmt'],
                comment_count=post_dict['comment_count'],
                menu_order=post_dict['menu_order'], 
                )
        post.connect(self.connectionsetting)


        return post


    def insert_post(self, **args):
        if 'ID' in args:
            args.popitem('ID')

        post = WPPost(**args)
        post.connect(self.connectionsetting)
        post.commit()

        return post
