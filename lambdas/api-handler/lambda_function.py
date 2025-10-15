# lambdas/api-handler/lambda_function.py
import json
import boto3
import uuid
import os
import base64
from datetime import datetime

# Initialize clients
bedrock_agent = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
s3_client = boto3.client('s3')

# Get agent details from environment variables
AGENT_ID = os.environ.get('AGENT_ID', 'ZWOLVYWCJ1')
AGENT_ALIAS_ID = os.environ.get('AGENT_ALIAS_ID', 'EDAOMXHJBL')
S3_BUCKET = os.environ.get('S3_BUCKET', 'threadher-garment-images-2025')

def lambda_handler(event, context):
    """
    API handler for ThreadHer frontend
    Routes requests to Bedrock Agent with image support
    """
    
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        user_query = body.get('query', '')
        session_id = body.get('session_id', str(uuid.uuid4()))
        image_data = body.get('image', None)  # Base64 image from frontend
        
        if not user_query:
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({
                    'error': 'No query provided'
                })
            }
        
        # Prepare input text
        input_text = user_query
        image_key = None
        
        # Handle image if present
        if image_data:
            try:
                print("Processing image upload...")
                
                # Create unique image key
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                image_key = f'uploads/{session_id}/{timestamp}.jpg'
                
                # Decode base64 image
                # Handle both formats: "data:image/jpeg;base64,..." and raw base64
                if ',' in image_data:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                else:
                    image_bytes = base64.b64decode(image_data)
                
                # Upload to S3
                s3_client.put_object(
                    Bucket=S3_BUCKET,
                    Key=image_key,
                    Body=image_bytes,
                    ContentType='image/jpeg'
                )
                
                print(f"Image uploaded to s3://{S3_BUCKET}/{image_key}")
                
                # Add image reference to query for the agent
                input_text = f"{user_query}\n\n[IMAGE UPLOADED: s3://{S3_BUCKET}/{image_key}]\nPlease analyze the garment in the uploaded image."
                
            except Exception as img_error:
                print(f"Image upload error: {str(img_error)}")
                # Continue without image if upload fails
                input_text = f"{user_query}\n\n[Note: Image upload failed, proceeding with text-only analysis]"
        
        print(f"Invoking agent with query: {input_text[:200]}...")
        
        # Invoke Bedrock Agent
        response = bedrock_agent.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=input_text,
            enableTrace=False  # Set to True for debugging
        )
        
        # Collect streaming response
        full_response = ""
        for event_chunk in response['completion']:
            if 'chunk' in event_chunk:
                chunk = event_chunk['chunk']
                if 'bytes' in chunk:
                    full_response += chunk['bytes'].decode('utf-8')
        
        print(f"Agent response: {full_response[:200]}...")
        
        # Return response
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'response': full_response,
                'session_id': session_id,
                'image_stored': image_key if image_key else None
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        }

def options_handler(event, context):
    """Handle OPTIONS requests for CORS"""
    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': ''
    }

def get_cors_headers():
    """Return standard CORS headers"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST, OPTIONS, GET'
    }