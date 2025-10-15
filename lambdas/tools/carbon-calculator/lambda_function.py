# lambdas/tools/calculate-carbon/lambda_function.py
import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = os.environ.get('DYNAMODB_TABLE', 'ThreadHerCalculations')
table = dynamodb.Table(table_name)

# Carbon footprint data (kg CO2e per item)
CARBON_FOOTPRINTS = {
    'tshirt': {'cotton': 7.0, 'polyester': 5.5, 'organic_cotton': 3.5, 'default': 6.0},
    'jeans': {'cotton': 33.4, 'denim': 33.4, 'organic_cotton': 20.0, 'default': 33.4},
    'dress': {'cotton': 12.0, 'polyester': 10.0, 'silk': 15.0, 'default': 12.0},
    'jacket': {'leather': 50.0, 'polyester': 25.0, 'wool': 35.0, 'default': 30.0},
    'sweater': {'wool': 20.0, 'cotton': 12.0, 'acrylic': 15.0, 'default': 15.0},
    'shoes': {'leather': 30.0, 'synthetic': 20.0, 'default': 25.0},
    'default': {'default': 10.0}
}

# Recommended lifespan (years)
RECOMMENDED_LIFESPAN = {
    'tshirt': 2,
    'jeans': 5,
    'dress': 3,
    'jacket': 7,
    'sweater': 5,
    'shoes': 3,
    'default': 3
}

def convert_to_decimal(obj):
    """Convert floats to Decimal for DynamoDB compatibility"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    return obj

def get_carbon_footprint(garment_type, material):
    """Get carbon footprint based on garment type and material"""
    garment_type = garment_type.lower() if garment_type else 'default'
    material = material.lower() if material else 'default'
    
    garment_data = CARBON_FOOTPRINTS.get(garment_type, CARBON_FOOTPRINTS['default'])
    return garment_data.get(material, garment_data.get('default', 10.0))

def calculate_sustainability_score(age_years, recommended_years, material):
    """Calculate sustainability score (0-100)"""
    # Base score
    score = 50
    
    # Longevity bonus (up to +40 points)
    if age_years >= recommended_years:
        longevity_bonus = min(40, (age_years / recommended_years) * 20)
        score += longevity_bonus
    else:
        # Penalty for short use
        score -= (recommended_years - age_years) * 5
    
    # Sustainable material bonus (up to +10 points)
    if material and 'organic' in material.lower():
        score += 10
    elif material and any(m in material.lower() for m in ['recycled', 'hemp', 'linen']):
        score += 8
    
    return max(0, min(100, score))

def lambda_handler(event, context):
    """
    Calculate carbon footprint and sustainability metrics for a garment
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse the request body - handle both direct invocation and API Gateway
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        # Extract parameters with defaults
        garment_type = body.get('garment_type', '').strip()
        material = body.get('material', '').strip()
        origin = body.get('origin', 'unknown').strip()
        estimated_age_years = body.get('estimated_age_years', 0)
        
        # Validation
        if not garment_type:
            garment_type = 'default'
            print("Warning: No garment_type provided, using 'default'")
        
        if not material:
            material = 'default'
            print("Warning: No material provided, using 'default'")
        
        # Convert age to float if it's a string
        try:
            estimated_age_years = float(estimated_age_years) if estimated_age_years else 0
        except (ValueError, TypeError):
            estimated_age_years = 0
        
        print(f"Calculating for: {garment_type}, {material}, from {origin}")
        
        # Get carbon footprint
        total_carbon = get_carbon_footprint(garment_type, material)
        
        # Calculate metrics
        recommended_years = RECOMMENDED_LIFESPAN.get(garment_type.lower(), 3)
        carbon_per_year = total_carbon / max(estimated_age_years, 1)
        
        # Calculate potential savings (if kept vs buying new)
        remaining_years = max(0, recommended_years - estimated_age_years)
        potential_savings = carbon_per_year * remaining_years if remaining_years > 0 else 0
        
        # Calculate sustainability score
        sustainability_score = calculate_sustainability_score(
            estimated_age_years, 
            recommended_years, 
            material
        )
        
        # Prepare results
        calculation_results = {
            'total_carbon_footprint_kg': total_carbon,
            'carbon_per_year_kg': carbon_per_year,
            'potential_savings_kg': potential_savings,
            'remaining_recommended_years': remaining_years,
            'sustainability_score': sustainability_score,
            'calculated_at': datetime.utcnow().isoformat(),
            'garment_type': garment_type,
            'material': material,
            'origin': origin,
            'estimated_age_years': estimated_age_years
        }
        
        print(f"Calculation results: {calculation_results}")
        
        # Convert floats to Decimal for DynamoDB
        try:
            dynamodb_item = convert_to_decimal(calculation_results)
            dynamodb_item['calculation_id'] = context.request_id if hasattr(context, 'request_id') else str(datetime.utcnow().timestamp())
            
            # Store in DynamoDB
            table.put_item(Item=dynamodb_item)
            print(f"Successfully stored calculation in DynamoDB")
        except Exception as db_error:
            print(f"Warning: Could not store in DynamoDB: {str(db_error)}")
            # Continue even if DynamoDB fails
        
        # Return response (keep as regular floats for API response)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(calculation_results)
        }
        
    except Exception as e:
        print(f"Error in carbon calculation: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to calculate carbon footprint'
            })
        }