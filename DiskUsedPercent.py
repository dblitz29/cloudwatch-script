import boto3

def create_disk_usage_alarms():
    region = "ap-southeast-1"  # Sesuaikan dengan region AWS kamu
    namespace_ec2 = "CWAgent"  # Namespace untuk CloudWatch Agent pada EC2
    namespace_rds = "AWS/RDS"  # Namespace untuk CloudWatch RDS
    metric_name_ec2 = "disk_used_percent"  # Metrik Disk Used Percent untuk EC2
    metric_name_rds = "FreeStorageSpace"  # Metrik Disk Used untuk RDS
    threshold_ec2 = 80.0  # Threshold untuk EC2
    threshold_rds = 80.0  # Threshold untuk RDS dalam persen
    sns_topic_arn = "arn:aws:sns:ap-southeast-1:686255980268:CloudOps"  # ARN SNS Topic untuk notifikasi

    cw = boto3.client("cloudwatch", region_name=region)

    # Fungsi untuk membuat alarm pada EC2
    def create_ec2_disk_alarms():
        print("Fetching EC2 metrics for 'disk_used_percent'...")
        response = cw.list_metrics(Namespace=namespace_ec2, MetricName=metric_name_ec2)
        metrics = response.get("Metrics", [])

        if not metrics:
            print("No EC2 disk metrics found.")
            return

        for metric in metrics:
            instance_id = None
            path = None

            for dimension in metric["Dimensions"]:
                if dimension["Name"] == "InstanceId":
                    instance_id = dimension["Value"]
                if dimension["Name"] == "path":
                    path = dimension["Value"]

            if instance_id and path:
                alarm_name = f"DiskUsedPercent-EC2-{instance_id}-{path.replace('/', '-')}"
                print(f"Creating EC2 alarm: {alarm_name}")

                try:
                    cw.put_metric_alarm(
                        AlarmName=alarm_name,
                        Namespace=namespace_ec2,
                        MetricName=metric_name_ec2,
                        Statistic="Average",
                        Period=300,
                        EvaluationPeriods=1,
                        Threshold=threshold_ec2,
                        ComparisonOperator="GreaterThanThreshold",
                        ActionsEnabled=True,
                        AlarmActions=[sns_topic_arn],
                        Dimensions=[
                            {"Name": "InstanceId", "Value": instance_id},
                            {"Name": "path", "Value": path}
                        ]
                    )
                    print(f"EC2 Alarm created: {alarm_name}")
                except Exception as e:
                    print(f"Failed to create EC2 alarm for {alarm_name}: {e}")

    # Fungsi untuk membuat alarm pada RDS
    def create_rds_disk_alarms():
        print("Fetching RDS metrics for 'FreeStorageSpace'...")
        response = cw.list_metrics(Namespace=namespace_rds, MetricName=metric_name_rds)
        metrics = response.get("Metrics", [])

        if not metrics:
            print("No RDS disk metrics found.")
            return

        for metric in metrics:
            db_instance_identifier = None

            for dimension in metric["Dimensions"]:
                if dimension["Name"] == "DBInstanceIdentifier":
                    db_instance_identifier = dimension["Value"]

            if db_instance_identifier:
                alarm_name = f"DiskUsedPercent-RDS-{db_instance_identifier}"
                print(f"Creating RDS alarm: {alarm_name}")

                try:
                    cw.put_metric_alarm(
                        AlarmName=alarm_name,
                        Namespace=namespace_rds,
                        MetricName=metric_name_rds,
                        Statistic="Average",
                        Period=300,
                        EvaluationPeriods=1,
                        Threshold=threshold_rds,
                        ComparisonOperator="LessThanThreshold",
                        ActionsEnabled=True,
                        AlarmActions=[sns_topic_arn],
                        Dimensions=[
                            {"Name": "DBInstanceIdentifier", "Value": db_instance_identifier}
                        ]
                    )
                    print(f"RDS Alarm created: {alarm_name}")
                except Exception as e:
                    print(f"Failed to create RDS alarm for {alarm_name}: {e}")

    # Jalankan kedua fungsi untuk EC2 dan RDS
    create_ec2_disk_alarms()
    create_rds_disk_alarms()

if __name__ == "__main__":
    create_disk_usage_alarms()
