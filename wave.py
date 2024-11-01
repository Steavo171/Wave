import sys
import pathlib
import json

sp = " " * 4

html_body = ""

p_title = "Wave Document"
p_bgcolor = "white"
p_bgimage = "none"
p_align = "left"
p_box = 0
p_box_style = "hidden"

def key_exists(dict_key, dictionary):
    return dict_key in dictionary

def starts_with(long_str, sub_str):
    return long_str.startswith(sub_str)

#file paths
if len(sys.argv) == 1:
    path = input("Specify the path to the script: ")
else:
    path = sys.argv[1]

if pathlib.Path(path).exists():
    with open(path, "r", encoding="utf-8") as script_file:
        script = json.load(script_file)
else:
    print(f"Invalid Path: {path}")
    exit()

#properties
if key_exists("~page", script):
    page_property = script["~page"]

    if key_exists("~title", page_property):
        p_title = page_property["~title"]

    if key_exists("~bg", page_property):
        p_bgcolor = page_property["~bg"]

    if key_exists("~pic", page_property):
        p_bgimage = page_property["~pic"]

    if key_exists("~align", page_property):
        p_align = page_property["~align"]

    if key_exists("~box", page_property):
        p_box = page_property["~box"]

    if key_exists("~box-style", page_property):
        p_box_style = page_property["~box-style"]

#properties defaults
c_p_bgcolor = p_bgcolor
c_p_align = p_align
c_p_color = "black"
c_p_size = 17
c_p_box = 0
c_p_body = ""
c_p_points_type = "disc"
c_p_point_start = "ul"

def set_defaults():
    global c_p_bgcolor, c_p_align, c_p_color, c_p_size, c_p_box, c_p_body, c_p_points_type, c_p_point_start
    c_p_bgcolor = p_bgcolor
    c_p_align = p_align
    c_p_color = "black"
    c_p_size = 17
    c_p_box = 0
    c_p_body = ""
    c_p_points_type = "disc"
    c_p_point_start = "ul"

if key_exists("$content", script):
    content_property = script["$content"]

    if key_exists("$heading", content_property):
        heading = content_property["$heading"]
        html_body += f"\t<br>\n\t<h1 style='text-align: center; font-family: Arial Narrow, sans-serif'>{heading}</h1>\n"

    if key_exists("$author", content_property):
        author = content_property["$author"]
        html_body += f"\t<br>\n\t<h2 style='text-align: center; font-family: URW Chancery L, cursive'><i>{author}</i></h2>\n"

    content_property_copy = content_property.copy()
    if key_exists("$heading", content_property_copy):
        del content_property_copy["$heading"]
    if key_exists("$author", content_property_copy):
        del content_property_copy["$author"]

    regular_keywords = list(content_property_copy.keys())
    regular_values = list(content_property_copy.values())

    for i, keyword in enumerate(regular_keywords):
        inherit = None

        if starts_with(keyword, "!inherit"):
            inherit = content_property[keyword]

        if isinstance(inherit, str):
            if inherit == "!default":
                set_defaults()
        elif isinstance(inherit, dict):
            if key_exists("!size", inherit):
                c_p_size = inherit["!size"]
            if key_exists("!color", inherit):
                c_p_color = inherit["!color"]
            if key_exists("!align", inherit):
                c_p_align = inherit["!align"]
            if key_exists("!bg", inherit):
                c_p_bgcolor = inherit["!bg"]
            if key_exists("!box", inherit):
                c_p_box = inherit["!box"]
            if key_exists("!points-type", inherit):
                c_p_points_type = inherit["!points-type"]
                c_p_point_start = "ol" if c_p_points_type in ["lower-roman", "upper-roman", "decimal", "lower-alpha", "upper-alpha"] else "ul"

        if starts_with(keyword, "$text"):
            html_body += f"\t<p style='color: {c_p_color}; background-color: {c_p_bgcolor}; font-size: {c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;'>{regular_values[i]}</p>\n"

        if starts_with(keyword, "$points"):
            points = regular_values[i]
            points_head = f"\t<{c_p_point_start} style='color: {c_p_color}; background-color: {c_p_bgcolor}; font-size: {c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px; list-style-type: {c_p_points_type};'>\n"
            points_body = "".join(f"\t\t<li>{point}</li>\n" for point in points)
            html_body += points_head + points_body + f"\t</{c_p_point_start}>\n"

        if starts_with(keyword, "$n1"):
            times = int(regular_values[i])
            html_body += "\n" + ("<br>" * times) + "\n"

        if starts_with(keyword, "$pic"):
            html_body += f"\t<img style='color: {c_p_color}; background-color: {c_p_bgcolor}; font-size: {c_p_size}px; text-align: {c_p_align}; margin: {c_p_box}px;' src='{regular_values[i]}'>\n"

html_top = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{p_title}</title>
    <style>
        body {{
            background-color: {p_bgcolor};
            background-image: url({p_bgimage});
            text-align: {p_align};
            margin: {p_box}px;
            border-style: {p_box_style};
        }}
    </style>
</head>
"""

html_document = html_top + f"\n{sp}<body>\n\n" + html_body + f"\n{sp}</body>\n</html>\n"

# Save the HTML document
file_name = path.split(".")
if len(file_name) == 1:
    file_name.append(".html")
else:
    file_name[-1] = "html"

out_name = ".".join(file_name)
with open(out_name, "w+", encoding="utf-8") as out_file:
    out_file.write(html_document)

print(f"Transpiled successfully to file: {out_name}")