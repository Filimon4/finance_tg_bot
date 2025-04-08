from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
from typing import List, Optional, Generator
from dataclasses import dataclass
import os
from modules.finance.operations.operationsRepository import OperationsRepository
from sqlalchemy.orm import Session
from datetime import datetime

class ExcelReportGenerator:
    # ... (остальной код класса остается без изменений)

    def generate_operations_report(self, session: Session, page_size: int = 40) -> str:
        """
        Generate a complete Excel report with all operations from the database.
        
        Args:
            session: SQLAlchemy session
            page_size: Number of operations per page
            
        Returns:
            Path to the generated report file
        """
        # Clear existing data (optional - remove if you want to append to existing data)
        if os.path.exists(self.report_file):
            os.remove(self.report_file)
        self._initialize_workbook()
        
        wb = load_workbook(self.report_file)
        ws = wb["data"]
        
        # Process operations page by page
        for operations in self.paginatedOperationsGenerator(session, page_size):
            for operation in operations:
                # Convert operation to ReportDTO
                report_data = ReportDTO(
                    date=operation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    category=operation.category.name if operation.category else "Unknown",
                    amount=float(operation.amount),
                    description=operation.description or "",
                    user_id=operation.account_id or 0,
                    username=operation.account.username if operation.account else "Unknown"
                )
                
                # Add to Excel
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
        
        # Save the final file
        wb.save(self.report_file)
        wb.close()
        
        return self.report_file

    def paginatedOperationsGenerator(self, session: Session, page_size: int = 40) -> Generator:
        """
        Generator that yields operations page by page.
        
        Args:
            session: SQLAlchemy session
            page_size: Number of operations per page
            
        Yields:
            List of operations for each page
        """
        page = 1
        while True:
            data_operations = OperationsRepository.getPaginatedOperations(session, page, page_size)
            if not data_operations['operations']:
                break
                
            yield data_operations['operations']
            page += 1