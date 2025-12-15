# Project Steps

1. Làm theo Tutorials trong C5L3, sẽ tạo đc 1 Redshift workgroup, 2 Airflow connections `aws_credentials, redshift`
2. Set up Airflow  
   Env vars:
   ```bash
   AIRFLOW__CORE__TEST_CONNECTION=Enabled
   AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=10
   ```
 
    Requirements: \
    `apache-airflow-providers-amazon==9.10.0`
3. Tạo S3 bucket `nd027-hieu` (nhớ sửa `s3_bucket` trong file `final_project.py` cho khớp) -> Vào AWS CLI chạy:
   ```bash
   aws s3 cp s3://udacity-dend/log-data/ s3://nd027-hieu/log-data/ --recursive
   aws s3 cp s3://udacity-dend/song-data/A/A/ s3://nd027-hieu/song-data/A/A/ --recursive
   aws s3 cp s3://udacity-dend/log_json_path.json s3://nd027-hieu/
   ```
 4. Chạy DAG -> Vào Redshift, query data để kiểm tra
