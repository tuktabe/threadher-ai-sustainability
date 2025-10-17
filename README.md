# ThreadHer - AI Fashion Sustainability Advisor

**AWS AI Hackathon 2025 Submission**

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://threadher-app.s3.us-east-1.amazonaws.com/index.html)
[![Video](https://img.shields.io/badge/Video-Demo-red)](https://www.loom.com/share/7fb3ca3a02fc45b4a80818e49dab4d77?sid=1e6e18d7-c3ba-4627-8982-c0c50d46daac)

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

**Website**: [https://threadher-app.s3.us-east-1.amazonaws.com/index.html]

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

## 🎓 What We Learned

- **Prompt Engineering**: Detailed systematic instructions are crucial for accurate AI classification
- **Serverless Architecture**: Reduced operational overhead with automatic scaling
- **User Experience**: Real-time feedback builds trust and engagement
- **AWS Integration**: Seamless integration of multiple AWS services for production-ready solution

## 🔮 Future Enhancements

- [ ] Wardrobe tracking dashboard with aggregate sustainability metrics
- [ ] Brand database with transparency ratings
- [ ] Mobile app (iOS/Android)
- [ ] Community garment exchange marketplace
- [ ] AR virtual try-on integration

## 🛠️ Setup & Deployment

### Prerequisites
- AWS Account with Bedrock access
- Claude 3.5 Sonnet model enabled
- AWS CLI configured

### Quick Start

1. **Clone repository**
```bash
git clone https://github.com/YOUR_USERNAME/threadher-ai-sustainability.git
cd threadher-ai-sustainability
```

2. **Deploy Lambda Functions**
```bash
cd lambda
# Update environment variables in code
# Deploy via AWS Console or AWS CLI
```

3. **Configure API Gateway**
- Create REST API
- Set up `/chat` and `/upload-url` endpoints
- Enable CORS
- Deploy to production stage

4. **Deploy Frontend**
```bash
cd frontend
# Update API URLs in index.html
# Upload to S3 bucket with static website hosting enabled
```

### Environment Variables

Lambda requires:
- `AGENT_ID`: Your Bedrock Agent ID
- `AGENT_ALIAS_ID`: Your Bedrock Agent Alias ID
- `S3_BUCKET`: S3 bucket name for image storage

## 📊 AWS Services Used

- **Amazon Bedrock**: Claude 3.5 Sonnet for AI analysis
- **AWS Lambda**: Serverless compute
- **Amazon S3**: Image storage and static hosting
- **Amazon API Gateway**: REST API management
- **Amazon CloudWatch**: Logging and monitoring
- **AWS IAM**: Security and permissions

## 🏆 Hackathon Criteria

**Innovation**: Hybrid AI approach combining Bedrock Agent and Claude Vision API

**Technical Excellence**: Production-ready serverless architecture with error handling

**Impact**: Measurable environmental benefit (14 kg CO2 per garment)

**User Experience**: Intuitive, accessible interface with real-time feedback

**Scalability**: Serverless design handles variable load efficiently

## 👥 Team

Built by [Nichchaphat Sommhai (Tukta Belding)] for AWS AI Hackathon 2025

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Amazon Bedrock team for Claude 3.5 Sonnet access
- AWS for hosting the hackathon
- Sustainable fashion community for inspiration

## 📞 Contact

- **Demo**: [https://threadher-app.s3.us-east-1.amazonaws.com/index.html]
- **Video**: [https://www.loom.com/share/7fb3ca3a02fc45b4a80818e49dab4d77?sid=1e6e18d7-c3ba-4627-8982-c0c50d46daac]
- **GitHub**: [https://github.com/tuktabe/threadher-ai-sustainability]

---

**Built with 💜 for sustainable fashion and women in tech**

*"Threading sustainability into every wardrobe, one garment at a time."*

## 🚀 Quick Start

### Prerequisites
- AWS Account
- Amazon Bedrock access (Claude 3.5 Sonnet enabled)
- AWS CLI configured

### Deployment Steps

#### 1. Create S3 Bucket for Images
```bash
aws s3 mb s3://threadher-garment-images-2025 --region us-east-1
```

#### 2. Deploy Lambda Function
```bash
cd lambda
zip -r function.zip lambda_function.py
aws lambda create-function \
  --function-name ThreadHer-APIHandler \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::YOUR_ACCOUNT:role/ThreadHer-LambdaRole \
  --zip-file fileb://function.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables="{AGENT_ID=YOUR_AGENT_ID,AGENT_ALIAS_ID=YOUR_ALIAS_ID,S3_BUCKET=threadher-garment-images-2025}"
```

#### 3. Create Bedrock Agent
1. Go to Amazon Bedrock Console
2. Create new Agent with Claude 3.5 Sonnet
3. Copy instructions from `bedrock-agent-instructions.md`
4. Create alias and note IDs

#### 4. Deploy Frontend
```bash
cd frontend
aws s3 sync . s3://your-website-bucket --acl public-read
```

#### 5. Update API Gateway URL
Edit `frontend/index.html` line 119 with your API Gateway endpoint.

## 📁 Project Structure

```
threadher/
├── frontend/
│   └── index.html              # Main web interface
├── lambda/
│   └── lambda_function.py      # API handler
├── docs/
│   ├── bedrock-agent-instructions.md
│   ├── architecture-diagram.png
│   └── iam-policy.json
└── README.md
```

## 🔐 IAM Permissions Required

Lambda needs:
- `bedrock:InvokeAgent`
- `s3:PutObject`, `s3:GetObject`
- CloudWatch Logs access

See `docs/iam-policy.json` for complete policy.

## 🧪 Testing

### Test Lambda Function
```bash
aws lambda invoke \
  --function-name ThreadHer-APIHandler \
  --payload '{"body":"{\"query\":\"What is sustainable fashion?\",\"session_id\":\"test-123\"}"}' \
  response.json
```

### Test with Image
Upload a garment photo via the web interface and ask "Analyze this garment"

## 📊 Sample Outputs

**Input**: Wedding dress image
**Output**:
```
🔍 Garment Type: Wedding dress / Evening gown
👔 Occasion: Wedding/Bridal, Formal
🧵 Material: Silk, lace, tulle
⭐ Condition: Excellent

🌍 Environmental Impact:
• Carbon Footprint: ~25-40 kg CO2e
• Water Usage: ~15,000-20,000 liters
• Material: Natural fibers (silk, cotton lace)

♻️ Your Options:
✨ Keep & Care: Dry clean only, proper storage
💚 Donate/Resell: Stillwhite.com, PreOwnedWeddingDresses.com
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

## 🌍 Sustainability Impact

ThreadHer helps users:
- Extend garment lifecycles (reduce waste)
- Make informed purchasing decisions
- Find repair and donation options
- Understand environmental impact

**Average carbon savings**: 14kg CO2e per garment kept 2 extra years

## 🎯 Future Enhancements

- [ ] Wardrobe tracking dashboard
- [ ] Brand sustainability database integration
- [ ] Mobile app (iOS/Android)
- [ ] Virtual try-on with AR
- [ ] Community garment exchange platform

## 👥 Team

Built by [Your Name] for AWS AI Hackathon 2025

## 📄 License

MIT License

## 🙏 Acknowledgments

- Amazon Bedrock team
- Claude AI by Anthropic
- AWS Community

## 📞 Contact

- Demo: [Your deployed URL]
- GitHub: [Your repo URL]
- Video: [Your demo video URL]

---

**Built with 💜 for sustainable fashion and women in tech**