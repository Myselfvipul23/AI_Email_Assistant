from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from dotenv import load_dotenv
from datetime import datetime
import os
import speech_recognition as sr
from werkzeug.utils import secure_filename
import tempfile
import re
import PyPDF2
import docx
from PIL import Image
import pytesseract
import google.generativeai as genai
import base64
from io import BytesIO

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = "AIzaSyC8TuaeXrHs1tkFFOM6hjQPXaFeZehxRYs"
EMAIL_ADDRESS = "vipulsingh993452@gmail.com"
EMAIL_PASSWORD = "rjbe fqpz jtft qfve"
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'webm', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

HISTORY_FILE = "email_history.json"
USER_PROFILE_FILE = "user_profile.json"

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Enhanced user profile with professional details
DEFAULT_PROFILE = {
    "personal_info": {
        "full_name": "Vipul Kr Singh",
        "email": "vipulsingh98710@gmail.com",
        "phone": "+91 9661810942",
        "address": "Sector 36, Greater Noida, India",
        "company": "AI Developer & Innovator",
        "job_title": "Full Stack Developer & AI Engineer",
        "linkedin": "https://www.linkedin.com/in/vipul-singh-88b868285",
        "website": "",
        "github": "",
        "professional_summary": "Passionate AI Developer creating innovative solutions and transforming ideas into reality through cutting-edge technology."
    },
    "preferences": {
        "default_tone": "professional",
        "include_phone": True,
        "include_address": False,
        "include_email": True,
        "include_linkedin": True,
        "include_website": False,
        "signature_style": "modern",
        "email_style": "elegant"
    },
    "social_links": {
        "linkedin": "https://www.linkedin.com/in/vipul-singh-88b868285",
        "github": "",
        "portfolio": "",
        "twitter": ""
    }
}

