from fastmcp import FastMCP
from enum import Enum
import geoip2.database
import os
from pathlib import Path


class Database(Enum):
    GEOIP2_ANONYMOUS_IP_TEST = "GeoIP2-Anonymous-IP-Test.json"
    GEOIP2_CONNECTION_TYPE_TEST = "GeoIP2-Connection-Type-Test.json"
    GEOIP2_DENSITY_INCOME_TEST = "GeoIP2-DensityIncome-Test.json"
    GEOIP2_ENTERPRISE_TEST = "GeoIP2-Enterprise-Test.json"
    GEOIP2_ISP_TEST = "GeoIP2-ISP-Test.json"
    GEOIP2_PRECISION_ENTERPRISE_TEST = "GeoIP2-Precision-Enterprise-Test.json"
    GEOIP2_USER_COUNT_TEST = "GeoIP2-User-Count-Test.json"
    GEOLITE2_ASN_TEST = "GeoLite2-ASN-Test.json"
    GEOLITE2_COUNTRY_TEST = "GeoLite2-Country-Test.json"
    GEOIP2_CITY_TEST = "GeoIP2-City-Test.json"
    GEOIP2_COUNTRY_TEST = "GeoIP2-Country-Test.json"
    GEOIP2_DOMAIN_TEST = "GeoIP2-Domain-Test.json"
    GEOIP2_IP_RISK_TEST = "GeoIP2-IP-Risk-Test.json"
    GEOIP2_PRECISION_ENTERPRISE_SANDBOX_TEST = (
        "GeoIP2-Precision-Enterprise-Sandbox-Test.json"
    )
    GEOIP2_STATIC_IP_SCORE_TEST = "GeoIP2-Static-IP-Score-Test.json"
    GEOIP_ANONYMOUS_PLUS_TEST = "GeoIP-Anonymous-Plus-Test.json"
    GEOLITE2_CITY_TEST = "GeoLite2-City-Test.json"


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


@mcp.tool
def list_databases() -> list:
    """
    List all available GeoIP databases.

    Returns:
        list: A list of available database names.
    """
    return [db.value for db in Database]


@mcp.tool
def reverse_country_lookup(country_code: str, database: Database) -> dict:
    """
    Perform a reverse country lookup for the given country code using the specified database.

    Args:
        country_code (str): The country code to look up.
        database (Database): The database to use for the lookup. Should be one of the values from the Database enum.

    Returns:
        dict: A dictionary containing the IP ranges associated with the country code.
    """
    source_data_path = Path(__file__).parent / "source-data" / database.value

    try:
        with open(source_data_path, "r") as f:
            import json

            data = json.load(f)

        ip_ranges = []
        for record in data:
            for ip_range, details in record.items():
                if details.get("country", {}).get("iso_code") == country_code:
                    ip_ranges.append(ip_range)

        return {
            "database": database.value,
            "country_code": country_code,
            "ip_ranges": ip_ranges,
        }

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
