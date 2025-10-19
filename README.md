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
User → Frontend (S3) → API Gateway (/chat, /uploadurl)
                            ↓                    ↓
                       APIHandler         Upload Lambda
                    (Request Processor)  (Image Handler)
                            ↓                    ↓
                       Bedrock          →    Amazon S3
                   (Claude 3.5 Sonnet)    (Image Storage)
                            ↓
                    • Image Analysis
                    • Classification
```

**Tech Stack:**
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS (hosted on S3)
- **Backend**: 2 AWS Lambda Functions (Python 3.11)
  - Upload Lambda: Image Handler
  - APIHandler: Request Processor (Vision + Agent)
- **AI Engine**: Amazon Bedrock with Claude 3.5 Sonnet
- **Storage**: Amazon S3
- **API**: Amazon API Gateway (REST endpoints: /chat, /uploadurl)

## 🚀 Live Demo

**Website**: https://threadher-app.s3.us-east-1.amazonaws.com/index.html

**Try these:**
1. Upload a garment image (dress, blouse, skirt, jacket)
2. Ask: "What's the environmental impact of this dress?"
3. Ask: "How can I extend the life of this garment?"
4. Ask: "Where can I donate or resell this item?"

## 📊 Sample Results

**Input**: Floral summer dress image

**Output**:
```
🔍 Type: Summer dress / Midi dress
👔 Occasion: Casual, Daywear, Garden party
🧵 Material: Cotton blend (appears to be cotton/polyester)
⭐ Condition: Good

🌍 Environmental Impact:
• Carbon Footprint: ~15-22 kg CO2e
• Water Usage: ~6,000-8,000 liters
• Material: Mixed fibers (natural + synthetic)
• Microplastics: Moderate shedding if polyester blend

♻️ Your Options:
✨ Keep & Care: 
   - Wash in cold water to reduce microplastic shedding
   - Air dry to extend fabric life
   - Proper storage to prevent fading
💚 Donate/Resell: ThredUp, Poshmark, Depop, local consignment
🔄 Repair: Simple repairs like hem adjustments, button replacements
🌱 Sustainable Alternatives: Look for 100% organic cotton or GOTS-certified dresses
```

## 💡 Key Innovations

1. **Direct Bedrock Integration**: Seamless integration with Claude 3.5 Sonnet for real-time image analysis and conversational AI
2. **Dual Lambda Architecture**: Separation of concerns with dedicated Upload and APIHandler functions for optimal performance
3. **Accurate Classification**: Systematic analysis methodology ensures precise garment identification from images
4. **Real Environmental Impact**: Actual sustainability metrics, not generic advice
5. **User-Centric Design**: Conversational, educational, non-judgmental interface

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

#### 2. Deploy Lambda Functions

**APIHandler Lambda (Request Processor)**
```bash
cd lambdas/api-handler
# If deployment.zip doesn't exist, create it with dependencies
zip -r deployment.zip lambda_function.py $(ls -d */ 2>/dev/null)

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

**Upload Lambda (Image Handler)**
```bash
cd ../upload-lambda
# If deployment.zip doesn't exist, create it with dependencies
zip -r deployment.zip lambda_function.py $(ls -d */ 2>/dev/null)

aws lambda create-function \
  --function-name ThreadHer-UploadHandler \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::YOUR_ACCOUNT:role/ThreadHer-LambdaRole \
  --zip-file fileb://deployment.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{S3_BUCKET=threadher-garment-images-2025}"
```

#### 3. Create Bedrock Agent
1. Go to Amazon Bedrock Console
2. Create new Agent with Claude 3.5 Sonnet
3. Configure agent with instructions from `agents/orchestrator/`
4. Create alias and note AGENT_ID and AGENT_ALIAS_ID
5. Update Lambda environment variables with these IDs

**Note**: The `deployment.zip` files should include the `lambda_function.py` along with ALL dependent library folders.

#### 4. Deploy Frontend
```bash
cd frontend
aws s3 sync . s3://your-website-bucket --acl public-read
aws s3 website s3://your-website-bucket --index-document index.html
```

#### 5. Update API Gateway URL
Edit `frontend/index.html` with your API Gateway endpoint.

### Environment Variables

**APIHandler Lambda** requires:
- `AGENT_ID`: Your Bedrock Agent ID
- `AGENT_ALIAS_ID`: Your Bedrock Agent Alias ID
- `S3_BUCKET`: S3 bucket name for image storage

**Upload Lambda** requires:
- `S3_BUCKET`: S3 bucket name for image storage

## 📁 Project Structure

```
threadher-ai/
├── agents/
│   └── orchestrator/          # Bedrock agent configuration
│       ├── <dependent libraries>
│       ├── action_handler.py
│       ├── deployment.zip
│       └── tools-schema.json
├── docs/
│   └── architecture_diagram.png
├── frontend/
│   └── index.html             # Main web interface
├── lambdas/
│   ├── api-handler/           # APIHandler Lambda (Request Processor)
│   │   ├── <dependent libraries>
│   │   ├── lambda_function.py
│   │   └── deployment.zip
│   └── upload-lambda/         # Upload Lambda (Image Handler)
│       ├── <dependent libraries>
│       ├── lambda_function.py
│       └── deployment.zip
├── setup/
│   └── create_tables.py
├── test-events/
│   ├── test-api-event.json
│   ├── test-event.json
│   └── test-upload-event.json
├── config.txt
└── README.md
```

## 🔐 IAM Permissions Required

**APIHandler Lambda** needs:
- `bedrock:InvokeModel` (for Claude Vision API)
- `bedrock:InvokeAgent`
- `s3:GetObject` (read images from S3)
- CloudWatch Logs access

