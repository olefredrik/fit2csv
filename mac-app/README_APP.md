# macOS Automator App Instructions

This document explains how to build the standalone macOS Automator application
that wraps the `fit2csv_batch.py` script.

The Automator app provides:
- GUI folder selection
- Automatic output folder creation
- Notification when conversion finishes
- Automatic opening of the output folder
- Bundled Python script inside the `.app`

---

## 📁 Folder Structure

Place the Automator app inside the `mac-app` folder:

```
mac-app/
    README_APP.md
    (your .app will NOT be stored in the git repo)
```

Instead of committing the `.app` package, upload it as a ZIP file in **GitHub Releases**.

---

## 🛠 How to Build the macOS App

### 1. Open Automator

- Open **Automator.app**
- Select **New Document**
- Choose **Application**

### 2. Add “Run AppleScript”

In Automator:
- Search for **Run AppleScript**
- Drag it into the workflow area

Delete everything in the script window and paste the following AppleScript:

```applescript
on run {input, parameters}

    -- Ask user to select the folder containing FIT files
    set inputFolder to choose folder with prompt "Select the folder that contains your FIT files"

    -- Ask user to select output folder; if cancelled, use default csv_out folder
    try
        set outputFolder to choose folder with prompt "Select output folder for CSV files"
        set useDefaultOutput to false
    on error
        -- User cancelled the dialog, so we use default output under input folder
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

    -- Build the shell command to run Python script
    set cmd to "/usr/bin/env python3 " & quoted form of scriptPath & " " & quoted form of inputPath & " --out " & quoted form of outputPath

    -- Run the conversion, with simple error handling
    try
        do shell script cmd
    on error errMsg number errNum
        display dialog "Conversion failed:" & return & errMsg buttons {"OK"} default button 1 with title "FIT to CSV"
        return input
    end try

    -- Show macOS notification after finishing
    display notification "Conversion finished" with title "FIT to CSV"

    -- Open output folder in Finder using the 'open' command
    do shell script "open " & quoted form of outputPath

    return input
end run
```

---

## 📦 Embed the Python Script Inside the `.app`

1. Save the Automator application:
   - **File → Save**
   - Choose a name, e.g. `fit2csv.app`

2. Right‑click the new `.app` → **Show Package Contents**

3. Create a folder:
```
Contents/Resources/
```

4. Copy the Python script:
```
src/fit2csv_batch.py
```

Into:

```
fit2csv.app/Contents/Resources/fit2csv_batch.py
```

The app will now work *stand‑alone*.

---

## 🚀 Running the App

Double-click the app:

1. Select the folder containing `.fit` files  
2. Select output folder  
   - or press “Cancel” to auto‑use `csv_out`  
3. Wait for “Conversion finished” notification  
4. Output folder opens automatically

---

## 📤 Publishing the App

Do **not** commit the `.app` bundle to the Git repository.

Instead:

1. Compress it:
   - Right‑click → **Compress "fit2csv.app"**
2. Upload the ZIP file in GitHub under:
   **Releases → Draft a new Release**

Users can then download the latest `.app` from Releases.

---

## 🧪 Troubleshooting

### macOS says:
> “App can’t be opened because the developer cannot be verified”

Right‑click the app → **Open** → **Open**  
This must be done once.

### Python not found

Ensure Python 3 is available on the system:
```
python3 --version
```

### Missing dependencies

Install:
```
pip install fitdecode
```

---

## ✔️ Done!

Your macOS Automator app is now fully portable and ready for open‑source distribution.

