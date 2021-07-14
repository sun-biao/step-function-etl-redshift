# step-function-etl-redshift



ETL步骤:
1. 创建mysql作为source,创建源表，注意security group
2. 作为redshift 作为target，创建目标表以及store procedure。 注意security group ,并创建secret manager key
3. 创建lambda来调用redshift (需要redshift-data作为endpooint，并且注意lambda 需要需要的安全组和子网要能访问endpoint和redshift)，lambda要赋予vpc权限用来创建销毁eni
4. 创建SNS用来通知事故
5. 创建glue connection/crawler/job 用来完成etl (需要 s3的endpoint)
6. 创建一个stepfunction,注意 gluejob的output,以及wait到结束，注意step function需要有读取glue 状态的权限
