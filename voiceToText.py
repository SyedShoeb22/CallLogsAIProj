import os
import shutil
from datetime import datetime
import subprocess

source_folder = r"/data/data/com.termux/files/home/downloads"
destination_base = r"/data/data/com.termux/files/home/downloads/CallrecProj"

def organize_recordings():
    os.makedirs(destination_base, exist_ok=True)

    for file in os.listdir(source_folder):
        if file.endswith(".m4a") and file.startswith("Call recording"):
            # Remove prefix and extension
            filename = file.replace("Call recording ", "").replace(".m4a", "")

            # filename = "DIM Ujjwal Porwal_250420_152358"
            parts = filename.rsplit("_", 2)
            if len(parts) < 3:
                print(f"Skipping: {file} (invalid format)")
                continue

            name_part, date_part, time_part = parts
            try:
                date_obj = datetime.strptime(date_part, "%d%m%y")
            except ValueError as e:
                print(f"Skipping {file}: invalid date format → {e}")
                continue

            month_folder = date_obj.strftime("%b_%Y").lower()
            person = name_part.strip().replace("+91", "").replace(" ", "_")
            dest_folder = os.path.join(destination_base, person, month_folder)

            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy(os.path.join(source_folder, file), os.path.join(dest_folder, file))
            print(f"Copied: {file} → {dest_folder}")

def upload_to_drive():
    subprocess.run([
        "rclone", "copy", destination_base, "gdrive:CallRecordings", "--create-empty-src-dirs"
    ])

organize_recordings()
upload_to_drive()
