import json
import boto3
import base64


# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2024-03-14-07-24-09-804" 
client= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # Decode the image data
    x=event['image_data']
    image = base64.b64decode(x)   

    # Instantiate a Predictor
    predictor = client.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/x-image', Body=image)
     ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    
    
    # Make a prediction:
    inferences = predictor['Body'].read().decode('utf-8')
    ## TODO: fill in
    
    # We return the data back to the Step Function    
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')]
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['image_data'],
            "s3_bucket": event['s3_bucket'],
            "s3_key": event['s3_key'],
            "inferences": event['inferences'],
        }
    }