# ThreadHer - AI Fashion Sustainability Advisor

**AWS AI Hackathon 2025 Submission**

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://threadher-app.s3.us-east-1.amazonaws.com/index.html)
[![Video](https://img.shields.io/badge/Video-Demo-red)](https://youtu.be/zU20ZlaQraw)

ThreadHer is an AI-powered fashion sustainability advisor that analyzes garment images using Claude 3.5 Sonnet to provide actionable sustainability recommendations, carbon footprint estimates, and eco-friendly alternatives.

## 🌟 Features

- **AI Image Analysis**: Upload garment photos for instant classification and analysis
- **Sustainability Metrics**: Real-time carbon footprint and water usage calculations
- **Smart Recommendations**: Personalized advice for repair, donation, and sustainable alternatives
- **Conversational AI**: Natural language interaction powered by Amazon Bedrock
- **Session Memory**: Contextual conversations that remember previous exchanges

## 🎯 Problem Statement

The fashion industry accounts for 10% of global carbon emissions and generates 92 million tons of textile waste annually. Consumers lack accessible tools to understand their clothing's environmental impact and make informed sustainable choices.

## ✨ Solution

ThreadHer bridges this gap by providing instant AI-powered analysis that:
- Identifies garment types, materials, and condition from images
- Calculates environmental impact (CO2, water usage, microplastics)
- Offers actionable next steps (repair, donate, sustainable alternatives)
- Educates users about sustainable fashion practices

## 🏗️ Architecture

```
User → Frontend (S3) → API Gateway → Lambda Functions → Amazon Bedrock (Claude 3.5 Sonnet)
                                  ↓
                              Amazon S3 (Image Storage)
```

**Tech Stack:**
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Backend**: AWS Lambda (Python 3.11)
- **AI Engine**: Amazon Bedrock with Claude 3.5 Sonnet
- **Storage**: Amazon S3
- **API**: Amazon API Gateway

## 🚀 Live Demo

**Website**: https://threadher-app.s3.us-east-1.amazonaws.com/index.html

**Try these:**
1. Upload a garment image (jeans, dress, t-shirt)
2. Ask: "Calculate the carbon footprint of a cotton t-shirt"
3. Ask: "My jeans are damaged. What should I do?"

## 📊 Sample Results

**Input**: Blue denim jeans image

**Output**:
```
🔍 Type: Wide-leg jeans
👔 Occasion: Casual
🧵 Material: Denim (cotton)
⭐ Condition: New

🌍 Carbon: ~20-33 kg CO2e
💧 Water: ~7,000-10,000 liters

Recommendations: Care tips, donation platforms, sustainable alternatives
```

## 💡 Key Innovations

1. **Hybrid AI Architecture**: Combines Bedrock Agent for text queries and Claude Vision API for image analysis
2. **Accurate Classification**: Systematic analysis methodology ensures precise garment identification
3. **Environmental Impact**: Real sustainability metrics, not generic advice
4. **User-Centric Design**: Conversational, educational, non-judgmental interface

## 📈 Impact

**Environmental Benefits:**
- Average 14 kg CO2e saved per garment kept 2 extra years
- Reduces textile waste through repair/donation guidance
- Promotes circular economy principles

**User Benefits:**
- Instant sustainability analysis (<10 seconds)
- Personalized recommendations
- Increased awareness of fashion's environmental impact

## 🚀 Setup & Deployment

### Prerequisites
- AWS Account with Bedrock access
- Claude 3.5 Sonnet model enabled
- AWS CLI configured

### Deployment Steps

#### 1. Create S3 Bucket for Images
```bash
aws s3 mb s3://threadher-garment-images-2025 --region us-east-1
```

#### 2. Deploy Lambda Function
```bash
cd lambdas
zip -r deployment.zip lambda_function.py
aws lambda create-function \
  --function-name ThreadHer-APIHandler \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::YOUR_ACCOUNT:role/ThreadHer-LambdaRole \
  --zip-file fileb://deployment.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables="{AGENT_ID=YOUR_AGENT_ID,AGENT_ALIAS_ID=YOUR_ALIAS_ID,S3_BUCKET=threadher-garment-images-2025}"
```

#### 3. Create Bedrock Agent
1. Go to Amazon Bedrock Console
2. Create new Agent with Claude 3.5 Sonnet
3. Deploy agent orchestrator from `agents/orchestrator/`
4. Create alias and note IDs

#### 4. Deploy Frontend
```bash
cd docs/frontend
aws s3 sync . s3://your-website-bucket --acl public-read
```

#### 5. Update API Gateway URL
Edit `docs/frontend/index.html` with your API Gateway endpoint.

### Environment Variables

Lambda requires:
- `AGENT_ID`: Your Bedrock Agent ID
- `AGENT_ALIAS_ID`: Your Bedrock Agent Alias ID
- `S3_BUCKET`: S3 bucket name for image storage

## 📁 Project Structure

```
threadher-ai/
├── agents/
│   └── orchestrator/          # Bedrock agent dependencies
│       ├── <dependent libraries>
│       ├── action_handler.py
│       ├── deployment.zip
│       └── tools-schema.json
├── docs/
│   └── architecture_diagram.png
├── frontend/
│   └── index.html         # Main web interface
├── lambdas/
│   ├── api-handler/           # Lambda dependencies
│   |   ├── <dependent libraries>  
│   |   ├── lambda_function.py     # API handler
│   |   └── deployment.zip
│   └── tools/
│       ├── carbon-calculator/
|       |   ├── <dependent libraries>  
|       |   ├── lambda_function.py     # Carbon calculator
│       |   └── deployment.zip
│       ├── get-circular-options/
|       |   ├── <dependent libraries>  
|       |   ├── lambda_function.py     # Circular economy options
│       |   └── deployment.zip
│       └── image-analyzer/
|           ├── <dependent libraries>  
|           ├── lambda_function.py     # Image analyzer
│           └── deployment.zip
├── setup/
│   └── create_tables.py
├── test-events/
│       ├── test-api-event.json
│       ├── test-event.json
│       └── test-image-analyzer.json
├── config.txt
└── README.md
```

## 🔐 IAM Permissions Required

Lambda needs:
- `bedrock:InvokeAgent`
- `s3:PutObject`, `s3:GetObject`
- CloudWatch Logs access

## 🧪 Testing

### Test Lambda Function
```bash
aws lambda invoke \
  --function-name ThreadHer-APIHandler \
  --payload file://lambdas/test-events/test-api-event.json \
  response.json
```
## 💡 Key Implementation Details

### AI Agent Instructions
- Systematic 5-step image analysis
- 40+ garment type taxonomy
- Material identification from visual cues
- Sustainability metrics database

### Image Processing
- Base64 encoding in browser
- Automatic S3 upload
- Reference passing to Bedrock Agent

### Session Management
- Unique session IDs per user
- Conversation continuity
- Context preservation

## 🎓 What We Learned

- **Prompt Engineering**: Detailed systematic instructions are crucial for accurate AI classification
- **Serverless Architecture**: Reduced operational overhead with automatic scaling
- **User Experience**: Real-time feedback builds trust and engagement
- **AWS Integration**: Seamless integration of multiple AWS services for production-ready solution

## 📊 AWS Services Used

- **Amazon Bedrock**: Claude 3.5 Sonnet for AI analysis
- **AWS Lambda**: Serverless compute
- **Amazon S3**: Image storage and static hosting
- **Amazon API Gateway**: REST API management
- **Amazon CloudWatch**: Logging and monitoring
- **AWS IAM**: Security and permissions

## 🏆 Criteria

**Innovation**: Hybrid AI approach combining Bedrock Agent and Claude Vision API

**Technical Excellence**: Production-ready serverless architecture with error handling

**Impact**: Measurable environmental benefit 

**User Experience**: Intuitive, accessible interface with real-time feedback

**Scalability**: Serverless design handles variable load efficiently

## 🔮 Future Enhancements

- [ ] Wardrobe tracking dashboard with aggregate sustainability metrics
- [ ] Brand database with transparency ratings
- [ ] Mobile app (iOS/Android)
- [ ] Community garment exchange marketplace
- [ ] AR virtual try-on integration

## 👥 Team

Built by Nichchaphat Sommhai (Tukta Belding) for AWS AI Hackathon 2025

## 🙏 Acknowledgments

- Amazon Bedrock team for Claude 3.5 Sonnet access
- AWS for hosting the hackathon
- Sustainable fashion community for inspiration

## 📞 Contact

- **Demo**: https://threadher-app.s3.us-east-1.amazonaws.com/index.html
- **Video**: https://youtu.be/zU20ZlaQraw
- **GitHub**: https://github.com/tuktabe/threadher-ai-sustainability

---

**Built with 💜 for sustainable fashion and women in tech**

*"Threading sustainability into every wardrobe, one garment at a time."*