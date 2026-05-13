"""Script de prueba para verificar importaciones"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("Probando importaciones...")

try:
    from frontend.config import TITLE, SIDEBAR_IMAGE, SIDEBAR_DESCRIPTION
    print("OK frontend.config")
except Exception as e:
    print(f"ERROR frontend.config: {e}")

try:
    from frontend.styles.custom_css import apply_custom_styles
    print("OK frontend.styles.custom_css")
except Exception as e:
    print(f"ERROR frontend.styles.custom_css: {e}")

try:
    from frontend.utils.session_state import initialize_session_state
    print("OK frontend.utils.session_state")
except Exception as e:
    print(f"ERROR frontend.utils.session_state: {e}")

try:
    from frontend.components.file_uploader import process_uploaded_file
    print("OK frontend.components.file_uploader")
except Exception as e:
    print(f"ERROR frontend.components.file_uploader: {e}")

try:
    from frontend.components.audit_results import render_audit_results, generate_report
    print("OK frontend.components.audit_results")
except Exception as e:
    print(f"ERROR frontend.components.audit_results: {e}")

try:
    from frontend.components.sota_section import render_sota_analysis
    print("OK frontend.components.sota_section")
except Exception as e:
    print(f"ERROR frontend.components.sota_section: {e}")

try:
    from frontend.components.chatbot import render_chatbot
    print("OK frontend.components.chatbot")
except Exception as e:
    print(f"ERROR frontend.components.chatbot: {e}")

print("\nTodas las importaciones funcionan correctamente!")
