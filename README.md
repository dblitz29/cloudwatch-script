# 🚀 Auto-Generated AWS Alarms for ALB, ASG, and EC2

This project automates the creation of CloudWatch alarms for various AWS services, including Application Load Balancers (ALB), Auto Scaling Groups (ASG), and EC2 instances. The alarms monitor critical metrics and ensure your infrastructure is healthy and performant.

## 📋 Features

### Alarms for ALB (Application Load Balancer):
- **Unhealthy Targets**: Triggered when the number of unhealthy targets exceeds 0.
- **Response Time**: Triggered when the average response time per target group exceeds 1 second.

### Alarms for ASG (Auto Scaling Group):
- **GroupMaxSize**: Triggered when the group exceeds the maximum size threshold.
- **GroupPendingInstances**: Triggered when pending instances exceed the defined threshold.

### Alarms for EC2:
- **Disk Used Percent**: Monitors disk usage for specific partitions like `/` and `/var/log`.

---

## ⚙️ Setup Instructions

### Prerequisites
1. **AWS CLI** installed and configured with appropriate credentials.
2. **Python 3.7+** installed.
3. **Boto3 library** installed.
   ```bash
   pip install boto3
   ```
4. An existing **SNS Topic** for notifications.

### IAM Permissions
The script requires the following permissions:
- `autoscaling:DescribeAutoScalingGroups`
- `elasticloadbalancing:DescribeLoadBalancers`
- `elasticloadbalancing:DescribeTargetGroups`
- `cloudwatch:PutMetricAlarm`
- `sns:Publish`

---

## 🛠️ How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/aws-alarms-automation.git
cd aws-alarms-automation
```

### 2. Configure AWS Region and SNS Topic
Update the SNS topic ARN and AWS region in the respective Python scripts.

### 3. Run Scripts for Specific Alarms

#### ALB Alarms
- **Unhealthy Targets**:
  ```bash
  python create_alb_unhealthy_alarm.py
  ```
- **Response Time**:
  ```bash
  python create_alb_response_time_alarm.py
  ```

#### ASG Alarms
- **GroupMaxSize**:
  ```bash
  python create_asg_groupmaxsize_alarm.py
  ```
- **GroupPendingInstances**:
  ```bash
  python create_asg_pending_instances_alarm.py
  ```

#### EC2 Alarms
- **Disk Used Percent**:
  ```bash
  python create_disk_usage_alarm.py
  ```

---

## 📊 Alarm Details

### ALB Alarms
| Alarm Name                          | Metric Name         | Threshold |
|-------------------------------------|---------------------|-----------|
| ALB-UnhealthyTargets-<LB>-<TG>      | UnHealthyHostCount  | > 0       |
| ALB-ResponseTime-<LB>-<TG>          | TargetResponseTime  | > 1 sec   |

### ASG Alarms
| Alarm Name                          | Metric Name           | Threshold |
|-------------------------------------|-----------------------|-----------|
| ASG-GroupMaxSize-<ASG>              | GroupMaxSize          | Custom    |
| ASG-PendingInstances-<ASG>          | GroupPendingInstances | > 1       |

### EC2 Alarms
| Alarm Name                          | Metric Name         | Threshold |
|-------------------------------------|---------------------|-----------|
| DiskUsedPercent-EC2-<Instance>-<Path>| disk_used_percent   | > 80%     |

---

## 🎯 Example Output

```plaintext
Fetching Load Balancers...
Creating alarm: ALB-UnhealthyTargets-my-loadbalancer-my-targetgroup
Alarm created successfully: ALB-UnhealthyTargets-my-loadbalancer-my-targetgroup
```

---

## 📌 Notes
- Ensure that CloudWatch Agent is configured and running for EC2 alarms.
- Monitor alarm states in the **CloudWatch Console** under the **Alarms** section.

---

## 🤝 Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue.

---

## 📞 Support
For support or questions, contact [your-email@example.com](mailto:your-email@example.com).

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.