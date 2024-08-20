CREATE TABLE IF NOT EXISTS customer_landing (
  serialnumber TEXT,
  sharewithpublicasofdate INT,
  birthday TEXT,
  registrationdate INT,
  sharewithresearchasofdate INT,
  customername TEXT,
  email TEXT,
  lastupdatedate INT,
  phone TEXT,
  sharewithfriendsasofdate INT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE',
  'mapping' = 'TRUE'
)
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://cd0030bucket/customers/'
TBLPROPERTIES ('classification' = 'json');