class OrionIntelligence:
    """Advanced AI Intelligence for ORION"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.conversation_history = []
        self.user_patterns = {}
        
    def analyze_user_intent(self, message, context=""):
        """Advanced intent analysis with context awareness"""
        prompt = f"""
        Analyze the user's message and determine the DEEP INTENT and CONTEXT.
        
        USER MESSAGE: {message}
        CONTEXT: {context}
        CONVERSATION HISTORY: {self.conversation_history[-3:] if self.conversation_history else "None"}
        
        Analyze:
        1. Primary intent (what they explicitly want)
        2. Secondary intent (what they might actually need)
        3. Emotional state
        4. Urgency level
        5. Professional context
        6. Hidden needs or unstated requirements
        
        Return JSON:
        {{
            "primary_intent": "main purpose",
            "secondary_intents": ["list", "of", "other", "intents"],
            "emotional_tone": "emotional state",
            "urgency": "high/medium/low",
            "context_understanding": "what this is really about",
            "suggested_approach": "how to handle this request",
            "potential_risks": "what could go wrong",
            "enhancement_opportunities": "how to exceed expectations"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {
                "primary_intent": "email_generation",
                "secondary_intents": ["communication"],
                "emotional_tone": "neutral",
                "urgency": "medium",
                "context_understanding": "Standard email request",
                "suggested_approach": "Professional response",
                "potential_risks": "None identified",
                "enhancement_opportunities": "Add personalization"
            }
    
    def strategic_thinking(self, user_message, document_context="", recipient_info=""):
        """Advanced strategic thinking for email composition"""
        prompt = f"""
        STRATEGIC THINKING MODE - Act as an expert communication strategist.
        
        REQUEST: {user_message}
        DOCUMENT CONTEXT: {document_context[:1000]}  # Limit context length
        RECIPIENT INFO: {recipient_info}
        
        STRATEGIC ANALYSIS REQUIRED:
        
        1. PSYCHOLOGICAL PROFILING:
           - What does the recipient care about?
           - What are their likely pain points?
           - What motivates them to respond?
        
        2. PERSUASION STRATEGY:
           - Key persuasion techniques to use
           - Emotional triggers to leverage
           - Value proposition framing
        
        3. RELATIONSHIP DYNAMICS:
           - Power dynamics analysis
           - Trust-building elements
           - Long-term relationship impact
        
        4. COMPETITIVE POSITIONING:
           - How to stand out
           - Unique value propositions
           - Competitive advantages to highlight
        
        5. RISK MITIGATION:
           - Potential objections
           - Preemptive solutions
           - Fallback positions
        
        Return strategic framework in JSON:
        {{
            "psychological_profile": {{"motivations": [], "pain_points": [], "decision_factors": []}},
            "persuasion_strategy": {{"primary_technique": "", "emotional_triggers": [], "value_framing": ""}},
            "relationship_approach": {{"power_dynamics": "", "trust_elements": [], "long_term_goals": ""}},
            "competitive_advantages": ["list", "of", "advantages"],
            "risk_mitigation": {{"potential_issues": [], "solutions": [], "contingency_plans": []}},
            "strategic_recommendations": ["actionable", "recommendations"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return self._default_strategy()
    
    def _default_strategy(self):
        return {
            "psychological_profile": {
                "motivations": ["efficiency", "value", "reliability"],
                "pain_points": ["time constraints", "information overload"],
                "decision_factors": ["clarity", "benefits", "credibility"]
            },
            "persuasion_strategy": {
                "primary_technique": "value_proposition",
                "emotional_triggers": ["confidence", "trust"],
                "value_framing": "problem-solution-benefit"
            },
            "relationship_approach": {
                "power_dynamics": "collaborative",
                "trust_elements": ["transparency", "reliability"],
                "long_term_goals": ["relationship building", "mutual success"]
            },
            "competitive_advantages": ["AI-powered precision", "personalized approach", "time efficiency"],
            "risk_mitigation": {
                "potential_issues": ["misunderstanding", "lack of response"],
                "solutions": ["clear communication", "follow-up plan"],
                "contingency_plans": ["alternative approaches"]
            },
            "strategic_recommendations": ["Focus on clear value", "Build rapport", "Provide clear next steps"]
        }
    
    def learn_from_interaction(self, user_input, ai_output, outcome_metrics):
        """Machine learning from user interactions"""
        # Simple pattern learning - in production, use proper ML
        key_phrases = self._extract_key_phrases(user_input)
        for phrase in key_phrases:
            if phrase in self.user_patterns:
                self.user_patterns[phrase] += 1
            else:
                self.user_patterns[phrase] = 1
        
        # Keep only top patterns
        self.user_patterns = dict(sorted(self.user_patterns.items(), 
                                       key=lambda x: x[1], reverse=True)[:50])
    
    def _extract_key_phrases(self, text):
        """Extract meaningful phrases from text"""
        words = text.lower().split()
        phrases = []
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        return phrases

# Initialize ORION Intelligence
orion_ai = OrionIntelligence()

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"conversations": []}

def save_history(user_message, ai_message, tone, recipients, email_type, intelligence_metrics=None):
    history = load_history()
    history_entry = {
        "user_message": user_message,
        "ai_message": ai_message,
        "tone": tone,
        "recipients": recipients,
        "email_type": email_type,
        "timestamp": datetime.now().isoformat()
    }
    
    if intelligence_metrics:
        history_entry["intelligence_metrics"] = intelligence_metrics
    
    history["conversations"].append(history_entry)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_user_profile():
    """Load user profile from file or create default"""
    if os.path.exists(USER_PROFILE_FILE):
        try:
            with open(USER_PROFILE_FILE, "r") as f:
                profile = json.load(f)
                return ensure_profile_structure(profile)
        except:
            return DEFAULT_PROFILE
    return DEFAULT_PROFILE

def ensure_profile_structure(profile):
    """Ensure the profile has all required keys"""
    if "personal_info" not in profile:
        profile["personal_info"] = DEFAULT_PROFILE["personal_info"].copy()
    else:
        for key in DEFAULT_PROFILE["personal_info"]:
            if key not in profile["personal_info"]:
                profile["personal_info"][key] = DEFAULT_PROFILE["personal_info"][key]
    
    if "preferences" not in profile:
        profile["preferences"] = DEFAULT_PROFILE["preferences"].copy()
    else:
        for key in DEFAULT_PROFILE["preferences"]:
            if key not in profile["preferences"]:
                profile["preferences"][key] = DEFAULT_PROFILE["preferences"][key]
    
    if "social_links" not in profile:
        profile["social_links"] = DEFAULT_PROFILE["social_links"].copy()
    else:
        for key in DEFAULT_PROFILE["social_links"]:
            if key not in profile["social_links"]:
                profile["social_links"][key] = DEFAULT_PROFILE["social_links"][key]
    
    return profile

def save_user_profile(profile):
    """Save user profile to file"""
    with open(USER_PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)

def get_professional_signature(email_type, tone_analysis):
    """Generate enhanced professional signature with LinkedIn"""
    profile = load_user_profile()
    personal_info = profile["personal_info"]
    preferences = profile["preferences"]
    social_links = profile.get("social_links", {})
    
    if preferences.get("signature_style") == "modern":
        signature_lines = []
        signature_lines.append(f"🔹 {personal_info['full_name']}")
        
        if personal_info.get("job_title"):
            signature_lines.append(f"   {personal_info['job_title']}")
        
        contact_lines = []
        if preferences.get("include_email", True):
            contact_lines.append(f"📧 {personal_info['email']}")
        
        if preferences.get("include_phone", True) and personal_info.get("phone"):
            contact_lines.append(f"📱 {personal_info['phone']}")
        
        if preferences.get("include_linkedin", True) and social_links.get("linkedin"):
            contact_lines.append(f"💼 LinkedIn: {social_links['linkedin']}")
        
        if preferences.get("include_website", False) and personal_info.get("website"):
            contact_lines.append(f"🌐 {personal_info['website']}")
        
        if contact_lines:
            signature_lines.append("")
            signature_lines.extend(contact_lines)
        
        if personal_info.get("professional_summary"):
            signature_lines.append("")
            signature_lines.append(f"🌟 {personal_info['professional_summary']}")
        
        return "\n".join(signature_lines)
    
    else:  # Formal style
        signature_lines = []
        signature_lines.append(personal_info["full_name"])
        
        if personal_info.get("job_title") and personal_info.get("company"):
            signature_lines.append(f"{personal_info['job_title']} | {personal_info['company']}")
        elif personal_info.get("job_title"):
            signature_lines.append(personal_info["job_title"])
        
        signature_lines.append("")
        
        if preferences.get("include_email", True):
            signature_lines.append(f"Email: {personal_info['email']}")
        
        if preferences.get("include_phone", True) and personal_info.get("phone"):
            signature_lines.append(f"Phone: {personal_info['phone']}")
        
        if preferences.get("include_linkedin", True) and social_links.get("linkedin"):
            signature_lines.append(f"LinkedIn: {social_links['linkedin']}")
        
        return "\n".join(signature_lines)

def detect_email_type(user_message):
    """Enhanced email type detection with AI"""
    message_lower = user_message.lower()
    
    # Advanced pattern matching with AI fallback
    patterns = {
        "professional_networking": ['networking', 'connect', 'linkedin', 'professional', 'introduction'],
        "business_proposal": ['sales', 'pitch', 'business proposal', 'collaboration', 'partnership'],
        "client_communication": ['client', 'customer', 'service', 'support', 'update'],
        "internal_communication": ['team', 'internal', 'colleague', 'meeting', 'update'],
        "wedding_invitation": ['wedding', 'marriage', 'bride', 'groom', 'invitation'],
        "celebration": ['birthday', 'party', 'celebration', 'anniversary'],
        "job_application": ['job', 'interview', 'resume', 'cv', 'application', 'hire'],
        "casual": ['friend', 'hangout', 'dinner', 'catch up', 'coffee'],
        "formal": ['formal', 'official', 'government', 'complaint', 'legal'],
        "thank_you": ['thank', 'thanks', 'grateful', 'appreciation'],
        "apology": ['sorry', 'apologize', 'apology', 'regret'],
        "follow_up": ['follow up', 'follow-up', 'checking in', 'status']
    }
    
    for email_type, keywords in patterns.items():
        if any(keyword in message_lower for keyword in keywords):
            return email_type
    
    return "general"

def extract_text_from_file(file_path, file_type):
    """Extract text from various file types"""
    try:
        if file_type == 'pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        
        elif file_type in ['doc', 'docx']:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        
        elif file_type in ['jpg', 'jpeg', 'png']:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        
        elif file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        
        else:
            return f"Unsupported file type: {file_type}"
    
    except Exception as e:
        return f"Error extracting text from file: {str(e)}"

def analyze_tone_and_generate_email(user_message, email_type, document_context="", strategic_insights=None):
    """DANGEROUSLY SMART email generation with strategic intelligence"""
    
    # Advanced intent analysis
    intent_analysis = orion_ai.analyze_user_intent(user_message, document_context)
    
    # Load user profile for personalization
    profile = load_user_profile()
    user_name = profile["personal_info"]["full_name"]
    linkedin_url = profile["personal_info"].get("linkedin", "")
    
    # Add strategic insights to prompt
    strategic_context = ""
    if strategic_insights:
        strategic_context = f"""
        
        STRATEGIC INTELLIGENCE:
        {json.dumps(strategic_insights, indent=2)}
        
        Use these strategic insights to craft a highly effective email that:
        - Addresses the recipient's core motivations
        - Mitigates potential risks
        - Leverages competitive advantages
        - Builds strong relationships
        """
    
    document_prompt = ""
    if document_context:
        document_prompt = f"""
        
        DOCUMENT INTELLIGENCE (AI-Analyzed Content):
        {document_context}
        
        CRITICAL: Seamlessly integrate relevant insights from documents into the email.
        """
    
    # DANGEROUSLY SMART PROMPT
    prompt = f"""
    You are ORION - a DANGEROUSLY SMART AI email strategist. Your goal: create the most effective, persuasive, and strategically perfect email possible.
    
    USER REQUEST: {user_message}
    EMAIL TYPE: {email_type}
    USER PROFILE: {user_name} - {profile["personal_info"].get("job_title", "Professional")}
    
    ADVANCED INTENT ANALYSIS:
    {json.dumps(intent_analysis, indent=2)}
    {strategic_context}
    {document_prompt}
    
    CREATION MANDATE - Create an email that:
    🔥 PSYCHOLOGICALLY PERSUASIVE: Use advanced persuasion techniques
    🎯 STRATEGICALLY PRECISE: Address hidden needs and unstated requirements  
    💫 RELATIONSHIP OPTIMIZED: Build instant rapport and long-term trust
    🚀 RESULTS-DRIVEN: Drive the desired action with maximum effectiveness
    🛡️  RISK-MITIGATED: Preempt objections and potential issues
    
    TECHNICAL REQUIREMENTS:
    - Write from {user_name}'s perspective naturally
    - Use professional yet powerfully engaging language
    - Structure for maximum impact and readability
    - Include strategic call-to-action
    - Incorporate document insights seamlessly
    - Use only standard ASCII characters
    
    Return in this exact JSON format:
    {{
        "intelligence_metrics": {{
            "strategic_score": "0-100",
            "persuasion_level": "0-100", 
            "relationship_impact": "0-100",
            "risk_mitigation": "0-100",
            "innovation_score": "0-100"
        }},
        "tone_analysis": {{
            "detected_tone": "strategic_tone",
            "confidence": "high/medium/low",
            "email_type": "{email_type}",
            "psychological_approach": "approach_used",
            "emotional_intelligence": "high/medium/low"
        }},
        "email_content": {{
            "subject": "highly_engaging_strategic_subject",
            "body": "powerfully_structured_email_body", 
            "closing": "strategic_closing",
            "strategic_notes": "key_strategic_decisions_made"
        }}
    }}
    Only return JSON, no other text.
    """

    try:
        response = orion_ai.model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean response
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        parsed_response = json.loads(response_text)
        
        # Learn from this interaction
        orion_ai.learn_from_interaction(
            user_message, 
            parsed_response, 
            parsed_response.get("intelligence_metrics", {})
        )
        
        return parsed_response
        
    except Exception as e:
        print(f"Advanced AI Error: {e}")
        return generate_enhanced_fallback_email(user_message, email_type)

def generate_enhanced_fallback_email(user_message, email_type):
    """Enhanced fallback with basic intelligence"""
    profile = load_user_profile()
    user_name = profile["personal_info"]["full_name"]
    
    return {
        "intelligence_metrics": {
            "strategic_score": "75",
            "persuasion_level": "70",
            "relationship_impact": "65",
            "risk_mitigation": "80",
            "innovation_score": "60"
        },
        "tone_analysis": {
            "detected_tone": "professional",
            "confidence": "medium",
            "email_type": email_type,
            "psychological_approach": "direct_communication",
            "emotional_intelligence": "medium"
        },
        "email_content": {
            "subject": f"Strategic Communication from {user_name}",
            "body": f"""Dear Recipient,

I hope this message finds you well.

{user_message}

This presents a significant opportunity for mutual benefit and collaboration.

I'm confident we can achieve outstanding results together.

Looking forward to your response.""",
            "closing": "Best regards",
            "strategic_notes": "Standard professional approach applied"
        }
    }

def clean_text(text):
    """Clean text to remove problematic characters"""
    if not text:
        return text
    
    text = text.replace('\xa0', ' ')
    text = text.replace('\u2028', ' ')
    text = text.replace('\u2029', ' ')
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text

def send_enhanced_email(to_emails, subject, body, closing, tone_analysis, attachments=None):
    """
    Send beautifully formatted email with attachments and professional signature
    """
    try:
        # Clean all text inputs
        clean_subject = clean_text(subject)
        clean_body = clean_text(body)
        clean_closing = clean_text(closing)
        
        # Get enhanced professional signature
        signature = get_professional_signature(tone_analysis.get("email_type", "general"), tone_analysis)
        
        # Create message with UTF-8 encoding
        msg = MIMEMultipart('alternative')
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ", ".join(to_emails)
        
        # Set subject with proper encoding
        msg["Subject"] = Header(clean_subject, 'utf-8').encode()
        
        email_type = tone_analysis.get("email_type", "general")
        
        # Enhanced body with beautiful formatting
        enhanced_body = f"""
{clean_body}

{clean_closing},

{signature}
"""
        
        # Beautiful HTML templates
        html_body = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 30px; }}
                .content {{ font-size: 16px; color: #555; }}
                .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
                .ai-badge {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; display: inline-block; margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="ai-badge">🤖 Powered by ORION AI</div>
                <div class="content">
                    {clean_body.replace('\n', '<br>')}
                </div>
                <div class="signature">
                    <strong>{clean_closing},</strong><br><br>
                    {signature.replace('\n', '<br>').replace('🔹', '<strong>').replace('📧', '✉️').replace('📱', '📞').replace('💼', '🔗').replace('🌟', '⭐')}
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create parts
        part1 = MIMEText(enhanced_body, 'plain', 'utf-8')
        part2 = MIMEText(html_body, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                try:
                    with open(attachment['path'], 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={attachment["filename"]}'
                    )
                    msg.attach(part)
                except Exception as e:
                    print(f"Error attaching file {attachment['filename']}: {e}")
                    continue
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_emails, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

# Enhanced API endpoints
@app.route("/profile", methods=["GET"])
def get_profile():
    """Get enhanced user profile"""
    try:
        profile = load_user_profile()
        return jsonify({
            "success": True,
            "profile": profile
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/profile", methods=["POST"])
def update_profile():
    """Update enhanced user profile"""
    try:
        data = request.json
        profile = load_user_profile()
        
        if "personal_info" in data:
            profile["personal_info"].update(data["personal_info"])
        
        if "preferences" in data:
            profile["preferences"].update(data["preferences"])
        
        if "social_links" in data:
            if "social_links" not in profile:
                profile["social_links"] = {}
            profile["social_links"].update(data["social_links"])
        
        save_user_profile(profile)
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "profile": profile
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/profile/social", methods=["POST"])
def update_social_links():
    """Update social media links specifically"""
    try:
        data = request.json
        profile = load_user_profile()
        
        if "social_links" in data:
            if "social_links" not in profile:
                profile["social_links"] = {}
            profile["social_links"].update(data["social_links"])
        
        save_user_profile(profile)
        
        return jsonify({
            "success": True,
            "message": "Social links updated successfully",
            "social_links": profile["social_links"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# DANGEROUSLY SMART MAIN ENDPOINT
@app.route("/generate_send", methods=["POST"])
def generate_and_send():
    """
    DANGEROUSLY SMART endpoint with advanced intelligence and file attachments
    """
    try:
        # Handle both form data and JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            to_emails = request.form.get("to_email", "").strip()
            user_message = request.form.get("user_message", "").strip()
            files = request.files.getlist('documents')
        else:
            data = request.get_json()
            to_emails = data.get("to_email", "").strip()
            user_message = data.get("user_message", "").strip()
            files = []

        to_emails_list = [email.strip() for email in to_emails.split(",") if email.strip()]
        
        if not to_emails_list:
            return jsonify({"error": "No valid email recipients provided"}), 400
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Process uploaded files and extract text
        document_context = ""
        attachment_files = []
        
        if files:
            document_texts = []
            for file in files:
                if file and file.filename:
                    # Save file temporarily for processing and attachment
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Store for attachment
                    attachment_files.append({
                        'path': file_path,
                        'filename': filename
                    })
                    
                    # Extract text from file
                    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                    extracted_text = extract_text_from_file(file_path, file_extension)
                    
                    if extracted_text and not extracted_text.startswith("Error"):
                        document_texts.append(f"--- Content from {filename} ---\n{extracted_text}\n")
            
            if document_texts:
                document_context = "\n".join(document_texts)
                print(f"Advanced Document Analysis: {document_context[:500]}...")

        # Advanced strategic thinking
        strategic_insights = orion_ai.strategic_thinking(user_message, document_context, to_emails)
        
        # Detect email type and generate DANGEROUSLY SMART content
        email_type = detect_email_type(user_message)
        ai_response = analyze_tone_and_generate_email(
            user_message, 
            email_type, 
            document_context, 
            strategic_insights
        )
        
        # Extract components
        intelligence_metrics = ai_response.get("intelligence_metrics", {})
        tone_analysis = ai_response.get("tone_analysis", {})
        email_content = ai_response.get("email_content", {})
        
        # Get professional signature
        signature = get_professional_signature(email_type, tone_analysis)
        full_email_body = f"{email_content.get('body', '')}\n\n{email_content.get('closing', 'Best regards')},\n\n{signature}"
        
        # Send enhanced email WITH ATTACHMENTS
        success = send_enhanced_email(
            to_emails_list, 
            email_content.get('subject', 'Strategic Communication'),
            email_content.get('body', ''),
            email_content.get('closing', 'Best regards'),
            tone_analysis,
            attachments=attachment_files  # Now includes attachments!
        )
        
        # Clean up temporary files
        for attachment in attachment_files:
            try:
                os.remove(attachment['path'])
            except:
                pass
        
        # Save to history with intelligence metrics
        save_history(
            user_message, 
            full_email_body, 
            tone_analysis.get('detected_tone', 'strategic'), 
            to_emails_list, 
            email_type,
            intelligence_metrics
        )
        
        return jsonify({
            "success": True,
            "ai_email": full_email_body,
            "intelligence_metrics": intelligence_metrics,
            "tone_analysis": tone_analysis,
            "strategic_insights": strategic_insights,
            "email_type_detected": email_type,
            "personalized": True,
            "professional_level": "EXTREME",
            "linkedin_included": True,
            "document_processed": bool(document_context),
            "attachments_sent": len(attachment_files),
            "email_metadata": {
                "subject": email_content.get('subject'),
                "sent": success,
                "recipients": to_emails_list,
                "type": email_type,
                "from_user": load_user_profile()["personal_info"]["full_name"],
                "signature_style": load_user_profile()["preferences"]["signature_style"],
                "strategic_notes": email_content.get('strategic_notes', '')
            }
        })
        
    except Exception as e:
        print(f"Error in generate_and_send: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# Advanced intelligence endpoints
@app.route("/analyze_strategy", methods=["POST"])
def analyze_strategy():
    """Advanced strategic analysis endpoint"""
    try:
        data = request.json
        user_message = data.get("user_message", "").strip()
        context = data.get("context", "")
        
        strategic_insights = orion_ai.strategic_thinking(user_message, context)
        
        return jsonify({
            "success": True,
            "strategic_insights": strategic_insights,
            "analysis_timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/intelligence_metrics", methods=["GET"])
def get_intelligence_metrics():
    """Get ORION's intelligence metrics and learning patterns"""
    return jsonify({
        "success": True,
        "user_patterns": orion_ai.user_patterns,
        "interaction_count": len(orion_ai.conversation_history),
        "ai_capabilities": [
            "Advanced Intent Analysis",
            "Strategic Thinking", 
            "Psychological Profiling",
            "Risk Mitigation Planning",
            "Persuasion Strategy",
            "Machine Learning",
            "Document Intelligence",
            "Relationship Optimization"
        ]
    })

# Keep other existing endpoints
@app.route("/analyze_message", methods=["POST"])
def analyze_message():
    """Analyze message and suggest email type without sending"""
    try:
        data = request.json
        user_message = data.get("user_message", "").strip()
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        email_type = detect_email_type(user_message)
        ai_response = analyze_tone_and_generate_email(user_message, email_type)
        
        return jsonify({
            "success": True,
            "detected_email_type": email_type,
            "tone_analysis": ai_response.get("tone_analysis", {}),
            "suggested_email": ai_response.get("email_content", {}),
            "personalized": True,
            "from_user": load_user_profile()["personal_info"]["full_name"]
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history_endpoint():
    """Get email generation history"""
    try:
        history = load_history()
        return jsonify({
            "success": True,
            "history": history
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/voice_transcribe", methods=["POST"])
def transcribe_voice():
    """Transcribe voice audio to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(filepath)
            
            transcribed_text = transcribe_audio(audio_file_path=filepath)
            
            os.remove(filepath)
            
            return jsonify({
                "success": True,
                "transcribed_text": transcribed_text
            })
        else:
            return jsonify({"error": "File type not allowed"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_audio(audio_data=None, audio_file_path=None):
    """Transcribe audio to text using speech recognition"""
    recognizer = sr.Recognizer()
    
    try:
        if audio_file_path:
            with sr.AudioFile(audio_file_path) as source:
                audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error processing audio: {e}"

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Initialize files if they don't exist
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump({"conversations": []}, f, indent=2)
    
    if not os.path.exists(USER_PROFILE_FILE):
        save_user_profile(DEFAULT_PROFILE)
    else:
        profile = load_user_profile()
        save_user_profile(profile)
    
    profile = load_user_profile()
    print("🚀 DANGEROUSLY SMART ORION AI Started!")
    print(f"👤 Welcome, {profile['personal_info']['full_name']}!")
    print("🧠 ADVANCED CAPABILITIES:")
    print("   ✅ Strategic Intelligence & Psychological Profiling")
    print("   ✅ Advanced Intent Analysis & Hidden Need Detection")  
    print("   ✅ Machine Learning from User Interactions")
    print("   ✅ Risk Mitigation & Persuasion Strategy")
    print("   ✅ Document Intelligence with OCR & Text Extraction")
    print("   ✅ File Attachment Support (FINALLY FIXED!)")
    print("   ✅ Relationship Optimization & Competitive Positioning")
    print("   ✅ Emotional Intelligence & Tone Analysis")
    print("📧 Your emails are now STRATEGICALLY PERFECT with attachments!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)