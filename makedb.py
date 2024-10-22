import sqlite3
import pandas as pd

# ชื่อไฟล์ CSV และชื่อฐานข้อมูล SQLite
csv_file = 'aihitdata-uk-10k.csv'
sqlite_db = 'database.db'

# อ่านข้อมูลจากไฟล์ CSV ด้วย pandas
df = pd.read_csv(csv_file)

# สร้างการเชื่อมต่อกับ SQLite (หากไม่มีไฟล์ database.db จะถูกสร้างขึ้น)
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# นำเข้าข้อมูล CSV เข้าไปในฐานข้อมูล
# โดยจะสร้างตารางใหม่อัตโนมัติตามโครงสร้างของ DataFrame
table_name = 'aihitdataUK'  # ตั้งชื่อตาราง
df.to_sql(table_name, conn, if_exists='replace', index=False)

# ตรวจสอบว่าข้อมูลถูกนำเข้าแล้ว
cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

# ปิดการเชื่อมต่อฐานข้อมูล
conn.close()