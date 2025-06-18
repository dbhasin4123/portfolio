import streamlit as st
import requests
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Deven Bhasin - Portfolio",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.8rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #333;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin: 3rem 0 1.5rem 0;
    }
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .skill-tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .contact-form {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .resume-button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 16px;
        display: inline-block;
        margin: 10px 5px;
        transition: all 0.3s ease;
    }
    .resume-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }
    .social-links a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    .social-links a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Discord notification function
def send_discord_notification(name, email, subject, message):
    """
    Function to send notification to Discord using webhook
    """
    try:
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL") or st.secrets.get("DISCORD_WEBHOOK_URL")
        
        if not webhook_url:
            return False, "Discord webhook URL not configured"
        embed = {
            "title": "🌟 New Portfolio Contact Message",
            "description": f"**Subject:** {subject}",
            "color": 6719530,
            "fields": [
                {
                    "name": "👤 Name",
                    "value": name,
                    "inline": True
                },
                {
                    "name": "📧 Email",
                    "value": email,
                    "inline": True
                },
                {
                    "name": "📝 Message",
                    "value": message[:1000] + ("..." if len(message) > 1000 else ""),
                    "inline": False
                }
            ],
            "footer": {
                "text": f"Portfolio Website • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            },
            "thumbnail": {
                "url": "https://cdn-icons-png.flaticon.com/512/3682/3682321.png"
            }
        }
        
        payload = {
            "username": "Portfolio Bot",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/3682/3682321.png",
            "embeds": [embed]
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 204:
            return True, "Discord notification sent successfully!"
        else:
            return False, f"Discord API returned status code: {response.status_code}"
            
    except Exception as e:
        return False, f"Error sending Discord notification: {str(e)}"

def send_simple_discord_notification(name, email, subject, message):
    """
    Simple Discord notification without embeds (fallback)
    """
    try:
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL") or st.secrets.get("DISCORD_WEBHOOK_URL")
        
        if not webhook_url:
            return False, "Discord webhook URL not configured"
        
        content = f"""
🌟 **New Portfolio Contact Message**

👤 **Name:** {name}
📧 **Email:** {email}
📋 **Subject:** {subject}

📝 **Message:**
{message}

---
*Sent from Portfolio Website at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
        """
        
        payload = {
            "content": content,
            "username": "Portfolio Bot"
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            return True, "Discord notification sent successfully!"
        else:
            return False, f"Discord API returned status code: {response.status_code}"
            
    except Exception as e:
        return False, f"Error sending Discord notification: {str(e)}"

def create_skill_tags(skills_list):
    skills_html = ""
    for skill in skills_list:
        skills_html += f'<span class="skill-tag">{skill}</span>'
    return skills_html

st.markdown('<h1 class="main-header">Deven Bhasin</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI/Software/Cloud Engineer</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("📍 **Brisbane, QLD, Australia**")
with col2:
    st.markdown("📞 **[+61 0412711759](tel:+610412711759)**")
with col3:
    st.markdown("✉️ **[devenbhasin4123@gmail.com](mailto:devenbhasin4123@gmail.com)**")
with col4:
    st.markdown("""
    <div class="social-links">
    🔗 <a href="https://www.linkedin.com/in/devenbhasin/" target="_blank">LinkedIn</a> | 
    <a href="https://github.com/dbhasin4123" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <a href="https://drive.google.com/file/d/1f07tZ_zD3VcSpMkuMj2zW69mTJgOahxE/view?usp=sharing" target="_blank" class="resume-button">
        📄 View Resume
    </a>
</div>
""", unsafe_allow_html=True)

# Key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🎓 Education</h3>
        <p>Software Engineering (Hons)<br>University of Queensland<br><strong>GPA: 5.5/7</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>💼 Experience</h3>
        <p>Research Student at CSIRO<br>Data Analyst Intern<br><strong>93% Model Accuracy</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>🚀 Projects</h3>
        <p>8+ Major Projects<br>AI/ML & Full-Stack<br><strong>30% Efficiency Gains</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ABOUT SECTION
st.markdown('<h2 class="section-header">About Me</h2>', unsafe_allow_html=True)

st.markdown("""
Curious and adaptable software developer passionate about building reliable, efficient, and user-centric applications. 
Enthusiastic about AI, programming languages, and system design, with a mindset geared toward lifelong learning and impactful problem-solving.

**Key Strengths:**
- 🤖 **AI/ML Expertise**: Developed models achieving 93% mean IoU, specializing in computer vision and NLP
- ☁️ **Cloud Architecture**: AWS certified with hands-on experience in scalable system design
- 🔧 **Full-Stack Development**: Built applications from Chrome extensions to mobile apps
- 📊 **Data-Driven Solutions**: Automated workflows increasing efficiency by 30%
- 🌍 **Languages**: English (Fluent), Hindi (Native), Punjabi (Native)
""")

# EXPERIENCE SECTION
st.markdown('<h2 class="section-header">Professional Experience</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h3>🔬 Research Student - CSIRO</h3>
        <p><strong>Nov 2024 – Feb 2025</strong></p>
        <ul>
            <li>Developed image segmentation models to quantify blackleg disease in canola</li>
            <li>Implemented UNet, ResUNet, and SegFormer architectures achieving <strong>93% mean IoU</strong></li>
            <li>Applied ViT and EfficientNet for disease quantification with expert correlation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3>📊 Data Analyst Intern - FutureXEnergy</h3>
        <p><strong>Sep 2023 – Dec 2023</strong></p>
        <ul>
            <li>Automated Excel workflows using Python, increasing efficiency by <strong>30%</strong></li>
            <li>Created interactive dashboards for energy consumption analysis</li>
            <li>Built data validation tools ensuring downstream analysis integrity</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<h2 class="section-header">Featured Projects</h2>', unsafe_allow_html=True)

# Project 1 & 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h3>🛒 Later - Chrome Extension</h3>
        <p><strong>Full-Stack Wishlist Application</strong></p>
        <ul>
            <li>Full-stack app (Python API, Node.js frontend, Chrome Extension) on AWS</li>
            <li>Layered Architecture for maintainability and rapid development</li>
            <li>Load tested with k6 for <strong>50 concurrent users</strong></li>
            <li>Web-scraping service for <strong>8+ e-commerce sites</strong></li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["Python", "Node.js", "AWS", "Docker", "PostgreSQL"]), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3>📰 News Summarizer</h3>
        <p><strong>AI-Powered News Analysis</strong></p>
        <ul>
            <li>Streamlit interface with personalized article delivery</li>
            <li>Llama LLM integration for AI-powered summaries</li>
            <li>Smart filtering by interests, location, and time range</li>
            <li>NLTK preprocessing for enhanced text analysis</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/news-summarizer" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["Python", "Llama 3.2", "Streamlit", "OpenAI"]), unsafe_allow_html=True)

# Project 3 & 4
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h3>🤖 AI Recruiter Platform</h3>
        <p><strong>Automated Recruitment System</strong></p>
        <ul>
            <li>AI agents for resume analysis and candidate screening</li>
            <li>PDF data extraction with confidence scoring</li>
            <li>Intelligent job-to-candidate matching</li>
            <li>OpenAI GPT integration for advanced analysis</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/ai-recruiter" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["Python", "OpenAI", "Streamlit", "PDF Processing"]), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3>📄 Doc Assistant</h3>
        <p><strong>RAG-based Document AI</strong></p>
        <ul>
            <li>Local AI assistant using RAG pipeline</li>
            <li>Offline document conversations</li>
            <li>ChromaDB for semantic search</li>
            <li>LangChain integration for advanced NLP</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/doc-assistant" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["Python", "LangChain", "ChromaDB", "RAG"]), unsafe_allow_html=True)

# Project 5 & 6
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h3>🌐 Translatify</h3>
        <p><strong>Real-time Translation App</strong></p>
        <ul>
            <li>React Native app for elderly immigrants</li>
            <li>Real-time translation with WebSocket</li>
            <li>Accessibility-focused design</li>
            <li>Multi-language support</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/Elderly-Immigrant-Integration" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["React Native", "Node.js", "WebSocket", "Translation APIs"]), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3>🏥 Medical Image Segmentation</h3>
        <p><strong>Enhanced U-Net Model</strong></p>
        <ul>
            <li>Skin lesion segmentation from ISIC 2018 dataset</li>
            <li>Enhanced U-Net architecture in TensorFlow</li>
            <li>Achieved <strong>90% Dice coefficient</strong></li>
            <li>Medical AI with high precision requirements</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/PatternAnalysis-2023/tree/topic-recognition/recognition/Improved%20UNet%20Model%20ISIC-48241328" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["TensorFlow", "Medical AI", "Computer Vision"]), unsafe_allow_html=True)

# Additional Projects
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h3>🌦️ Weather-Energy Correlation</h3>
        <p><strong>Research & Thesis Project</strong></p>
        <ul>
            <li>Predictive models for NEM Australia</li>
            <li>Weather uncertainty and energy dispatch analysis</li>
            <li>Spatio-temporal correlation studies</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/REIT4842_Thesis" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Research
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["Python", "Machine Learning", "Statistical Analysis"]), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3>🏭 IoT Blockchain Monitoring</h3>
        <p><strong>Production Quality Control</strong></p>
        <ul>
            <li>End-to-end IoT system with C firmware</li>
            <li>nRF52 and STM32 platforms with Zephyr RTOS</li>
            <li>Proof-of-Work blockchain for data integrity</li>
        </ul>
        <div style="margin-top: 10px;">
            <a href="https://github.com/dbhasin4123/Blockchain-Embedded-system" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 View Project
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(create_skill_tags(["C", "Zephyr RTOS", "Blockchain", "IoT"]), unsafe_allow_html=True)

# SKILLS SECTION
st.markdown('<h2 class="section-header">Technical Skills</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🤖 AI/ML & Data Science")
    st.markdown(create_skill_tags([
        "TensorFlow", "PyTorch", "Scikit-Learn", "LangChain", "RAG",
        "OpenAI", "Ollama", "NumPy", "Pandas", "Matplotlib"
    ]), unsafe_allow_html=True)
    
    st.markdown("### 💻 Programming Languages")
    st.markdown(create_skill_tags([
        "Python", "JavaScript", "C/C++", "Java", "Dart", "HTML/CSS", "R", "MATLAB"
    ]), unsafe_allow_html=True)
    
    st.markdown("### 🗄️ Databases")
    st.markdown(create_skill_tags([
        "MySQL", "PostgreSQL", "SQLite3", "ChromaDB"
    ]), unsafe_allow_html=True)

with col2:
    st.markdown("### ☁️ Cloud & DevOps")
    st.markdown(create_skill_tags([
        "AWS", "Docker", "Kubernetes", "Terraform", "Git", "GitHub"
    ]), unsafe_allow_html=True)
    
    st.markdown("### 🌐 Web & Mobile Development")
    st.markdown(create_skill_tags([
        "React", "React Native", "Flutter", "Streamlit", "Flask", "Express.js", "Node.js"
    ]), unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Tools & Environment")
    st.markdown(create_skill_tags([
        "VS Code", "Google Colab", "Linux", "Windows", "WSL", "Poetry"
    ]), unsafe_allow_html=True)

# EDUCATION SECTION
st.markdown('<h2 class="section-header">Education</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🎓 Bachelor of Engineering (Hons)</h4>
        <p><strong>Software Engineering w/ Computer Engineering</strong><br>
        University of Queensland, Australia<br>
        July 2023 - July 2025<br>
        <strong>GPA: 5.5/7</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🎓 Bachelor of Engineering</h4>
        <p><strong>Computer Engineering</strong><br>
        TIET, Patiala, India<br>
        Sep 2021 - June 2023<br>
        <strong>CGPA: 8/10</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>🏫 12th Standard</h4>
        <p><strong>Maths, Physics, Chemistry</strong><br>
        GPS, Punjab, India<br>
        Completed: June 2021<br>
        <strong>94.6%</strong></p>
    </div>
    """, unsafe_allow_html=True)

# CERTIFICATIONS
st.markdown("### 🏆 Certifications & Awards")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **AWS Certifications:**
    - AWS Cloud Foundations
    - AWS Cloud Architecting  
    - AWS Cloud Developing
    
    **Research & Academic:**
    - CSIRO Studentship
    - Global Connect Scholarship (2023)
    """)

with col2:
    st.markdown("""
    **Technical Certifications:**
    - Google Python Courses (2x)
    - Computer Vision Applications (TIET)
    - Mobile App Development (TIET)
    - Robotic Arm Development (TIET)
    - Handwritten Text Recognition (TIET)
    """)

# CONTACT SECTION with Discord notifications
st.markdown('<h2 class="section-header">Get In Touch</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 💼 I'm interested in:")
    st.markdown("""
    - **Full-time Software Engineering roles**
    - **AI/ML Research positions**
    - **Cloud Engineering opportunities**
    - **Collaboration on open source projects**
    - **Technical discussions and mentorship**
    """)
    
    st.markdown("### 📱 Connect with me:")
    st.markdown("""
    **📧 Email:** [devenbhasin4123@gmail.com](mailto:devenbhasin4123@gmail.com)  
    **📱 Phone:** [+61 0412711759](tel:+610412711759)  
    **🔗 LinkedIn:** [linkedin.com/in/devenbhasin](https://www.linkedin.com/in/devenbhasin/)  
    **👨‍💻 GitHub:** [github.com/dbhasin4123](https://github.com/dbhasin4123)  
    **📍 Location:** Brisbane, Queensland, Australia
    """)

with col2:
    st.markdown("### 💬 Send me a message")
    
    with st.form("contact_form"):
        st.markdown('<div class="contact-form">', unsafe_allow_html=True)
        
        name = st.text_input("Your Name *", placeholder="Enter your full name")
        email = st.text_input("Your Email *", placeholder="your.email@example.com")
        subject = st.selectbox("Subject", [
            "General Inquiry",
            "Job Opportunity", 
            "Collaboration Proposal",
            "Technical Discussion",
            "Project Inquiry",
            "Other"
        ])
        message = st.text_area("Message *", placeholder="Tell me about your inquiry...", height=120)
        
        submitted = st.form_submit_button("Send Message 💬", use_container_width=True)
        
        if submitted:
            if not name or not email or not message:
                st.error("Please fill in all required fields (*)")
            elif "@" not in email:
                st.error("Please enter a valid email address")
            else:
                # Try to send Discord notification
                success, msg = send_discord_notification(name, email, subject, message)
                
                if success:
                    st.success("✅ Thank you for your message! I'll get back to you soon.")
                    st.info("💬 Your message has been sent to Discord! I typically respond within 24 hours.")
                else:
                    # Try simple notification as fallback
                    success_simple, msg_simple = send_simple_discord_notification(name, email, subject, message)
                    
                    if success_simple:
                        st.success("✅ Thank you for your message! I'll get back to you soon.")
                        st.info("💬 Your message has been sent! I typically respond within 24 hours.")
                    else:
                        # Fallback - show mailto link
                        st.info("📧 Click here to send email directly:")
                        mailto_link = f"mailto:devenbhasin4123@gmail.com?subject=Portfolio Contact: {subject}&body=Name: {name}%0D%0AEmail: {email}%0D%0A%0D%0AMessage:%0D%0A{message}"
                        st.markdown(f"[📧 Send Email]({mailto_link})")
                        st.warning(f"⚠️ Discord notification failed: {msg}. Please use the direct email link above.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Discord Setup Instructions (only show if webhook not configured)
webhook_url = os.getenv("DISCORD_WEBHOOK_URL") or st.secrets.get("DISCORD_WEBHOOK_URL", "")
if not webhook_url:
    st.markdown("---")
    st.markdown("### 🔧 Discord Setup Instructions")
    with st.expander("Click to see Discord webhook setup guide"):
        st.markdown("""
        **To enable Discord notifications:**
        
        1. **Create a Discord Server** (if you don't have one)
        2. **Create a Webhook:**
           - Go to your Discord server
           - Right-click on a channel → Edit Channel
           - Go to Integrations → Webhooks
           - Click "New Webhook"
           - Copy the webhook URL
        
        3. **Configure the webhook URL:**
           
           **For local development:**
           ```bash
           export DISCORD_WEBHOOK_URL="your_webhook_url_here"
           ```
           
           **For Streamlit Cloud:**
           - Go to your app settings
           - Add a secret: `DISCORD_WEBHOOK_URL = "your_webhook_url_here"`
           
           **For other platforms:**
           - Set the environment variable `DISCORD_WEBHOOK_URL`
        
        4. **Test the integration** by submitting a message through the contact form
        
        **Security Note:** Never commit webhook URLs to public repositories!
        """)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Built with ❤️ using Streamlit | © 2025 Deven Bhasin</strong></p>
    <p>🚀 Passionate about AI, Software Engineering, and Cloud Computing</p>
    <p>📧 Always open to new opportunities and collaborations</p>
    <div style="margin-top: 20px;">
        <a href="https://www.linkedin.com/in/devenbhasin/" target="_blank" style="margin: 0 10px; color: #667eea; text-decoration: none;">
            LinkedIn
        </a>
        <a href="https://github.com/dbhasin4123" target="_blank" style="margin: 0 10px; color: #667eea; text-decoration: none;">
            GitHub
        </a>
        <a href="mailto:devenbhasin4123@gmail.com" style="margin: 0 10px; color: #667eea; text-decoration: none;">
            Email
        </a>
    </div>
</div>
""", unsafe_allow_html=True)