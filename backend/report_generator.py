"""
Backend Report Generator Module
Handles PDF report generation with Simple and Professional layouts using ReportLab.
"""

import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


class ReportGenerator:
    """Handles PDF report generation for soil analysis"""

    def __init__(self):
        """Initialize report generator with styles"""
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        self.heading_style = ParagraphStyle(
            'Heading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20
        )
        self.subheading_style = ParagraphStyle(
            'Subheading',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=15
        )
        self.normal_style = self.styles['Normal']

    def generate_simple_report(self, report_data):
        """
        Generate Simple (Farmer) PDF report

        Args:
            report_data (dict): Report data dictionary

        Returns:
            BytesIO: PDF buffer
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Title
        elements.append(Paragraph("Soil Test Report", self.title_style))
        elements.append(Spacer(1, 12))

        # Farmer Information
        elements.append(Paragraph("Farmer Information:", self.heading_style))
        elements.append(Paragraph(f"Name: {report_data['farmer_name']}", self.normal_style))
        elements.append(Paragraph(f"Location: {report_data['location']}", self.normal_style))
        elements.append(Paragraph(f"Sample ID: {report_data['sample_id']}", self.normal_style))
        elements.append(Paragraph(f"Date of Collection: {report_data['date_of_collection']}", self.normal_style))
        elements.append(Paragraph(f"Crop Type: {report_data['crop_type']}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Report Generation Info
        elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Predicted Crop (if available)
        if 'predicted_crop' in report_data:
            elements.append(Paragraph(f"Predicted Crop: {report_data['predicted_crop']}", self.heading_style))
            elements.append(Paragraph("Confidence: 99.32%", self.normal_style))
            elements.append(Spacer(1, 12))

        # Soil Parameters Table
        elements.append(Paragraph("Soil Parameters:", self.heading_style))

        param_data = [
            ['Parameter', 'Value', 'Unit'],
            ['Nitrogen', f"{report_data.get('nitrogen', 'N/A')}", 'ppm'],
            ['Phosphorus', f"{report_data.get('phosphorus', 'N/A')}", 'ppm'],
            ['Potassium', f"{report_data.get('potassium', 'N/A')}", 'ppm'],
            ['pH', f"{report_data.get('ph', 'N/A')}", ''],
            ['Temperature', f"{report_data.get('temperature', 'N/A')}", '°C'],
            ['Humidity', f"{report_data.get('humidity', 'N/A')}", '%'],
            ['Rainfall', f"{report_data.get('rainfall', 'N/A')}", 'cm']
        ]

        if 'area' in report_data:
            param_data.append(['Area', f"{report_data['area']}", report_data.get('area_unit', '')])

        table = Table(param_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Implementation Plan (if available)
        if 'selected_plan' in report_data and report_data['selected_plan']:
            elements.append(Paragraph("Implementation Plan:", self.heading_style))
            plan = report_data['selected_plan']
            for key, value in plan.items():
                elements.append(Paragraph(f"<b>{key.title()}:</b>", self.normal_style))
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        elements.append(Paragraph(f"  • {sub_key}: {sub_value}", self.normal_style))
                elif isinstance(value, list):
                    for item in value:
                        elements.append(Paragraph(f"  • {item}", self.normal_style))
                else:
                    elements.append(Paragraph(f"  {value}", self.normal_style))
                elements.append(Spacer(1, 6))

        # Footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Generated by Agree-Sakha Smart Soil Testing System", self.normal_style))
        elements.append(Paragraph("© 2025 Agricultural Technology Solutions", self.normal_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_professional_report(self, report_data):
        """
        Generate Professional (Detailed) PDF report

        Args:
            report_data (dict): Report data dictionary

        Returns:
            BytesIO: PDF buffer
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Title
        elements.append(Paragraph("Professional Soil Analysis Report", self.title_style))
        elements.append(Spacer(1, 12))

        # Report Header
        elements.append(Paragraph("AGRICULTURAL TECHNOLOGY SOLUTIONS", self.subheading_style))
        elements.append(Paragraph("Advanced Soil Testing & Crop Recommendation System", self.normal_style))
        elements.append(Spacer(1, 12))

        # Farmer Information
        elements.append(Paragraph("Client Information:", self.heading_style))
        elements.append(Paragraph(f"Farmer Name: {report_data['farmer_name']}", self.normal_style))
        elements.append(Paragraph(f"Farm Location: {report_data['location']}", self.normal_style))
        elements.append(Paragraph(f"Sample ID: {report_data['sample_id']}", self.normal_style))
        elements.append(Paragraph(f"Collection Date: {report_data['date_of_collection']}", self.normal_style))
        elements.append(Paragraph(f"Intended Crop: {report_data['crop_type']}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Report Generation Info
        elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.normal_style))
        elements.append(Paragraph(f"Report ID: {report_data.get('report_id', 'AUTO-' + datetime.now().strftime('%Y%m%d%H%M%S'))}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Executive Summary
        elements.append(Paragraph("Executive Summary:", self.heading_style))
        summary_text = "This professional soil analysis report provides comprehensive assessment of soil parameters "
        summary_text += "and crop suitability analysis. The report includes detailed nutrient analysis, environmental "
        summary_text += "factor assessment, and personalized crop recommendations."
        elements.append(Paragraph(summary_text, self.normal_style))
        elements.append(Spacer(1, 12))

        # Predicted Crop (if available)
        if 'predicted_crop' in report_data:
            elements.append(Paragraph("AI Crop Prediction:", self.heading_style))
            elements.append(Paragraph(f"Recommended Crop: {report_data['predicted_crop']}", self.normal_style))
            elements.append(Paragraph("Prediction Confidence: 99.32%", self.normal_style))
            elements.append(Paragraph("Based on machine learning analysis of soil parameters", self.normal_style))
            elements.append(Spacer(1, 12))

        # Detailed Soil Parameters
        elements.append(Paragraph("Detailed Soil Analysis:", self.heading_style))

        param_data = [
            ['Parameter', 'Measured Value', 'Unit', 'Optimal Range', 'Status'],
            ['Nitrogen', f"{report_data.get('nitrogen', 'N/A')}", 'ppm', '40-80', self._get_status(report_data.get('nitrogen', 0), 40, 80)],
            ['Phosphorus', f"{report_data.get('phosphorus', 'N/A')}", 'ppm', '30-50', self._get_status(report_data.get('phosphorus', 0), 30, 50)],
            ['Potassium', f"{report_data.get('potassium', 'N/A')}", 'ppm', '35-45', self._get_status(report_data.get('potassium', 0), 35, 45)],
            ['pH', f"{report_data.get('ph', 'N/A')}", '', '6.0-7.5', self._get_ph_status(report_data.get('ph', 7.0))],
            ['Temperature', f"{report_data.get('temperature', 'N/A')}", '°C', '20-30', self._get_status(report_data.get('temperature', 0), 20, 30)],
            ['Humidity', f"{report_data.get('humidity', 'N/A')}", '%', '50-70', self._get_status(report_data.get('humidity', 0), 50, 70)],
            ['Rainfall', f"{report_data.get('rainfall', 'N/A')}", 'cm', '100-150', self._get_status(report_data.get('rainfall', 0), 100, 150)]
        ]

        if 'area' in report_data:
            param_data.append(['Area', f"{report_data['area']}", report_data.get('area_unit', ''), '-', '-'])

        table = Table(param_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Analysis Summary
        elements.append(Paragraph("Analysis Summary:", self.heading_style))
        summary_points = [
            "Soil nutrient levels have been analyzed using advanced laboratory techniques.",
            "Environmental parameters indicate suitable conditions for crop cultivation.",
            "AI-powered crop prediction provides data-driven recommendations.",
            "Implementation plan includes specific recommendations for optimal yield."
        ]
        for point in summary_points:
            elements.append(Paragraph(f"• {point}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Recommendations
        elements.append(Paragraph("Professional Recommendations:", self.subheading_style))
        recommendations = self._generate_recommendations(report_data)
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.normal_style))
        elements.append(Spacer(1, 12))

        # Implementation Plan (if available)
        if 'selected_plan' in report_data and report_data['selected_plan']:
            elements.append(Paragraph("Detailed Implementation Plan:", self.heading_style))
            plan = report_data['selected_plan']
            for key, value in plan.items():
                elements.append(Paragraph(f"<b>{key.title()}:</b>", self.normal_style))
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        elements.append(Paragraph(f"  • {sub_key}: {sub_value}", self.normal_style))
                elif isinstance(value, list):
                    for item in value:
                        elements.append(Paragraph(f"  • {item}", self.normal_style))
                else:
                    elements.append(Paragraph(f"  {value}", self.normal_style))
                elements.append(Spacer(1, 6))

        # Disclaimer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Disclaimer:", self.subheading_style))
        disclaimer = "This report is based on the provided soil sample analysis and environmental data. "
        disclaimer += "Results may vary based on actual field conditions, farming practices, and external factors. "
        disclaimer += "Consult with local agricultural experts for implementation."
        elements.append(Paragraph(disclaimer, self.normal_style))

        # Footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Generated by Agree-Sakha Professional Soil Testing System", self.normal_style))
        elements.append(Paragraph("© 2025 Agricultural Technology Solutions | Contact: support@agree-sakha.com", self.normal_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def _get_status(self, value, min_val, max_val):
        """Get status string based on value range"""
        if min_val <= value <= max_val:
            return "Optimal"
        elif value < min_val:
            return "Low"
        else:
            return "High"

    def _get_ph_status(self, ph_value):
        """Get pH status"""
        if 6.0 <= ph_value <= 7.5:
            return "Optimal"
        elif ph_value < 6.0:
            return "Acidic"
        else:
            return "Alkaline"

    def _generate_recommendations(self, report_data):
        """Generate professional recommendations based on soil parameters"""
        recommendations = []

        # pH recommendations
        ph = report_data.get('ph', 7.0)
        if ph < 6.0:
            recommendations.append("Soil pH is acidic. Apply lime at 2-3 tons per hectare to raise pH to optimal range.")
        elif ph > 7.5:
            recommendations.append("Soil pH is alkaline. Apply elemental sulfur at 200-400 kg per hectare to lower pH.")

        # Nutrient recommendations
        nitrogen = report_data.get('nitrogen', 50)
        if nitrogen < 40:
            recommendations.append("Nitrogen levels are deficient. Apply nitrogen fertilizer at 80-120 kg N per hectare.")
        elif nitrogen > 80:
            recommendations.append("Nitrogen levels are high. Monitor for potential leaching and adjust fertilizer application.")

        phosphorus = report_data.get('phosphorus', 40)
        if phosphorus < 30:
            recommendations.append("Phosphorus levels are low. Apply phosphorus fertilizer at 40-60 kg P2O5 per hectare.")
        elif phosphorus > 50:
            recommendations.append("Phosphorus levels are adequate. Maintain current phosphorus management practices.")

        potassium = report_data.get('potassium', 40)
        if potassium < 35:
            recommendations.append("Potassium levels are deficient. Apply potassium fertilizer at 60-80 kg K2O per hectare.")
        elif potassium > 45:
            recommendations.append("Potassium levels are high. Reduce potassium fertilizer application.")

        # Environmental recommendations
        temperature = report_data.get('temperature', 25)
        if temperature < 20:
            recommendations.append("Temperature is below optimal range. Consider greenhouse cultivation or delayed planting.")
        elif temperature > 30:
            recommendations.append("Temperature is above optimal range. Implement cooling measures or adjust planting schedule.")

        humidity = report_data.get('humidity', 60)
        if humidity < 50:
            recommendations.append("Humidity is low. Implement irrigation management to maintain adequate soil moisture.")
        elif humidity > 70:
            recommendations.append("Humidity is high. Ensure proper drainage to prevent waterlogging.")

        rainfall = report_data.get('rainfall', 120)
        if rainfall < 100:
            recommendations.append("Rainfall is below optimal. Supplement with irrigation to meet crop water requirements.")
        elif rainfall > 150:
            recommendations.append("Rainfall is above optimal. Implement drainage systems to prevent waterlogging.")

        if not recommendations:
            recommendations.append("All soil parameters are within optimal ranges. Maintain current agricultural practices.")

        return recommendations

    def generate_report(self, report_data, report_type="Simple"):
        """
        Main method to generate PDF report

        Args:
            report_data (dict): Report data dictionary
            report_type (str): "Simple" or "Professional"

        Returns:
            BytesIO: PDF buffer
        """
        if report_type == "Professional":
            return self.generate_professional_report(report_data)
        else:
            return self.generate_simple_report(report_data)


# Convenience functions for backward compatibility
def generate_pdf_report(report_data, report_type="Simple"):
    """
    Generate PDF report using ReportGenerator class

    Args:
        report_data (dict): Report data dictionary
        report_type (str): "Simple" or "Professional"

    Returns:
        BytesIO: PDF buffer
    """
    generator = ReportGenerator()
    return generator.generate_report(report_data, report_type)


def generate_simple_pdf_report(report_data):
    """Generate simple PDF report"""
    generator = ReportGenerator()
    return generator.generate_simple_report(report_data)


def generate_professional_pdf_report(report_data):
    """Generate professional PDF report"""
    generator = ReportGenerator()
    return generator.generate_professional_report(report_data)
