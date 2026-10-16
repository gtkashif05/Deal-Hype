import re
import urllib.parse

def clean_amazon_url(raw_url: str, tag: str) -> str:
    """
    Extracts the clean ASIN (Amazon Standard Identification Number)
    and attaches the user's affiliate tag.
    Example: https://www.amazon.in/dp/B0DXPHFMLX?tag=yourtag-21
    """
    if not tag:
        return raw_url

    # Match ASIN like B0XXXXXXXX or 10-digit alphanumeric
    asin_match = re.search(r'(?:/dp/|/gp/product/|/d/|/ASIN/)([A-Z0-9]{10})', raw_url, re.IGNORECASE)
    if asin_match:
        asin = asin_match.group(1).upper()
        return f"https://www.amazon.in/dp/{asin}?tag={tag}"
    
    # Fallback: Parse URL and append/replace tag
    parsed = urllib.parse.urlparse(raw_url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs['tag'] = [tag]
    # Remove unwanted tracking parameters
    for param in ['ascsubtag', 'linkCode', 'ref', 'ref_', 'pf_rd_r', 'pf_rd_m']:
        qs.pop(param, None)
    
    clean_query = urllib.parse.urlencode(qs, doseq=True)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, clean_query, ''))

def clean_flipkart_url(raw_url: str, affid: str) -> str:
    """
    Cleans Flipkart tracking links and attaches user's Flipkart affiliate ID.
    """
    if not affid:
        return raw_url

    parsed = urllib.parse.urlparse(raw_url)
    qs = urllib.parse.parse_qs(parsed.query)
    
    # Strip previous affiliate tracking
    for p in ['affid', 'affExtParam1', 'affExtParam2', '_app_id']:
        qs.pop(p, None)
        
    qs['affid'] = [affid]
    clean_query = urllib.parse.urlencode(qs, doseq=True)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, clean_query, ''))

def convert_to_earnkaro(target_url: str, earnkaro_user_id: str) -> str:
    """
    Converts any store link (Flipkart, Myntra, Ajio, Nykaa, etc.)
    into an EarnKaro profit link with automatic commission routing.
    """
    if not earnkaro_user_id:
        return target_url
    
    encoded_url = urllib.parse.quote(target_url, safe='')
    return f"https://earnkaro.com/deals?r={earnkaro_user_id}&url={encoded_url}"

def build_affiliate_link(store: str, raw_url: str, config) -> str:
    """
    Master router that converts raw product link to affiliate link
    based on store and configured credentials.
    """
    store_lower = store.lower() if store else ""
    
    # If user configured EarnKaro, it can handle multi-store links easily
    if getattr(config, 'EARNKARO_USER_ID', '') and 'amazon' not in store_lower:
        return convert_to_earnkaro(raw_url, config.EARNKARO_USER_ID)
        
    if 'amazon' in store_lower or 'amzn' in raw_url.lower():
        if getattr(config, 'AMAZON_AFFILIATE_TAG', ''):
            return clean_amazon_url(raw_url, config.AMAZON_AFFILIATE_TAG)
            
    elif 'flipkart' in store_lower or 'fkrt' in raw_url.lower():
        if getattr(config, 'FLIPKART_AFFID', ''):
            return clean_flipkart_url(raw_url, config.FLIPKART_AFFID)
            
    return raw_url
