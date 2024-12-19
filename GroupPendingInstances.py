import boto3

def create_asg_pending_instances_alarms():
    region = "ap-southeast-1"  # Sesuaikan dengan region AWS kamu
    namespace = "AWS/AutoScaling"  # Namespace untuk Auto Scaling Group
    metric_name = "GroupPendingInstances"  # Nama metrik untuk ASG
    threshold = 1  # Threshold untuk GroupPendingInstances (sesuaikan kebutuhan)
    sns_topic_arn = "arn:aws:sns:ap-southeast-1:686255980268:CloudOps"  # ARN SNS Topic kamu

    # Inisialisasi client CloudWatch dan Auto Scaling
    cw = boto3.client("cloudwatch", region_name=region)
    asg = boto3.client("autoscaling", region_name=region)

    print("Fetching Auto Scaling Groups...")

    try:
        # Ambil daftar Auto Scaling Groups
        response = asg.describe_auto_scaling_groups()
        auto_scaling_groups = response.get("AutoScalingGroups", [])

        if not auto_scaling_groups:
            print("No Auto Scaling Groups found.")
            return

        # Iterasi melalui ASG untuk membuat alarm
        for group in auto_scaling_groups:
            asg_name = group["AutoScalingGroupName"]

            # Nama alarm dinamis berdasarkan ASG
            alarm_name = f"ASG-PendingInstances-{asg_name}"
            print(f"Creating alarm: {alarm_name}")

            # Membuat alarm di CloudWatch
            cw.put_metric_alarm(
                AlarmName=alarm_name,
                Namespace=namespace,
                MetricName=metric_name,
                Statistic="Average",
                Period=300,  # Interval 5 menit
                EvaluationPeriods=1,
                Threshold=threshold,
                ComparisonOperator="GreaterThanThreshold",
                ActionsEnabled=True,
                AlarmActions=[sns_topic_arn],
                Dimensions=[
                    {"Name": "AutoScalingGroupName", "Value": asg_name}
                ]
            )
            print(f"Alarm created successfully: {alarm_name}")

    except Exception as e:
        print(f"Failed to create ASG alarms: {e}")

if __name__ == "__main__":
    create_asg_pending_instances_alarms()
