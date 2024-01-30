import json
import base64

def process_line(line):
    data = json.loads(line)

    # Rename the videoId field to strIdent
    data["strIdent"] = data.pop("videoId", "")

    # Change "Title" to "strTitle"
    data["strTitle"] = data.pop("title", "")

    # Change "timeWatched" to "intTimestamp"
    data["intTimestamp"] = data.pop("timeWatched", "")

    # Add "intCount": 1 before the end of each JSON object
    data["intCount"] = 1

    # Remove specified fields
    fields_to_remove = ["author", "authorId", "published", "description", 
                        "viewCount", "lengthSeconds", "watchProgress", 
                        "isLive", "type", "_id"]

    for field in fields_to_remove:
        data.pop(field, None)

    # Define the order of keys for the final JSON string
    order_of_keys = ["strIdent", "intTimestamp", "strTitle", "intCount"]

    # Return the modified data as a JSON-formatted string
    return json.dumps({key: data.get(key, "") for key in order_of_keys}, separators=(',', ':'))

# Input and output file paths
input_file_path = 'freetube-history-2024-01-30.db'
output_file_path = 'output_file.txt' # Debug non encoded output
base64_output_file_path = 'freetubeconverted.database'

# Read the input file and process each line
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

# Process each line and store the results in a list
processed_lines = [process_line(line.strip()) for line in lines]

# Write the modified content to the output file
with open(output_file_path, 'w') as output_file:
    # Write [ at the beginning of the file
    output_file.write("[\n")

    # Write each processed line to the output file
    for i, processed_line in enumerate(processed_lines):
        output_file.write(processed_line)

        # Add a comma after each line (except for the last one)
        if i < len(processed_lines) - 1:
            output_file.write(",\n")

    # Write ] at the end of the file
    output_file.write("\n]")

# Encode the modified content using Base64
with open(output_file_path, 'rb') as input_file:
    base64_content = base64.b64encode(input_file.read()).decode('utf-8')

# Write the Base64-encoded content to a new file
with open(base64_output_file_path, 'w') as base64_output_file:
    base64_output_file.write(base64_content)
