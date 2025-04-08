from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
from typing import List, Optional
from dataclasses import dataclass
import os

@dataclass
class ReportDTO:
    """Data Transfer Object for report data"""
    date: str
    category: str
    amount: float
    description: str
    user_id: int
    username: str

class ExcelReportGenerator:
    """
    Singleton class for generating Excel reports.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExcelReportGenerator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.report_file = "analytic_report.xlsx"
        self._initialize_workbook()
    
    def _initialize_workbook(self):
        """Initialize workbook with headers if it doesn't exist"""
        if not os.path.exists(self.report_file):
            wb = Workbook()
            ws = wb.active
            ws.title = "data"
            
            # Write headers
            headers = [
                "Date", "Category", "Amount", 
                "Description", "User ID", "Username"
            ]
            
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
            
            wb.save(self.report_file)
            wb.close()
    
    def add_data(self, report_data: ReportDTO) -> str:
        """
        Add data to the report and return the file path.
        
        Args:
            report_data: ReportDTO containing the data to add
            
        Returns:
            Path to the generated report file
        """
        wb = load_workbook(self.report_file)
        ws = wb["data"]
        
        next_row = ws.max_row + 1
        
        data_values = [
            report_data.date,
            report_data.category,
            report_data.amount,
            report_data.description,
            report_data.user_id,
            report_data.username
        ]
        
        for col_num, value in enumerate(data_values, start=1):
            ws.cell(row=next_row, column=col_num, value=value)
        
        wb.save(self.report_file)
        wb.close()
        
        return self.report_file
    
    def generate_report(self, data_list: List[ReportDTO]) -> str:
        """
        Generate a complete report from multiple data entries.
        
        Args:
            data_list: List of ReportDTO objects
            
        Returns:
            Path to the generated report file
        """
        for data in data_list:
            self.add_data(data)
        
        return self.report_file
    
    def get_report(self) -> Optional[str]:
        """
        Get the path to the current report file if it exists.
        
        Returns:
            Path to the report file or None if it doesn't exist
        """
        if os.path.exists(self.report_file):
            return self.report_file
        return None
