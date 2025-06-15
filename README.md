# Turing-Complete-Game-Translator

A Python script that uses Anthropic's Claude API to translate game localization files with contextual translation guides.

## Overview

This project provides an automated translation system specifically designed for translating the game "Turing Complete" (2021) to Brazilian Portuguese (PT-BR). It uses Claude's batch API to process translation files while maintaining technical accuracy and consistency through a comprehensive translation guide.

## Features

- **Batch Processing**: Efficiently processes multiple text sections using Claude's batch API
- **Section-based Translation**: Parses files separated by `===` markers into individual sections
- **Translation Consistency**: Uses a detailed translation guide to ensure consistent terminology
- **Error Handling**: Gracefully handles API errors and refused requests
- **Preserve Formatting**: Maintains original text formatting, markup tags, and placeholders
- **Technical Accuracy**: Specialized for technical/gaming content with proper terminology handling

## Prerequisites

- Python 3.6+
- Anthropic API key
- `anthropic` Python package

## Installation

1. Clone this repository or download the script files
2. Install the required Python package:
   ```bash
   pip install anthropic
   ```
3. Set up your Anthropic API key by replacing the placeholder in the script:
   ```python
   api_key = "sk-ant-api03-your_api_key_here"
   ```

## File Structure

```
project/
├── claude_translate_game.py           # Main translation script
├── guia_traducao_turing_complete_pt-br.md  # Translation guide (PT-BR)
├── English.txt                        # Source text file (not included)
└── Portuguese.txt                     # Output translated file
```

## Usage

1. **Prepare your files**:
   - Place your source text file as `English.txt` in the project directory
   - Ensure the translation guide for your language (in this case `guia_traducao_turing_complete_pt-br.md`) is present
   - Update the API key in the script

2. **Run the translation**:
   ```bash
   python claude_translate_game.py
   ```

3. **Check the output**:
   - Translated text will be saved to `Portuguese.txt`
   - Progress updates will be displayed in the console

## Input File Format

The source text file should contain sections separated by `===` markers:

```
=== foo/bar1 ===

$31415926535897* Good morning player


=== foo/barbar/foo1 ===

$01234567898765* Love some fryed circuits in the morning!


=== bar/foofoo/bar ===

$42042042042042*
I hate to get in the way
of a good fight!


```

## Translation Guide

The included translation guide (`guia_traducao_turing_complete_pt-br.md`) provides:

- **General Conventions**: Tone, formality, and style guidelines
- **Technical Glossary**: Consistent translations for technical terms
- **Formatting Rules**: How to handle markup tags and placeholders
- **Translation Examples**: Sample translations for reference
- **Preservation Rules**: Elements that should remain unchanged

### Key Translation Principles

- Maintain informal technical tone with appropriate humor
- Use "você" (informal "you") and direct language
- Don't translate electronic component names (NAND, XOR, etc.)
- Use infinitive verbs for actions ("Salvar", "Carregar")
- Preserve all markup tags (`[center]`, `[b]`, `{placeholders}`, etc.)

## API Usage

The script uses Claude Sonnet 4 (`claude-sonnet-4-20250514`) with the following configuration:
- **Max tokens**: 4096 per request
- **Processing**: Batch API for efficient handling
- **Polling interval**: 60 seconds for batch completion

## Error Handling

The script handles various error scenarios:
- Missing required files
- API errors and failed requests
- Claude refusals (returns original text)
- Network timeouts during batch processing

## Output

The translated file maintains:
- Original section structure with proper spacing
- All markup tags and formatting
- Technical term consistency
- Contextual accuracy based on the translation guide

## Customization

To adapt this script for other languages or projects:

1. **Update the translation guide**: Modify `guia_traducao_turing_complete_pt-br.md` with your target language rules
2. **Adjust file paths**: Change input/output filenames in the `main()` function
3. **Modify system prompt**: Update the system prompt for different translation contexts
4. **Configure API settings**: Adjust model, max tokens, or other parameters as needed

## Limitations

- Requires valid Anthropic API key with sufficient credits
- Processing time depends on batch size and API response times
- Large files may require splitting into smaller batches
- Technical accuracy depends on the quality of the translation guide

## Contributing

When contributing to this project:
- Maintain the existing code structure and error handling
- Update the translation guide for any new terminology
- Add translation guides for other languages
- Test with sample files before submitting changes
- Follow Python best practices and include proper documentation

