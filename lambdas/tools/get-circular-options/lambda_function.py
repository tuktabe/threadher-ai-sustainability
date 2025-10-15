# lambdas/tools/get-circular-options/lambda_function.py
import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = os.environ.get('DYNAMODB_TABLE', 'ThreadHerCircularOptions')
table = dynamodb.Table(table_name)

# Circular economy options database
REPAIR_SERVICES = {
    'default': [
        {'name': 'Local tailor', 'type': 'repair', 'avg_cost': 15},
        {'name': 'Dry cleaner with alterations', 'type': 'repair', 'avg_cost': 20},
        {'name': 'DIY repair kits', 'type': 'diy', 'avg_cost': 10}
    ],
    'jeans': [
        {'name': 'Denim repair specialist', 'type': 'repair', 'avg_cost': 25},
        {'name': 'Visible mending workshop', 'type': 'workshop', 'avg_cost': 30}
    ],
    'shoes': [
        {'name': 'Cobbler/shoe repair', 'type': 'repair', 'avg_cost': 35},
        {'name': 'Sole replacement service', 'type': 'repair', 'avg_cost': 50}
    ]
}

RESALE_PLATFORMS = [
    {'name': 'ThredUp', 'type': 'online', 'commission': 0.2},
    {'name': 'Poshmark', 'type': 'online', 'commission': 0.2},
    {'name': 'Depop', 'type': 'online', 'commission': 0.1},
    {'name': 'The RealReal', 'type': 'luxury', 'commission': 0.3},
    {'name': 'Local consignment shop', 'type': 'local', 'commission': 0.5}
]

RECYCLING_OPTIONS = [
    {'name': 'H&M garment collection', 'type': 'brand', 'incentive': 'discount coupon'},
    {'name': 'Textile recycling center', 'type': 'municipal', 'incentive': 'environmental impact'},
    {'name': 'For Days take-back program', 'type': 'brand', 'incentive': 'store credit'},
    {'name': 'Donation to thrift store', 'type': 'charity', 'incentive': 'tax deduction'}
]

UPCYCLING_IDEAS = {
    'tshirt': ['tote bag', 'cleaning rags', 'pet toy', 'headband'],
    'jeans': ['denim bag', 'pillow cover', 'plant holder', 'organizer'],
    'dress': ['apron', 'fabric panels', 'scarf', 'quilt squares'],
    'default': ['fabric scrap art', 'patchwork project', 'stuffing material']
}

def get_condition_recommendations(condition):
    """Get recommendations based on garment condition"""
    condition = condition.lower()
    
    if condition in ['excellent', 'good']:
        return {
            'primary_action': 'resale',
            'message': 'This item is in great condition for resale!',
            'priority_options': ['resale', 'donation', 'keep']
        }
    elif condition == 'fair':
        return {
            'primary_action': 'repair',
            'message': 'Consider repairing before resale or continued use.',
            'priority_options': ['repair', 'resale', 'donation']
        }
    else:  # poor condition
        return {
            'primary_action': 'recycle',
            'message': 'This item is best suited for textile recycling or upcycling.',
            'priority_options': ['recycle', 'upcycle', 'textile-waste']
        }

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
    Provide circular economy options for garments
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        # Extract parameters
        garment_type = body.get('garment_type', 'default').strip().lower()
        condition = body.get('condition', 'unknown').strip().lower()
        user_location = body.get('user_location', 'US').strip()
        
        print(f"Getting options for: {garment_type} in {condition} condition")
        
        # Get condition-based recommendations
        recommendations = get_condition_recommendations(condition)
        
        # Compile circular options
        circular_options = {
            'repair_options': REPAIR_SERVICES.get(garment_type, REPAIR_SERVICES['default']),
            'resale_platforms': RESALE_PLATFORMS,
            'recycling_options': RECYCLING_OPTIONS,
            'upcycling_ideas': UPCYCLING_IDEAS.get(garment_type, UPCYCLING_IDEAS['default']),
            'recommended_action': recommendations['primary_action'],
            'priority_options': recommendations['priority_options'],
            'message': recommendations['message']
        }
        
        # Add location-specific options if available
        if user_location and user_location != 'US':
            circular_options['note'] = f"Options shown are general. Check local options in {user_location}."
        
        # Calculate environmental impact potential
        impact_estimates = {
            'repair': {
                'carbon_saved_kg': 10.0,
                'water_saved_liters': 2000,
                'message': 'Repairing extends garment life and saves resources'
            },
            'resale': {
                'carbon_saved_kg': 8.0,
                'water_saved_liters': 1500,
                'message': 'Reselling prevents one new item from being produced'
            },
            'recycle': {
                'carbon_saved_kg': 3.0,
                'water_saved_liters': 500,
                'message': 'Recycling keeps textiles out of landfills'
            },
            'upcycle': {
                'carbon_saved_kg': 5.0,
                'water_saved_liters': 1000,
                'message': 'Upcycling creates new value without new production'
            }
        }
        
        circular_options['environmental_impact'] = impact_estimates.get(
            recommendations['primary_action'],
            impact_estimates['recycle']
        )
        
        result = {
            'garment_type': garment_type,
            'condition': condition,
            'circular_options': circular_options,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        print(f"Recommended action: {recommendations['primary_action']}")
        
        # Store in DynamoDB
        try:
            dynamodb_item = convert_to_decimal(result)
            dynamodb_item['option_id'] = f"{garment_type}_{condition}_{datetime.utcnow().timestamp()}"
            table.put_item(Item=dynamodb_item)
            print("Stored options in DynamoDB")
        except Exception as db_error:
            print(f"Warning: Could not store in DynamoDB: {str(db_error)}")
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(result)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e), 'message': 'Failed to get circular options'})
        }