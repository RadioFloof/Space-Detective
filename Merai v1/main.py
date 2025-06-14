import streamlit as st
st.set_page_config(page_title="Merai")
from datetime import date, datetime
from skyfield.api import utc
import pandas as pd
from astro_utils import get_visible_objects
from wiki_utils import get_object_image_url, get_object_description, extract_name_from_description
from location_utils import get_user_location
from constellation_utils import load_constellation_data # Import new utility

# Load constellation data once at the start
CONSTELLATION_MAP = load_constellation_data()

# Immersive background and custom styles
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(120deg, #0f2027 0%, #2c5364 100%) !important;
        color: #f1f1f1 !important;
    }
    .stApp {
        background: linear-gradient(120deg, #0f2027 0%, #2c5364 100%) !important;
    }
    .block-container {
        background: rgba(20, 20, 30, 0.85) !important;
        border-radius: 18px;
        padding: 2rem 2rem 1rem 2rem;
        box-shadow: 0 8px 32px #000a;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffd700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Merai") # Changed from STAR DUST

# Location
st.header("Location")
lat, lon, address = get_user_location()
if lat is None:
    st.error("Could not determine location.")
    st.stop()
st.success(f"Detected location: {address} ({lat}, {lon})")
st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

# Date and Time
st.header("Date and Time")
d = st.date_input("Date", value=date.today())
t = st.time_input("Time", value=datetime.now().time())
dt = datetime.combine(d, t).replace(tzinfo=utc)

# Fetch Data
st.header("Visible Astronomical Objects")
with st.spinner("Fetching visible astronomical objects and details..."): # Updated spinner message
    visible_objects = get_visible_objects(lat, lon, dt)
    if not visible_objects:
        st.warning("No astronomical objects are currently visible from your location.")
        st.stop()

    # Enhance objects with descriptions and refined names for DataFrame and Tiles
    for obj in visible_objects:
        original_astro_name = obj['name'] # Name from astro_utils (proper name or HIP ID)
        hip_id = obj.get('hip_id')

        description_lookup_key = hip_id if obj['type'] == 'Star' and hip_id else original_astro_name
        description = get_object_description(description_lookup_key)
        name_from_desc = extract_name_from_description(description) if description else None

        # Update obj['name'] for DataFrame display: Wikipedia name > Hipparcos proper name > HIP ID
        if name_from_desc:
            obj['name'] = name_from_desc
        # else obj['name'] remains what astro_utils set it to (proper_name or HIP ID)
        
        # Store details for tile generation to avoid re-fetching
        obj['fetched_description'] = description
        obj['name_extracted_from_description_for_tile_h1'] = name_from_desc
        
        # Add constellation for DataFrame if it's a star
        obj['constellation'] = "N/A"
        if obj['type'] == 'Star':
            hip_int_for_lookup = obj.get('hip_int')
            if hip_int_for_lookup and CONSTELLATION_MAP:
                obj['constellation'] = CONSTELLATION_MAP.get(hip_int_for_lookup, "Unknown")

# Create DataFrame for display
df_columns = ['name', 'hip_id', 'type', 'altitude', 'azimuth', 'constellation']
# hip_int is useful for debugging but maybe not for final table, user screenshot included it.
if visible_objects and 'hip_int' in visible_objects[0]: # Check if hip_int exists
    df_columns.insert(2, 'hip_int') # Insert hip_int after hip_id if present

df_display_data = []
for obj in visible_objects:
    row = {col: obj.get(col, 'N/A') for col in df_columns}
    df_display_data.append(row)

df = pd.DataFrame(df_display_data)
st.dataframe(df[df_columns]) # Ensure column order

# Details as uniform dark-mode friendly tiles with fixed height and content truncation
st.header("Learn More About Each Object")
cols = st.columns(3)
MAX_DESC_LEN = 120  # characters
TILE_HEIGHT = 550   # px, (already adjusted for constellation line)
import re
for idx, obj_data in enumerate(visible_objects): 
    with cols[idx % 3]:
        display_name_h1 = obj_data['name_extracted_from_description_for_tile_h1'] if obj_data['name_extracted_from_description_for_tile_h1'] else "NULL"
        display_name_h2 = obj_data.get('hip_id', '') 
        description_for_tile = obj_data['fetched_description']
        constellation_name_for_tile = obj_data.get('constellation', "N/A")

        if display_name_h1 == display_name_h2 and display_name_h1 != "NULL":
            display_name_h2 = ''

        image_lookup_key = display_name_h2 if obj_data['type'] == 'Star' and display_name_h2 else obj_data['name']
        image_url = get_object_image_url(image_lookup_key)

        # Prepare HTML parts for embedding in the main f-string
        image_html_part = f"<img src='{image_url}' style='width:100%;height:180px;object-fit:cover;border-top-left-radius:16px;border-top-right-radius:16px;margin-bottom:0;' alt='object image' />" if image_url else "<div style='width:100%;height:180px;display:flex;align-items:center;justify-content:center;background:#333;border-top-left-radius:16px;border-top-right-radius:16px;color:#ff6666;font-size:18px;'>No image found.</div>"
        h1_html_part = f"<h1 style='color:#ffd700;margin:10px 0 0 0;font-size:1.5em;text-align:center;'>{display_name_h1}</h1>"
        h2_html_part = f"<h2 style='color:#fff;margin:0 0 8px 0;font-size:1.1em;text-align:center;letter-spacing:1px;'>{display_name_h2}</h2>" if display_name_h2 else ""
        details_html_part = f"<div style='text-align:center;color:#eee;font-size:0.95em;'><b>Type:</b> {obj_data['type']}<br><b>Altitude:</b> {obj_data['altitude']}°<br><b>Azimuth:</b> {obj_data['azimuth']}°<br><b>Constellation:</b> {constellation_name_for_tile}</div>"
        
        description_html_part = ""
        if description_for_tile:
            desc_content = description_for_tile[:MAX_DESC_LEN] + "..." if len(description_for_tile) > MAX_DESC_LEN else description_for_tile
            description_html_part = f"<h3 style='color:#bbb;font-size:0.9em;margin:8px 0 0 0;text-align:left;overflow-y:auto;max-height:60px;padding:0 5px;'>{desc_content}</h3>"

        tile_html = f"""
        <div style='height:{TILE_HEIGHT}px; display:flex; flex-direction:column; justify-content:space-between; border:2px solid #ffd700; border-radius:18px; padding:0; margin-bottom:18px; background:linear-gradient(135deg,#232526 0%,#414345 100%); box-shadow:0 4px 24px #000a;'>
            <div> <!-- Top content container -->
                {image_html_part}
                <div style='padding: 0 10px;'> <!-- Text content padding -->
                    {h1_html_part}
                    {h2_html_part}
                    {details_html_part}
                    {description_html_part}
                </div> <!-- Close Text content padding -->
            </div> <!-- Close Top content container -->
            <div style="flex-grow: 1;"></div> <!-- Spacer div to push content up, works with justify-content:space-between -->
        </div>
        """ # Closing triple quote for tile_html
        st.markdown(tile_html, unsafe_allow_html=True)

        if description_for_tile and len(description_for_tile) > MAX_DESC_LEN:
            with st.expander("Know more"):
                st.markdown(f"<h4 style='color:#bbb;font-size:1em;margin:0;'>{description_for_tile}</h4>", unsafe_allow_html=True)
