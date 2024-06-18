import json

with open("vpn_types.json") as f:
    VPNS = json.load(f)

VPN_NAMES = [vpn["name"] for vpn in VPNS]


def speed_format(speed: str):
    """Format speed to float number"""
    if "kbit/s" in speed:
        return float(speed.replace("kbit/s", "").strip()) / 1024
    elif "Mbit/s" in speed:
        return float(speed.replace("Mbit/s", "").strip())


# reverse of the above function
def speed_format_reverse(speed: float):
    """Format speed to string"""
    if speed < 1:
        return f"{speed*1024} kbit/s"
    else:
        return f"{speed} Mbit/s"


def format_vpn_name(name: str):
    """Format vpn name"""
    for i in VPN_NAMES:
        if i in name:
            name = name.replace(i, "").strip()
    return name
