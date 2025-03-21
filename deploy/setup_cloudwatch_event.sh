#!/bin/bash

# === CONFIGURATION ===
REGION="eu-north-1"
ACCOUNT_ID="ACCOUNT_ID"
CLUSTER_NAME="CLUSTER_NAME"
TASK_DEFINITION="TASK_DEFINITION"
SUBNET_ID="subnet-SUBNET_ID"
SECURITY_GROUP_ID="sg-SECURITY_GROUP_ID"
RULE_NAME="run-every-hour"
ROLE_NAME="CloudWatchEventsRole"
RULE_SCHEDULE="rate(1 hour)"

# === 1. Create IAM role (If not exists) ===
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://trust-policy.json || echo "Role exists"

# === 2. Add ECS policy ===
cat > permission-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:RunTask",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name "${ROLE_NAME}Policy" \
  --policy-document file://permission-policy.json

# === 3. Create CloudWatch Rule (if not exists) ===
aws events put-rule \
  --name "$RULE_NAME" \
  --schedule-expression "$RULE_SCHEDULE" \
  --region "$REGION"

# === 4. ADD Target с RoleArn ===
aws events put-targets \
  --rule "$RULE_NAME" \
  --targets "[
    {
      \"Id\": \"1\",
      \"Arn\": \"arn:aws:ecs:$REGION:$ACCOUNT_ID:cluster/$CLUSTER_NAME\",
      \"RoleArn\": \"arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME\",
      \"EcsParameters\": {
        \"TaskDefinitionArn\": \"arn:aws:ecs:$REGION:$ACCOUNT_ID:task-definition/$TASK_DEFINITION\",
        \"LaunchType\": \"FARGATE\",
        \"NetworkConfiguration\": {
          \"awsvpcConfiguration\": {
            \"Subnets\": [\"$SUBNET_ID\"],
            \"SecurityGroups\": [\"$SECURITY_GROUP_ID\"],
            \"AssignPublicIp\": \"ENABLED\"
          }
        }
      }
    }
  ]" \
  --region "$REGION"

# === clean temporary files ===
rm trust-policy.json permission-policy.json

echo "Dove: CloudWatch Event '$RULE_NAME' starts ECS task every hour."
