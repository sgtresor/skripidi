import subprocess

# CONFIGURATION
TARGET_DIR = "/sdcard/Android/data/com.miui.gallery/files/gallery_disk_cache"
TOP_N = 50

def get_human_size(kb_val):
    """Converts KB to MB/GB"""
    if kb_val < 1024:
        return f"{kb_val} KB"
    mb_val = kb_val / 1024
    if mb_val < 1024:
        return f"{mb_val:.2f} MB"
    return f"{mb_val/1024:.2f} GB"

def main():
    print(f"[-] Scanning ALL files in: {TARGET_DIR}")
    print(f"[-] This might take 10-20 seconds to list everything...")

    # We use 'du -k' (disk usage in Kilobytes) for every file.
    # This is faster than 'ls -l' and easier to sort.
    cmd = f'adb shell "find {TARGET_DIR} -type f -exec du -k {{}} +"'
    
    try:
        # Increase buffer limit for massive output
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        
        if not output:
            print("[!] No files found or permission denied.")
            return

        file_list = []
        
        # Parse the output: "1234   /path/to/file"
        for line in output.split('\n'):
            parts = line.split('\t') # du output usually tab-separated
            if len(parts) < 2:
                parts = line.split() # fallback to spaces
            
            if len(parts) >= 2:
                try:
                    size_kb = int(parts[0])
                    path = parts[1]
                    file_list.append((size_kb, path))
                except ValueError:
                    continue

        # Sort by Size (Descending)
        file_list.sort(key=lambda x: x[0], reverse=True)

        print("-" * 100)
        print(f"{'SIZE':<15} | {'FILENAME'}")
        print("-" * 100)
        
        for i, (size_kb, path) in enumerate(file_list[:TOP_N]):
            # Shorten path for readability
            short_name = path.replace(TARGET_DIR, "...")
            print(f"{get_human_size(size_kb):<15} | {short_name}")

    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()