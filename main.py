import badge
import time

APP_NAME = "Emoji_App"

class App(badge.BaseApp):
    def __init__(self):
        self.current_screen = "menu"
        self.selected_emoji = None
        
        # Emoji definitions with proper PBM files
        self.emojis = {
            "smile": {
                "name": "Smile",
                "button": "SW9",
                "pbm_file": "smile.pbm"
            },
            "thumbs_up": {
                "name": "Thumbs Up",
                "button": "SW18",
                "pbm_file": "thumbs_up.pbm"
            },
            "laugh": {
                "name": "Laugh",
                "button": "SW10",
                "pbm_file": "laugh.pbm"
            },
            "rose": {
                "name": "Wilted Flower srsly",
                "button": "SW17",
                "pbm_file": "rose.pbm"
            },
            "peace": {
                "name": "Peace",
                "button": "SW7",
                "pbm_file": "peace.pbm"
            },
            "heart": {
                "name": "Spread love",
                "button": "SW13",
                "pbm_file": "love.pbm"
            },
            "ok": {
                "name": "Skull",
                "button": "SW6",
                "pbm_file": "skull.pbm"
            },
            "wave": {
                "name": "Poo",
                "button": "SW14",
                "pbm_file": "poo.pbm"
            }
        }
        
        # Button mapping
        self.button_map = {}
        for emoji_key, emoji_data in self.emojis.items():
            button_name = emoji_data["button"]
            self.button_map[button_name] = emoji_key

    def on_open(self):
        self.current_screen = "menu"
        self.debug_list_files()
        self.draw_menu()
        
    def debug_list_files(self):
        try:
            import os
            directories_to_check = [".", "/", "/apps", f"/apps/{APP_NAME}"]
            
            for directory in directories_to_check:
                try:
                    files = os.listdir(directory)
                    self.logger.info(f"Files in '{directory}': {files}")
                except OSError as e:
                    self.logger.debug(f"Cannot list '{directory}': {e}")
                    
        except Exception as e:
            self.logger.error(f"Debug file listing error: {e}")

    def draw_menu(self):
        badge.display.fill(1)
        
        badge.display.nice_text(APP_NAME, 50, 5, font=24, color=0)
        badge.display.hline(0, 30, badge.display.width, 0)
        
        y_position = 40
        line_height = 18
        
        emoji_order = ["smile", "thumbs_up", "laugh", "rose", "peace", "heart", "ok", "wave"]
        
        for emoji_key in emoji_order:
            emoji_data = self.emojis[emoji_key]
            badge.display.nice_text(emoji_data["name"], 10, y_position, font=18, color=0)
            
            button_text = f"[{emoji_data['button']}]"
            text_width = len(button_text) * 10
            badge.display.nice_text(button_text, badge.display.width - text_width - 10, y_position, font=18, color=0)
            
            y_position += line_height
            
            if y_position < 185:
                badge.display.hline(0, y_position - 2, badge.display.width, 0)
        
        badge.display.show()

    def draw_emoji(self, emoji_key):
        badge.display.fill(1)
        
        emoji_data = self.emojis[emoji_key]
        
        title = emoji_data["name"]
        badge.display.nice_text(title, 10, 2, font=20, color=0)
        
        # Line under title, moved up slightly
        badge.display.hline(0, 24, badge.display.width, 0)
        
        # Draw the emoji using PBM file
        self.draw_emoji_from_pbm(emoji_data["pbm_file"])
        
        # Back button section
        badge.display.hline(0, 175, badge.display.width, 0)
        badge.display.nice_text("Go Back", 10, 182, font=18, color=0)
        badge.display.nice_text("[SW5]", badge.display.width - 50, 182, font=18, color=0)
        
        badge.display.show()
    
    def play_emoji_sound(self, emoji_key):
        """Play a buzzer sound that matches the emoji"""
        try:
            if emoji_key == "smile":
                # Happy ascending notes
                badge.buzzer.tone(523, 0.15)  # C5
                badge.buzzer.tone(659, 0.15)  # E5
                badge.buzzer.tone(784, 0.2)   # G5
            elif emoji_key == "thumbs_up":
                # Positive confirmation beep
                badge.buzzer.tone(880, 0.1)   # A5
                badge.buzzer.tone(1109, 0.2)  # C#6
            elif emoji_key == "laugh":
                # Bouncy laughing sound
                badge.buzzer.tone(698, 0.1)   # F5
                badge.buzzer.tone(784, 0.1)   # G5
                badge.buzzer.tone(698, 0.1)   # F5
                badge.buzzer.tone(880, 0.15)  # A5
            elif emoji_key == "rose":
                # Gentle romantic melody
                badge.buzzer.tone(587, 0.2)   # D5
                badge.buzzer.tone(698, 0.2)   # F5
                badge.buzzer.tone(784, 0.3)   # G5
            elif emoji_key == "peace":
                # Calm peaceful tone
                badge.buzzer.tone(440, 0.4)   # A4 - long and peaceful
            elif emoji_key == "heart":
                # Sweet love melody
                badge.buzzer.tone(659, 0.2)   # E5
                badge.buzzer.tone(784, 0.2)   # G5
                badge.buzzer.tone(880, 0.3)   # A5
            elif emoji_key == "ok":
                # Approval beep
                badge.buzzer.tone(1047, 0.15) # C6
                badge.buzzer.tone(1319, 0.2)  # E6
            elif emoji_key == "wave":
                # Waving goodbye melody
                badge.buzzer.tone(784, 0.1)   # G5
                badge.buzzer.tone(659, 0.1)   # E5
                badge.buzzer.tone(523, 0.1)   # C5
                badge.buzzer.tone(392, 0.2)   # G4
        except Exception as e:
            self.logger.error(f"Buzzer error: {e}")

    def draw_emoji_from_pbm(self, pbm_filename):
        try:
            width, height, pixel_data = self.parse_pbm_file(pbm_filename)
            
            if width is None or height is None or pixel_data is None:
                self.logger.error(f"Failed to parse PBM file: {pbm_filename}")
                badge.display.text("Error loading", 10, 70, 1)
                badge.display.text("emoji image", 10, 90, 1)
                return
            
            # Emoji display area (adjusted for slightly bigger title)
            emoji_area_height = 175 - 27  # From y=27 to y=175
            emoji_area_width = badge.display.width
            
            # Scale up the emoji if it's smaller than the available space
            scale_factor = min(emoji_area_width // width, emoji_area_height // height)
            if scale_factor < 1:
                scale_factor = 1
            
            scaled_width = width * scale_factor
            scaled_height = height * scale_factor
            
            # Center the scaled emoji
            center_x = (emoji_area_width - scaled_width) // 2
            center_y = 27 + (emoji_area_height - scaled_height) // 2
            
            # Draw scaled emoji
            for y in range(height):
                for x in range(width):
                    if y < len(pixel_data) and x < len(pixel_data[y]):
                        pixel_value = pixel_data[y][x]
                        color = 1 - pixel_value
                        
                        # Draw scaled pixel block
                        for sy in range(scale_factor):
                            for sx in range(scale_factor):
                                draw_x = center_x + x * scale_factor + sx
                                draw_y = center_y + y * scale_factor + sy
                                
                                if 0 <= draw_x < badge.display.width and 0 <= draw_y < badge.display.height:
                                    badge.display.pixel(draw_x, draw_y, color)
            
        except Exception as e:
            self.logger.error(f"PBM Error: {e}")
            self.draw_test_pattern()
            
    def draw_test_pattern(self):
        center_x, center_y = 100, 90
        
        # Simple smiley face fallback
        badge.display.rect(center_x - 30, center_y - 30, 60, 60, 0)
        badge.display.fill_rect(center_x - 15, center_y - 10, 5, 5, 0)
        badge.display.fill_rect(center_x + 10, center_y - 10, 5, 5, 0)
        badge.display.hline(center_x - 15, center_y + 10, 30, 0)
        badge.display.pixel(center_x - 16, center_y + 9, 0)
        badge.display.pixel(center_x + 16, center_y + 9, 0)

    def parse_pbm_file(self, filename):
        try:
            file_path = f"/apps/{APP_NAME}/assets/{filename}"
            self.logger.info(f"Opening PBM file at: {file_path}")
            
            # Try ASCII format first
            try:
                with open(file_path, 'r') as f:
                    file_content = f.readlines()
                self.logger.info(f"Successfully opened PBM file as text from: {file_path}")
                return self._parse_ascii_pbm(file_content)
            except (OSError, ValueError) as e:
                # Try binary format
                self.logger.info(f"Text reading failed ({e}), trying binary format for: {file_path}")
                try:
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    return self._parse_binary_pbm(file_content)
                except Exception as binary_error:
                    self.logger.error(f"Binary reading also failed: {binary_error}")
                    raise
            
        except Exception as e:
            self.logger.error(f"Error parsing PBM file {filename}: {e}")
            return None, None, None
    
    def _parse_ascii_pbm(self, file_content):
        # Remove comments and empty lines
        clean_lines = []
        for line in file_content:
            line = line.strip()
            if line and not line.startswith('#'):
                clean_lines.append(line)
        
        if len(clean_lines) < 3:
            raise ValueError("Invalid PBM file format")
        
        if not clean_lines[0].startswith('P1'):
            raise ValueError(f"Not a valid ASCII PBM file - magic number is {clean_lines[0]}")
        
        width, height = map(int, clean_lines[1].split())
        self.logger.info(f"PBM dimensions: {width}x{height}")
        
        # Get pixel data
        pixel_data = []
        for line in clean_lines[2:]:
            for char in line:
                if char in '01':
                    pixel_data.append(int(char))
        
        if len(pixel_data) != width * height:
            while len(pixel_data) < width * height:
                pixel_data.append(0)
        
        return width, height, pixel_data
    
    def _parse_binary_pbm(self, file_content):
        # Find header end
        header_lines = []
        idx = 0
        while len(header_lines) < 2:
            eol = file_content.find(b'\n', idx)
            if eol == -1:
                raise ValueError("Invalid PBM file: no newline found")
            line = file_content[idx:eol].strip()
            idx = eol + 1
            if line and not line.startswith(b'#'):
                header_lines.append(line.decode('ascii'))

        if header_lines[0] != 'P4':
            raise ValueError(f"Not a valid binary PBM file - magic number is {header_lines[0]}")

        width, height = map(int, header_lines[1].split())
        self.logger.info(f"Binary PBM dimensions: {width}x{height}")

        # Parse binary pixel data
        binary_data = file_content[idx:]
        pixels_2d = []

        row_bytes = (width + 7) // 8
        for y in range(height):
            row_bits = []
            row_start = y * row_bytes
            row_end = row_start + row_bytes
            for byte in binary_data[row_start:row_end]:
                for bit in range(8):
                    if len(row_bits) >= width:
                        break
                    pixel = (byte >> (7 - bit)) & 1
                    row_bits.append(pixel)
            pixels_2d.append(row_bits)

        return width, height, pixels_2d


    def check_button_presses(self):
        if self.current_screen == "menu":
            for button_name, emoji_key in self.button_map.items():
                button_attr = getattr(badge.input.Buttons, button_name, None)
                if button_attr and badge.input.get_button(button_attr):
                    self.selected_emoji = emoji_key
                    self.current_screen = "emoji"
                    self.play_emoji_sound(emoji_key)  # Play sound for the emoji
                    self.draw_emoji(emoji_key)
                    time.sleep(0.3)
                    return
                    
        elif self.current_screen == "emoji":
            if badge.input.get_button(badge.input.Buttons.SW5):
                self.current_screen = "menu"
                self.draw_menu()
                time.sleep(0.3)
                return

    def loop(self):
        self.check_button_presses()
        time.sleep(0.05)