import yaml

def parse_database_config(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data