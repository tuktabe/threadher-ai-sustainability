# agents/orchestrator/action_handler.py
import json
import boto3
from datetime import datetime

# Initialize AWS clients
lambda_client = boto3.client('lambda', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    """
    Action handler for Bedrock Agent
    Routes requests to appropriate Lambda functions
    """
    
    print(f"Received event from Bedrock Agent: {json.dumps(event)}")
    
    try:
        # Extract action information from Bedrock Agent event
        agent = event.get('agent', '')
        action_group = event.get('actionGroup', '')
        api_path = event.get('apiPath', '')
        http_method = event.get('httpMethod', 'POST')
        request_body = event.get('requestBody', {})
        
        # Parse parameters from request body
        parameters = {}
        if 'content' in request_body:
            for content_item in request_body['content'].values():
                for prop in content_item:
                    if 'properties' in prop:
                        for param in prop['properties']:
                            param_name = param.get('name', '')
                            param_value = param.get('value', '')
                            parameters[param_name] = param_value
        
        print(f"Action: {api_path}, Parameters: {parameters}")
        
        # Route to appropriate function
        result = route_action(api_path, parameters)
        
        # Return in Bedrock Agent format
        response = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": action_group,
                "apiPath": api_path,
                "httpMethod": http_method,
                "httpStatusCode": 200,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps(result)
                    }
                }
            }
        }
        
        print(f"Returning response: {json.dumps(response)}")
        return response
        
    except Exception as e:
        print(f"Error in action handler: {str(e)}")
        
        # Return error in Bedrock Agent format
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": action_group,
                "apiPath": api_path,
                "httpMethod": http_method,
                "httpStatusCode": 500,
                "responseBody": {
                    "application/json": {
                        "body": json.dumps({
                            "error": str(e)
                        })
                    }
                }
            }
        }


def route_action(api_path, parameters):
    """Route to the appropriate action handler"""
    
    if api_path == '/analyze-garment':
        return analyze_garment(parameters)
    
    elif api_path == '/calculate-carbon':
        return calculate_carbon(parameters)
    
    elif api_path == '/get-circular-options':
        return get_circular_options(parameters)
    
    else:
        return {"error": f"Unknown action: {api_path}"}


def analyze_garment(params):
    """Call the Image Analyzer Lambda"""
    
    print(f"Calling ThreadHer-ImageAnalyzer with params: {params}")
    
    try:
        response = lambda_client.invoke(
            FunctionName='ThreadHer-ImageAnalyzer',
            InvocationType='RequestResponse',
            Payload=json.dumps(params)
        )
        
        result = json.loads(response['Payload'].read())
        print(f"Image Analyzer response: {result}")
        
        # Parse the response
        if result.get('statusCode') == 200:
            body = json.loads(result['body'])
            return body
        else:
            return {"error": "Image analysis failed"}
            
    except Exception as e:
        print(f"Error calling Image Analyzer: {e}")
        return {"error": str(e)}


def calculate_carbon(params):
    """Call the Carbon Calculator Lambda"""
    
    print(f"Calling ThreadHer-CarbonCalculator with params: {params}")
    
    try:
        # Format for Carbon Calculator
        payload = {
            "body": json.dumps(params)
        }
        
        response = lambda_client.invoke(
            FunctionName='ThreadHer-CarbonCalculator',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response['Payload'].read())
        print(f"Carbon Calculator response: {result}")
        
        if result.get('statusCode') == 200:
            body = json.loads(result['body'])
            return body
        else:
            return {"error": "Carbon calculation failed"}
            
    except Exception as e:
        print(f"Error calling Carbon Calculator: {e}")
        return {"error": str(e)}


def get_circular_options(params):
    """Provide circular economy options"""
    
    garment_type = params.get('garment_type', '')
    condition = params.get('condition', '').lower()
    location = params.get('user_location', 'unknown')
    
    options = []
    
    # Based on condition, suggest options
    if condition in ['damaged', 'worn', 'fair']:
        options.append({
            "option": "Repair",
            "description": f"Find a local tailor to repair your {garment_type}",
            "estimated_cost": "$15-40",
            "environmental_benefit": "Extends garment life, saves carbon from producing new item",
            "resources": [
                "Search 'clothing repair near me'",
                "Check if brand offers repair services"
            ]
        })
        
        options.append({
            "option": "Upcycle",
            "description": f"Transform your {garment_type} into something new",
            "estimated_cost": "$0-20",
            "environmental_benefit": "Creative reuse, prevents textile waste",
            "resources": [
                f"YouTube: 'upcycle {garment_type}'",
                "Local craft workshops"
            ]
        })
        
        options.append({
            "option": "Recycle",
            "description": "Textile recycling to create new materials",
            "estimated_cost": "$0",
            "environmental_benefit": "Prevents landfill waste, materials recovery",
            "resources": [
                "H&M Garment Collecting program",
                "The North Face Clothes The Loop",
                "Local textile recycling centers"
            ]
        })
        
    elif condition in ['good', 'new']:
        options.append({
            "option": "Resell",
            "description": f"Sell your {garment_type} on secondhand marketplace",
            "estimated_value": "$20-100",
            "environmental_benefit": "Extends product life, reduces new production demand",
            "platforms": [
                "Poshmark",
                "ThredUp",
                "Depop",
                "Vestiaire Collective",
                "Facebook Marketplace"
            ]
        })
        
        options.append({
            "option": "Donate",
            "description": "Give to someone who needs it",
            "estimated_cost": "$0",
            "environmental_benefit": "Helps others, keeps clothing in use",
            "resources": [
                "Goodwill",
                "The Salvation Army",
                "Local homeless shelters",
                "Dress for Success"
            ]
        })
        
        options.append({
            "option": "Keep Wearing",
            "description": f"Your {garment_type} is in good condition - keep using it!",
            "environmental_benefit": "Most sustainable choice is to use what you have",
            "tip": "Each additional year of use significantly reduces environmental impact"
        })
    
    return {
        "circular_options": options,
        "recommended_action": options[0]["option"] if options else "Keep wearing",
        "location_note": f"Options available in your area: {location}" if location != 'unknown' else None
    }