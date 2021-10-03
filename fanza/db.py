from pymysql import connect
from fanza.items import FalenoActressItem, FanzaAmateurItem, FanzaItem, MgsItem, PrestigeActressItem, S1ActressItem, ItemMap, Item
from pymysql import IntegrityError
from fanza.db_constants import *
import logging
from fanza.db_error_msg_constatns import INTEGRITY_ERROR_MSG
from pymysql import ProgrammingError
from pymysql.err import DataError
from fanza.db_error_msg_constatns import PROGRAMMING_ERROR_MSG, DROP_ITEM_PROGRAMMING_ERROR_MSG, DATA_ERROR_MSG, DROP_ITEM_DATA_ERROR_MSG, ATTRIBUTE_ERROR_MSG, DROP_ITEM_ATTRIBUTE_ERROR_MSG
from scrapy.exceptions import DropItem

class DB:
    def __init__(self, host, user, passwd, database, port) -> None:
        self.db = connect(host=host, user=user, passwd=passwd, database=database, port=port)
        self.chain = [
            ItemMap('Fanza', FanzaItem, self.insert_fanza_movie),
            ItemMap('Mgstage', MgsItem, self.insert_mgs_movie),
            ItemMap('Fanza Amateur', FanzaAmateurItem, self.insert_fanza_amateur_movie),
            ItemMap('S1 Actress', S1ActressItem, self.insert_s1_actress),
            ItemMap('Prestige Actress', PrestigeActressItem, self.insert_prestige_actress),
            ItemMap('Faleno Actress', FalenoActressItem, self.insert_faleno_actress),
        ]
        self.logger = logging.getLogger("database-mysql")

    def trans_dispatch(self, item: Item) -> str:
        for map in self.chain:
            if isinstance(item, map.type):
                self.logger.info('--------------------------------------Sync %s mysql-------------------------------------', map.itemName)
                try:
                    return map.callback(item)
                except ProgrammingError as err:
                    self.db.rollback()
                    self.logger.exception(PROGRAMMING_ERROR_MSG, err)
                    raise DropItem(DROP_ITEM_PROGRAMMING_ERROR_MSG.format(item))
                except DataError as err:
                    self.db.rollback()
                    self.logger.exception(DATA_ERROR_MSG, err)
                    raise DropItem(DROP_ITEM_DATA_ERROR_MSG.format(item))
                except AttributeError as err:
                    self.db.rollback()
                    self.logger.exception(ATTRIBUTE_ERROR_MSG, err)
                    raise DropItem(DROP_ITEM_ATTRIBUTE_ERROR_MSG.format(item))

    def insert_fanza_movie(self, fanza_item: FanzaItem) -> str:
        pass

    def insert_mgs_movie(self, mgs_item: MgsItem) -> str:
        pass

    def insert_fanza_amateur_movie(self, fanza_amateur_item: FanzaAmateurItem) -> str:
        pass

    def insert_s1_actress(self, s1_actress_item: S1ActressItem) -> str:
        pass

    def insert_prestige_actress(self, prestige_actress_item: PrestigeActressItem) -> str:
        pass

    def insert_faleno_actress(self, faleno_actress_item: FalenoActressItem) -> str:
        pass

