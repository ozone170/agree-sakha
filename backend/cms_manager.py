import json
import os
from datetime import datetime

# CMS content file
CMS_CONTENT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'cms_content.json')

def load_cms_content():
    """Load CMS content from JSON file"""
    os.makedirs(os.path.dirname(CMS_CONTENT_FILE), exist_ok=True)
    if os.path.exists(CMS_CONTENT_FILE):
        with open(CMS_CONTENT_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return get_default_cms_content()

def save_cms_content(content):
    """Save CMS content to JSON file"""
    os.makedirs(os.path.dirname(CMS_CONTENT_FILE), exist_ok=True)
    with open(CMS_CONTENT_FILE, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=2, ensure_ascii=False)

def get_default_cms_content():
    """Get default CMS content"""
    return {
        "home_content": {
            "about": "AgriSakha is an intelligent platform that combines cutting-edge AI technology with agricultural expertise to provide farmers with precise soil analysis and personalized crop recommendations. Our mission is to bridge the gap between traditional farming practices and modern data-driven agriculture.",
            "vision": "To empower every farmer with data, technology, and insights for sustainable and profitable agriculture. Our vision is to create a future where technology meets the soil, enabling farmers worldwide to make informed decisions that maximize yield while preserving natural resources.",
            "mission": "To provide accessible, accurate, and actionable agricultural intelligence to farmers globally. Through our AI-driven platform, we are committed to delivering real-time soil analysis, personalized crop recommendations, and comprehensive farming guidelines.",
            "contact": {
                "email": "contact@agrisakha.com",
                "phone": "+91 98765 43210",
                "address": "2nd Floor, Innovation Hub, Bhubaneswar, Odisha, India"
            }
        },
        "last_updated": datetime.now().isoformat(),
        "updated_by": "system"
    }

def update_home_content(updates, updated_by="admin"):
    """Update home page content"""
    content = load_cms_content()
    content["home_content"].update(updates)
    content["last_updated"] = datetime.now().isoformat()
    content["updated_by"] = updated_by
    save_cms_content(content)
    return True

def get_home_content():
    """Get current home page content"""
    return load_cms_content()["home_content"]

def get_cms_metadata():
    """Get CMS metadata (last updated, etc.)"""
    content = load_cms_content()
    return {
        "last_updated": content.get("last_updated"),
        "updated_by": content.get("updated_by")
    }

# Initialize default content if not exists
def initialize_cms():
    """Initialize CMS with default content if not exists"""
    if not os.path.exists(CMS_CONTENT_FILE):
        save_cms_content(get_default_cms_content())
        print("CMS content initialized with default values")

# Call initialization
initialize_cms()
