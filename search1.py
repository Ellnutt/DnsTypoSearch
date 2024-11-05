import subprocess
import re
import requests

# List of common TLDs to check for typosquatting
COMMON_TLDS = [".com", ".org", ".net", ".info", ".co", ".us", ".uk", ".ca", ".de", ".jp"]

# Insert your ipinfo API key here
IPINFO_API_KEY = '*******'

def run_dig(domain):
    """Runs the dig command and returns the result."""
    try:
        result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running dig for {domain}: {e}"

def get_geolocation(ip_address):
    """Fetches geolocation data for the given IP address using ipinfo.io."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}?token={IPINFO_API_KEY}")
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": ip_address,
                "country": data.get("country", "N/A"),
                "region": data.get("region", "N/A"),
                "city": data.get("city", "N/A"),
                "org": data.get("org", "N/A")
            }
        else:
            return {"error": f"Failed to get location for {ip_address}"}
    except Exception as e:
        return {"error": str(e)}

def generate_typosquats(domain):
    """Generates common typosquatting domains by manipulating characters with common spelling errors."""
    typosquats = set()
    
    # Original domain without TLD for manipulation
    base_domain = domain.split('.')[0]
    
    # Basic letter substitutions (0 for o, 1 for i, 3 for e)
    typosquats.add(base_domain.replace("o", "0"))
    typosquats.add(base_domain.replace("i", "1"))
    typosquats.add(base_domain.replace("e", "3"))

    # Missing letters (omitting one character)
    for i in range(len(base_domain)):
        typosquats.add(base_domain[:i] + base_domain[i + 1:])  # Remove one character
    
    # Duplicate adjacent letters
    for i in range(len(base_domain)):
        typosquats.add(base_domain[:i] + base_domain[i] + base_domain[i:])  # Duplicate a letter

    # Swap adjacent characters (e.g., "faceobok" for "facebook")
    for i in range(len(base_domain) - 1):
        swapped = list(base_domain)
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        typosquats.add(''.join(swapped))
    
    # QWERTY keyboard adjacency errors
    qwerty_adjacent = {
        "a": "qs", "s": "ad", "d": "sf", "f": "dg", "g": "fh", "h": "gj", "j": "hk", "k": "jl", "l": "k;",
        "q": "wa", "w": "qe", "e": "wr", "r": "et", "t": "ry", "y": "tu", "u": "yi", "i": "uo", "o": "ip", "p": "o",
        "z": "as", "x": "zs", "c": "xv", "v": "cb", "b": "vn", "n": "bm", "m": "n"
    }
    for index, char in enumerate(base_domain):
        if char in qwerty_adjacent:
            for replacement in qwerty_adjacent[char]:
                typosquats.add(base_domain[:index] + replacement + base_domain[index + 1:])

    # Include common TLD variations
    for tld in COMMON_TLDS:
        typosquats.add(base_domain + tld)

    return typosquats

def osint_search(base_domain):
    """Conducts an OSINT search by performing dig on typosquatted domains with various TLDs and fetching geolocation."""
    print(f"\nChecking base domain: {base_domain}")
    
    # Generate typosquats for the base domain
    typosquats = generate_typosquats(base_domain)
    typosquats.add(base_domain)  # Include the original domain for comparison

    # Loop through each typosquatted domain
    for typo in typosquats:
        for tld in COMMON_TLDS:
            full_domain = typo + tld
            dig_result = run_dig(full_domain)
            if dig_result:  # Only print if there's a DNS response
                print(f"\nDomain: {full_domain}")
                print(f"DNS Records:\n{dig_result}")
                
                # For each IP in the DNS result, fetch geolocation data
                for ip in dig_result.splitlines():
                    geolocation = get_geolocation(ip)
                    if "error" not in geolocation:
                        print(f"IP Address: {ip}")
                        print(f"  Country: {geolocation['country']}")
                        print(f"  Region: {geolocation['region']}")
                        print(f"  City: {geolocation['city']}")
                        print(f"  Organization: {geolocation['org']}")
                    else:
                        print(f"Error fetching geolocation for IP {ip}: {geolocation['error']}")

def main():
    user_input = input("Enter the base domain name you want to check (e.g., facebook): ")
    if not re.match(r'^[a-zA-Z0-9-]+$', user_input):
        print("Invalid format. Please enter the domain without the TLD.")
        return
    
    osint_search(user_input)

if __name__ == "__main__":
    main()
