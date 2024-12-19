import json
import boto3

def lambda_handler(event, context):
    metric_name = event.get("metric_name", "CPUUtilization")
    namespace = event.get("namespace", "AWS/EC2")
    threshold = event.get("threshold", 80)
    account_name = event.get("account_name", "Shared Services")
    account_number = event.get("account_number", "686255980268")  # Ganti dengan AWS Account ID
    environment = event.get("environment", "prod")
    region = event.get("region", "ap-southeast-1")  # Sesuaikan region
    
    instance_id_list = []

    availMetrics = []
    cw = boto3.client("cloudwatch", region_name=region)
    
    # Ambil metrik yang tersedia
    response = cw.list_metrics(Namespace=namespace, MetricName=metric_name, RecentlyActive="PT3H")
    availMetrics.extend(response["Metrics"])
    while "NextToken" in response:
        response = cw.list_metrics(Namespace=namespace, MetricName=metric_name, RecentlyActive="PT3H", NextToken=response["NextToken"])
        availMetrics.extend(response["Metrics"])
    
    # Proses metrik
    result = []
    for item in availMetrics:
        tempDict = {}
        dimList = item.get("Dimensions")
        for iter in dimList:
            tempDict[iter["Name"]] = iter["Value"]
        result.append(tempDict)
    
    # Membuat alarm CloudWatch
    for metric in result:
        if metric.get("InstanceId"):
            instance_id_list.append(metric.get("InstanceId"))
            alarm_name = f"{environment.upper()} {account_name.upper()} - {metric_name} - {metric.get('InstanceId')}"
            print(f"Creating Alarm: {alarm_name}")
            try:
                paginator = cw.get_paginator('describe_alarms')
                response_iterator = paginator.paginate(AlarmNames=[alarm_name])
                
                # Cek apakah alarm sudah ada
                alarm_exists = False
                for response in response_iterator:
                    if len(response['MetricAlarms']) > 0:
                        alarm_exists = True
                
                # Jika alarm tidak ada, buat alarm
                if not alarm_exists:
                    cw.put_metric_alarm(
                        AlarmName=alarm_name,
                        ComparisonOperator="GreaterThanThreshold",
                        EvaluationPeriods=1,
                        Threshold=threshold,
                        ActionsEnabled=True,
                        AlarmActions=["arn:aws:sns:ap-southeast-1:686255980268:CloudOps"],  # ARN SNS Topic
                        Metrics=[
                            {
                                'Id': "getMetricData",
                                'AccountId': str(account_number),
                                'MetricStat': {
                                    'Metric': {
                                        'Namespace': namespace,
                                        'MetricName': metric_name,
                                        'Dimensions': [
                                            {
                                                'Name': 'InstanceId',
                                                'Value': metric.get("InstanceId")
                                            },
                                        ]
                                    },
                                    "Period": 300,
                                    'Stat': 'Average',
                                },
                            }
                        ]
                    )
                    print(f"Alarm created: {alarm_name}")
                else:
                    print(f"Alarm already exists: {alarm_name}")
                    
            except Exception as e:
                print(f"Error creating alarm for {metric.get('InstanceId')}: {e}")

if __name__ == "__main__":
    # Event dummy untuk eksekusi lokal
    event = {
        "metric_name": "CPUUtilization",
        "namespace": "AWS/EC2",
        "threshold": 80,
        "account_name": "Shared Services",
        "account_number": "686255980268",
        "environment": "prod",
        "region": "ap-southeast-1"
    }
    lambda_handler(event, None)
