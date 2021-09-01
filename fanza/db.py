from pymysql import connect
from fanza.items import FanzaItem, MgsItem
from fanza.constants import GENRE_TABLE, LABEL_TABLE, SERIES_TABLE, MAKER_TABLE, DIRECTOR_TABLE, ACTRESS_TABLE


class AvDB:
    def __init__(self, host, user, passwd, database, port):
        self.db = connect(host=host, user=user, passwd=passwd, database=database, port=port)
        

    def insert_fanza_movie(self, fanza_item: FanzaItem):
        self.insert_avbook_fanza_movie(fanza_item)
        self.insert_avbook_fanza(fanza_item, LABEL_TABLE)
        self.insert_avbook_fanza(fanza_item, MAKER_TABLE)
        self.insert_avbook_fanza(fanza_item, SERIES_TABLE)
        for genre_id, genre_name in fanza_item.genre.items():
            self.insert_avbook_fanza_dict(int(genre_id), genre_name, GENRE_TABLE, fanza_item)
            self.insert_avbook_fanza_rel(fanza_item, int(genre_id), GENRE_TABLE)
        for actress_id, actress_name in fanza_item.actress.items():
            self.insert_avbook_fanza_dict(int(actress_id), actress_name, ACTRESS_TABLE, fanza_item)
            self.insert_avbook_fanza_rel(fanza_item, int(actress_id), ACTRESS_TABLE)
        for director_id, dirctor_name in fanza_item.director.items():
            self.insert_avbook_fanza_dict(int(director_id), dirctor_name, DIRECTOR_TABLE, fanza_item)
            self.insert_avbook_fanza_rel(fanza_item, int(director_id), DIRECTOR_TABLE)

    def insert_mgs_movie(self, mgs_item: MgsItem):
        self.insert_avbook_mgs(mgs_item, LABEL_TABLE)
        self.insert_avbook_mgs(mgs_item, ACTRESS_TABLE)
        self.insert_avbook_mgs(mgs_item, MAKER_TABLE)
        self.insert_avbook_mgs(mgs_item, SERIES_TABLE)
        for genre_name in mgs_item.genre:
            self.insert_avbook_mgs_list(mgs_item, genre_name, GENRE_TABLE)
        self.insert_avbook_mgs_movie(mgs_item)

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()

    def insert_avbook_fanza_movie(self, fanza_item: FanzaItem):
        if fanza_item.censoredId is None:
            return
        with self.db.cursor() as cursor:
            sql_movie = "INSERT INTO `avbook_fanza_movie` (`censored_id`," \
                        "`title`," \
                        "`release_date`," \
                        "`video_len`," \
                        "`maker_id`," \
                        "`label_id`," \
                        "`series_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_movie, (fanza_item.censoredId,
                                           fanza_item.title,
                                           fanza_item.releaseDate,
                                           fanza_item.videoLen,
                                           fanza_item.makerId,
                                           fanza_item.labelId,
                                           fanza_item.seriesId))
            self.db.commit()                

    def insert_avbook_mgs_movie(self, mgs_item: MgsItem):
        if mgs_item.censoredId is None:
            return
        with self.db.cursor() as cursor:
            sql_movie = "INSERT INTO `avbook_mgs_movie` (`censored_id`," \
                        "`title`," \
                        "`release_date`," \
                        "`actress_id`," \
                        "`video_len`," \
                        "`maker_id`," \
                        "`label_id`," \
                        "`series_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_movie, (mgs_item.censoredId,
                                           mgs_item.title,
                                           mgs_item.releaseDate,
                                           mgs_item.actressId,
                                           mgs_item.videoLen,
                                           mgs_item.makerId,
                                           mgs_item.labelId,
                                           mgs_item.seriesId))
            self.db.commit()

    def insert_avbook_fanza(self, fanza_item: FanzaItem, attr: str):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(attr)
            id = getattr(fanza_item, '%sId' % attr)
            name = getattr(fanza_item, attr + 'Name')
            if name is None:
                return
            cursor.execute(sql_insert, (id, name))
            self.db.commit()

    def insert_avbook_fanza_dict(self, id: int, name: str, table: str, fanza_item: FanzaItem):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(table)
            cursor.execute(sql_insert, (id, name))
            self.db.commit()
    
    def insert_avbook_fanza_rel(self, fanza_item: FanzaItem, id: int, table: str):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_movie_{0}_rel` (`censored_id`, `{0}_id`) VALUES (%s, %s)".format(table)
            cursor.execute(sql_insert, (fanza_item.censoredId, id))
            self.db.commit()
                
    def insert_avbook_mgs(self, mgs_item: MgsItem, attr: str):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_mgs_{0}` (`{0}_name`) VALUES (%s)".format(attr)
            sql_select = "SELECT `{0}_id` FROM `avbook_mgs_{0}` WHERE `{0}_name` = %s".format(attr)
            name = getattr(mgs_item, '%sName' % attr)
            if name is None:
                return
            cursor.execute(sql_select, (name))
            result = cursor.fetchone()
            if result is None:
                cursor.execute(sql_insert, (name))
                self.db.commit()
                id = cursor.lastrowid
            else:
                id = result[0]
            setattr(mgs_item, '%sId' % attr, id)

    def insert_avbook_mgs_list(self, mgs_item: MgsItem, name: str, attr: str):
        sql_insert = "INSERT INTO `avbook_mgs_{0}` (`{0}_name`) VALUES (%s)".format(attr)
        sql_insert_rel = "INSERT INTO `avbook_mgs_movie_{0}_rel` (`censored_id`, `{0}_id`) VALUES (%s, %s)".format(attr)
        sql_select = "SELECT `{0}_id` FROM `avbook_mgs_{0}` WHERE `{0}_name` = %s".format(attr)
        with self.db.cursor() as cursor:
            cursor.execute(sql_select, (name))
            result = cursor.fetchone()
            if result is None:
                cursor.execute(sql_insert, (name))
                self.db.commit()
                id = cursor.lastrowid
            else:
                id = result[0]
            cursor.execute(sql_insert_rel, (mgs_item.censoredId, id))
            self.db.commit()
