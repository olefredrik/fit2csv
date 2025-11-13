# macOS Automator App – Build Instructions

This guide explains how to build the standalone macOS Automator application that wraps the `fit2csv_batch.py` script and includes a custom app icon.

The Automator app provides:

- A simple macOS GUI for selecting input and output folders
- Batch conversion of `.FIT` files to `.CSV`
- Automatic creation of a `csv_out` folder if needed
- macOS notification on completion
- Automatic opening of output folder
- A bundled Python script
- A custom macOS `.icns` application icon

---

## 📁 Repository Structure (relevant parts)

```
mac-app/
    README_APP.md
    icon.icns             # App icon (ready to use)
src/
    fit2csv_batch.py      # Python conversion script
```

---

# 🧱 1. Create a New Automator Application

1. Open **Automator.app**
2. Choose **New Document**
3. Select **Application**
4. In the search field, find **Run AppleScript**
5. Drag **Run AppleScript** into the workflow area
6. Delete everything in the AppleScript window and replace it with the script below:

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

    -- Determine the app's own path and locate the embedded Python script
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

7. Save the app, for example as:

```
fit2csv.app
```

---

# 📦 2. Embed the Python Script

1. Right‑click the newly created app → **Show Package Contents**
2. Navigate to:

```
Contents/Resources/
```

3. Copy:

```
src/fit2csv_batch.py
```

into this folder.

Your structure should now look like:

```
fit2csv.app/
    Contents/
        Resources/
            fit2csv_batch.py
```

This makes the app fully standalone.

---

# 🎨 3. Add the Custom App Icon

The repository includes a ready-made macOS application icon:

```
mac-app/icon.icns
```

To use it:

1. Copy `icon.icns` into:

```
fit2csv.app/Contents/Resources/icon.icns
```

2. Open:

```
fit2csv.app/Contents/Info.plist
```

3. Add (or update):

```xml
<key>CFBundleIconFile</key>
<string>icon.icns</string>
```

4. Save the file.

If the icon does not appear right away, refresh Finder:

```bash
killall Finder
```

(or simply rename the app temporarily and rename it back).

---

# 🚀 4. Test the App

Double‑click `fit2csv.app` and verify:

- Folder selection dialogs work
- Conversion runs correctly
- Notification appears
- Output folder opens
- Icon appears in Finder and Dock

If everything works, the app is ready for packaging.

---

# 📤 5. Distribute the Application

To ship your app:

1. Right‑click `fit2csv.app` → **Compress**
2. Upload the resulting ZIP file as a Release asset on GitHub
3. Name it:

```
fit2csv-macos-vX.Y.Z.zip
```

(where X.Y.Z is your release version)

Users can now download and run the app without building it manually.

---

# 🛠 Requirements

Users must have:

- Python 3 installed
- `fitdecode` installed:

```bash
pip install fitdecode
```

---

# 📝 Notes for Advanced Users

- The `.app` is not committed to the repository  
  → Keeping binaries out of Git is best practice
- Instead, releases contain ZIP files of the compiled app
- Developers cloning the repo can rebuild the app using this guide

---

# ✔️ Done!

You now have a full macOS GUI app that bundles the Python converter and uses a custom icon.

Happy shipping!
