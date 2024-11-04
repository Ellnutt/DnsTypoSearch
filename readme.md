# DNS OSINT Tool

This is an OSINT (Open Source Intelligence) tool for investigating domain typosquatting and gathering geolocation data on DNS records. It allows users to input a base domain name (like `facebook`), automatically generates common typosquatting variations, and performs DNS lookups to identify potential misdirected domains. For each discovered IP address, the tool fetches geolocation data to provide insight into where the domain might be hosted.

## Features

- **DNS Lookup**: Queries DNS records for each typosquatted domain variation.
- **Typosquatting Variations**: Automatically generates common spelling errors, including:
  - Character substitution (like `o` to `0`, `i` to `1`)
  - Character omissions
  - Adjacent character swaps
  - Keyboard adjacency errors (e.g., `facebok` for `facebook`)
- **Multi-TLD Support**: Checks multiple TLDs (like `.com`, `.org`, `.net`, `.uk`).
- **Geolocation Data**: Retrieves location data for each IP address using the `ipinfo.io` API.

## Requirements

- **Python 3.x**
- **Required Packages**:
  - `requests`: For making API requests
- **API Key**: A free API key from `ipinfo.io` for fetching geolocation data.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/dns-osint-tool.git
   cd dns-osint-tool
