# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import mysql.connector
import MySQLdb
from superbet_speciale.items import DaNuItem, InainteDupaItem, F1x2Item, TotaluriItem

class MysqlOdds(object):
    def __init__(self):
        self.connection = MySQLdb.connect('localhost', 'root', '', 'superbet')
        self.cursor = self.connection.cursor()
        
        self.connection.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        if isinstance(item, DaNuItem):
            self.process_danu(item)
            return item
        elif isinstance(item, InainteDupaItem):
            self.process_inainte_dupa(item)
            return item
        elif isinstance(item, F1x2Item):
            self.process_1x2(item)
            return item
        elif isinstance(item, TotaluriItem):
            self.process_total(item)
            return item



    ## for bandy
    def process_danu(self, item):
        self.cursor.execute("""
        INSERT INTO sp_danu (
            s_id,
            group_name,
            type_name,
            da,
            nu
            )
            VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            da = VALUES(da),
            nu = VALUES(nu)
            """, 
        (
            item['s_id'],
            item['group_name'],
            item['odd_name'],
            item['da'],
            item['nu']
            ))
        self.connection.commit()

    def process_inainte_dupa(self, item):
        self.cursor.execute("""
        INSERT INTO sp_inaintedupa (
            s_id,
            group_name,
            type_name,
            minutul,
            inainte,
            dupa
            )
            VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            inainte = VALUES(inainte),
            dupa = VALUES(dupa)
            """, 
        (
            item['s_id'],
            item['group_name'],
            item['odd_name'],
            item['minutul'],
            item['inainte'],
            item['dupa']
            ))
        self.connection.commit()

    def process_1x2(self, item):
        self.cursor.execute("""
        INSERT INTO sp_1x2 (
            s_id,
            group_name,
            type_name,
            _1,
            _x,
            _2
            )
            VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            _1 = VALUES(_1),
            _x = VALUES(_x),
            _2 = VALUES(_2)
            """, 
        (
            item['s_id'],
            item['group_name'],
            item['odd_name'],
            item['_1'],
            item['_x'],
            item['_2']
            ))
        self.connection.commit()

    def process_total(self, item):
        self.cursor.execute("""
        INSERT INTO sp_total (
            s_id,
            group_name,
            type_name,
            sbval,
            sub,
            peste
            )
            VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            sub = VALUES(sub),
            peste = VALUES(peste)
            """, 
        (
            item['s_id'],
            item['group_name'],
            item['odd_name'],
            item['sbval'],
            item['sub'],
            item['peste']
            ))
        self.connection.commit()