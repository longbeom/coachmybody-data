import csv

import pymysql

from config import Config


def fitness_csv_to_db():
    conn = pymysql.connect(host=Config.HOST, port=Config.PORT, user=Config.USER, passwd=Config.PASSWORD, db=Config.DB,
                           charset=Config.CHARSET)
    cursor = conn.cursor()

    with open('fitness.csv', newline='') as file:
        reader = csv.reader(file, delimiter='|')
        i = 46
        for row in reader:
            id = i
            name = row[0]
            body_part = row[1]
            description = row[2]
            caution = row[3]

            insert_exercise_sql = "INSERT INTO exercise(id, body_part, category, caution, description, image_uri, name) " \
                                  "VALUES(%d, '%s', 'FITNESS', '%s', '%s','기본이미지', '%s')" % \
                                  (id, body_part, caution, description, name)

            lab = row[4]
            set = int(row[5][:-3])

            if lab.endswith('분'):
                lab = int(lab[:-1])
                insert_exercise_record_sql = "INSERT INTO exercise_record(exercise_id, type, exercise_minutes, exercise_set) " \
                                             "VALUES(%d, 'TIME_SET', %d, %d)" % (id, lab, set)
            else:
                lab = int(lab[:-1])
                insert_exercise_record_sql = "INSERT INTO exercise_record(exercise_id, type, exercise_lab, exercise_set) " \
                                             "VALUES(%d, 'LAB_SET', %d, %d)" % (id, lab, set)

            try:
                # cursor.execute(insert_exercise_sql)
                cursor.execute(insert_exercise_record_sql)
                conn.commit()
                i += 1
            except Exception as ex:
                print('에러 발생 ', ex)
                conn.rollback()


fitness_csv_to_db()
