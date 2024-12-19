import boto3

def create_alb_unhealthy_target_alarms():
    region = "ap-southeast-1"  # Sesuaikan dengan region AWS kamu
    namespace = "AWS/ApplicationELB"  # Namespace untuk ALB
    metric_name = "UnHealthyHostCount"  # Nama metrik untuk ALB
    threshold = 0  # Threshold Unhealthy Target (> 0)
    sns_topic_arn = "arn:aws:sns:ap-southeast-1:686255980268:CloudOps"  # ARN SNS Topic kamu

    # Inisialisasi client CloudWatch dan ELB
    cw = boto3.client("cloudwatch", region_name=region)
    elbv2 = boto3.client("elbv2", region_name=region)

    print("Fetching Load Balancers...")

    try:
        # Ambil daftar Load Balancers
        response = elbv2.describe_load_balancers()
        load_balancers = response.get("LoadBalancers", [])

        if not load_balancers:
            print("No Load Balancers found.")
            return

        # Iterasi melalui Load Balancers untuk membuat alarm
        for lb in load_balancers:
            lb_arn = lb["LoadBalancerArn"]
            lb_name = lb["LoadBalancerName"]

            # Ambil target groups terkait load balancer
            tg_response = elbv2.describe_target_groups(LoadBalancerArn=lb_arn)
            target_groups = tg_response.get("TargetGroups", [])

            for tg in target_groups:
                tg_name = tg["TargetGroupName"]
                alarm_name = f"ALB-UnhealthyTargets-{lb_name}-{tg_name}"
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
                        {"Name": "LoadBalancer", "Value": lb_arn.split("/")[1]},
                        {"Name": "TargetGroup", "Value": tg["TargetGroupArn"].split(":targetgroup/")[1]}
                    ]
                )
                print(f"Alarm created successfully: {alarm_name}")

    except Exception as e:
        print(f"Failed to create ALB alarms: {e}")

if __name__ == "__main__":
    create_alb_unhealthy_target_alarms()
