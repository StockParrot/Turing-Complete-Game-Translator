#!/usr/bin/env python3
"""
Claude Translation Script
Translates text files using Claude's batch API with a translation guide.
"""

import anthropic
import time
import os
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


def parse_sections(filepath):
    """Parse sections from a file separated by '===' markers."""
    sections = []
    current_section = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("==="):
                if current_section:
                    sections.append(''.join(current_section).strip())
                    current_section = []
            current_section.append(line)
        
        if current_section:
            sections.append(''.join(current_section))

    return sections


def process_strings_with_claude(strings_list, system_prompt, user_message_template, api_key):
    """
    Process a list of strings using Claude via batch API.
    
    Args:
        strings_list: List of strings to process
        system_prompt: System prompt to use for each conversation
        user_message_template: User message template. The current string will be appended one line below the user template
        api_key: Anthropic API key
    
    Returns:
        List of strings containing Claude's responses
    """
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"Creating batch request for {len(strings_list)} items...")
    
    # Create batch requests
    requests = []
    for i, string_item in enumerate(strings_list):
        # Format the user message with the current string
        formatted_user_message = user_message_template + "\n" + string_item
        
        request = Request(
            custom_id=f"request-{i}",
            params=MessageCreateParamsNonStreaming(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": formatted_user_message,
                }]
            )
        )
        requests.append(request)
    
    # Create the batch
    print("Submitting batch request to Claude...")
    message_batch = client.messages.batches.create(requests=requests)
    print(f"Batch created with ID: {message_batch.id}")
    
    # Poll for completion every minute
    print("Waiting for batch to complete...")
    while True:
        message_batch = client.messages.batches.retrieve(message_batch.id)
        
        if message_batch.processing_status == "ended":
            print("Batch processing completed!")
            break
        
        print(f"Batch {message_batch.id} is still processing... (Status: {message_batch.processing_status})")
        time.sleep(60)
    
    # Collect results
    print("Retrieving results...")
    results = []
    result_dict = {}
    
    # First, collect all results into a dictionary keyed by custom_id
    for result in client.messages.batches.results(message_batch.id):
        result_dict[result.custom_id] = result
    
    # Then, extract responses in the original order
    for i in range(len(strings_list)):
        custom_id = f"request-{i}"
        if custom_id in result_dict:
            result = result_dict[custom_id]
            if result.result.type == "succeeded":
                # Check if Claude refused to respond
                if result.result.message.stop_reason == "refusal":
                    # Return the original string unprocessed
                    results.append(strings_list[i])
                    print(f"Request {i} was refused by Claude, returning original string")
                else:
                    # Extract the text content from Claude's response
                    response_text = result.result.message.content[0].text
                    results.append(response_text)
            else:
                # Handle failed requests
                error_info = f"Error: {result.result.error.type} - {result.result.error.message}"
                results.append(error_info)
                print(f"Request {i} failed: {error_info}")
        else:
            results.append("Error: No result found for this request")
            print(f"No result found for request {i}")
    
    print(f"Successfully processed {len(results)} items")
    return results


def main():
    """Main function to run the translation process."""
    
    # File paths
    english_file = "English.txt"
    translation_guide_file = "guia_traducao_turing_complete_pt-br.md"
    output_file = "Portuguese.txt"
    
    # Check if required files exist
    if not os.path.exists(english_file):
        print(f"Error: {english_file} not found in current directory")
        return
    
    if not os.path.exists(translation_guide_file):
        print(f"Error: {translation_guide_file} not found in current directory")
        return
    
    # Get API key from environment variable
    api_key = "sk-ant-api03-your_api_key_here"
    
    try:
        # Parse the English text file
        print(f"Parsing {english_file}...")
        parsed_sections = parse_sections(english_file)
        print(f"Found {len(parsed_sections)} sections to translate")
        
        # Add spacing to all sections except the last one
        parsed_fix = [s + '\n\n\n' for s in parsed_sections[:-1]] + [parsed_sections[-1]]
        
        # Load translation guide
        print(f"Loading translation guide from {translation_guide_file}...")
        with open(translation_guide_file, 'r', encoding='utf-8') as f:
            translation_guide = f.read()
        
        # System prompt for Claude
        system_prompt = """You are a translation AI. Whenever you receive any text, you consider the user provided translation guide and translate the user appointed text into the target language without adding any comments, explanations, or introductions. Return only the translated text—nothing more, nothing less."""
        
        # Process all sections with Claude
        print("Starting translation process...")
        responses = process_strings_with_claude(
            parsed_fix, 
            system_prompt, 
            translation_guide, 
            api_key
        )
        
        # Prepare output with proper spacing
        printable_results = [s + '\n\n\n' for s in responses]
        
        # Save translated text to output file
        output_text = ''.join(printable_results)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output_text)
        
        print(f"Translation completed! Output saved to {output_file}")
        print(f"Translated {len(responses)} sections")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return


if __name__ == "__main__":
    main()
