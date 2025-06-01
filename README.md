# SQL to PNG Converter

This web application takes SQL code as input and generates a PNG image. The image displays the SQL code with syntax highlighting and a frame designed to resemble a query tool interface.

## Features

*   Accepts SQL code via a web form.
*   Generates a PNG image of the SQL code.
*   Applies syntax highlighting to the SQL code.
*   Adds a decorative frame and title bar to the image.

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # HTML template for the web form
└── .github/
    └── copilot-instructions.md # Instructions for GitHub Copilot
```

## Setup and Running

1.  **Prerequisites:**
    *   Python 3.x
    *   pip (Python package installer)

2.  **Clone the repository (if applicable) or ensure you have the files.**

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` in your web browser.

## How it Works

*   The frontend is a simple HTML form where users can paste their SQL code.
*   The backend is a Flask application:
    *   It receives the SQL code from the form.
    *   Uses the `Pygments` library for syntax highlighting and initial image generation.
    *   Uses the `Pillow` (PIL Fork) library to draw a frame and a mock title bar (with macOS-like buttons) around the highlighted code image.
    *   Sends the final image back to the user as a PNG download.

## Customization

*   **Syntax Highlighting Style:** You can change the Pygments style in `app.py` (e.g., `style='monokai'`). A list of available styles can be found in the Pygments documentation.
*   **Font and Colors:** The font, font size, colors for the frame, and title bar can be adjusted in `app.py` within the `ImageFormatter` and image drawing sections.
*   **HTML/CSS:** The appearance of the web form can be modified in `templates/index.html`.
