import json
import boto3
import time

client = boto3.client('redshift-data')
def lambda_handler(event, context):
    # TODO implement
    print('start.....')
    try:
        response = client.execute_statement(
            ClusterIdentifier='redshift-cluster-1',
            Database='dev',
            SecretArn=<YOUR REDSHIFT SECRET ARN>,
            # Parameters=[
            #     {
            #         'name': 'f1',
            #         'value': '2021-06-23 07:41:18'
            #     },
            # ],
            Sql='call test_sp1(1000000)',
            # Sql='select count(*) from redshifttestdb_table1',
            StatementName='get result'
        )
    except Exception as e:
        subject = "Error:" + ":" + str(e)
        print(subject)
        raise
    query_id = response["Id"]
    done = False
    while not done:
        time.sleep(1)
        status = status_check(client, query_id)
        if status in ("STARTED", "FAILED", "FINISHED"):
            print("status is: {}".format(status))
            break
    print(response)
    desc = client.describe_statement(Id=response["Id"])
    result = client.get_statement_result(Id=response["Id"])
    print(result)
    return str(result)
def status_check(client, query_id):
    desc = client.describe_statement(Id=query_id)
    status = desc["Status"]
    if status == "FAILED":
        raise Exception('SQL query failed:' + query_id + ": " + desc["Error"])
    return status.strip('"')
