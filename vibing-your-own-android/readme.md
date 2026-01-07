# Android Storage Analysis - Phase 1

## 1. Environment Setup (Ubuntu Host)

We prepared the host machine to communicate with the Android device using the Android Debug Bridge (ADB) protocol.

**Commands Executed:**

```bash
sudo apt update
sudo apt install android-tools-adb android-tools-fastboot
```

## 2. Target Device Preparation (Android)

We elevated privileges on the phone to accept remote debugging commands.

**Actions Taken:**

1. **Unlocked Developer Mode:** Settings > About Phone > Tapped "Build Number" 7 times.
2. **Enabled Debugging:** Settings > Developer Options > Toggled "USB Debugging" to ON.
3. **Physical Connection:** Connected via USB and selected "File Transfer / MTP" mode.

## 3. Handshake & Authorization

We established the RSA trust relationship between the Ubuntu PC and the Android Phone.

**Commands Executed:**

```bash
# Start the ADB server and list devices
adb devices
```

**Verification:**

* Accepted the "Allow USB debugging?" RSA fingerprint prompt on the phone screen.
* Confirmed status changed from `unauthorized` to `device`.

**Final Output:**

```text
List of devices attached
awesomedeviceid    device
```

# Android Storage Analysis - Phase 2

Standard Android `diskstats` output varies by manufacturer. For MIUI/Xiaomi devices, the output is often unstructured parallel arrays (JSON-like). We developed a custom Python script to parse this data and correlate package names with their data sizes.

### The Script: `audit_apps.py`

This script executes `dumpsys diskstats`, extracts the parallel lists, and generates a ranked table of storage consumers.

**Usage:**

```bash
python3 audit_apps.py
```

**Key Metrics:**

* **TOTAL:** The physical space the app occupies.
* **DATA (BLOAT):** User-generated data (Databases, Downloads, Internal Media). This is the primary target for cleanup.
* **CACHE:** Temporary files (Safe to clear via Android Settings).


Once a heavy app is identified, we use advanced shell commands to inspect its internal structure.

### Checking "Debuggable" Status

If an app has `android:debuggable="true"` in its manifest (or is a development build), we can access its private data (`/data/data/`) without Root privileges using the `run-as` command.

```bash
adb shell run-as <package_name>
```

### Internal File Inspection

Inside the `run-as` shell, we identify large files or hidden archives:

```bash
# Check folder sizes recursively
du -h -d 1 .

# Find top 10 largest specific files
find . -type f -printf "%s %p\n" | sort -rn | head -n 10
```

### Data Extraction

To analyze databases (SQLite) or suspicious archives on the host machine:

```bash
# Stream the file content directly to the local machine
adb exec-out run-as <package_name> cat path/to/file > local_filename.ext
```