**Upload Lambda** needs:
- `s3:PutObject` (write images to S3)
- CloudWatch Logs access

See IAM policy documentation for complete policy configuration.

## 🧪 Testing

### Test APIHandler Lambda
```bash
aws lambda invoke \
  --function-name ThreadHer-APIHandler \
  --payload file://test-events/test-api-event.json \
  response.json

cat response.json
```

### Test Upload Lambda
```bash
aws lambda invoke \
  --function-name ThreadHer-UploadHandler \
  --payload file://test-events/test-upload-event.json \
  response.json

cat response.json
```

### Test via Web Interface
Upload a garment photo via the web interface and ask "Analyze this garment"

## 📊 More Sample Outputs

**Input**: Navy blue business suit image

**Output**:
```
🔍 Garment Type: Two-piece suit (blazer + trousers)
👔 Occasion: Business/Professional, Formal
🧵 Material: Wool blend
⭐ Condition: Good

🌍 Environmental Impact:
• Carbon Footprint: ~35-45 kg CO2e
• Water Usage: ~12,000-15,000 liters
• Material: Natural fibers (wool)

♻️ Your Options:
✨ Keep & Care: Dry clean sparingly, proper storage, professional alterations
💚 Donate/Resell: ThredUp, Poshmark, local consignment shops
🔄 Repair: Tailors can extend lifespan significantly
🌱 Sustainable Alternatives: Consider wool from certified sustainable sources
```

## 💡 Key Implementation Details

### Lambda Functions Architecture

**APIHandler** (`lambdas/api-handler/`)
- Main request processor for chat queries
- Invokes Bedrock Agent with user questions
- Integrates Claude Vision API for image analysis
- Manages session state and conversation context
- Returns sustainability recommendations and metrics

**Upload Lambda** (`lambdas/upload-lambda/`)
- Handles image upload requests from frontend
- Generates pre-signed S3 URLs for secure uploads
- Manages image storage in S3 bucket
- Returns image references for analysis

### Data Flow Process

1. **Upload**: User uploads garment image via frontend
2. **Route**: API Gateway routes to Upload Lambda (/uploadurl endpoint)
3. **Store**: Image stored in Amazon S3 (threadher-garment-images)
4. **Process**: User asks question, routed to APIHandler (/chat endpoint)
5. **Analyze**: Bedrock (Claude 3.5 Sonnet) performs image analysis and classification
6. **Return**: Response with sustainability metrics and recommendations

### AI Agent Instructions
- Systematic 5-step image analysis
- 40+ garment type taxonomy
- Material identification from visual cues
- Sustainability metrics database

### API Gateway Endpoints

**POST /chat**
- Routes to APIHandler Lambda
- Processes user queries and image analysis requests
- Returns AI-generated sustainability advice

**POST /uploadurl**
- Routes to Upload Lambda
- Generates pre-signed S3 URLs for image uploads
- Enables secure client-side uploads

### Image Processing
- Base64 encoding in browser
- Automatic S3 upload
- Reference passing to Bedrock Agent

### Session Management
- Unique session IDs per user
- Conversation continuity
- Context preservation

## 🎓 What I Learned

- **Prompt Engineering**: Detailed systematic instructions are crucial for accurate AI classification
- **Serverless Architecture**: Dual Lambda design (Upload + APIHandler) optimizes performance and reduces latency
- **Image Processing**: Pre-signed S3 URLs enable secure client-side uploads without server bottlenecks
- **User Experience**: Real-time feedback and conversational AI build trust and engagement
- **AWS Integration**: Seamless integration of Bedrock, Lambda, S3, and API Gateway for production-ready solution

## 📊 AWS Services Used

- **Amazon Bedrock**: Claude 3.5 Sonnet for AI-powered image analysis and classification
- **AWS Lambda**: Serverless compute (2 functions: APIHandler, Upload Lambda)
- **Amazon S3**: Image storage (threadher-garment-images) and static website hosting
- **Amazon API Gateway**: REST API management with /chat and /uploadurl endpoints
- **Amazon CloudWatch**: Logging and monitoring for all Lambda functions
- **AWS IAM**: Security, roles, and permissions management

## 🏆 Criteria

**Innovation**: Direct Bedrock integration with Claude 3.5 Sonnet for real-time fashion sustainability analysis

**Technical Excellence**: Production-ready serverless architecture with dual Lambda design, error handling, and secure S3 image management

**Impact**: Measurable environmental benefit (14 kg CO2 per garment extended lifecycle)

**User Experience**: Intuitive, accessible interface with real-time feedback and conversational AI

**Scalability**: Serverless design with API Gateway and Lambda handles variable load efficiently

## 🔮 Future Enhancements

- [ ] Wardrobe tracking dashboard with aggregate sustainability metrics
- [ ] Brand database with transparency ratings
- [ ] Mobile app (iOS/Android)
- [ ] Community garment exchange marketplace
- [ ] AR virtual try-on integration

## 👥 Team

Built by Nichchaphat Sommhai (Tukta Belding) for AWS AI Hackathon 2025

## 📄 License

MIT License

Copyright (c) 2025 Nichchaphat Sommhai (Tukta Belding)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 🙏 Acknowledgments

- Amazon Bedrock team for Claude 3.5 Sonnet access
- AWS for hosting the hackathon
- Sustainable fashion community for inspiration

## 📞 Contact

- **Demo**: https://threadher-app.s3.us-east-1.amazonaws.com/index.html
- **Video**: https://youtu.be/zU20ZlaQraw
- **GitHub**: https://github.com/tuktabe/threadher-ai-sustainability

---

**Built with 💜 for sustainable fashion and woman in tech**

*"Threading sustainability into every wardrobe, one garment at a time."*