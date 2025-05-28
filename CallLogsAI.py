import os
import re
from pathlib import Path

def process_call_logs(file_path, base_dir="."):
    # Ensure base path exists
    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("Call recording "):
                continue
            
            # Remove "Call recording " prefix
            raw_name = line.replace("Call recording ", "", 1)

            # Extract date info using regex
            match = re.search(r"_\d{6}_", raw_name)
            if not match:
                print(f"Skipping invalid format: {raw_name}")
                continue

            date_part = match.group(0).strip("_")  # e.g. 250420
            month = date_part[2:4]  # Extract month (MM)

            # Extract caller (before date part)
            caller = raw_name.split(f"_{date_part}_")[0]

            # Remove +91 if present
            caller = caller.replace("+91", "").strip()

            # Construct folder paths
            caller_folder = base_dir / caller
            month_folder = caller_folder / f"Month_{month}"

            # Make directories
            month_folder.mkdir(parents=True, exist_ok=True)

            # Simulate file placement (you could move or create a dummy file if needed)
            print(f"Would place '{raw_name}' in '{month_folder}'")

# Example usage
process_call_logs("calllogs.txt", "output_calls")
