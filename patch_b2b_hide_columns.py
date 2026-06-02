"""
patch_b2b_hide_columns.py
=========================
Patch B2b: Hide kolom yang tidak perlu di setiap sheet Excel.

Sheet 1 PSList  : hide Handles, __children, File output
Sheet 2 PSTree  : hide Handles, __children
Sheet 3 NetScan : hide __children
Sheet 4 Malfind : hide __children

Cara pakai:
  python3 ~/forensic_triase/platform/patch_b2b_hide_columns.py
"""

from pathlib import Path
import shutil

BASE     = Path.home() / "forensic_triase/platform"
REPORTER = BASE / "core/reporter.py"

# Kolom yang di-hide per sheet (nama kolom persis dari Volatility3)
HIDE_COLUMNS = {
    "PSList":  {"Handles", "__children", "File output"},
    "PSTree":  {"Handles", "__children"},
    "NetScan": {"__children"},
    "Malfind": {"__children"},
}

OLD_WRITE_PLUGIN = '''def _write_plugin_sheet(ws, records: list, sheet_title: str):
    """Tulis data plugin mentah ke worksheet."""
    ws.title = sheet_title

    if not records:
        ws.append(["(Tidak ada data)"])
        return

    # Ambil semua kolom dari record pertama
    headers = list(records[0].keys())
    ws.append(headers)
    _style_header(ws)

    for rec in records:
        row = [str(rec.get(h, "")) for h in headers]
        ws.append(row)

    _auto_width(ws)
    ws.freeze_panes = "A2"'''

NEW_WRITE_PLUGIN = '''# Kolom yang di-hide per sheet
HIDE_COLUMNS = {
    "PSList":  {"Handles", "__children", "File output"},
    "PSTree":  {"Handles", "__children"},
    "NetScan": {"__children"},
    "Malfind": {"__children"},
}


def _write_plugin_sheet(ws, records: list, sheet_title: str):
    """Tulis data plugin mentah ke worksheet, hide kolom yang tidak perlu."""
    ws.title = sheet_title

    if not records:
        ws.append(["(Tidak ada data)"])
        return

    # Ambil semua kolom dari record pertama
    headers = list(records[0].keys())
    ws.append(headers)
    _style_header(ws)

    for rec in records:
        row = [str(rec.get(h, "")) for h in headers]
        ws.append(row)

    _auto_width(ws)
    ws.freeze_panes = "A2"

    # Hide kolom yang tidak perlu
    hidden = HIDE_COLUMNS.get(sheet_title, set())
    for col_idx, header in enumerate(headers, start=1):
        if header in hidden:
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].hidden = True'''

# ---------------------------------------------------------------------------
# Jalankan patch
# ---------------------------------------------------------------------------

print("\\n" + "=" * 60)
print("  PATCH B2b: Hide Kolom Excel")
print("=" * 60)

shutil.copy(REPORTER, str(REPORTER) + ".bak2b")
content = REPORTER.read_text(encoding="utf-8")

if OLD_WRITE_PLUGIN not in content:
    print("  [!] GAGAL — string tidak ditemukan. Cek reporter.py.")
else:
    content = content.replace(OLD_WRITE_PLUGIN, NEW_WRITE_PLUGIN, 1)
    REPORTER.write_text(content, encoding="utf-8")
    print("  [✓] Patch berhasil")

print("\\n  Test:")
print("  python3 ~/forensic_triase/platform/main.py /mnt/d/forensic_triase/dataset/infected_rogue.raw")
print("=" * 60 + "\\n")