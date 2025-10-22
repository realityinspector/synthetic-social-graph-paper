#!/usr/bin/env python3
"""
Convert PDF to LaTeX using Anthropic API
This script reads a PDF file and uses Claude to convert it to LaTeX source code
suitable for arXiv submission.
"""

import os
import base64
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def pdf_to_base64(pdf_path):
    """Convert PDF file to base64 encoding"""
    with open(pdf_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')

def convert_pdf_to_latex(pdf_path, output_path='paper.tex'):
    """
    Convert PDF to LaTeX using Anthropic API

    Args:
        pdf_path: Path to the input PDF file
        output_path: Path where the LaTeX file will be saved
    """
    # Initialize Anthropic client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Read and encode PDF
    print(f"Reading PDF from: {pdf_path}")
    pdf_data = pdf_to_base64(pdf_path)

    # Create the conversion prompt
    prompt = """Please convert this PDF document to a complete, publication-ready LaTeX source file suitable for arXiv submission.

IMPORTANT REQUIREMENTS:

1. **Document Structure**:
   - Use the article document class
   - Include all necessary packages (amsmath, amssymb, graphicx, etc.)
   - Preserve all sections, subsections, and heading hierarchy
   - Include proper title, author, date, and abstract

2. **Mathematics**:
   - Convert ALL equations to proper LaTeX math notation
   - Use appropriate environments (equation, align, gather, etc.)
   - Preserve equation numbering and labels
   - Include all mathematical symbols, operators, and special notation
   - Use \\displaystyle where appropriate for readability

3. **Figures and Diagrams**:
   - For each figure/diagram in the PDF, create a figure environment with:
     - A descriptive \\includegraphics command (e.g., \\includegraphics[width=0.8\\textwidth]{figure1.pdf})
     - The original caption text
     - A label for cross-referencing
   - Add comments indicating what each figure should contain
   - Note that actual figure files will need to be created separately

4. **Formatting**:
   - Preserve all emphasized, bold, and italic text
   - Maintain bullet points and numbered lists
   - Keep table structures intact
   - Preserve all citations and references (create a bibliography section)

5. **Code Quality**:
   - Use proper LaTeX best practices
   - Add comments for complex sections
   - Ensure the document will compile with pdflatex
   - Use semantic commands (\\emph, \\textbf) over formatting commands

6. **Completeness**:
   - Include EVERYTHING from the PDF - don't omit any content
   - Preserve the exact wording and structure
   - Include all footnotes, captions, and annotations

Please output ONLY the complete LaTeX source code, starting with \\documentclass and ending with \\end{document}. Do not include any explanatory text before or after the LaTeX code."""

    print("Sending PDF to Claude API for conversion...")
    print("This may take a minute as Claude analyzes the document...")

    # Make API request with PDF
    message = client.messages.create(
        model="claude-sonnet-4-20250514",  # Using latest model with vision
        max_tokens=16000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    # Extract LaTeX content
    latex_content = message.content[0].text

    # Clean up the output - remove markdown code blocks if present
    if latex_content.startswith('```latex'):
        latex_content = latex_content.split('```latex\n', 1)[1]
        latex_content = latex_content.rsplit('```', 1)[0]
    elif latex_content.startswith('```'):
        latex_content = latex_content.split('```\n', 1)[1]
        latex_content = latex_content.rsplit('```', 1)[0]

    # Write to file
    print(f"Writing LaTeX to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"✓ Conversion complete!")
    print(f"✓ LaTeX file saved to: {output_path}")
    print(f"\nNext steps:")
    print("1. Review the generated LaTeX file")
    print("2. Create/extract any figures referenced in the document")
    print("3. Test compile with: pdflatex paper.tex")
    print("4. Run arxiv-collector to prepare submission package")

    return latex_content

if __name__ == "__main__":
    # Find the PDF file
    pdf_file = "The Synthetic Social Graph Theorem_ Energy-Based Models for Hyper-Realistic Social Simulations.pdf"

    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        exit(1)

    # Convert
    convert_pdf_to_latex(pdf_file, "paper.tex")
