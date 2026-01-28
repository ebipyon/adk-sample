import difflib

def generate_diff_html(text1: str, text2: str) -> str:
    """
    Generates an HTML diff between two strings.
    
    Args:
        text1: The first string (e.g., Google STT result).
        text2: The second string (e.g., Whisper result).
        
    Returns:
        A string containing a complete HTML document for the side-by-side diff.
    """
    if not text1 or not text2:
        return "<html><body><p>Both texts are required for comparison.</p></body></html>"

    # Split lines for difflib
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()

    # Generate complete HTML document with make_file
    differ = difflib.HtmlDiff()
    html_diff = differ.make_file(
        text1_lines, 
        text2_lines, 
        fromdesc="Google Cloud STT", 
        todesc="Local Whisper", 
        context=True, 
        numlines=2
    )
    
    # Custom CSS to improve the look
    custom_css = """
<style type="text/css">
    body { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
        font-size: 13px; 
        margin: 0;
        padding: 0;
    }
    table.diff { 
        width: 100%; 
        border-collapse: collapse; 
        border: 1px solid #d1d5da; 
    }
    table.diff td, table.diff th { 
        padding: 4px 8px; 
        border: 1px solid #d1d5da; 
        vertical-align: top;
        word-wrap: break-word;
        white-space: normal;
    }
    .diff_header { 
        background-color: #f6f8fa; 
        color: #5b616b; 
        text-align: left; 
        font-weight: bold;
    }
    .diff_next { 
        background-color: #f6f8fa; 
        width: 30px;
        text-align: center;
    }
    .diff_add { background-color: #e6ffec; color: #24292e; }
    .diff_chg { background-color: #fffbdd; color: #24292e; }
    .diff_sub { background-color: #ffeef0; color: #24292e; }
    a { text-decoration: none; color: #0366d6; }
    
    /* Hide legends */
    table[summary="Legends"], table[summary="Links"] { display: none; }
</style>
"""
    
    # Inject custom CSS - replace the closing head tag
    html_diff = html_diff.replace('</head>', f'{custom_css}</head>')
    
    # Remove nowrap attributes which cause overlap issues
    html_diff = html_diff.replace('nowrap="nowrap"', '')
    
    return html_diff
