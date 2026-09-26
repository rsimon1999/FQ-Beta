import os
import shutil

# Target directory to search (defaults to current directory)
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SOURCE_DIR, "md_exports")

for root, dirs, files in os.walk(SOURCE_DIR):
    # Avoid scanning inside the output directory itself
    if OUTPUT_DIR in root:
        continue

    for file in files:
        if file.endswith('.py') and file != os.path.basename(__file__):
            source_file_path = os.path.join(root, file)

            # Recreate relative directory structure inside OUTPUT_DIR
            rel_path = os.path.relpath(root, SOURCE_DIR)
            target_folder = os.path.join(OUTPUT_DIR, rel_path)
            os.makedirs(target_folder, exist_ok=True)

            # Define new .md filename
            base_name = os.path.splitext(file)[0]
            target_file_path = os.path.join(target_folder, f"{base_name}.md")

            print(f"Exporting: {os.path.relpath(source_file_path, SOURCE_DIR)} -> {os.path.relpath(target_file_path, SOURCE_DIR)}")

            # Read python code and write formatted markdown
            try:
                with open(source_file_path, 'r', encoding='utf-8') as f_in:
                    code_content = f_in.read()

                with open(target_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(f"# {file}\n\n")
                    f_out.write("```python\n")
                    f_out.write(code_content)
                    if not code_content.endswith('\n'):
                        f_out.write('\n')
                    f_out.write("```\n")

            except Exception as e:
                print(f" -> Error processing {file}: {e}")

print("\nExport complete! All files saved in 'md_exports/'.")
