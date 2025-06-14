# constellation_utils.py

CONSTELLATION_FILE_PATH = r"D:\NITM ED\Coding - Python\Final Whatsups\CodingNITSoSe25\Assignment Whats Up\Merai\Merai v1\constellationship.fab"

# Full constellation names from abbreviations
CONSTELLATION_NAMES = {
    "AND": "Andromeda", "ANT": "Antlia", "APS": "Apus", "AQL": "Aquila", "AQR": "Aquarius",
    "ARA": "Ara", "ARI": "Aries", "AUR": "Auriga", "BOO": "Boötes", "CAE": "Caelum",
    "CAM": "Camelopardalis", "CAP": "Capricornus", "CAR": "Carina", "CAS": "Cassiopeia",
    "CEN": "Centaurus", "CEP": "Cepheus", "CET": "Cetus", "CHA": "Chamaeleon", "CIR": "Circinus",
    "CMA": "Canis Major", "CMI": "Canis Minor", "CNC": "Cancer", "COL": "Columba", "COM": "Coma Berenices",
    "CRA": "Corona Australis", "CRB": "Corona Borealis", "CRT": "Crater", "CRU": "Crux", "CRV": "Corvus",
    "CVN": "Canes Venatici", "CYG": "Cygnus", "DEL": "Delphinus", "DOR": "Dorado", "DRA": "Draco",
    "EQU": "Equuleus", "ERI": "Eridanus", "FOR": "Fornax", "GEM": "Gemini", "GRU": "Grus",
    "HER": "Hercules", "HOR": "Horologium", "HYA": "Hydra", "HYI": "Hydrus", "IND": "Indus",
    "LAC": "Lacerta", "LEO": "Leo", "LEP": "Lepus", "LIB": "Libra", "LMI": "Leo Minor",
    "LUP": "Lupus", "LYN": "Lynx", "LYR": "Lyra", "MEN": "Mensa", "MIC": "Microscopium",
    "MON": "Monoceros", "MUS": "Musca", "NOR": "Norma", "OCT": "Octans", "OPH": "Ophiuchus",
    "ORI": "Orion", "PAV": "Pavo", "PEG": "Pegasus", "PER": "Perseus", "PHE": "Phoenix",
    "PIC": "Pictor", "PSA": "Piscis Austrinus", "PSC": "Pisces", "PUP": "Puppis", "PYX": "Pyxis",
    "RET": "Reticulum", "SCL": "Sculptor", "SCO": "Scorpius", "SCT": "Scutum", "SER": "Serpens",
    "SEX": "Sextans", "SGE": "Sagitta", "SGR": "Sagittarius", "TAH": "Taurus", "TEL": "Telescopium",
    "TRA": "Triangulum Australe", "TRI": "Triangulum", "TUC": "Tucana", "UMA": "Ursa Major",
    "UMI": "Ursa Minor", "VEL": "Vela", "VIR": "Virgo", "VOL": "Volans", "VUL": "Vulpecula"
}

def load_constellation_data(file_path=CONSTELLATION_FILE_PATH):
    """Loads constellation data from the .fab file.
    Assumes format: HIP_ID CONSTELLATION_ABBREVIATION (potentially with other data)
    Returns a dictionary mapping HIP ID (int) to full constellation name (str).
    """
    constellation_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        # Assuming HIP ID is the first part and is an integer
                        # Sometimes .fab files have HIP prefix, sometimes not.
                        hip_str = parts[0].replace("HIP", "").strip()
                        hip_id = int(hip_str)
                        # Assuming constellation abbreviation is the second part
                        const_abbr = parts[1].upper()
                        constellation_map[hip_id] = CONSTELLATION_NAMES.get(const_abbr, const_abbr) # Fallback to abbr if full name not found
                    except ValueError:
                        # Skip lines that don't conform to expected HIP ID format
                        continue
    except FileNotFoundError:
        print(f"Error: Constellation file not found at {file_path}")
    return constellation_map

# Example usage (optional, for testing)
# if __name__ == "__main__":
#     const_data = load_constellation_data()
#     if const_data:
#         print(f"Loaded {len(const_data)} constellation entries.")
#         # print(const_data.get(11767)) # Example lookup for Polaris
