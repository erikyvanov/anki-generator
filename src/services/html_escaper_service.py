"""HTMLEscaperService for safely escaping HTML content while preserving tags."""
from html.parser import HTMLParser


class HTMLEscaper(HTMLParser):
    """Custom HTML parser to escape text content while preserving tags.
    
    This class processes HTML content and escapes special characters (< and >)
    in text content while preserving HTML tags intact. This is useful for
    preventing warnings when content contains comparison operators like '< 50 km'
    mixed with HTML markup.
    """
    
    def __init__(self):
        """Initialize the HTML escaper."""
        super().__init__()
        self.result = []
        
    def handle_starttag(self, tag, attrs):
        """Handle opening tags.
        
        Args:
            tag: The tag name.
            attrs: List of (name, value) tuples for attributes.
        """
        attrs_str = ''.join(f' {name}="{value}"' for name, value in attrs)
        self.result.append(f'<{tag}{attrs_str}>')
        
    def handle_endtag(self, tag):
        """Handle closing tags.
        
        Args:
            tag: The tag name.
        """
        self.result.append(f'</{tag}>')
        
    def handle_data(self, data):
        """Handle text content - escape special characters.
        
        Args:
            data: The text content between tags.
        """
        # Escape < and > in text content
        escaped = data.replace('<', '&lt;').replace('>', '&gt;')
        self.result.append(escaped)
        
    def handle_startendtag(self, tag, attrs):
        """Handle self-closing tags.
        
        Args:
            tag: The tag name.
            attrs: List of (name, value) tuples for attributes.
        """
        attrs_str = ''.join(f' {name}="{value}"' for name, value in attrs)
        self.result.append(f'<{tag}{attrs_str} />')
        
    def get_result(self) -> str:
        """Get the processed HTML with escaped text content.
        
        Returns:
            The processed HTML string.
        """
        return ''.join(self.result)


class HTMLEscaperService:
    """Service for escaping HTML content safely."""
    
    @staticmethod
    def escape_content(content: str) -> str:
        """Escape special characters in content while preserving HTML tags.
        
        This method processes HTML content and escapes characters like '<' and '>'
        that appear in text (e.g., '< 50 km') while preserving actual HTML tags.
        
        Args:
            content: The HTML content to process.
            
        Returns:
            Content with special characters properly escaped.
            
        Example:
            >>> HTMLEscaperService.escape_content('<li>< 50 km</li>')
            '<li>&lt; 50 km</li>'
        """
        import html
        
        try:
            parser = HTMLEscaper()
            parser.feed(content)
            return parser.get_result()
        except Exception:
            # Fallback: if parsing fails, just escape everything
            return html.escape(content)
