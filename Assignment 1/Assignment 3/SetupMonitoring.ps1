# Login to Azure account
Connect-AzAccount

# Variables
$ResourceGroupName = "rg-webapp"
$VMName = "webvm-0"

# Set up monitoring for a VM
$VM = Get-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName

# Configure metrics and logs
Add-AzMetricAlertRuleV2 -Name "CPU_Usage_Alert" -ResourceGroupName $ResourceGroupName -TargetResourceId $VM.Id -MetricName "Percentage CPU" -Operator GreaterThan -Threshold 80 -WindowSize 00:05:00 -TimeAggregation Average -ActionGroupId "/subscriptions/<SubscriptionID>/resourceGroups/<ResourceGroup>/providers/microsoft.insights/actionGroups/<ActionGroupName>"

# List active alerts
$alerts = Get-AzMetricAlertRuleV2 -ResourceGroupName $ResourceGroupName
$alerts | Format-Table Name, State, Severity, Description
