import streamlit as st
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re
import os
import uuid

# Page configuration
st.set_page_config(
    page_title="Table & Chair Rental Service",
    page_icon="🪑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for professional styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5em;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.1em;
        margin-top: 10px;
        opacity: 0.95;
    }
    
    /* Pricing Card */
    .price-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .price-item {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Section Headers */
    .section-header {
        color: #667eea;
        font-weight: 600;
        font-size: 1.3em;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    /* Total Section */
    .total-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .total-section h2, .total-section h3 {
        color: white !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Divider */
    hr {
        margin: 30px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 10px;
    }
    
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 10px;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 10px;
    }
    
    /* Info Box */
    .info-box {
        background: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 20px 0;
    }
    
    /* Feature Icons */
    .feature-icon {
        font-size: 2em;
        margin-right: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #7f8c8d;
        padding: 30px 20px;
        background: #f8f9fa;
        border-radius: 15px;
        margin-top: 30px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f5f7fa;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Date and Time Inputs */
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* Container Styling */
    .element-container {
        margin-bottom: 10px;
    }
    
    /* Discount Badge */
    .discount-badge {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        margin: 10px 0;
    }
    
    /* Summary Row */
    .summary-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .summary-row:last-child {
        border-bottom: none;
        border-top: 2px solid rgba(255,255,255,0.5);
        margin-top: 10px;
        padding-top: 15px;
        font-size: 1.3em;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_total(num_chairs, num_tables):
    """Calculate total cost with discount"""
    chair_cost = num_chairs * 1
    table_cost = num_tables * 5
    subtotal = chair_cost + table_cost
    
    # Apply 5% discount if subtotal >= $200
    discount = 0
    if subtotal >= 200:
        discount = subtotal * 0.05
    
    total = subtotal - discount
    
    return {
        'chair_cost': chair_cost,
        'table_cost': table_cost,
        'subtotal': subtotal,
        'discount': discount,
        'total': total
    }

def generate_invoice(order_data, costs):
    """Generate invoice HTML"""
    invoice_html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                max-width: 650px; 
                margin: 0 auto;
                background: #f5f5f5;
                padding: 20px;
            }}
            .invoice-container {{
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 40px 30px; 
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.2em;
                font-weight: 700;
            }}
            .header h2 {{
                margin: 10px 0 0 0;
                font-weight: 400;
                opacity: 0.9;
            }}
            .content {{ 
                padding: 30px;
            }}
            .greeting {{
                font-size: 1.2em;
                color: #333;
                margin-bottom: 20px;
            }}
            .order-details {{ 
                background: #f8f9fa; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }}
            .order-details h4 {{
                color: #667eea;
                margin-top: 0;
                font-size: 1.1em;
            }}
            .order-details p {{
                margin: 8px 0;
                color: #555;
            }}
            .item-row {{ 
                display: flex; 
                justify-content: space-between; 
                margin: 12px 0;
                padding: 10px;
                background: white;
                border-radius: 5px;
            }}
            .total-row {{ 
                font-weight: bold; 
                font-size: 1.3em; 
                border-top: 3px solid #667eea; 
                padding-top: 15px; 
                margin-top: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 8px;
            }}
            .discount {{ 
                color: #28a745;
                font-weight: 600;
            }}
            .footer {{ 
                text-align: center; 
                color: #7f8c8d; 
                margin-top: 30px; 
                padding-top: 30px; 
                border-top: 2px solid #e0e0e0;
            }}
            .footer p {{
                margin: 8px 0;
            }}
            .highlight {{
                color: #667eea;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="header">
                <h1>🪑 Table & Chair Rental Service</h1>
                <h2>Order Confirmation</h2>
            </div>
            <div class="content">
                <div class="greeting">
                    <p>Thank you for your order, <span class="highlight">{order_data['name']}</span>! 🎉</p>
                    <p>We have received your rental request and will contact you shortly to confirm availability.</p>
                </div>
                
                <div class="order-details">
                    <h4>👤 Customer Information</h4>
                    <p><strong>Name:</strong> {order_data['name']}</p>
                    <p><strong>Email:</strong> {order_data['email']}</p>
                    <p><strong>Phone:</strong> {order_data['phone'] or 'Not provided'}</p>
                </div>
                
                <div class="order-details">
                    <h4>📅 Event Details</h4>
                    <p><strong>Event Date:</strong> {order_data['event_date']}</p>
                    <p><strong>Pickup Time:</strong> {order_data['pickup_time']}</p>
                    <p><strong>Drop-off Time:</strong> {order_data['dropoff_time']}</p>
                </div>
                
                <div class="order-details">
                    <h4>📋 Order Summary</h4>
                    <div class="item-row">
                        <span>🪑 Chairs ({order_data['num_chairs']} × $1.00)</span>
                        <span><strong>${costs['chair_cost']:.2f}</strong></span>
                    </div>
                    <div class="item-row">
                        <span>🪑 Tables ({order_data['num_tables']} × $5.00)</span>
                        <span><strong>${costs['table_cost']:.2f}</strong></span>
                    </div>
                    <div class="item-row">
                        <span>Subtotal</span>
                        <span><strong>${costs['subtotal']:.2f}</strong></span>
                    </div>
                    {f'<div class="item-row discount"><span>🎉 Discount (5%)</span><span><strong>-${costs["discount"]:.2f}</strong></span></div>' if costs['discount'] > 0 else ''}
                    <div class="item-row total-row">
                        <span>💰 Total Amount</span>
                        <span>${costs['total']:.2f}</span>
                    </div>
                </div>
                
                <div class="footer">
                    <p>📞 If you have any questions about your order, please contact us.</p>
                    <p style="font-size: 0.9em; color: #999;">This is an automated confirmation email.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return invoice_html

def send_confirmation_email(to_email, order_data, costs):
    """Send confirmation email using environment variables or Streamlit secrets"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "aaal.enterprises.aaal@gmail.com"
    sender_password = "nrnboqihxwoldshr"

    try:
        if not sender_email or not sender_password:
            return False, "Email credentials not configured. Please set up environment variables or Streamlit secrets."
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🎉 Order Confirmation - Event on {order_data['event_date']}"
        message["From"] = sender_email
        message["To"] = to_email
        
        html_content = generate_invoice(order_data, costs)
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True, "Confirmation email sent successfully!"
    
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def send_calendar_invite(to_email, order_data, event_date_str, start_time="09:00", end_time="09:15"):
    """Send calendar invite for the event"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "aaal.enterprises.aaal@gmail.com"
    sender_password = "nrnboqihxwoldshr"
    
    try:
        if not sender_email or not sender_password:
            return False, "Email credentials not configured."
        
        if isinstance(event_date_str, str):
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
        else:
            event_date = event_date_str
        
        start_dt = datetime.combine(event_date, datetime.strptime(start_time, "%H:%M").time())
        end_dt = datetime.combine(event_date, datetime.strptime(end_time, "%H:%M").time())
        
        dtstart = start_dt.strftime("%Y%m%dT%H%M%S")
        dtend = end_dt.strftime("%Y%m%dT%H%M%S")
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        uid = str(uuid.uuid4())
        
        ical_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Table & Chair Rental Service//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:Table & Chair Rental - {order_data['name']}
DESCRIPTION:Rental Details:\\n\\nChairs: {order_data['num_chairs']}\\nTables: {order_data['num_tables']}\\n\\nPickup: {order_data['pickup_time']}\\nDrop-off: {order_data['dropoff_time']}\\n\\nCustomer: {order_data['name']}\\nEmail: {order_data['email']}\\nPhone: {order_data.get('phone', 'Not provided')}
LOCATION:To be confirmed
ORGANIZER:mailto:{sender_email}
ATTENDEE;RSVP=TRUE;CN={order_data['name']}:mailto:{to_email}
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT24H
ACTION:DISPLAY
DESCRIPTION:Reminder: Table & Chair Rental tomorrow
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        message = MIMEMultipart("mixed")
        message["Subject"] = f"📅 Calendar Invite - Rental on {order_data['event_date']}"
        message["From"] = sender_email
        message["To"] = to_email
        
        text_body = f"""
Hello {order_data['name']},

Please find attached a calendar invite for your table and chair rental.

Event Details:
- Date: {order_data['event_date']}
- Time: {start_time} - {end_time}
- Chairs: {order_data['num_chairs']}
- Tables: {order_data['num_tables']}

Pickup: {order_data['pickup_time']}
Drop-off: {order_data['dropoff_time']}

Best regards,
Table & Chair Rental Service
        """
        
        message.attach(MIMEText(text_body, "plain"))
        
        ical_part = MIMEBase("text", "calendar", method="REQUEST", name="invite.ics")
        ical_part.set_payload(ical_content.encode('utf-8'))
        encoders.encode_base64(ical_part)
        ical_part.add_header("Content-Disposition", "attachment", filename="invite.ics")
        ical_part.add_header("Content-class", "urn:content-classes:calendarmessage")
        message.attach(ical_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True, "Calendar invite sent successfully!"
    
    except Exception as e:
        return False, f"Error sending calendar invite: {str(e)}"

# Main App Header
st.markdown("""
    <div class='main-header'>
        <h1>🪑 Table & Chair Rental Service</h1>
        <p>Professional Event Rentals Made Easy</p>
    </div>
""", unsafe_allow_html=True)

# Pricing Information with enhanced design
st.markdown("<h2 class='section-header'>💰 Our Pricing</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class='price-item'>
            <div style='text-align: center;'>
                <div class='feature-icon'>🪑</div>
                <h3 style='color: #667eea; margin: 10px 0;'>Chairs</h3>
                <p style='font-size: 2em; font-weight: 700; color: #333; margin: 10px 0;'>$1.00</p>
                <p style='color: #666;'>per chair</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='price-item'>
            <div style='text-align: center;'>
                <div class='feature-icon'>🪑</div>
                <h3 style='color: #667eea; margin: 10px 0;'>Tables</h3>
                <p style='font-size: 2em; font-weight: 700; color: #333; margin: 10px 0;'>$5.00</p>
                <p style='color: #666;'>per table</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='price-item'>
            <div style='text-align: center;'>
                <div class='feature-icon'>🎉</div>
                <h3 style='color: #667eea; margin: 10px 0;'>Discount</h3>
                <p style='font-size: 2em; font-weight: 700; color: #28a745; margin: 10px 0;'>5%</p>
                <p style='color: #666;'>on orders $200+</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='info-box'>ℹ️ <strong>No hidden fees!</strong> What you see is what you pay - no tax, no delivery charges for local areas.</div>", unsafe_allow_html=True)

st.divider()

# Order Form
st.markdown("<h2 class='section-header'>📝 Place Your Order</h2>", unsafe_allow_html=True)

# Customer Information
st.markdown("<h3 style='color: #667eea; margin-top: 20px;'>👤 Customer Information</h3>", unsafe_allow_html=True)
name = st.text_input("Full Name *", placeholder="Enter your full name", key="name_input")

col1, col2 = st.columns(2)
with col1:
    email = st.text_input("Email Address *", placeholder="your@email.com", key="email_input")
with col2:
    phone = st.text_input("Phone Number", placeholder="(555) 123-4567", key="phone_input")

st.divider()

# Event Details
st.markdown("<h3 style='color: #667eea;'>📅 Event Details</h3>", unsafe_allow_html=True)
event_date = st.date_input(
    "Event Date *", 
    min_value=datetime.now().date(),
    key="event_date_input"
)

col1, col2 = st.columns(2)
with col1:
    pickup_time = st.time_input(
        "⏰ Pickup Time", 
        value=datetime.strptime("09:00", "%H:%M").time(),
        key="pickup_time_input"
    )
with col2:
    default_dropoff = (datetime.combine(datetime.today(), pickup_time) + timedelta(hours=24)).time()
    dropoff_time = st.time_input(
        "⏰ Drop-off Time", 
        value=default_dropoff,
        key="dropoff_time_input"
    )

st.divider()

# Rental Items
st.markdown("<h3 style='color: #667eea;'>🪑 Select Your Rental Items</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    num_chairs = st.number_input(
        "🪑 Number of Chairs", 
        min_value=0, 
        value=0, 
        step=1,
        key="chairs_input",
        help="Each chair costs $1.00"
    )
with col2:
    num_tables = st.number_input(
        "🪑 Number of Tables", 
        min_value=0, 
        value=0, 
        step=1,
        key="tables_input",
        help="Each table costs $5.00"
    )

st.divider()

# Calculate and display total
if num_chairs > 0 or num_tables > 0:
    costs = calculate_total(num_chairs, num_tables)
    
    st.markdown("<div class='total-section'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: white; margin-top: 0;'>💵 Order Summary</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='summary-row'>
            <span>🪑 Chairs ({num_chairs} × $1.00)</span>
            <span>${costs['chair_cost']:.2f}</span>
        </div>
        <div class='summary-row'>
            <span>🪑 Tables ({num_tables} × $5.00)</span>
            <span>${costs['table_cost']:.2f}</span>
        </div>
        <div class='summary-row'>
            <span>Subtotal</span>
            <span>${costs['subtotal']:.2f}</span>
        </div>
        {f"<div class='summary-row' style='color: #90EE90;'><span>🎉 Discount (5%)</span><span>-${costs['discount']:.2f}</span></div>" if costs['discount'] > 0 else ''}
        <div class='summary-row'>
            <span><strong>💰 Total Amount</strong></span>
            <span><strong>${costs['total']:.2f}</strong></span>
        </div>
    """, unsafe_allow_html=True)
    
    if costs['discount'] > 0:
        st.markdown(f"<div class='discount-badge'>🎊 You're saving ${costs['discount']:.2f} with our 5% discount!</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Submit Button
st.markdown("<div style='text-align: center; margin: 30px 0;'>", unsafe_allow_html=True)
submit_button = st.button("🚀 Submit Order", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    # Validation
    errors = []
    
    if not name.strip():
        errors.append("❌ Name is required")
    if not email.strip():
        errors.append("❌ Email is required")
    elif not validate_email(email):
        errors.append("❌ Invalid email format")
    if not event_date:
        errors.append("❌ Event date is required")
    if num_chairs == 0 and num_tables == 0:
        errors.append("❌ Please select at least one chair or table")
    
    if errors:
        st.error("⚠️ Please fix the following errors:")
        for error in errors:
            st.write(error)
    else:
        # Prepare order data
        order_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'event_date': event_date.strftime("%B %d, %Y"),
            'pickup_time': pickup_time.strftime("%I:%M %p"),
            'dropoff_time': dropoff_time.strftime("%I:%M %p"),
            'num_chairs': num_chairs,
            'num_tables': num_tables
        }
        
        costs = calculate_total(num_chairs, num_tables)
        
        # Display success message
        st.success("✅ Order submitted successfully!")
        st.balloons()
        
        # Display invoice
        with st.expander("📄 View Order Summary", expanded=True):
            st.markdown(generate_invoice(order_data, costs), unsafe_allow_html=True)
        
        # Send confirmation email
        with st.spinner("📧 Sending confirmation email..."):
            success, message = send_confirmation_email(email, order_data, costs)
            
            if success:
                st.success(f"✉️ {message}")
                
                # Send calendar invite
                with st.spinner("📅 Sending calendar invite..."):
                    invite_success, invite_message = send_calendar_invite(
                        email, 
                        order_data, 
                        event_date.strftime("%Y-%m-%d"),
                        start_time="09:00",
                        end_time="09:15"
                    )
                    
                    if invite_success:
                        st.success(f"📅 {invite_message}")
                    else:
                        st.warning(f"⚠️ Calendar invite: {invite_message}")
            else:
                st.warning(f"⚠️ {message}")

# Footer
st.divider()
st.markdown("""
    <div class='footer'>
        <h3 style='color: #667eea; margin-bottom: 15px;'>🪑 Table & Chair Rental Service</h3>
        <p style='font-size: 1.1em;'><strong>Making Your Events Memorable</strong></p>
        <p style='margin: 10px 0;'>📞 Contact us for special requests or bulk orders</p>
        <p style='font-size: 0.85em; color: #999; margin-top: 15px;'>* Required fields</p>
        <p style='font-size: 0.8em; color: #bbb; margin-top: 10px;'>© 2026 Table & Chair Rental Service. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)