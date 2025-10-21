import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unidad_medica.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        # Check if the table exists
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('usuarios_pacientes', 'estado_civil');
        """)
        tables = cursor.fetchall()
        print("Tables found:", [t[0] for t in tables])
        
        # Check columns in usuarios_pacientes
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios_pacientes';
        """)
        columns = cursor.fetchall()
        print("\nColumns in usuarios_pacientes:")
        for col in columns:
            print(f"- {col[0]}: {col[1]}")

if __name__ == "__main__":
    check_tables()
