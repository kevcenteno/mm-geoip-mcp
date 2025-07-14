# mm-geoip-mcp

A minimal MCP (Model Context Protocol) server providing GeoIP lookup and
anonymous IP detection using MaxMind GeoIP2 databases.

## Features

- **GeoIP Lookup:** Returns location and related info for an IP address using the MaxMind GeoIP2 City database.
- **Anonymous IP Detection:** Detects if an IP is a proxy, VPN, or other anonymizer using the MaxMind GeoIP2 Anonymous IP database.

## Requirements

- Python 3.11+
- The following MaxMind database files (for testing, test files are included in `test-data/`):
  - `GeoIP2-City-Test.mmdb`
  - `GeoIP2-Anonymous-IP-Test.mmdb`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kevcenteno/mm-geoip-mcp.git
   cd mm-geoip-mcp
   ```
2. Install dependencies using one of the following methods:
   - With [uv](https://github.com/astral-sh/uv) (recommended for speed, uses `uv.lock`):
     ```bash
     uv pip install -r requirements.txt
     ```
   - With pip:
     ```bash
     pip install -r requirements.txt
     ```
   - With Poetry:
     ```bash
     poetry install
     ```

   The `uv.lock` file is provided for reproducible installs with uv.

## Usage

### Environment Variables
Optionally configure the paths to the MaxMind database files using environment variables:

- `CITY_DB_PATH`: Path to the GeoIP2 City database file.
- `ANONYMOUS_DB_PATH`: Path to the GeoIP2 Anonymous IP database file.

If not set, the server will use the test databases in `test-data/`.

### Running the MCP Server

```bash
python main.py
```

or 

```bash
uv run main.py
```

The server will start and expose the following MCP tools:

- `geoip_lookup(ip: str) -> dict`: Performs a GeoIP City lookup on the provided IP address.
- `anonymous_ip_lookup(ip: str) -> dict`: Checks if the IP is detected as an anonymizer (proxy/VPN).

## License

MIT

