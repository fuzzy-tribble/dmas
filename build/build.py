import yaml
import os

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_code(file_path, code):
    with open(file_path, 'w') as file:
        file.write(code)

def generate_code(yaml_data):
    # This is where you'll generate your code based on the YAML data.
    # This is just a placeholder implementation.
    return str(yaml_data)

def build_project():
    # Specify the directory containing your YAML files
    yaml_dir = 'path_to_your_yaml_files'
    
    # Specify the directory where you want to generate your code
    output_dir = 'src/generated'
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all YAML files in the directory
    for file_name in os.listdir(yaml_dir):
        if file_name.endswith('.yaml'):
            yaml_data = read_yaml(os.path.join(yaml_dir, file_name))
            code = generate_code(yaml_data)
            
            # Write the generated code to a new file in the output directory
            # The new file has the same name as the YAML file, but with a .py extension
            output_file_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.py')
            write_code(output_file_path, code)

if __name__ == "__main__":
    build_project()
