import boto3

ec2 = boto3.client("ec2")

def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    instances_to_stop = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            tags = {
                tag["Key"]: tag["Value"]
                for tag in instance.get("Tags", [])
            }

            if tags.get("Name") == "Cost-Optimizer-Test":
                instances_to_stop.append(instance_id)

    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)

        print("Stopped instances:", instances_to_stop)

        return {
            "statusCode": 200,
            "message": "EC2 instance stopped successfully",
            "instances": instances_to_stop
        }

    print("No matching running instances found")

    return {
        "statusCode": 200,
        "message": "No matching running instances found"
    }
