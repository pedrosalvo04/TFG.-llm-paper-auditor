"""Componente de pantalla de carga inicial"""
import streamlit as st
import time

def render_initial_loader():
    """Renderiza una pantalla de carga premium mientras se inicializa la app"""
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
        <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #0f172a !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%) !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999999 !important;
            backdrop-filter: blur(20px) !important;
        }
        .loader-card {
            background: rgba(30, 41, 59, 0.7) !important;
            backdrop-filter: blur(16px) !important;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            width: 420px;
            animation: fadeIn 0.8s ease;
        }
        .loader-dna {
            width: 100%;
            height: 80px;
            margin-bottom: 25px;
            position: relative;
        }
        .dot {
            width: 16px;
            height: 16px;
            background: #3b82f6;
            border-radius: 50%;
            position: absolute;
            top: 40%;
            animation: dna-bounce 2s infinite ease-in-out;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        }
        .dot.strand-2 {
            background: #10b981;
            animation-delay: -1s !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
        }
        @keyframes dna-bounce {
            0%, 100% { transform: translateY(0) scale(0.8); opacity: 0.4; }
            50% { transform: translateY(-45px) scale(1.4); opacity: 1; }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loading-text {
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 800;
            margin-top: 20px;
            letter-spacing: -0.5px;
        }
        .loading-subtext {
            color: #94a3b8;
            font-size: 1rem;
            margin-top: 12px;
            font-weight: 400;
        }
        </style>
        <div class="loading-overlay">
            <div class="loader-card">
                <div class="loader-dna">
                    <!-- Strand 1 -->
                    <div class="dot" style="left: 15%; animation-delay: 0s;"></div>
                    <div class="dot" style="left: 32.5%; animation-delay: 0.2s;"></div>
                    <div class="dot" style="left: 50%; animation-delay: 0.4s;"></div>
                    <div class="dot" style="left: 67.5%; animation-delay: 0.6s;"></div>
                    <div class="dot" style="left: 85%; animation-delay: 0.8s;"></div>
                    <!-- Strand 2 -->
                    <div class="dot strand-2" style="left: 15%; animation-delay: 0s;"></div>
                    <div class="dot strand-2" style="left: 32.5%; animation-delay: 0.2s;"></div>
                    <div class="dot strand-2" style="left: 50%; animation-delay: 0.4s;"></div>
                    <div class="dot strand-2" style="left: 67.5%; animation-delay: 0.6s;"></div>
                    <div class="dot strand-2" style="left: 85%; animation-delay: 0.8s;"></div>
                </div>
                <div class="loading-text">Nature Auditor Pro</div>
                <div class="loading-subtext">Iniciando motor de análisis científico...</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Retardo para asegurar la experiencia visual
    time.sleep(2.5)
    return loading_placeholder
