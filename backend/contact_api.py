import json
import os
import uuid
from datetime import datetime

# Contact messages file
CONTACT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'contacts.json')

def load_contact_messages():
    """Load contact messages from JSON file"""
    os.makedirs(os.path.dirname(CONTACT_FILE), exist_ok=True)
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_contact_messages(messages):
    """Save contact messages to JSON file"""
    os.makedirs(os.path.dirname(CONTACT_FILE), exist_ok=True)
    with open(CONTACT_FILE, 'w', encoding='utf-8') as file:
        json.dump(messages, file, indent=2, ensure_ascii=False)

def save_contact_message(name, email, message):
    """Save a new contact message"""
    messages = load_contact_messages()

    new_message = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "message": message,
        "created_at": datetime.now().isoformat(),
        "status": "unread"
    }

    messages.append(new_message)
    save_contact_messages(messages)
    return True

def get_contact_message(message_id):
    """Get a specific contact message by ID"""
    messages = load_contact_messages()
    for message in messages:
        if message.get("id") == message_id:
            return message
    return None

def update_message_status(message_id, status):
    """Update message status (read/unread)"""
    messages = load_contact_messages()
    for message in messages:
        if message.get("id") == message_id:
            message["status"] = status
            message["updated_at"] = datetime.now().isoformat()
            save_contact_messages(messages)
            return True
    return False

def get_unread_count():
    """Get count of unread messages"""
    messages = load_contact_messages()
    return len([m for m in messages if m.get("status") == "unread"])

# Initialize empty contacts file if not exists
def initialize_contacts():
    """Initialize contacts file if not exists"""
    if not os.path.exists(CONTACT_FILE):
        save_contact_messages([])
        print("Contacts file initialized")

# Call initialization
initialize_contacts()
