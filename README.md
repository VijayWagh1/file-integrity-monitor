# File Integrity Monitor (Ransomware Detection Style)

This is a simple File Integrity Monitor designed to detect potential ransomware attacks by monitoring file changes, sudden modifications, and mass file renaming.

## Features

- **SHA256 Hashing**: Computes SHA256 hashes for all files in the monitored directory.
- **Sudden Changes Detection**: Alerts when files are modified unexpectedly.
- **Mass File Renaming Detection**: Detects when many files are renamed at once, a common ransomware behavior.
- **Alert System**: Currently prints alerts to the console. Can be extended to send emails or other notifications.
- **Configurable**: Uses `config.ini` for settings like monitored path and check interval.

## Structure

```
file-integrity-monitor/
│
├── monitor.py          # Main monitoring script
├── alert.py            # Alert system module
├── config.ini          # Configuration file
├── monitored_dir/      # Example monitored directory (create your own)
│   ├── example1.txt    # Example file
│   └── example2.txt    # Example file
└── README.md           # This file
```

## How It Works

1. The monitor scans the specified directory periodically.
2. Computes SHA256 hashes for all files.
3. Compares with the stored database (created on first run).
4. Detects changes, new files, deletions.
5. Checks for mass renaming by comparing deleted and new file counts and hashes.
6. Updates the database and alerts if anomalies are found.

## Usage

1. Clone or download this repository.
2. Create a directory you want to monitor (e.g., `my_documents`).
3. Edit `config.ini` to set the `path` to your directory and adjust the `interval` in seconds.
4. Run the monitor: `python monitor.py`
5. The monitor will run continuously, checking every `interval` seconds.
6. To stop, press Ctrl+C.

## Configuration

- `path`: Relative or absolute path to the directory to monitor.
- `interval`: Time in seconds between scans (default: 10).

## Extending Alerts

In `alert.py`, you can add email sending or other notification methods. For example, using smtplib for emails.

## Requirements

- Python 3.x
- Standard library only (no external dependencies)

## Note

This is a basic implementation for demonstration. In production, consider permissions, large directories, and more sophisticated detection algorithms. The hash database is created locally and not included in the repository for privacy.