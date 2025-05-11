import os
import boto3
import json
import base64
from tqdm import tqdm
from PIL import Image

# ------------------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------------------

def get_image_files(directory):
    """Return a list of all .jpg, .jpeg, and .png files in the given directory."""
    return [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

def should_process_file(file_path):
    """Return True if the image hasn't already been processed into a .txt summary."""
    txt_path = os.path.splitext(file_path)[0] + '.txt'
    return not os.path.exists(txt_path)

# ------------------------------------------------------------------------------
# Core Bedrock Analysis Logic
# ------------------------------------------------------------------------------

def analyze_image_with_bedrock(image_path):
    """Use Amazon Bedrock to analyze an image and return a text-based summary."""
    bedrock_client = boto3.client('bedrock-runtime')

    # Load and base64-encode the image
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode()

    # Construct the input payload for Claude 3 via Bedrock API
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Explain the content of this image."
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "anthropic_version": "bedrock-2023-05-31"
    }

    try:
        # Call the Claude 3 Haiku model hosted via Bedrock
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps(payload)
        )

        # Parse the raw JSON response
        response_body = response['body'].read().decode('utf-8')
        response_json = json.loads(response_body)

        # Extract the summary content if available
        analysis = response_json.get('message', {}).get('content', 'No analysis generated.')

        # If summary content is missing, fall back to full JSON string
        if analysis == 'No analysis generated.':
            analysis = response_body

        return analysis

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "Error occurred during analysis."

# ------------------------------------------------------------------------------
# File Output Handling
# ------------------------------------------------------------------------------

def save_analysis_to_file(analysis, file_path):
    """Save the summary analysis to a .txt file next to the original image."""
    analysis_path = os.path.splitext(file_path)[0] + '_summary.txt'
    with open(analysis_path, 'w', encoding='utf-8') as f:
        f.write(analysis)

# ------------------------------------------------------------------------------
# Batch Image Processing
# ------------------------------------------------------------------------------

def process_images_in_directory(directory):
    """Process all images in the given directory using Bedrock."""
    image_files = get_image_files(directory)

    with tqdm(total=len(image_files), desc="Processing images") as pbar:
        for image_file in image_files:
            image_path = os.path.join(directory, image_file)

            if should_process_file(image_path):
                pbar.set_postfix({'Current file': image_file})
                analysis = analyze_image_with_bedrock(image_path)
                save_analysis_to_file(analysis, image_path)

            pbar.update(1)

# ------------------------------------------------------------------------------
# Entry Point (for Jupyter notebook or script use)
# ------------------------------------------------------------------------------

directory = '.'  # Directory to scan for images
process_images_in_directory(directory)
