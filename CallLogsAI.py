import os
import re
import shutil
from pathlib import Path

def organize_call_recordings(source_dir, target_dir="."):
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    for file in source_dir.iterdir():
        if not file.name.lower().startswith("call recording") or not file.name.endswith(".m4a"):
            continue

        # Remove "Call recording " prefix
        raw_name = file.name.replace("Call recording ", "", 1)

        # Match date pattern _YYMMDD_
        match = re.search(r"_(\d{6})_", raw_name)
        if not match:
            print(f"Skipping file with invalid format: {file.name}")
            continue

        date_part = match.group(1)  # e.g., 250420
        month = date_part[2:4]      # Extract MM

        # Extract caller name/number
        caller = raw_name.split(f"_{date_part}_")[0]
        caller = caller.replace("+91", "").strip()

        # Build target path
        caller_folder = target_dir / caller
        month_folder = caller_folder / f"Month_{month}"
        month_folder.mkdir(parents=True, exist_ok=True)

        # New filename without "Call recording "
        new_filename = raw_name

        # Move the file
        shutil.move(str(file), month_folder / new_filename)
        print(f"Moved: {file.name} -> {month_folder / new_filename}")

organize_call_recordings("recordings_folder", "organized_calls")
