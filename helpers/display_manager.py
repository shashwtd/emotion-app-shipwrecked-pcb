import badge
import time

class DisplayManager:
    def __init__(self, logger, app_name, pbm_parser, sound_manager):
        self.logger = logger
        self.app_name = app_name
        self.pbm_parser = pbm_parser
        self.sound_manager = sound_manager
    
    def draw_menu(self):
        """Draw the emoji selection menu"""
        # Import here to avoid circular imports
        from . import emoji_data
        
        badge.display.fill(1)
        
        badge.display.nice_text(self.app_name, 50, 5, font=24, color=0)
        badge.display.hline(0, 30, badge.display.width, 0)
        
        y_position = 40
        line_height = 19
        
        for emoji_key in emoji_data.EMOJI_ORDER:
            emoji_data_item = emoji_data.EMOJIS[emoji_key]
            badge.display.nice_text(emoji_data_item["name"], 10, y_position, font=18, color=0)
            
            button_text = f"[{emoji_data_item['button']}]"
            text_width = len(button_text) * 10
            badge.display.nice_text(button_text, badge.display.width - text_width - 10, y_position, font=18, color=0)
            
            y_position += line_height
            
            if y_position < 185:
                badge.display.hline(0, y_position - 2, badge.display.width, 0)
        
        badge.display.show()
    
    def draw_emoji(self, emoji_key):
        """Draw the selected emoji in large format"""
        # Import here to avoid circular imports
        from . import emoji_data
        
        badge.display.fill(1)
        
        emoji_data_item = emoji_data.EMOJIS[emoji_key]
        
        title = emoji_data_item["name"]
        badge.display.nice_text(title, 10, 2, font=24, color=0)
        
        badge.display.hline(0, 32, badge.display.width, 0)
        
        self.draw_emoji_from_pbm(emoji_data_item["pbm_file"])
        
        badge.display.hline(0, 175, badge.display.width, 0)
        badge.display.nice_text("Go Back", 10, 182, font=18, color=0)
        badge.display.nice_text("[SW5]", badge.display.width - 50, 182, font=18, color=0)
        
        badge.display.show()
    
    def draw_received_emoji(self, received_emoji):
        """Display a received emoji from another badge with improved UI"""
        # Import here to avoid circular imports
        from . import emoji_data
        
        if not received_emoji:
            return
            
        badge.display.fill(1)
        
        # Get sender handle and format it properly
        sender_handle = received_emoji['sender']
        if not sender_handle.startswith('@'):
            sender_handle = f"@{sender_handle}"
        
        # Main message - "@handle says" - centered and prominent
        says_text = f"{sender_handle} says"
        says_width = len(says_text) * 9  # Approximate character width for font 24
        says_x = (badge.display.width - says_width) // 2
        badge.display.nice_text(says_text, says_x, 15, font=24, color=0)
        
        # Subtle separator line
        badge.display.hline(20, 45, badge.display.width - 40, 0)
        
        # Emoji name - smaller, less prominent
        emoji_data_item = emoji_data.EMOJIS.get(received_emoji['emoji'])
        if emoji_data_item:
            emoji_name = emoji_data_item['name']
            name_width = len(emoji_name) * 7  # Approximate character width for font 18
            name_x = (badge.display.width - name_width) // 2
            badge.display.nice_text(emoji_name, name_x, 55, font=18, color=0)
            
            # Draw emoji with more space (starts lower to avoid overlap)
            self.draw_emoji_from_pbm_received(emoji_data_item["pbm_file"])
        else:
            badge.display.nice_text("Unknown Emoji", 60, 80, font=18, color=0)
        
        # Bottom instruction area - more subtle
        badge.display.hline(0, 175, badge.display.width, 0)
        badge.display.nice_text("Back [SW5]", 10, 182, font=18, color=0)
        
        # Auto-close indicator - updated timing
        badge.display.nice_text("Auto-close 25s", 120, 182, font=18, color=0)
        
        badge.display.show()
    
    def draw_emoji_from_pbm_received(self, pbm_filename):
        """Load and draw a PBM file for received emoji display with adjusted positioning"""
        try:
            width, height, pixel_data = self.pbm_parser.parse_pbm_file(pbm_filename)
            
            if width is None or height is None or pixel_data is None:
                self.logger.error(f"Failed to parse PBM file: {pbm_filename}")
                badge.display.text("Error loading", 60, 100, 1)
                badge.display.text("emoji image", 60, 120, 1)
                return
            
            # Emoji display area specifically for received emoji 
            emoji_area_top = 80  # Start after the emoji name
            emoji_area_bottom = 170  # Leave more space for bottom text
            emoji_area_height = emoji_area_bottom - emoji_area_top
            emoji_area_width = badge.display.width
            
            # Scale up the emoji if it's smaller than the available space
            scale_factor = min(emoji_area_width // width, emoji_area_height // height)
            if scale_factor < 1:
                scale_factor = 1
            
            scaled_width = width * scale_factor
            scaled_height = height * scale_factor
            
            # Center the scaled emoji in the dedicated area
            center_x = (emoji_area_width - scaled_width) // 2
            center_y = emoji_area_top + (emoji_area_height - scaled_height) // 2
            
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
            self.logger.error(f"PBM Error in received display: {e}")
            badge.display.text("Image error", 60, 100, 1)

    def draw_emoji_from_pbm(self, pbm_filename):
        """Load and draw a PBM file using custom parser"""
        try:
            width, height, pixel_data = self.pbm_parser.parse_pbm_file(pbm_filename)
            
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
            self.sound_manager.draw_test_pattern()
    
    def debug_list_files(self):
        """Debug function to list available files"""
        try:
            import os
            directories_to_check = [".", "/", "/apps", f"/apps/{self.app_name}"]
            
            for directory in directories_to_check:
                try:
                    files = os.listdir(directory)
                    self.logger.info(f"Files in '{directory}': {files}")
                except OSError as e:
                    self.logger.debug(f"Cannot list '{directory}': {e}")
                    
        except Exception as e:
            self.logger.error(f"Debug file listing error: {e}")
