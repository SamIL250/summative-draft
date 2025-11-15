from database.connection import DatabaseConnection
from tabulate import tabulate
import os

class Document:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
    
    def add_document(self, student_id, doc_type, doc_name, file_path, description):
        query = """
        INSERT INTO documents (student_id, document_type, document_name, file_path, description)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (student_id, doc_type, doc_name, file_path, description)
        result = self.db.execute_query(query, params)
        if result:
            print(f"✓ Document {doc_name} added successfully!")
            return True
        return False
    
    def view_student_documents(self, student_id):
        query = """
        SELECT document_id, document_type, document_name, upload_date, description
        FROM documents
        WHERE student_id = %s
        ORDER BY upload_date DESC
        """
        docs = self.db.fetch_all(query, (student_id,))
        
        if docs:
            headers = docs[0].keys()
            rows = [list(doc.values()) for doc in docs]
            print("\n=== Documents ===")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No documents found")
    
    def delete_document(self, document_id):
        query = "DELETE FROM documents WHERE document_id = %s"
        result = self.db.execute_query(query, (document_id,))
        if result:
            print(f"✓ Document deleted successfully!")
            return True
        return False