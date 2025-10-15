# setup/create_tables.py
import boto3
import sys

def create_dynamodb_tables():
    """Create DynamoDB tables for ThreadHer"""
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    print("Creating DynamoDB tables for ThreadHer...")
    
    tables_created = []
    
    # Table 1: Garments
    try:
        print("\n1. Creating ThreadHer-Garments table...")
        garments_table = dynamodb.create_table(
            TableName='ThreadHer-Garments',
            KeySchema=[
                {'AttributeName': 'garment_id', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'garment_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'UserIdIndex',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for table to be created
        garments_table.meta.client.get_waiter('table_exists').wait(
            TableName='ThreadHer-Garments'
        )
        print("✅ ThreadHer-Garments table created successfully!")
        tables_created.append('ThreadHer-Garments')
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("⚠️  ThreadHer-Garments table already exists, skipping...")
    except Exception as e:
        print(f"❌ Error creating ThreadHer-Garments: {e}")
    
    # Table 2: Sustainability Scores
    try:
        print("\n2. Creating ThreadHer-SustainabilityScores table...")
        sustainability_table = dynamodb.create_table(
            TableName='ThreadHer-SustainabilityScores',
            KeySchema=[
                {'AttributeName': 'score_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'score_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        sustainability_table.meta.client.get_waiter('table_exists').wait(
            TableName='ThreadHer-SustainabilityScores'
        )
        print("✅ ThreadHer-SustainabilityScores table created successfully!")
        tables_created.append('ThreadHer-SustainabilityScores')
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("⚠️  ThreadHer-SustainabilityScores table already exists, skipping...")
    except Exception as e:
        print(f"❌ Error creating ThreadHer-SustainabilityScores: {e}")
    
    # Table 3: User Wardrobe
    try:
        print("\n3. Creating ThreadHer-Wardrobe table...")
        wardrobe_table = dynamodb.create_table(
            TableName='ThreadHer-Wardrobe',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},      # Partition key
                {'AttributeName': 'garment_id', 'KeyType': 'RANGE'}   # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'garment_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        wardrobe_table.meta.client.get_waiter('table_exists').wait(
            TableName='ThreadHer-Wardrobe'
        )
        print("✅ ThreadHer-Wardrobe table created successfully!")
        tables_created.append('ThreadHer-Wardrobe')
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("⚠️  ThreadHer-Wardrobe table already exists, skipping...")
    except Exception as e:
        print(f"❌ Error creating ThreadHer-Wardrobe: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    if tables_created:
        print(f"✅ Successfully created {len(tables_created)} table(s):")
        for table in tables_created:
            print(f"   - {table}")
    else:
        print("ℹ️  All tables already exist")
    
    print("\n🎉 Database setup complete!")
    print("\nYou can view your tables at:")
    print("https://console.aws.amazon.com/dynamodb/")

if __name__ == "__main__":
    try:
        create_dynamodb_tables()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)