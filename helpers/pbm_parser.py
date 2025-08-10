class PBMParser:
    def __init__(self, logger, app_name):
        self.logger = logger
        self.app_name = app_name
    
    def parse_pbm_file(self, filename):
        """Parse a PBM file and return width, height, and pixel data array"""
        try:
            file_path = f"/apps/{self.app_name}/{filename}"
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
        """Parse ASCII PBM format (P1)"""
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
        """Parse binary PBM format (P4)"""
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
