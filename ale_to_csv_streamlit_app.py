import streamlit as st
import csv
import io
import datetime
import os

st.title("🎬 ALE oder Tab-getrennte TXT ➜ CSV Konverter")

uploaded_file = st.file_uploader("Lade eine ALE- oder TXT-Datei hoch", type=["ale", "txt"])

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8").splitlines()

    header = []
    rows = []
    is_ale = False
    start_index = None

    # Prüfe auf ALE-Format
    for i, line in enumerate(content):
        if line.strip() == "Column":
            header = content[i + 1].strip().split('\t')
            is_ale = True
        elif line.strip() == "Data":
            start_index = i + 1
            break

    if is_ale and start_index:
        data_lines = content[start_index + 1:]
        rows = [row.strip().split('\t') for row in data_lines if row.strip()]
    else:
        # Tab-delimited TXT-Fallback
        content = [line for line in content if line.strip()]
        header = content[0].strip().split('\t')
        rows = [line.strip().split('\t') for line in content[1:]]

    if not rows:
        st.error("Keine Datenzeilen gefunden.")
    else:
        # CSV-Inhalt vorbereiten
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(rows)

        # Ursprungsname + _processed_YYMMDD.csv
        base_name = os.path.splitext(uploaded_file.name)[0]
        today_str = datetime.datetime.now().strftime("%y%m%d")
        export_filename = f"{base_name}_processed_{today_str}.csv"

        st.success("✅ Datei erfolgreich konvertiert!")
        st.download_button(
            label="💾 CSV herunterladen",
            data=output.getvalue(),
            file_name=export_filename,
            mime="text/csv"
        )
