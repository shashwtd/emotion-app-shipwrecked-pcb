import badge
import time
import sys

APP_NAME = "emojito"


# Add the current directory to the path for imports
try:
    import os
    current_dir = f"/apps/{APP_NAME}"
    if current_dir not in sys.path:
        sys.path.append(current_dir)
except:
    # Fallback if os module issues
    sys.path.append(f"/apps/{APP_NAME}")

# Import helper modules
import apps.emojito.helpers.emoji_data as emoji_data
import apps.emojito.helpers.radio_handler as radio_handler
import apps.emojito.helpers.pbm_parser as pbm_parser
import apps.emojito.helpers.display_manager as display_manager


class App(badge.BaseApp):
    def __init__(self):
        self.current_screen = "menu"  # "menu", "emoji", or "received"
        self.selected_emoji = None
        self.received_emoji = None  # Store last received emoji data
        self.last_received_time = 0
        
        # Helper modules will be initialized in on_open()
        self.radio_handler = None
        self.sound_manager = None
        self.pbm_parser = None
        self.display_manager = None
        self.button_map = None

    def on_open(self):
        # Initialize helper modules here where logger is available
        self._initialize_helpers()
        
        self.current_screen = "menu"
        self.display_manager.debug_list_files()
        self.display_manager.draw_menu()
    
    def on_packet(self, packet, is_foreground):
        """Handle incoming radio packets with emoji data"""
        try:
            # Ensure helpers are initialized (for background packet handling)
            if self.radio_handler is None:
                self._initialize_helpers()
            
            emoji_data = self.radio_handler.handle_packet(packet)
            
            if emoji_data:
                self.received_emoji = emoji_data
                self.last_received_time = badge.time.monotonic()
                
                self.logger.info(f"Received emoji '{emoji_data['emoji']}' from {emoji_data['sender']}")
                
                # If we're in foreground, show the received emoji immediately
                if is_foreground:
                    self.current_screen = "received"
                    self.display_manager.draw_received_emoji(self.received_emoji)
                    # Play a notification sound for received emoji
                    self.sound_manager.play_notification_sound()
                else:
                    # If in background, play a subtle notification tone to alert user
                    badge.buzzer.tone(800, 0.1)  # Short beep
                    badge.buzzer.tone(1000, 0.1)  # Double beep pattern
                    
        except Exception as e:
            self.logger.error(f"Error in on_packet: {e}")

    def _initialize_helpers(self):
        """Initialize helper modules - can be called multiple times safely"""
        if self.radio_handler is None:
            self.radio_handler = radio_handler.RadioHandler(self.logger)
            self.sound_manager = emoji_data.SoundManager(self.logger)
            self.pbm_parser = pbm_parser.PBMParser(self.logger, APP_NAME)
            self.display_manager = display_manager.DisplayManager(self.logger, APP_NAME, self.pbm_parser, self.sound_manager)
            self.button_map = emoji_data.get_button_map()

    def check_button_presses(self):
        if self.current_screen == "menu":
            for button_name, emoji_key in self.button_map.items():
                button_attr = getattr(badge.input.Buttons, button_name, None)
                if button_attr and badge.input.get_button(button_attr):
                    self.selected_emoji = emoji_key
                    self.current_screen = "emoji"
                    
                    # Broadcast the emoji selection to other badges
                    self.radio_handler.broadcast_emoji(emoji_key)
                    
                    self.display_manager.draw_emoji(emoji_key)
                    # Wait a moment for rendering, then play sound
                    time.sleep(0.1)
                    self.sound_manager.play_emoji_sound(emoji_key)
                    time.sleep(0.3)
                    return
                    
        elif self.current_screen == "emoji" or self.current_screen == "received":
            if badge.input.get_button(badge.input.Buttons.SW5):
                self.current_screen = "menu"
                self.display_manager.draw_menu()
                time.sleep(0.3)
                return

    def loop(self):
        # Auto-return to menu from received emoji screen after 25 seconds
        if self.current_screen == "received" and self.received_emoji:
            if (badge.time.monotonic() - self.last_received_time) > 25:
                self.current_screen = "menu"
                self.display_manager.draw_menu()
                return
        
        self.check_button_presses()
        time.sleep(0.05)
