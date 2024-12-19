import json
import boto3

def lambda_handler(event, context):
    metric_name = event.get("metric_name", "mem_used_percent")  # Metrik memori
    namespace = event.get("namespace", "CWAgent")  # Namespace untuk CWAgent
    threshold = event.get("threshold", 80)  # Threshold penggunaan memori
    account_name = event.get("account_name", "Shared Services")
    account_number = event.get("account_number", "686255980268")  # AWS Account ID kamu
    environment = event.get("environment", "prod")
    region = event.get("region", "ap-southeast-1")  # Region AWS
    
    cw = boto3.client("cloudwatch", region_name=region)
    print("Fetching available metrics...")

    # Ambil metrik memori yang tersedia di namespace CWAgent
    response = cw.list_metrics(Namespace=namespace, MetricName=metric_name)
    availMetrics = response["Metrics"]
    
    for metric in availMetrics:
        instance_id = None
        for dimension in metric["Dimensions"]:
            if dimension["Name"] == "InstanceId":
                instance_id = dimension["Value"]
        
        if instance_id:
            alarm_name = f"{environment.upper()} {account_name.upper()} - {metric_name} - {instance_id}"
            print(f"Creating Alarm: {alarm_name}")
            try:
                cw.put_metric_alarm(
                    AlarmName=alarm_name,
                    ComparisonOperator="GreaterThanThreshold",
                    EvaluationPeriods=1,
                    Threshold=threshold,
                    ActionsEnabled=True,
                    AlarmActions=["arn:aws:sns:ap-southeast-1:686255980268:CloudOps"],  # ARN SNS Topic
                    MetricName=metric_name,
                    Namespace=namespace,
                    Period=300,
                    Statistic="Average",
                    Dimensions=[
                        {"Name": "InstanceId", "Value": instance_id}
                    ]
                )
                print(f"Alarm created successfully: {alarm_name}")
            except Exception as e:
                print(f"Error creating alarm for {instance_id}: {e}")

if __name__ == "__main__":
    # Event dummy untuk eksekusi lokal
    event = {
        "metric_name": "mem_used_percent",
        "namespace": "CWAgent",
        "threshold": 80,
        "account_name": "Shared Services",
        "account_number": "686255980268",
        "environment": "prod",
        "region": "ap-southeast-1"
    }
    lambda_handler(event, None)