class AvDB(DB):
    def __init__(self, host, user, passwd, database, port) -> None:
        super().__init__(host, user, passwd, database, port)
        
    def insert_fanza_movie(self, fanza_item: FanzaItem) -> str:
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
        return fanza_item.censoredId

    def insert_mgs_movie(self, mgs_item: MgsItem) -> str:
        self.insert_avbook_mgs(mgs_item, LABEL_TABLE)
        self.insert_avbook_mgs(mgs_item, MAKER_TABLE)
        self.insert_avbook_mgs(mgs_item, SERIES_TABLE)
        for genre_name in mgs_item.genre:
            self.insert_avbook_mgs_list(mgs_item, genre_name, GENRE_TABLE)
        for actress_name in mgs_item.actress:
            self.insert_avbook_mgs_list(mgs_item, actress_name, ACTRESS_TABLE)
        self.insert_avbook_mgs_movie(mgs_item)
        return mgs_item.censoredId

    def insert_fanza_amateur_movie(self, fanza_amateur_item: FanzaAmateurItem) -> str:
        self.insert_avbook_fanza_amateur_movie(fanza_amateur_item)
        self.insert_avbook_fanza_amateur(fanza_amateur_item, LABEL_TABLE)
        for genre_id, genre_name in fanza_amateur_item.genre.items():
            self.insert_avbook_fanza_amateur_dict(int(genre_id), genre_name, GENRE_TABLE, fanza_amateur_item)
        return fanza_amateur_item.censoredId

    def insert_s1_actress(self, s1_actress_item: S1ActressItem) -> str:
        self.insert_avbook_s1_actress(s1_actress_item)
        return s1_actress_item.actressName

    def insert_prestige_actress(self, prestige_actress_item: PrestigeActressItem) -> str:
        self.insert_avbook_prestige_actress(prestige_actress_item)
        return prestige_actress_item.actressName
    
    def insert_faleno_actress(self, faleno_actress_item: FalenoActressItem) -> str:
        self.insert_avbook_faleno_actress(faleno_actress_item)
        return faleno_actress_item.actressName

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
            try:
                cursor.execute(sql_movie, (
                    fanza_item.censoredId,
                    fanza_item.title,
                    fanza_item.releaseDate,
                    fanza_item.videoLen,
                    fanza_item.makerId,
                    fanza_item.labelId,
                    fanza_item.seriesId
                ))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_item.censoredId, err)            

    def insert_avbook_mgs_movie(self, mgs_item: MgsItem):
        if mgs_item.censoredId is None:
            return
        with self.db.cursor() as cursor:
            sql_movie = "INSERT INTO `avbook_mgs_movie` (`censored_id`," \
                        "`title`," \
                        "`release_date`," \
                        "`video_len`," \
                        "`maker_id`," \
                        "`label_id`," \
                        "`series_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql_movie, (
                    mgs_item.censoredId,
                    mgs_item.title,
                    mgs_item.releaseDate,
                    mgs_item.videoLen,
                    mgs_item.makerId,
                    mgs_item.labelId,
                    mgs_item.seriesId
                ))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, mgs_item.censoredId, err)

    def insert_avbook_fanza_amateur_movie(self, fanza_amateur_item: FanzaAmateurItem):
        if fanza_amateur_item is None:
            return
        with self.db.cursor() as cursor:
            sql_movie = "INSERT INTO `avbook_fanza_amateur_movie` (`censored_id`," \
                        "`title`," \
                        "`delivery_date`," \
                        "`video_len`," \
                        "`three_size`," \
                        "`amateur`," \
                        "`label_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql_movie, (
                    fanza_amateur_item.censoredId,
                    fanza_amateur_item.title,
                    fanza_amateur_item.deliveryDate,
                    fanza_amateur_item.videoLen,
                    fanza_amateur_item.threeSize,
                    fanza_amateur_item.amateur,
                    fanza_amateur_item.labelId
                ))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_amateur_item.censoredId, err)
        
    def insert_avbook_s1_actress(self, s1_actress_item: S1ActressItem):
        if s1_actress_item is None:
            return
        with self.db.cursor() as cursor:
            sql_actress = "INSERT INTO `avbook_s1_actress` (`id`," \
                "`actress_name`," \
                "`actress_en_name`," \
                "`birth`," \
                "`height`," \
                "`three_size`," \
                "`birth_place`," \
                "`blood_type`," \
                "`hobby`," \
                "`trick`," \
                "`twitter`," \
                "`ins`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            try:
                cursor.execute(sql_actress, (
                    s1_actress_item.id,
                    s1_actress_item.actressName,
                    s1_actress_item.actressNameEn,
                    s1_actress_item.birth,
                    s1_actress_item.height,
                    s1_actress_item.threeSize,
                    s1_actress_item.birthPlace,
                    s1_actress_item.bloodType,
                    s1_actress_item.hobby,
                    s1_actress_item.trick,
                    s1_actress_item.twitter,
                    s1_actress_item.ins
                ))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, s1_actress_item.actressName, err)
    
    def insert_avbook_prestige_actress(self, prestige_actress_item: PrestigeActressItem):
        if prestige_actress_item is None:
            return
        with self.db.cursor() as cursor:
            sql_actress = "INSERT INTO `avbook_prestige_actress` (`id`," \
                "`actress_name`," \
                "`actress_en_name`," \
                "`birth`," \
                "`height`," \
                "`three_size`," \
                "`birth_place`," \
                "`blood_type`," \
                "`hobby_trick`," \
                "`twitter`," \
                "`ins`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            try:
                cursor.execute(
                    sql_actress, (
                        prestige_actress_item.id,
                        prestige_actress_item.actressName,
                        prestige_actress_item.actressNameEn,
                        prestige_actress_item.birth,
                        prestige_actress_item.height,
                        prestige_actress_item.threeSize,
                        prestige_actress_item.birthPlace,
                        prestige_actress_item.bloodType,
                        prestige_actress_item.hobbyTrick,
                        prestige_actress_item.twitter,
                        prestige_actress_item.ins
                    )
                )
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, prestige_actress_item.actressName, err)
    
    def insert_avbook_faleno_actress(self, faleno_actress_item: FalenoActressItem):
        if faleno_actress_item is None:
            return
        with self.db.cursor() as cursor:
            sql_actress = "INSERT INTO `avbook_faleno_actress` (" \
                    "`actress_name`," \
                    "`actress_en_name`," \
                    "`birth`," \
                    "`height`," \
                    "`three_size`," \
                    "`birth_place`," \
                    "`hobby`," \
                    "`trick`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(
                    sql_actress, (
                        faleno_actress_item.actressName,
                        faleno_actress_item.actressNameEn,
                        faleno_actress_item.birth,
                        faleno_actress_item.height,
                        faleno_actress_item.threeSize,
                        faleno_actress_item.birthPlace,
                        faleno_actress_item.hobby,
                        faleno_actress_item.trick
                    )
                )
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, faleno_actress_item.actressName, err)
            

    def insert_avbook_fanza(self, fanza_item: FanzaItem, attr: str):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(attr)
            id = getattr(fanza_item, attr + 'Id')
            name = getattr(fanza_item, attr + 'Name')
            if id is None or name is None:
                return
            try:
                cursor.execute(sql_insert, (id, name))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_item.censoredId, err)

    def insert_avbook_fanza_dict(self, id: int, name: str, table: str, fanza_item: FanzaItem):
        if id is None or name is None:
                return
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(table)
            try:
                cursor.execute(sql_insert, (id, name))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_item.censoredId, err)
    
    def insert_avbook_fanza_rel(self, fanza_item: FanzaItem, id: int, table: str):
        if id is None:
            return
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_movie_{0}_rel` (`censored_id`, `{0}_id`) VALUES (%s, %s)".format(table)
            try:
                cursor.execute(sql_insert, (fanza_item.censoredId, id))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_item.censoredId, err)
                
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
                id = cursor.lastrowid
                cursor.execute(sql_insert_rel, (mgs_item.censoredId, id))
                self.db.commit()
            else:
                id = result[0]

    def insert_avbook_fanza_amateur(self, fanza_amateur_item: FanzaAmateurItem, attr: str):
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_amateur_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(attr)
            id = getattr(fanza_amateur_item, attr + 'Id')
            name = getattr(fanza_amateur_item, attr + 'Name')
            if id is None or name is None:
                return
            try:
                cursor.execute(sql_insert, (id, name))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_amateur_item.censoredId, err)
    
    def insert_avbook_fanza_amateur_dict(self, id: int, name: str, table: str, fanza_amateur_item: FanzaAmateurItem):
        if id is None or name is None:
            return
        with self.db.cursor() as cursor:
            sql_insert = "INSERT INTO `avbook_fanza_amateur_{0}` (`{0}_id`, `{0}_name`) VALUES (%s, %s)".format(table)
            sql_insert_rel = "INSERT INTO `avbook_fanza_amateur_movie_{0}_rel` (`censored_id`, `{0}_id`) VALUES (%s, %s)".format(table)
            try:
                cursor.execute(sql_insert, (id, name))
                cursor.execute(sql_insert_rel, (fanza_amateur_item.censoredId, id))
                self.db.commit()
            except IntegrityError as err:
                self.db.rollback()
                self.logger.debug(INTEGRITY_ERROR_MSG, fanza_amateur_item.censoredId, err)
