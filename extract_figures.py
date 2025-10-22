#!/usr/bin/env python3
"""
Extract figure pages from the PDF as separate image/PDF files
"""

from PyPDF2 import PdfReader, PdfWriter
import os

def extract_page_as_pdf(input_pdf, page_num, output_pdf):
    """Extract a single page from PDF and save as separate PDF"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add the page (0-indexed)
    writer.add_page(reader.pages[page_num - 1])

    # Write to output
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f"✓ Extracted page {page_num} to {output_pdf}")

if __name__ == "__main__":
    input_pdf = "The Synthetic Social Graph Theorem_ Energy-Based Models for Hyper-Realistic Social Simulations.pdf"

    # Extract the figure pages
    # Page 3 contains the Identity Tensors figure
    extract_page_as_pdf(input_pdf, 3, "synthetic_identity_tensors.pdf")

    # Page 4 contains the ADPRS and Energy Landscape figures
    extract_page_as_pdf(input_pdf, 4, "adprs_energy_landscape.pdf")

    print("\n✓ All figures extracted successfully!")
    print("Note: These are full-page PDFs. For best results in LaTeX,")
    print("you may want to crop them to just the figure content.")
