import boto3

def create_varlog_usage_alarms():
    region = "ap-southeast-1"  # Sesuaikan dengan region AWS kamu
    namespace = "CWAgent"      # Namespace untuk CloudWatch Agent
    metric_name = "disk_used_percent"  # Nama metrik yang digunakan
    threshold = 80.0  # Threshold penggunaan disk untuk /var/log
    sns_topic_arn = "arn:aws:sns:ap-southeast-1:686255980268:CloudOps"  # ARN SNS Topic kamu

    # Inisialisasi client CloudWatch
    cw = boto3.client("cloudwatch", region_name=region)

    print("Fetching available metrics for 'disk_used_percent' with path '/var/log'...")

    # Mengambil metrik dari CloudWatch
    response = cw.list_metrics(Namespace=namespace, MetricName=metric_name)
    metrics = response.get("Metrics", [])

    if not metrics:
        print("No metrics found for 'disk_used_percent'. Ensure CloudWatch Agent is configured and running.")
        return

    # Iterasi melalui metrik dan filter untuk path '/var/log'
    for metric in metrics:
        instance_id = None
        path = None

        for dimension in metric["Dimensions"]:
            if dimension["Name"] == "InstanceId":
                instance_id = dimension["Value"]
            if dimension["Name"] == "path":
                path = dimension["Value"]

        # Hanya buat alarm untuk path '/var/log'
        if instance_id and path == "/var/log":
            alarm_name = f"DiskUsedPercent-{instance_id}-varlog"
            print(f"Creating alarm: {alarm_name}")

            try:
                cw.put_metric_alarm(
                    AlarmName=alarm_name,
                    Namespace=namespace,
                    MetricName=metric_name,
                    Statistic="Average",
                    Period=300,
                    EvaluationPeriods=1,
                    Threshold=threshold,
                    ComparisonOperator="GreaterThanThreshold",
                    ActionsEnabled=True,
                    AlarmActions=[sns_topic_arn],
                    Dimensions=[
                        {"Name": "InstanceId", "Value": instance_id},
                        {"Name": "path", "Value": path}
                    ]
                )
                print(f"Alarm created successfully: {alarm_name}")
            except Exception as e:
                print(f"Failed to create alarm for {alarm_name}: {e}")

if __name__ == "__main__":
    create_varlog_usage_alarms()
