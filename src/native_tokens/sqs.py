#!/usr/bin/env python3

import boto3

# Create SQS client
sqs = boto3.client('sqs')

class MSQS:
    """
    The message attributes is a simple json object of a certain format:
    {
    'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        }
    }

    The message is just a: 'string like this'.

    Every message has a retention period and should be deleted explicitly.
    For standard queues, it is possible to receive a message even after you delete it. This might happen on rare occasions if 
    one of the servers which stores a copy of the message is unavailable when you send the request to delete the message. The 
    copy remains on the server and might be returned to you during a subsequent receive request. You should ensure that your 
    application is idempotent, so that receiving a message more than once does not cause issues.

    """
    
    def __init__(self, queue):
        self.qurl = "https://sqs.eu-central-1.amazonaws.com/839835762980/"+queue
        self.delay = 10 #in seconds
        self.MaxNumMsg = 1
        self.VisibilityTimeout = 0
        self.WaitTimeSeconds = 0
        self.MessageAttributeNames = ["All"]
        self.AttributeNames = ["SentTimestamp"]
        
    def send_msg(self, msg_attr, msg):
        response = sqs.send_message(QueueUrl=self.qurl,
                                    self.delay,
                                    MessageAttributes=msg_attr,
                                    MessageBody=msg )
        return response["MessageId"]

    def recv_msg(self):
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=self.qurl,
            AttributeNames=self.AttributeNames,
            MaxNumberOfMessages=self.MaxNumMsg,
            MessageAttributeNames=self.MessageAttributeNames,
            VisibilityTimeout=self.VisibilityTimeout,
            WaitTimeSeconds=self.WaitTimeSeconds)
        return response['Messages'][0]

    def delete_msg(self, receipt_handle):
        """
        after recieving the response from recv_msg above, 
        receipt_handle = message['ReceiptHandle']
        where 'message' is the response from recv_msg
        """
        sqs.delete_message(
            QueueUrl=self.qurl,
            ReceiptHandle=receipt_handle
        )
        
