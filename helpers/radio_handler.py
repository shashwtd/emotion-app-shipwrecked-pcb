import badge
import json

class RadioHandler:
    def __init__(self, logger):
        self.logger = logger
    
    def broadcast_emoji(self, emoji_key):
        """Broadcast selected emoji to all nearby badges"""
        try:
            # Get our contact info for the sender field
            my_contact = badge.contacts.my_contact()
            sender_handle = my_contact.handle if my_contact and my_contact.handle else "Unknown"
            
            # Create emoji broadcast message
            emoji_message = {
                'emoji': emoji_key,
                'sender': sender_handle
            }
            
            # Convert to JSON and encode as bytes
            message_data = json.dumps(emoji_message).encode('utf-8')
            
            # Broadcast to all badges (dest=0 means broadcast)
            badge.radio.send_packet(0xffff, message_data)
            self.logger.info(f"Broadcasted emoji '{emoji_key}' from {sender_handle}")
            
        except Exception as e:
            self.logger.error(f"Error broadcasting emoji: {e}")
    
    def handle_packet(self, packet):
        """Process incoming radio packet and return decoded emoji data"""
        try:
            # Decode the emoji data
            emoji_data = json.loads(packet.data.decode('utf-8'))
            
            # Validate the packet format
            if 'emoji' in emoji_data and 'sender' in emoji_data:
                # Get sender contact info
                sender_contact = badge.contacts.get_contact_by_badge_id(packet.source)
                sender_name = sender_contact.handle if sender_contact and sender_contact.handle else f"Badge {packet.source:04X}"
                
                # Return processed emoji data
                return {
                    'emoji': emoji_data['emoji'],
                    'sender': sender_name,
                    'badge_id': packet.source
                }
                
        except Exception as e:
            self.logger.error(f"Error handling radio packet: {e}")
            
        return None
