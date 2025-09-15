# TODO: Implement PDF Report Generation Combining JSON and CSV Data

## Tasks

- [x] Import reportlab modules in streamlit_app.py
- [x] Create generate_pdf_report function that:
  - Takes analysis_data and plan as input
  - Creates a PDF with title, predicted crop, date, soil parameters table, and implementation plan
- [x] Add PDF download button in the export section of show_soil_analysis function
- [ ] Test PDF generation by running the app and downloading a sample report

## Notes

- Reportlab is already in requirements.txt
- PDF will combine analysis data (JSON-like) and present parameters in a table format (CSV-like)
- Implementation plan will be included in the PDF
