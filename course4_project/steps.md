# Project Steps

Data: https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project

S3 bucket sẽ có dạng:
- `stedi-lake-house-hieu`
  - `customer/`
     - `landing/`
     - `trusted/`
  - `accelerometer/`
    - `landing/`
    - `trusted/`
  - `step_trainer/`
    - `landing/`
    - `trusted/`
  - `ml_curated/`
1. Làm theo Tutorials trong C4L4 và C4L5, sẽ có các tables sau trong Athena: `customer_landing, customer_trusted, accelerometer_landing, accelerometer_trusted`
2. Copy data của `step_trainer/landing` vào S3, ở Athena tạo table `step_trainer_landing`
3. Tạo Glue job để join `step_trainer_landing` với `customer_trusted`, tạo ra `step_trainer/trusted/` ở S3. Dùng Transform SQL:
   ```sql
   select s.sensorReadingTime, s.serialNumber, s.distanceFromObject
   from step_trainer_landing s
   join customer_trusted c
   on c.serialNumber = s.serialNumber 
   ```
   (ko dùng Transform Join vì sẽ join lỗi do có 2 cols trùng tên) \
   Ở Athena tạo table `step_trainer_trusted`.
4. Tạo Glue job để join `step_trainer_trusted` với `accelerometer_trusted`, tạo ra `ml_curated/` ở S3. Dùng Transform SQL:
   ```sql
   select *
   from step_trainer_trusted s
   join accelerometer_trusted a
   on a.timeStamp = s.sensorReadingTime 
   ```
