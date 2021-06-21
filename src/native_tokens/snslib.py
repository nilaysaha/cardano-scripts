#!/bin/env python3

import boto3
sns = boto3.client('sns')


class Message:
    def __init__(self):
        pass

    def publish(self):
        # Publish a simple message to the specified SNS topic
        response = sns.publish(
            TopicArn='arn:aws:sns:region:0786589:my-topic-arn',   
            Message='Hello World',   
        )
        
        # Print out the response
        print(response

        )

        
