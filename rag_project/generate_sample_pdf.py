import os
from fpdf import FPDF

def create_sample_pdf():
    # Ensure data directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    pdf_path = os.path.join(data_dir, "TechNova_Policies.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    content = """TechNova Solutions - Customer Support Knowledge Base

1. Refund and Return Policy
- 30-Day Money-Back Guarantee: Customers can return physical hardware products within 30 days of purchase for a full refund, provided the item is in its original packaging and undamaged.
- Software Licenses: All software subscriptions and digital licenses are non-refundable once activated.
- Return Shipping: The customer is responsible for return shipping costs unless the device was defective upon arrival.

2. Shipping Policy
- Standard Shipping: Takes 3 to 5 business days and costs $5.99.
- Expedited Shipping: Takes 1 to 2 business days and costs $14.99.
- Free Shipping: All orders over $100 automatically qualify for free standard shipping.

3. Warranty Information
- Hardware Warranty: TechNova provides a 1-year limited warranty on all hardware devices covering manufacturing defects.
- Exclusions: Accidental damage, water damage, and unauthorized modifications void the warranty.

4. Troubleshooting Guide
- Device won't turn on: Press and hold the power button for 15 seconds to perform a hard reset. If it still doesn't turn on, ensure the device is charged using the provided USB-C cable for at least 30 minutes.
- Wi-Fi keeps dropping: Update the device firmware to version 2.4.1 or higher via the TechNova Mobile App. If the issue persists, reset your home router.
- App crashes on startup: Clear the app cache in your phone's settings or reinstall the application.

5. Escalation and Contact
- If a customer is highly frustrated or asks to speak to a manager, immediately escalate the conversation to a human support agent.
- Contact Email: support@technovasolutions.com
- Contact Phone: 1-800-555-0199 (Available Mon-Fri, 9 AM to 5 PM EST)
"""
    
    # Write content to PDF
    for line in content.split('\n'):
        # Multi_cell handles text wrapping
        pdf.multi_cell(0, 10, txt=line)
        
    pdf.output(pdf_path)
    print(f"Sample PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    create_sample_pdf()
