from skyfield.api import load, Topos, Star
from skyfield.data import hipparcos

DE421_PATH = r"D:\NITM ED\Coding - Python\Final Whatsups\CodingNITSoSe25\Assignment Whats Up\Merai\de421.bsp"
HIPP_PATH = r"D:\NITM ED\Coding - Python\Final Whatsups\CodingNITSoSe25\Assignment Whats Up\Merai\hip_main.dat"

def get_visible_objects(lat, lon, user_dt=None):
    ts = load.timescale()
    t = ts.from_datetime(user_dt) if user_dt else ts.now()
    planets = load(DE421_PATH)
    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    visible = []
    for name in planets.names():
        if name == 'earth':
            continue
        try:
            planet = planets[name]
            alt, az, _ = observer.at(t).observe(planet).apparent().altaz()
            if alt.degrees > 0:
                pretty_name = name.replace(' barycenter', '').capitalize()
                obj_type = 'Planet' if pretty_name in ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto'] else pretty_name
                visible.append({
                    'name': pretty_name,
                    'type': obj_type,
                    'altitude': round(alt.degrees, 2),
                    'azimuth': round(az.degrees, 2)
                })
        except Exception:
            continue
    with open(HIPP_PATH, 'rb') as f:
        stars = hipparcos.load_dataframe(f)
    bright_stars = stars[stars['magnitude'] < 2.0]
    for hip, star_row in bright_stars.iterrows():
        star = Star(ra_hours=star_row['ra_hours'], dec_degrees=star_row['dec_degrees'])
        alt, az, _ = observer.at(t).observe(star).apparent().altaz()
        if alt.degrees > 0:
            proper_name = star_row.get('proper')
            hip_id_int = int(hip) # HIP ID as integer for map lookup
            hip_id_str = f"HIP {hip_id_int}"
            
            # Determine the primary display name for H1
            display_name_h1 = proper_name if proper_name and proper_name.strip() else hip_id_str
            
            visible.append({
                'name': display_name_h1, # Primary name for H1 (Common name or HIP ID)
                'hip_id': hip_id_str,    # Always the HIP ID, for H2
                'hip_int': hip_id_int, # Add integer HIP ID for constellation lookup
                'type': 'Star',
                'altitude': round(alt.degrees, 2),
                'azimuth': round(az.degrees, 2)
            })
    return visible
