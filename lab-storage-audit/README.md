# Databricks Lab Storage Audit

This script calculates the **total storage size (in GB)** of each **top-level folder**
under a Databricks DBFS path (for example `/mnt/lab/unrestricted/`).

It is designed for **lab / unmanaged areas** where users freely upload data, and where
storage usage needs to be audited or monitored.

---

## What this script does

- Lists **only the top-level folders** under a given root path
- Recursively scans **all subfolders and files**
- Sums file sizes using DBFS metadata (`dbutils.fs.ls`)
- Produces a **table of folder → total size (GB)**
- Sorts results in **descending size order**
- Uses `display(df)` so results can be **downloaded as CSV from Databricks UI**

---
## Output 

The script outputs a Spark DataFrame displayed using Databricks display().
Each row represents a top-level folder under the configured root path, with the
total size of all files contained within that folder including all subfolders.

Example Output:
The displayed table should look like this:

Folder	                        Size_GB
/mnt/lab/unrestricted/FolderA/	2340.45
/mnt/lab/unrestricted/FolderB/	1876.12
/mnt/lab/unrestricted/FolderC/	1520.78

---

## Requirements

- Databricks Runtime
- Access to the target DBFS mount
- `dbutils` and `spark` available (standard Databricks notebook environment)

---

## How to use

1. Open a Databricks notebook
2. Paste the contents of `folder_size_audit.py` into a cell
3. Update the root directory if needed:

```python
root_dir = "/mnt/lab/unrestricted/"
