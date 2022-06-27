from pyspark.sql import SparkSession
from pyspark.sql import functions as F

import socket

LOCAL_IP = socket.gethostbyname(socket.gethostname())

spark = SparkSession\
    .builder\
    .master("k8s://https://10.32.7.103:6443")\
    .config("spark.driver.host", LOCAL_IP)\
    .config("spark.driver.memory", "4g")\
    .config("spark.driver.bindAddress", "0.0.0.0")\
    .config("spark.executor.instances", "1")\
    .config("spark.executor.cores", '1')\
    .config("spark.executor.memory", "4g")\
    .config("spark.kubernetes.namespace", "mrjazanov-338247")\
    .config("spark.kubernetes.container.image.pullPolicy", "Always")\
    .config("spark.kubernetes.container.image", "node03.st:5000/spark-executor:mrjazanov-338247")\
    .config("spark.kubernetes.executor.deleteOnTermination", "true")\
    .config("spark.driver.extraClassPath","./clickhouse-native-jdbc-shaded-2.6.5.jar")\
    .config("spark.executor.extraClassPath", "./clickhouse-native-jdbc-shaded-2.6.5.jar")\
    .config("spark.jars", "./clickhouse-native-jdbc-shaded-2.6.5.jar")\
    .getOrCreate()

url="jdbc:clickhouse://clickhouse-0.clickhouse.clickhouse"
user="mrjazanov_338247" #replace by whatever you use
password="6TGFWHEOeX" #same here
dbtable='mrjazanov_338247.ibd_dist_sales_autodoc'
driver="com.github.housepower.jdbc.ClickHouseDriver"

sales_autodoc = spark.read.option("header", "true").csv('hdfs:///tmp/mkoroleva-309944/sales_autodoc.csv', inferSchema=True)
sales_autodoc_cleand = sales_autodoc.drop_duplicates().dropna().withColumn('date', F.to_timestamp('date', 'yyyy-MM-dd'))
sales_autodoc_cleand.write.format('jdbc').option('driver',driver).option('url',url).option('user',user).option('password',password).option('dbtable',dbtable).save(mode='append')