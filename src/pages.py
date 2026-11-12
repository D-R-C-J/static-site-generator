import os
import shutil
from splitblocks import markdown_to_html_node

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

public_path = os.path.join(root_dir, "public")
static_path = os.path.join(root_dir, "static")

def copy_to_destination():
  if os.path.exists(public_path):
    print(f"Deleting directory: {public_path}")
    shutil.rmtree(public_path)

  print(f"Copying {static_path} to {public_path}")
  shutil.copytree(static_path, public_path)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown. Title must be the first line and start with '# '")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}  to {dest_path} using template {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    converted_markdown = markdown_to_html_node(markdown)
    html_string = converted_markdown.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list_of_files = os.listdir(dir_path_content)
    for file_name in list_of_files:
        if os.path.isfile(os.path.join(dir_path_content, file_name)):
            if file_name.endswith(".md"):
                with open(os.path.join(dir_path_content, file_name), "r", encoding="utf-8") as f:
                    markdown = f.read()
                with open(template_path, "r", encoding="utf-8") as f:
                    template = f.read()
                converted_markdown = markdown_to_html_node(markdown)
                html_string = converted_markdown.to_html()
                title = extract_title(markdown)
                template = template.replace("{{ Title }}", title)
                template = template.replace("{{ Content }}", html_string)
                os.makedirs(dest_dir_path, exist_ok=True)
                with open(os.path.join(dest_dir_path, file_name.replace(".md", ".html")), "w", encoding="utf-8") as f:
                    f.write(template)
        elif os.path.isdir(os.path.join(dir_path_content, file_name)):
            generate_pages_recursive(os.path.join(dir_path_content, file_name), template_path, os.path.join(dest_dir_path, file_name))
