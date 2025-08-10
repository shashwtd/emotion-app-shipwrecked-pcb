# Emoji definitions and configuration
import badge
import time

EMOJIS = {
    "smile": {
        "name": "Smile",
        "button": "SW9",
        "pbm_file": "assets/smile.pbm"
    },
    "thumbs_up": {
        "name": "Thumbs Up",
        "button": "SW18",
        "pbm_file": "assets/thumbs_up.pbm"
    },
    "laugh": {
        "name": "Laugh",
        "button": "SW10",
        "pbm_file": "assets/laugh.pbm"
    },
    "rose": {
        "name": "Tilted Rose",
        "button": "SW17",
        "pbm_file": "assets/rose.pbm"
    },
    "peace": {
        "name": "Peace",
        "button": "SW7",
        "pbm_file": "assets/peace.pbm"
    },
    "heart": {
        "name": "Heart",
        "button": "SW13",
        "pbm_file": "assets/love.pbm"
    },
    "skull": {
        "name": "Skull",
        "button": "SW6",
        "pbm_file": "assets/skull.pbm"
    },
    "poo": {
        "name": "Poo",
        "button": "SW14",
        "pbm_file": "assets/poo.pbm"
    }
}

EMOJI_ORDER = ["smile", "thumbs_up", "laugh", "rose", "peace", "heart", "skull", "poo"]

def get_button_map():
    """Generate button to emoji mapping"""
    button_map = {}
    for emoji_key, emoji_data in EMOJIS.items():
        button_name = emoji_data["button"]
        button_map[button_name] = emoji_key
    return button_map

class SoundManager:
    def __init__(self, logger):
        self.logger = logger
    
    def play_emoji_sound(self, emoji_key):
        """Play buzzer sounds that *accurately* match the emoji's vibe."""
        try:
            b = badge.buzzer

            if emoji_key == "smile":
                # Bright, upbeat, sunshine vibe — major arpeggio + bounce
                for _ in range(2):
                    b.tone(523, 0.18)  # C5
                    b.tone(659, 0.18)  # E5
                    b.tone(784, 0.18)  # G5
                    b.tone(1047, 0.25) # C6
                    time.sleep(0.05)
                    b.tone(784, 0.15)  # Bounce back down

            elif emoji_key == "thumbs_up":
                # Short victory fanfare — confident & strong
                b.tone(784, 0.15)   # G5
                b.tone(988, 0.15)   # B5
                b.tone(1175, 0.2)   # D6
                b.tone(1319, 0.25)  # E6
                time.sleep(0.05)
                b.tone(1568, 0.3)   # G6 - punchy finish

            elif emoji_key == "laugh":
                # Rolling giggle — fast up/down pattern
                for _ in range(3):
                    b.tone(784, 0.08)   # G5
                    b.tone(880, 0.08)   # A5
                    b.tone(784, 0.08)   # G5
                    b.tone(988, 0.1)    # B5
                    time.sleep(0.03)
                b.tone(659, 0.12)       # End with a little “heh”

            elif emoji_key == "rose":
                # Gentle romantic waltz — soft rise & fall
                b.tone(392, 0.3)    # G4
                b.tone(523, 0.35)   # C5
                b.tone(659, 0.4)    # E5
                b.tone(587, 0.25)   # D5
                time.sleep(0.05)
                b.tone(784, 0.4)    # G5 (hold)

            elif emoji_key == "peace":
                # Calm meditation chime — spaced long notes
                b.tone(440, 0.6)    # A4
                time.sleep(0.1)
                b.tone(523, 0.7)    # C5
                time.sleep(0.15)
                b.tone(659, 0.9)    # E5

            elif emoji_key == "heart":
                # Two heartbeat pulses — realistic lub-dub
                for _ in range(2):
                    b.tone(400, 0.12)   # Lub
                    time.sleep(0.05)
                    b.tone(300, 0.18)   # Dub
                    time.sleep(0.25)

            elif emoji_key == "skull":
                # Creepy toll — slow drop + rumble
                b.tone(220, 0.4)    # Low toll
                time.sleep(0.05)
                b.tone(196, 0.35)   # Slightly lower
                b.tone(110, 0.5)    # Deep rumble

            elif emoji_key == "poo":
                # Comical fart-blip pattern
                for _ in range(2):
                    b.tone(300, 0.12)
                    b.tone(250, 0.1)
                    b.tone(180, 0.15)
                    time.sleep(0.05)
                    b.tone(150, 0.2)  # Low bubbly end

        except Exception as e:
            self.logger.error(f"Buzzer error: {e}")

    
    def play_notification_sound(self):
        """Play a gentle notification sound for received emojis"""
        try:
            # Simple notification chime
            badge.buzzer.tone(800, 0.1)
            badge.buzzer.tone(1000, 0.15)
        except Exception as e:
            self.logger.error(f"Notification sound error: {e}")
    
    def draw_test_pattern(self):
        """Draw a simple test pattern when PBM files can't be loaded"""
        center_x, center_y = 100, 90
        
        # Simple smiley face fallback
        badge.display.rect(center_x - 30, center_y - 30, 60, 60, 0)
        badge.display.fill_rect(center_x - 15, center_y - 10, 5, 5, 0)
        badge.display.fill_rect(center_x + 10, center_y - 10, 5, 5, 0)
        badge.display.hline(center_x - 15, center_y + 10, 30, 0)
        badge.display.pixel(center_x - 16, center_y + 9, 0)
        badge.display.pixel(center_x + 16, center_y + 9, 0)
