import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unidad_medica.settings')
try:
    django.setup()
    
    # Now we can import models
    from django.db import connection
    from index.models import Paciente, EstadoCivil
    
    # Check if tables exist
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('usuarios_pacientes', 'estado_civil');
        """)
        print("Tables found in database:")
        for table in cursor.fetchall():
            print(f"- {table[0]}")
    
    # Check Paciente model fields
    print("\nPaciente model fields:")
    for field in Paciente._meta.get_fields():
        print(f"- {field.name}: {field.get_internal_type()}")
    
    # Check EstadoCivil model fields
    print("\nEstadoCivil model fields:")
    for field in EstadoCivil._meta.get_fields():
        print(f"- {field.name}: {field.get_internal_type()}")
    
    # Check if we can query the data
    print("\nSample EstadoCivil records:")
    for ec in EstadoCivil.objects.all()[:5]:
        print(f"- {ec.id_Estado_Civil}: {ec.estado_civil}")
    
    print("\nSample Paciente records with Estado_Civil:")
    for p in Paciente.objects.select_related('Estado_Civil').all()[:5]:
        print(f"- {p.Nombres_Paciente} {p.Apellidos_Paciente}: {p.Estado_Civil}")
        
except Exception as e:
    print(f"Error: {str(e)}")
