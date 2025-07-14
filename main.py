from fastmcp import FastMCP
import geoip2.database
import os
from pathlib import Path

mcp = FastMCP("mm-geoip-mcp")
city_reader = None
anonymous_ip_reader = None


@mcp.tool
def geoip_lookup(ip: str) -> dict:
    """
    Perform a GeoIP lookup for the given IP address.

    Args:
        ip (str): The IP address to look up.

    Returns:
        dict: A dictionary containing the GeoIP information.
    """
    if not city_reader:
        return {"error": "GeoIP database reader for city data is not initialized."}
    try:
        response = city_reader.city(ip)
        return response.to_dict()

    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def anonymous_ip_lookup(ip: str) -> dict:
    """
    Check if the given IP address is an anonymous proxy or VPN.

    Args:
        ip (str): The IP address to check.

    Returns:
        dict: A dictionary containing the result of the check.
    """
    if not anonymous_ip_reader:
        return {"error": "Anonymous IP database reader is not initialized."}
    try:
        response = anonymous_ip_reader.anonymous_ip(ip)
        return response.to_dict()

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":

    current_dir = Path(__file__).parent

    anonymous_db_path = os.environ.get(
        "ANONYMOUS_DB_PATH", current_dir / "test-data/GeoIP2-Anonymous-IP-Test.mmdb"
    )
    if os.path.exists(anonymous_db_path):
        anonymous_ip_reader = geoip2.database.Reader(anonymous_db_path)
    else:
        print(
            f"Anonymous IP database not found at {anonymous_db_path}. Skipping anonymous IP lookups."
        )

    city_db_path = os.environ.get(
        "CITY_DB_PATH", current_dir / "test-data/GeoIP2-City-Test.mmdb"
    )
    if os.path.exists(city_db_path):
        city_reader = geoip2.database.Reader(city_db_path)
    else:
        print(f"City database not found at {city_db_path}. Skipping GeoIP lookups.")

    mcp.run()
