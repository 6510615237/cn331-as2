# cn331-as2
team member
- พลวิชญ์ วงษ์สุนทร 6510615237
- จักรภัทร สมบัติเจริญเมือง 6510685024

ระบบการขอโควต้าวิชาเรียนของกลุ่มเรามีความสามารถ ดังต่อไปนี้
1.  การเข้าสู่ระบบมีการแยก admin กับ user ธรรมดา (adminใช้/admin/ ส่วน student ใช้ได้แค่ /login/)
2.  admin นั้นสามารถจัดการข้อมูลในรายวิชาได้ และสามารถสร้าง user ให้กับ student ได้
3.  student สามารถดูรายวิชาที่เปิดให้ขอโควต้าได้หลังทำการ login และสามารถยกเลิกเป็นรายวิชาได้ผ่าน (/quota/student_request/) ซึ่งจะเป็นหน้าเพจที่จะแสดงรายวิชาต่าง ๆ ที่ student ได้จดทะเบียนไว้
4.  เราได้เพิ่มฟังก์ชันใหม่ขึ้นมาที่จะแสดง dashboard ที่่จะโชว์จำนวนวิชาทั้งหมด จำนวนการขอสมัครเรียน รายชื่อนักศึกษาในวิชา และสถานะต่างๆ เพื่อความสะดวกในการจัดการของ admin ซึ่งจะมีแค่ admin ที่เข้าถึงได้ผ่าน (/dashboard/)

ลิ้งค์วิดิโอ : https://drive.google.com/file/d/1OgTwDq1CP5FRZhlGbFWVo1Qo5VN0a3vU/view?usp=sharing
