import sqlite3
import os

root = os.path.dirname(__file__)
conn = sqlite3.connect(root + '/db/smarthome.db')

c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS sensors (id INTEGER PRIMARY KEY AUTOINCREMENT, sensor1 real, sensor2_value_t real, sensor2_value_h real, datetime string )')

class Sensors():
    def getLast(self):
        c.execute('SELECT round(sensor1, 2), round(sensor2_value_t, 2), round(sensor2_value_h, 2)  FROM sensors ORDER BY id DESC LIMIT 1')
        return c.fetchone()

    def getDay(self):
      sql =  "select "
      sql += "substr(datetime,12,4) || '0' as date, "
      sql += "round(min(sensor1), 2) as sensor1, "
      sql += "round(min(sensor2_value_t), 2) as sensor2_value_t "
      sql += "from sensors "
      sql += "where id in ( select id from sensors order by id desc limit 1440 ) "
      sql += "group by substr(datetime,1,15) || '0' "
      c.execute(sql)
      return c.fetchall()

    def InsertData(self, sensor1, sensor2_value_t, sensor2_value_h, datetime):
        c.execute("INSERT INTO sensors (sensor1, sensor2_value_t, sensor2_value_h, datetime)  VALUES ("+str(sensor1)+","+str(sensor2_value_t)+","+str(sensor2_value_h)+",'"+datetime+"')")
        conn.commit()

'''
from peewee import *

db = SqliteDatabase('/root/weatherstation/sensors.db')

class Sensors(Model):
    id = PrimaryKeyField()
    sensor1 = FloatField()
    datetime = DateTimeField()

    class Meta:
        database = db

    def getLast(self):
        return Sensors.select(Sensors.sensor1).order_by(Sensors.id.desc()).limit(1).get()

    def getDay(self):
        res= Sensors.select(
            fn.Substr(Sensors.datetime, 12, 4).concat('0').alias('date'),
            fn.round(fn.avg(Sensors.sensor1), 2).alias('sensor1')
            ).group_by('date').get()
        return [r[0] for r in res.fetchall()]

#        return Sensors.select(
#            fn.Substr(Sensors.datetime, 12, 4).concat('0').alias('date'),
#            fn.round(fn.avg(Sensors.sensor1), 2).alias('sensor1')
#            ).where(id in Sensors.select(Sensors.id).order_by(Sensors.id).desc().limit(1440).get()  ).group_by('date').get()

# Sensors.create_table()
# Sensors.insert(sensor1=10.5, datetime = datetime.today()).execute()
# print Sensors().getLast().sensor1
#print Sensors().getDay()

 
if __name__ == "__main__":
    try:
        print 'xxxxxxxxxxxxxxxxx'
        Sensors.create_table()
    except peewee.OperationalError:
        print "sensors table already exists!"

'''
