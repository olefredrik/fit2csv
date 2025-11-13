# macOS Automator App – Build Instructions (Updated)

This guide explains how to build the standalone macOS Automator application that wraps the `fit2csv_batch.py` script and includes the custom duotone runner icon.

It covers:

- Creating the Automator .app
- Embedding the Python script
- Adding and configuring the custom `.icns` icon
- Handling macOS icon caching
- Troubleshooting common issues

---

# 📁 Repository Structure (relevant parts)

```
mac-app/
    README_APP.md
    icon.icns                 # Final macOS application icon
src/
    fit2csv_batch.py          # Python conversion script
```

---

# 🧱 1. Create a New Automator Application

1. Open **Automator.app**
2. Select **New Document**
3. Choose **Application**
4. In the search field, locate **Run AppleScript**
5. Drag **Run AppleScript** into the workflow
6. Replace the default script with:

```applescript
on run {input, parameters}

    -- Ask user to select the folder containing FIT files
    set inputFolder to choose folder with prompt "Select the folder that contains your FIT files"

    -- Ask user to select output folder; if cancelled, use default csv_out folder
    try
        set outputFolder to choose folder with prompt "Select output folder for CSV files"
        set useDefaultOutput to false
    on error
        -- User cancelled the dialog, so we use default output inside input folder
        set useDefaultOutput to true
    end try

    -- Convert input folder to POSIX path (string)
    set inputPath to POSIX path of inputFolder

    if useDefaultOutput then
        -- Default output folder inside input folder
        set outputPath to inputPath & "csv_out/"
    else
        set outputPath to POSIX path of outputFolder
    end if

    -- Determine the app's path and locate the embedded Python script
    set appPath to POSIX path of (path to me)
    set scriptPath to appPath & "Contents/Resources/fit2csv_batch.py"

    -- Build shell command to run Python script
    set cmd to "/usr/bin/env python3 " & quoted form of scriptPath & " " & quoted form of inputPath & " --out " & quoted form of outputPath

    try
        do shell script cmd
    on error errMsg number errNum
        display dialog "Conversion failed:" & return & errMsg buttons {"OK"} default button 1 with title "FIT to CSV"
        return input
    end try

    -- macOS notification
    display notification "Conversion finished" with title "FIT to CSV"

    -- Open output folder
    do shell script "open " & quoted form of outputPath

    return input
end run
```

7. Save the app, for example:

```
fit2csv.app
```

---

# 📦 2. Embed the Python Script

1. Right-click the saved app → **Show Package Contents**
2. Navigate to:

```
Contents/Resources/
```

3. Copy:

```
src/fit2csv_batch.py
```

into that folder.

Your structure should look like:

```
fit2csv.app/
    Contents/
        Resources/
            fit2csv_batch.py
```

This makes the app fully standalone.

---

# 🎨 3. Add the Custom App Icon

The repository contains:

```
mac-app/icon.icns
```

To apply it:

1. Place `icon.icns` into:

```
fit2csv.app/Contents/Resources/icon.icns
```

2. Open:

```
fit2csv.app/Contents/Info.plist
```

3. Ensure:

```xml
<key>CFBundleIconFile</key>
<string>icon.icns</string>
```

## ⚠️ Important: Handle CFBundleIconName

If this key exists:

```xml
<key>CFBundleIconName</key>
<string>ApplicationStub</string>
```

Then macOS will ignore your `icon.icns` and use the Automator default icon.

You must either:

### Option A (Recommended) — Change value:

```xml
<key>CFBundleIconName</key>
<string>icon</string>
```

### Option B — Remove the key entirely

Both will allow macOS to use your custom icon.

---

# 🧹 4. Remove “Get Info” Icon Overrides

If you ever manually copied an icon onto the app using **Get Info**, macOS _overrides_ the bundle icon.

To remove it:

1. Right-click the app → **Get Info**
2. Click the small icon top-left
3. Press **Delete**
4. Close the window

---

# 🔄 5. Refresh macOS Icon Cache

macOS heavily caches icons.

If your icon does not update immediately, run:

```bash
killall Finder
killall Dock
```

Or log out and back in.

---

# 🧪 6. Test the App

- Double-click the app
- Select input folder with `.FIT` files
- Select (or skip) output folder
- Verify:
  - Conversion works
  - Output folder opens
  - Notification appears
  - Custom icon is visible in Finder

---

# 📤 7. Distribute the Application

1. Right-click `fit2csv.app` → **Compress "fit2csv.app"**
2. Upload the ZIP as a Release asset on GitHub
3. Recommended naming:

```
fit2csv-macos-vX.Y.Z.zip
```

---

# 🛠 Requirements for End Users

They must have:

- Python 3 installed
- `fitdecode` installed:

```bash
pip install fitdecode
```

---

# ✔️ Done!

You now have a fully configured macOS GUI app with:

- embedded Python logic
- folder selection
- notifications
- automatic output folder creation
- a polished custom icon

Perfect for distributing in GitHub Releases.
