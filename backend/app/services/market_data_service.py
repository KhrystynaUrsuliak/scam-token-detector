import requests
import os
from typing import Optional, Dict, Any, List


COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

def _headers():
    api_key = os.getenv("COINGECKO_API_KEY")
    if api_key:
        return {"x-cg-demo-api-key": api_key}
    return {}


def _clean_text(text: Optional[str], max_length: int = 500) -> Optional[str]:
    if not text:
        return None

    # CoinGecko descriptions sometimes contain HTML tags.
    text = text.replace("\r", " ").replace("\n", " ")
    text = text.replace("<p>", "").replace("</p>", "")
    text = text.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")

    if len(text) > max_length:
        return text[:max_length].strip() + "..."

    return text.strip()


def search_coin_id(name: str, slug: str) -> Optional[str]:
    """
    Search CoinGecko coin id by token name or slug.
    Example: Bitcoin -> bitcoin.
    """

    try:
        query = name or slug

        response = requests.get(
            f"{COINGECKO_BASE_URL}/search",
            params={"query": query},
            headers=_headers(),
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()
        coins = data.get("coins", [])

        if not coins:
            return None

        # Prefer exact id/name/symbol match.
        normalized_name = (name or "").lower().strip()
        normalized_slug = (slug or "").lower().strip()

        for coin in coins:
            coin_id = coin.get("id", "").lower()
            coin_name = coin.get("name", "").lower()
            coin_symbol = coin.get("symbol", "").lower()

            if (
                coin_id == normalized_slug
                or coin_name == normalized_name
                or coin_symbol == normalized_slug
            ):
                return coin.get("id")

        # Otherwise return first result.
        return coins[0].get("id")

    except requests.RequestException:
        return None


def get_coin_info(coin_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch token metadata and market data from CoinGecko.
    """

    try:
        response = requests.get(
            f"{COINGECKO_BASE_URL}/coins/{coin_id}",
            params={
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false"
            },
            headers=_headers(),
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        market_data = data.get("market_data", {}) or {}
        links = data.get("links", {}) or {}

        homepage = None
        homepage_list = links.get("homepage") or []
        if homepage_list and homepage_list[0]:
            homepage = homepage_list[0]

        return {
            "coin_id": data.get("id"),
            "name": data.get("name"),
            "symbol": (data.get("symbol") or "").upper(),
            "image": (data.get("image") or {}).get("large"),
            "description": _clean_text((data.get("description") or {}).get("en")),
            "homepage": homepage,
            "current_price_usd": (market_data.get("current_price") or {}).get("usd"),
            "market_cap_usd": (market_data.get("market_cap") or {}).get("usd"),
            "volume_24h_usd": (market_data.get("total_volume") or {}).get("usd"),
            "price_change_24h_percent": market_data.get("price_change_percentage_24h"),
            "market_cap_rank": data.get("market_cap_rank"),
        }

    except requests.RequestException:
        return None


def get_market_chart(coin_id: str, days: int = 7) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch price chart data from CoinGecko.
    Returns list of {timestamp, price}.
    """

    try:
        response = requests.get(
            f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart",
            params={
                "vs_currency": "usd",
                "days": days
            },
            headers=_headers(),
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()
        prices = data.get("prices", [])

        return [
            {
                "timestamp": item[0],
                "price": item[1]
            }
            for item in prices
        ]

    except requests.RequestException:
        return None


def get_token_market_data(name: str, slug: str, include_chart: bool = True) -> Optional[Dict[str, Any]]:
    """
    Main helper used by /predict.
    """

    coin_id = search_coin_id(name=name, slug=slug)

    if not coin_id:
        return None

    info = get_coin_info(coin_id)

    if not info:
        return None

    if include_chart:
        info["chart_7d"] = get_market_chart(coin_id, days=7)
    else:
        info["chart_7d"] = None

    return info