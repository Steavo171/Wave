# Wave: A Markup Language Transpiler

Wave is a lightweight, Python-based markup language that transpiles JSON to HTML with inline CSS, simplifying the process of creating structured documents like business cards, letters, and invitations. 

## Features
- **JSON-Based**: Write Wave programs in JSON format, using a structured approach to define document properties and content.
- **Easy Transpilation**: Wave converts JSON to HTML and CSS effortlessly using `wave.py`, generating styled HTML documents.
- **Containers for Structure**: The `~page` container defines global properties (e.g., background color, alignment), while `$content` manages the document's body elements (e.g., headings, text, images).
- **Property Inheritance**: Use `!inherit` to apply styles across multiple elements easily, with options for overriding and resetting properties.

## Requirements
- **Hardware**: Minimum Intel i3 or equivalent, 1 GB RAM, 500 GB storage.
- **Software**: Python 3, a text editor, and a web browser for viewing the output.

## Getting Started
1. Write your Wave program in a JSON file.
2. Use `wave.py` to transpile the JSON file into HTML.
3. Open the generated HTML in a web browser to view the styled document.

## Example
Here’s a basic Wave program:

```json
{
  "~page": {
    "~bg": "#fff39a",
    "~align": "center",
    "~box": "100"
  },
  "$content": {
    "$heading": "The C Programming Language",
    "$author": "Dennis Ritchie & Brian Kernighan",
    "$text": "A definitive guide to C Programming Language."
  }
}
