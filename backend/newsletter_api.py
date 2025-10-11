import json
import os
from datetime import datetime

# Newsletter subscribers file
NEWSLETTER_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'newsletter.json')

def load_subscribers():
    """Load newsletter subscribers from JSON file"""
    os.makedirs(os.path.dirname(NEWSLETTER_FILE), exist_ok=True)
    if os.path.exists(NEWSLETTER_FILE):
        with open(NEWSLETTER_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_subscribers(subscribers):
    """Save newsletter subscribers to JSON file"""
    os.makedirs(os.path.dirname(NEWSLETTER_FILE), exist_ok=True)
    with open(NEWSLETTER_FILE, 'w', encoding='utf-8') as file:
        json.dump(subscribers, file, indent=2, ensure_ascii=False)

def add_subscriber(email):
    """Add a new subscriber to the newsletter"""
    if not email or "@" not in email:
        return False
    
    subscribers = load_subscribers()
    
    # Check if already subscribed
    for subscriber in subscribers:
        if subscriber.get("email", "").lower() == email.lower():
            return False
    
    new_subscriber = {
        "email": email.lower(),
        "subscribed_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    subscribers.append(new_subscriber)
    save_subscribers(subscribers)
    return True

def remove_subscriber(email):
    """Remove a subscriber from the newsletter"""
    subscribers = load_subscribers()
    updated_subscribers = [s for s in subscribers if s.get("email", "").lower() != email.lower()]
    
    if len(updated_subscribers) < len(subscribers):
        save_subscribers(updated_subscribers)
        return True
    return False

def get_subscriber_count():
    """Get total number of active subscribers"""
    subscribers = load_subscribers()
    return len([s for s in subscribers if s.get("status") == "active"])

def update_subscriber_status(email, status):
    """Update subscriber status (active/unsubscribed)"""
    subscribers = load_subscribers()
    for subscriber in subscribers:
        if subscriber.get("email", "").lower() == email.lower():
            subscriber["status"] = status
            subscriber["updated_at"] = datetime.now().isoformat()
            save_subscribers(subscribers)
            return True
    return False

# Initialize empty newsletter file if not exists
def initialize_newsletter():
    """Initialize newsletter file if not exists"""
    if not os.path.exists(NEWSLETTER_FILE):
        save_subscribers([])
        print("Newsletter file initialized")

# Call initialization
initialize_newsletter()
