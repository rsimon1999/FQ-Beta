import os

# Define project folder layout
structure = {
    "src": {
        "audio": ["__init__.py", "engine.py", "generators.py", "presets.py"],
        "ui": ["__init__.py", "app.py", "frames.py"],
        "utils": ["__init__.py", "export.py", "config.py"],
    },
    "data": ["presets.json"],
    "output": [".gitkeep"],
    "tests": ["__init__.py", "test_audio.py"],
}

# Base files in root
root_files = ["main.py", "requirements.txt", "README.md", "PROJECT_PLAN.md"]


def create_structure(base_path="."):
    for item, content in structure.items():
        dir_path = os.path.join(base_path, item)
        os.makedirs(dir_path, exist_ok=True)
        if isinstance(content, list):
            for file_name in content:
                file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        pass
        elif isinstance(content, dict):
            for sub_dir, files in content.items():
                sub_dir_path = os.path.join(dir_path, sub_dir)
                os.makedirs(sub_dir_path, exist_ok=True)
                for file_name in files:
                    file_path = os.path.join(sub_dir_path, file_name)
                    if not os.path.exists(file_path):
                        with open(file_path, "w") as f:
                            pass

    for file_name in root_files:
        file_path = os.path.join(base_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass


if __name__ == "__main__":
    create_structure()
    print("✓ Production directory structure created successfully.")