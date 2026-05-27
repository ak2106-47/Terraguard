# Handles Terraform (.tf) parsing
import hcl2
import os

def parse_terraform_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as tf_file:
        content = hcl2.load(tf_file)
    
    return content


def extract_blocks(parsed_data):
    blocks = {
        "resource": parsed_data.get("resource", []),
        "variable": parsed_data.get("variable", []),
        "provider": parsed_data.get("provider", []),
        "output": parsed_data.get("output", []),
        "module": parsed_data.get("module", []),
        "data": parsed_data.get("data", [])
    }
    return blocks


# Example usage
if __name__ == "__main__":
    tf_file = "../examples/main.tf"  # adjust this as needed
    parsed = parse_terraform_file(tf_file)
    blocks = extract_blocks(parsed)
    
    for block_type, items in blocks.items():
        print(f"\n🔹 {block_type.upper()}:")
        print(items)
