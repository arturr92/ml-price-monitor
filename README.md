# ML Price Monitor

Sistema de monitoreo de precios de Mercado Libre con alertas automáticas por email y Telegram.

## Stack técnico

- Python + Flask
- SQLite
- API oficial de Mercado Libre
- APScheduler

## Estructura del proyecto

ml-price-monitor/
├── models/ # Modelos de base de datos (tablas y queries)
├── services/ # Lógica de negocio (API, alertas, scheduler)
├── routes/ # Rutas de Flask (endpoints web)
├── static/ # Archivos estáticos (CSS, JS)
├── templates/ # Templates HTML de Flask
├── config.py # Configuración centralizada con variables de entorno
├── .env.example # Template de variables de entorno (sin credenciales)
└── requirements.txt

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Copiar `.env.example` a `.env` y completar las variables
