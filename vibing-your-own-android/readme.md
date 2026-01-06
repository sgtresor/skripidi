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