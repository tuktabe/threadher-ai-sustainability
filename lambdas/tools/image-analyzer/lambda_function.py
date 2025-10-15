# lambdas/tools/analyze-garment/lambda_function.py
import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client('s3', region_name='us-east-1')
rekognition = boto3.client('rekognition', region_name='us-east-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_name = os.environ.get('DYNAMODB_TABLE', 'ThreadHerGarments')
table = dynamodb.Table(table_name)

def analyze_image_with_rekognition(bucket_name, image_key):
    """Use AWS Rekognition to detect labels in the image"""
    try:
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_key
                }
            },
            MaxLabels=20,
            MinConfidence=70
        )
        return response.get('Labels', [])
    except Exception as e:
        print(f"Rekognition error: {str(e)}")
        return []

def analyze_with_claude(image_bytes):
    """Use Claude 3 via Bedrock to analyze garment details"""
    try:
        import base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """Analyze this clothing item and provide:
1. Garment type (e.g., t-shirt, jeans, dress, jacket)
2. Primary material (e.g., cotton, polyester, denim, wool)
3. Condition (excellent, good, fair, poor)
4. Style category (casual, formal, athletic, etc.)
5. Estimated age/wear level
6. Any visible brand logos or tags

Respond in JSON format."""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        })
        
        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        analysis_text = response_body['content'][0]['text']
        
        # Try to parse JSON from response
        try:
            return json.loads(analysis_text)
        except:
            # If not valid JSON, create structured response from text
            return {
                'raw_analysis': analysis_text,
                'garment_type': 'unknown',
                'material': 'unknown',
                'condition': 'unknown'
            }
            
    except Exception as e:
        print(f"Claude analysis error: {str(e)}")
        return None

def convert_to_decimal(obj):
    """Convert floats to Decimal for DynamoDB"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    return obj

def lambda_handler(event, context):
    """
    Analyze a garment image using computer vision
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        # Extract parameters
        image_s3_key = body.get('image_s3_key', '').strip()
        bucket_name = body.get('bucket_name', '').strip()
        user_id = body.get('user_id', 'anonymous').strip()
        
        # Validation
        if not image_s3_key or not bucket_name:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'image_s3_key and bucket_name are required'})
            }
        
        print(f"Analyzing image: s3://{bucket_name}/{image_s3_key}")
        
        # Get image from S3
        try:
            s3_response = s3_client.get_object(Bucket=bucket_name, Key=image_s3_key)
            image_bytes = s3_response['Body'].read()
        except Exception as s3_error:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'Image not found: {str(s3_error)}'})
            }
        
        # Analyze with Rekognition
        rekognition_labels = analyze_image_with_rekognition(bucket_name, image_s3_key)
        
        # Analyze with Claude for detailed info
        claude_analysis = analyze_with_claude(image_bytes)
        
        # Generate garment ID
        garment_id = str(uuid.uuid4())
        
        # Compile analysis results
        analysis_result = {
            'garment_id': garment_id,
            'user_id': user_id,
            'image_s3_key': image_s3_key,
            'analyzed_at': datetime.utcnow().isoformat(),
            'rekognition_labels': [
                {'name': label['Name'], 'confidence': label['Confidence']}
                for label in rekognition_labels[:10]
            ],
            'claude_analysis': claude_analysis or {},
            'garment_type': (claude_analysis or {}).get('garment_type', 'unknown'),
            'material': (claude_analysis or {}).get('material', 'unknown'),
            'condition': (claude_analysis or {}).get('condition', 'unknown'),
            'style': (claude_analysis or {}).get('style_category', 'casual')
        }
        
        print(f"Analysis complete: {analysis_result['garment_type']}, {analysis_result['material']}")
        
        # Store in DynamoDB
        try:
            dynamodb_item = convert_to_decimal(analysis_result)
            table.put_item(Item=dynamodb_item)
            print("Stored analysis in DynamoDB")
        except Exception as db_error:
            print(f"Warning: Could not store in DynamoDB: {str(db_error)}")
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'garment_id': garment_id,
                'analysis': analysis_result
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e), 'message': 'Failed to analyze garment'})
        }