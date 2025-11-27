# app/utils.py
# Módulo para contener funciones de utilidad de infraestructura.

import os
from sqlalchemy import text 
from sqlalchemy.orm import Session 


def execute_sql_file(db_session: Session, file_path: str) -> bool:
    """
    Ejecuta todas las sentencias SQL contenidas en un archivo, reportando fallos.
    Esta función es crucial para la inicialización y siembra (seeding) de la base de datos.
    
    Args:
        db_session: Sesión de SQLAlchemy para ejecutar comandos.
        file_path: Ruta del archivo .sql a ejecutar.

    Returns:
        True si la ejecución fue exitosa, False en caso de error.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo SQL no encontrado: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    statements = [s.strip() for s in sql_script.split(';') if s.strip()]

    try:
        for statement in statements:
            # Ejecutamos la sentencia
            db_session.execute(text(statement))
            
        db_session.commit()
        print(f"✅ SQL ejecutado: {file_path}.")
        return True
    
    except Exception as e:
        db_session.rollback()
        print(f"❌ Error crítico en SQL: {file_path}")
        # Intentamos mostrar la sentencia que causó el fallo
        statement_display = statement[:100] + "..." if len(statement) > 100 else statement
        print(f"   Sentencia que causó el error: {statement_display}")
        print(f"   Error de DB: {e}")
        return False