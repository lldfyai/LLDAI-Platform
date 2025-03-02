import os
import json

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def convert_files_to_format(folder_path, problem_id, lang):
    files_data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".java") or file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            files_data[file_name] = read_file_content(file_path)
    
    formatted_data = {
        "problem_id": problem_id,
        "lang": lang,
        "files_metadata": files_data
    }
    
    return formatted_data

folder_path = "app/sample_files"
problem_id = "1"
lang = "java"

formatted_data = convert_files_to_format(folder_path, problem_id, lang)

# Store the formatted data in a text file
output_file_path = "app/util/formatted_data.json"
with open(output_file_path, 'w') as output_file:
    output_file.write(json.dumps(formatted_data, indent=4))

# Generate the cURL command
json_data = json.dumps(formatted_data)
curl_command = f"curl -X POST 'http://127.0.0.1:8000/api/v1/submit/' -H 'Content-Type: application/json' -d '{json_data}'"
# Store the cURL command in a text file
curl_output_file_path = "app/util/curl_command.txt"
with open(curl_output_file_path, 'w') as curl_output_file:
    curl_output_file.write(curl_command)