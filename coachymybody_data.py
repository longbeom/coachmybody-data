import csv

import pymysql

from config import Config


def fitness_csv_to_db():
    conn = pymysql.connect(host=Config.HOST, port=Config.PORT, user=Config.USER, passwd=Config.PASSWORD, db=Config.DB,
                           charset=Config.CHARSET)
    cursor = conn.cursor()

    with open('fitness.csv', newline='') as file:
        reader = csv.reader(file, delimiter='|')
        i = 46 # auto increment로 변경 예정
        for row in reader:
            id = i
            name = row[0]
            body_part = row[1]
            description = row[2]
            caution = row[3]

            insert_sql = "INSERT INTO exercise(id, body_part, category, caution, description, image_uri, name) " \
                         "VALUES(%d, '%s', 'FITNESS', '%s', '%s','기본이미지', '%s')" % (
                             id, body_part, caution, description, name)

            try:
                cursor.execute(insert_sql)
                conn.commit()
                i += 1
            except Exception:
                conn.rollback()


fitness_csv_to_db()
