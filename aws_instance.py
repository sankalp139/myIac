
import boto3
from base import Resource

class AWSInstance(Resource):
    def create(self):
        ec2 = boto3.resource('ec2', region_name=self.properties.get('region'))
                # Add default Name tag using logical resource name
        tags = [{
            'Key': 'Name',
            'Value': self.name  # Use the logical name from infra.yaml
        }]

        if 'tags' in self.properties:
            for k, v in self.properties['tags'].items():
                tags.append({'Key': k, 'Value': v})
        instance = ec2.create_instances(
            ImageId=self.properties['ami'],
            InstanceType=self.properties['instance_type'],
            MinCount=1,
            MaxCount=1,
            KeyName=self.properties.get('key_name'),
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': tags
                }
            ]
        )[0]
        instance.wait_until_running()
        return instance.id
    
    def destroy(self, instance_id):
        print(f"Destroying EC2 instance: {instance_id}")
        ec2 = boto3.resource('ec2', region_name=self.properties.get('region'))
        instance = ec2.Instance(instance_id)
        response = instance.terminate()
        print("Termination initiated.")
        return response