import os

base_dir = os.path.dirname(os.path.abspath(__file__))

for path in os.listdir(base_dir):
  full_path = os.path.join(base_dir, path)
  if os.path.isdir(full_path):
    readme_path = os.path.join(full_path, "README.md")
    with open(readme_path, "w") as fp:
      fp.write(f"# {path}") 
    gitkeepPath = os.path.join(full_path, '.gitkeep')
    if os.path.exists(gitkeepPath):
      os.remove(gitkeepPath)

    
