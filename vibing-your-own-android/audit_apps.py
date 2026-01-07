import subprocess
import re
import json

# --- CONFIGURATION ---
MIN_SIZE_MB = 100  # Show apps larger than 100MB

def get_human_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"

def parse_array(key, text):
    """
    Extracts a list from strings like: Key: [val1, val2, val3]
    """
    # Regex to find "Key: [content]"
    pattern = f"{key}: \\[(.*?)\\]"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return []
    
    content = match.group(1)
    # Split by comma, strip whitespace and quotes
    items = [x.strip().strip('"') for x in content.split(',')]
    
    # Handle empty list case
    if len(items) == 1 and items[0] == '':
        return []
        
    return items

def main():
    print("[-] Pulling disk stats from device...")
    try:
        raw_output = subprocess.run(['adb', 'shell', 'dumpsys', 'diskstats'], 
                                  capture_output=True, text=True, check=True).stdout
    except Exception as e:
        print(f"[!] ADB Error: {e}")
        return

    print("[-] Parsing MIUI/Parallel format...")

    # Extract the four parallel lists
    # Note: Using exact keys from your log
    names = parse_array("Package Names", raw_output)
    app_sizes = parse_array("App Sizes", raw_output)
    data_sizes = parse_array("App Data Sizes", raw_output)
    cache_sizes = parse_array("Cache Sizes", raw_output)

    # Validation
    count = len(names)
    if count == 0:
        print("[!] No apps found. The parser didn't match the output format.")
        return

    # Zip them together
    apps = []
    for i in range(count):
        try:
            # Convert sizes to integers (default to 0 if missing/error)
            a_size = int(app_sizes[i]) if i < len(app_sizes) else 0
            d_size = int(data_sizes[i]) if i < len(data_sizes) else 0
            c_size = int(cache_sizes[i]) if i < len(cache_sizes) else 0
            
            total = a_size + d_size + c_size
            
            if total > (MIN_SIZE_MB * 1024 * 1024):
                apps.append({
                    'name': names[i],
                    'total': total,
                    'data': d_size,
                    'cache': c_size
                })
        except (ValueError, IndexError):
            continue

    # Sort by Data Size (User Bloat) because that's what we care about most
    apps.sort(key=lambda x: x['total'], reverse=True)

    print(f"\n{'PACKAGE NAME':<45} | {'TOTAL':<10} | {'DATA (BLOAT)':<12} | {'CACHE':<10}")
    print("-" * 85)
    
    for app in apps:
        print(f"{app['name']:<45} | "
              f"{get_human_size(app['total']):<10} | "
              f"{get_human_size(app['data']):<12} | "
              f"{get_human_size(app['cache']):<10}")

if __name__ == "__main__":
    main()