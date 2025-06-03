from flask import Flask, request, render_template
from pygments import highlight
from pygments.lexers import SqlLexer, PythonLexer, JavaLexer, CLexer # Added more lexers
from pygments.lexers.special import TextLexer # Added TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name # To get styles dynamically
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

# Dictionary to map language names to Pygments Lexers
LEXERS = {
    'sql': SqlLexer,
    'python': PythonLexer,
    'java': JavaLexer,
    'c': CLexer,
    'text': TextLexer, # Added TextLexer
}

@app.route('/', methods=['GET', 'POST'])
def index():
    image_data = None
    # Default values
    default_code = {
        'sql': "SELECT * FROM users WHERE id = 1;",
        'python': "def hello_world():\n    print(\"Hello, World!\")",
        'java': "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        'c': "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
        'text': "This is some plain text.\nIt will be rendered as an image.", # Added default for text
    }
    selected_language = 'sql' # Default language
    selected_theme = 'light' # Default theme
    image_title = ''  # Default title
    code_input = default_code[selected_language]

    if request.method == 'POST':
        image_title = request.form.get('title', '')
        code_input = request.form['sql_code']
        selected_language = request.form.get('language', 'sql')
        selected_theme = 'dark' if request.form.get('theme') == 'dark' else 'light'

        try:
            LexerClass = LEXERS.get(selected_language, TextLexer) # Changed default to TextLexer for safety
            
            # Choose style based on theme
            style_name = 'monokai' if selected_theme == 'dark' else 'default'
            try:
                # Check if Pillow can find a font for the style, otherwise Pillow might error
                # This is a bit of a workaround for environments where font discovery is tricky
                ImageFormatter(style=style_name).get_style_defs('') 
            except Exception:
                # Fallback if the chosen style's default font isn't available
                if selected_theme == 'dark':
                    style_name = 'native' # native is often a safe dark theme fallback
                else:
                    style_name = 'default' # Should generally be safe

            formatter = ImageFormatter(
                font_size=16,
                line_pad=5,
                style=style_name,
                image_pad=20,
                line_numbers=False
            )
            img_bytes = highlight(code_input, LexerClass(), formatter)

            img = Image.open(io.BytesIO(img_bytes))
            
            # Determine title bar color based on theme
            title_bar_height = 30
            border_width = 1
            frame_color = (180, 180, 180) if selected_theme == 'dark' else (200, 200, 200)
            title_bar_color = (100, 100, 100) if selected_theme == 'dark' else (220, 220, 220)
            # Adjust button colors for dark theme if needed, here keeping them simple
            # For a more polished look, button colors could also change.

            new_width = img.width + (2 * border_width)
            new_height = img.height + title_bar_height + (2 * border_width)

            framed_img = Image.new('RGB', (new_width, new_height), frame_color)
            
            draw = ImageDraw.Draw(framed_img)
            draw.rectangle(
                [(border_width, border_width), (new_width - border_width, border_width + title_bar_height -1)],
                fill=title_bar_color
            )
            button_radius = 6
            # Red button
            draw.ellipse(
                (border_width + 10, border_width + title_bar_height // 2 - button_radius,
                 border_width + 10 + 2 * button_radius, border_width + title_bar_height // 2 + button_radius),
                fill=(255, 95, 86) 
            )
            # Yellow button
            draw.ellipse(
                (border_width + 30, border_width + title_bar_height // 2 - button_radius,
                 border_width + 30 + 2 * button_radius, border_width + title_bar_height // 2 + button_radius),
                fill=(255, 189, 46)
            )
            # Green button
            draw.ellipse(
                (border_width + 50, border_width + title_bar_height // 2 - button_radius,
                 border_width + 50 + 2 * button_radius, border_width + title_bar_height // 2 + button_radius),
                fill=(40, 200, 64)
            )

            framed_img.paste(img, (border_width, title_bar_height + border_width))

            # Draw the title text next to the buttons
            title_text_color = (255, 255, 255) if selected_theme == 'dark' else (0, 0, 0)
            # Load a larger TTF font for the title; fallback to default if unavailable
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
            except IOError:
                font = ImageFont.load_default()
            # Calculate text position for vertical centering in title bar
            text_width, text_height = font.getsize(image_title)
            text_x = border_width + 10 + 3 * (button_radius * 2 + 10)
            text_y = border_width + (title_bar_height - text_height) // 2
            draw.text((text_x, text_y), image_title, fill=title_text_color, font=font)

            byte_arr = io.BytesIO()
            framed_img.save(byte_arr, format='PNG')
            byte_arr.seek(0)
            
            image_data = base64.b64encode(byte_arr.getvalue()).decode('utf-8')

            return render_template('index.html', sql_code=code_input, image_data=image_data, selected_language=selected_language, selected_theme=selected_theme, image_title=image_title)
        except Exception as e:
            return render_template('index.html', error=str(e), sql_code=code_input, selected_language=selected_language, selected_theme=selected_theme, image_title=image_title)
    else: # GET request
        image_title = request.args.get('title', '')
        # Update code_input based on selected_language if it's a GET request and language is in query params (e.g. user changed lang)
        requested_language = request.args.get('language', selected_language)
        if requested_language in default_code:
            selected_language = requested_language
            code_input = default_code[selected_language]
        selected_theme = request.args.get('theme', 'light') # Persist theme on GET if changed
        if selected_theme == 'dark': # ensure checkbox reflects this if changed via GET (though not directly possible with current form)
             selected_theme = 'dark'
        else:
             selected_theme = 'light'

            
    return render_template('index.html', sql_code=code_input, image_data=image_data, selected_language=selected_language, selected_theme=selected_theme, image_title=image_title)

if __name__ == '__main__':
    app.run(debug=True) # Commented out for production
