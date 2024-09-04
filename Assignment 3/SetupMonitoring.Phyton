import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import (
    MetricAlertResource, 
    RuleMetricDataSource, 
    ThresholdRuleCondition, 
    RuleAction
)

# Authenticate to Azure
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
monitor_client = MonitorManagementClient(credential, subscription_id)

# Variables
resource_group = "rg-webapp"
vm_name = "webvm-0"
vm_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}"

# Configure CPU usage alert
alert_rule_name = "CPU_Usage_Alert"
alert_rule = MetricAlertResource(
    location="global",
    criteria=[
        ThresholdRuleCondition(
            data_source=RuleMetricDataSource(
                resource_uri=vm_id,
                metric_name="Percentage CPU"
            ),
            operator="GreaterThan",
            threshold=80,
            time_aggregation="Average"
        )
    ],
    actions=[],
    enabled=True,
    description="Alert when CPU usage exceeds 80%",
    severity=3
)

monitor_client.metric_alerts.create_or_update(
    resource_group_name=resource_group,
    rule_name=alert_rule_name,
    parameters=alert_rule
)

# List active alerts
alerts = monitor_client.metric_alerts.list_by_resource_group(resource_group_name=resource_group)
for alert in alerts:
    print(f"Alert Name: {alert.name}, State: {alert.enabled}, Severity: {alert.severity}, Description: {alert.description}")
