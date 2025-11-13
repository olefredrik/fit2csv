# fit2csv macOS App – Build Instructions

This document explains how to build the macOS `.app` version of **fit2csv**, including how to embed the Python script and bundle all required Python dependencies so the app works out-of-the-box for users (no Terminal, no pip install needed).

The goal:
A **fully self-contained macOS app** that can convert `.FIT` → `.CSV` without requiring users to install anything.

---

# 📦 1. Overview of the App Structure

The final app bundle should look like this:

```
fit2csv.app
  Contents/
    Info.plist
    MacOS/
    Resources/
      fit2csv_batch.py
      python_deps/
        fitdecode/
        fitdecode-0.11.0.dist-info/
        bin/
      icon.icns
```

- `fit2csv_batch.py` → The real converter logic
- `python_deps/` → All Python packages bundled locally
- `icon.icns` → Custom app icon
- `Info.plist` → Metadata and icon settings
- Automator → Provides a simple macOS GUI wrapper

---

# 🧰 2. Build Process Overview

To create a fresh bundled macOS app:

1. Open/modify the Automator workflow
2. **Save** the app (this always wipes the Resources folder)
3. Re-add:
   - `fit2csv_batch.py`
   - `python_deps/`
   - `icon.icns`
4. Update AppleScript to use the bundled Python dependencies
5. Test the app on a clean system

---

# 🧩 3. Preparing Python Dependencies (fitdecode)

These dependencies must **NOT** be committed to Git.  
They are build artefacts and belong only inside the final `.app` bundle.

Install dependencies locally using:

```bash
mkdir -p python_deps
python3 -m pip install --target ./python_deps fitdecode==0.11.0
```

This creates:

```
python_deps/
  bin/
  fitdecode/
  fitdecode-0.11.0.dist-info/
```

Later, copy this folder into:

```
fit2csv.app/Contents/Resources/python_deps/
```

---

# 🖼 4. Adding the App Icon

Place your `.icns` file here:

```
fit2csv.app/Contents/Resources/icon.icns
```

Add/update `Info.plist`:

```xml
<key>CFBundleIconFile</key>
<string>icon.icns</string>
```

If the icon does not update:

```bash
killall Finder
killall Dock
```

---

# 📝 5. Updating the AppleScript

After saving in Automator, ensure Run AppleScript contains:

```applescript
on run {input, parameters}

    -- Select folder containing FIT files
    set inputFolder to choose folder with prompt "Select the folder that contains your FIT files"

    -- Select output folder (fallback to default)
    try
        set outputFolder to choose folder with prompt "Select output folder for CSV files"
        set useDefaultOutput to false
    on error
        set useDefaultOutput to true
    end try

    set inputPath to POSIX path of inputFolder

    if useDefaultOutput then
        set outputPath to inputPath & "csv_out/"
    else
        set outputPath to POSIX path of outputFolder
    end if

    -- Embedded script + dependencies
    set appPath to POSIX path of (path to me)
    set scriptPath to appPath & "Contents/Resources/fit2csv_batch.py"
    set depsPath to appPath & "Contents/Resources/python_deps"

    -- Build command using bundled dependencies
    set cmd to "PYTHONPATH=" & quoted form of depsPath & " /usr/bin/env python3 " & quoted form of scriptPath & " " & quoted form of inputPath & " --out " & quoted form of outputPath

    try
        do shell script cmd
    on error errMsg number errNum
        display dialog "Conversion failed:" & return & errMsg buttons {"OK"} default button 1 with title "FIT to CSV"
        return input
    end try

    display notification "Conversion finished" with title "FIT to CSV"
    do shell script "open " & quoted form of outputPath

    return input
end run
```

---

# 📥 6. Copy Resources AFTER Saving the Automator App

🚨 Important:  
Automator **deletes the Resources folder every time you save the app**.

Correct order:

### 1. Open app in Automator

### 2. Modify AppleScript

### 3. Save the app

### 4. Re-add manually:

```
fit2csv_batch.py
python_deps/
icon.icns
```

---

# 🧪 7. Testing the Self-Contained App

To ensure bundling works:

1. Create a new macOS user
2. Log in
3. Make sure no `pip install fitdecode` was done
4. Launch the app
5. Convert some `.FIT` files

If it works — bundling is correct.

---

# 🚀 8. Packaging a Release

After confirming everything:

1. Right-click `fit2csv.app` → **Compress**
2. Rename to:

```
fit2csv-macos-v0.4.0.zip
```

3. Upload to GitHub Releases

---

# ❌ 9. What NOT to Commit to Git

Add to `.gitignore`:

```
python_deps/
*.app
*.zip
```

These are build artefacts only.

---

# 🎉 Done

Your macOS app is now fully self-contained and requires **no Python setup** from users.
