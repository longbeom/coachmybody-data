from statistics import mode

import pymysql

from config import Config


def get_main_part_by_muscles():
    conn = pymysql.connect(host=Config.HOST, port=Config.PORT, user=Config.USER, passwd=Config.PASSWORD, db=Config.DB,
                           charset=Config.CHARSET)
    cursor = conn.cursor()

    sql = 'SELECT exercise_id, bps.id FROM exercise e ' \
          'LEFT JOIN exercise_to_muscle etm ON e.id = etm.exercise_id ' \
          'LEFT JOIN muscle m ON etm.muscle_id = m.id ' \
          'LEFT JOIN body_part_sub bps on m.body_part_sub_id = bps.id ' \
          'ORDER BY exercise_id;'
    cursor.execute(sql)
    rows = cursor.fetchall()

    exercise_body = {}
    for row in rows:
        e_id = row[0]
        bps_id = row[1]
        try:
            exercise_body[e_id] += str(bps_id)
        except KeyError:
            exercise_body[e_id] = str(bps_id)

    try:
        for exercise_id, value in exercise_body.items():
            body_part_id = int(mode(value))
            update_sql = 'UPDATE exercise SET main_body_part_sub_id = %d WHERE id = %d' % (body_part_id, exercise_id)
            cursor.execute(update_sql)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        print('에러 발생', ex)


get_main_part_by_muscles()
