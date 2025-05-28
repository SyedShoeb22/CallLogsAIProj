import os
import re
import shutil
from pathlib import Path
import calendar

def organize_call_recordings(source_dir, destination_base="."):
    source_dir = Path(source_dir)
    destination_base = Path(destination_base)
    destination_base.mkdir(parents=True, exist_ok=True)

    for file in source_dir.glob("Call recording *.m4a"):
        filename = file.name.replace("Call recording ", "", 1)

        # Extract date part from filename
        match = re.search(r"_(\d{6})_", filename)
        if not match:
            print(f"Skipping file due to invalid format: {filename}")
            continue

        date_str = match.group(1)  # e.g., "250420"
        year = "20" + date_str[:2]
        month_num = int(date_str[2:4])
        month_name = calendar.month_abbr[month_num]
        month_folder = f"{month_name}_{year}"

        # Extract caller name or number (before date part)
        caller = filename.split(f"_{date_str}_")[0].replace("+91", "").strip()

        # Create destination folder
        destination_folder = destination_base / caller / month_folder
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Move file
        new_file_path = destination_folder / filename
        shutil.move(str(file), new_file_path)

        print(f"Moved: {file.name} -> {new_file_path}")

# Example usage:
organize_call_recordings("CallRecs", "organized_calls")
