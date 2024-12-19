import boto3

def create_alarm(cw, alarm_name, namespace, metric_name, threshold, dimensions, sns_topic):
    print(f"Creating alarm: {alarm_name}")
    cw.put_metric_alarm(
        AlarmName=alarm_name,
        Namespace=namespace,
        MetricName=metric_name,
        Statistic="Average",
        Period=300,
        EvaluationPeriods=1,
        Threshold=threshold,
        ComparisonOperator="GreaterThanThreshold",
        Dimensions=dimensions,
        AlarmActions=[sns_topic]
    )
    print(f"Alarm created: {alarm_name}")

def main():
    region = "ap-southeast-1"
    sns_topic = "arn:aws:sns:ap-southeast-1:686255980268:CloudOps"
    cw = boto3.client("cloudwatch", region_name=region)

    # Metrics and thresholds
    alarms = [
        {"metric": "mem_used_percent", "namespace": "CWAgent", "threshold": 80, "name": "MemoryUtilization"},
        {"metric": "used_percent", "namespace": "CWAgent", "threshold": 80, "name": "DiskUsedPercent"},
        {"metric": "CPUUtilization", "namespace": "AWS/EC2", "threshold": 80, "name": "CPUUtilization"},
        {"metric": "GroupMaxSize", "namespace": "AWS/AutoScaling", "threshold": 1, "name": "ASGGroupMaxSize"},
        {"metric": "UnHealthyHostCount", "namespace": "AWS/ApplicationELB", "threshold": 0, "name": "ALBUnhealthyTargets"}
    ]

    # Fetch instances and dimensions
    for alarm in alarms:
        response = cw.list_metrics(Namespace=alarm["namespace"], MetricName=alarm["metric"])
        for metric in response["Metrics"]:
            dimensions = metric["Dimensions"]
            alarm_name = f"{alarm['name']}-Alarm"
            create_alarm(cw, alarm_name, alarm["namespace"], alarm["metric"], alarm["threshold"], dimensions, sns_topic)

if __name__ == "__main__":
    main()
