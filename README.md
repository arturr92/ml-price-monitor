# 🔔 ML Price Monitor

Sistema de monitoreo de precios de Mercado Libre con alertas automáticas por email y Telegram. Desarrollado como proyecto de portfolio aplicando metodología Scrum con Jira y Miro.

---

## 📋 Stack técnico

| Capa                 | Tecnología                    |
| -------------------- | ----------------------------- |
| Backend              | Python 3.13 + Flask           |
| Base de datos        | SQLite + SQLAlchemy           |
| Automatización       | APScheduler / schedule        |
| Alertas              | SMTP Gmail + Telegram Bot API |
| Frontend             | Bootstrap 5 + Chart.js        |
| Gestión de proyecto  | Jira (Scrum) + Miro           |
| Control de versiones | Git + GitHub                  |

---

## 🏗️ Arquitectura

El proyecto está organizado en 3 capas siguiendo el principio de separación de responsabilidades:

```
ml-price-monitor/
├── models/ # Capa de datos
│ ├── database.py # Modelos SQLAlchemy (USERS, PRODUCTS, PRICE_HISTORY, ALERTS_SENT)
│ ├── price_repository.py # Operaciones sobre historial de precios
│ ├── product_repository.py# Operaciones sobre productos
│ └── alert_repository.py # Operaciones sobre alertas enviadas
├── services/ # Capa de negocio
│ ├── providers/ # Patrón Provider (escalable a múltiples fuentes)
│ │ ├── base_provider.py # Interfaz abstracta
│ │ ├── mercadolibre.py # Implementación ML (API oficial)
│ │ └── mock_provider.py # Implementación mock (desarrollo)
│ ├── price_service.py # Orquestador de providers
│ ├── email_service.py # Servicio de alertas por email
│ ├── telegram_service.py # Servicio de alertas por Telegram
│ ├── scheduler.py # Ciclo automático de monitoreo
│ └── logger.py # Sistema de logging centralizado
├── routes/ # Capa de presentación
│ ├── dashboard.py # Vista principal
│ ├── products.py # Alta de productos
│ └── history.py # Historial y gráficos
├── templates/ # Templates HTML (Flask + Bootstrap)
├── static/ # Archivos estáticos
├── app.py # Entry point de la aplicación
├── config.py # Configuración centralizada
└── requirements.txt
```

### Decisiones arquitecturales clave

- **Patrón Provider:** permite agregar nuevas fuentes de precios (Amazon, scraping genérico) creando un archivo nuevo sin modificar el código existente
- **Patrón Repository:** separa la lógica de acceso a datos de la lógica de negocio
- **Mock Provider:** permite desarrollar y testear sin depender de APIs externas

---

## ⚙️ Instalación

### Requisitos

- Python 3.10+
- Git

### Pasos

1. **Clonar el repositorio**

```bash
git clone https://github.com/arturr92/ml-price-monitor.git
cd ml-price-monitor
```

2. **Crear y activar entorno virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Inicializar la base de datos**

```bash
python models/init_db.py
```

6. **Levantar la aplicación**

```bash
python app.py
```

Abrí `http://127.0.0.1:5000` en el navegador.

---

## 🔧 Configuración (.env)

```env
# Base de datos
DATABASE_PATH=price_monitor.db

# Flask
SECRET_KEY=tu-clave-secreta
DEBUG=True

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-contraseña-de-aplicacion

# Telegram
TELEGRAM_TOKEN=tu-token-de-bot
TELEGRAM_CHAT_ID=tu-chat-id

# Scheduler
CHECK_INTERVAL_HOURS=6

# Desarrollo
USE_MOCK=False
LOG_FILE=logs/price_monitor.log
LOG_LEVEL=INFO
```

---

## 🚀 Uso

### Agregar un producto

1. Andá a `/add-product`
2. Pegá la URL del producto en Mercado Libre
3. Definí tu precio objetivo
4. Elegí el canal de alerta (email, Telegram o ambos)

### Monitoreo automático

El scheduler corre automáticamente cada `CHECK_INTERVAL_HOURS` horas. Para correrlo manualmente:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); from services.scheduler import run_price_check_cycle; run_price_check_cycle()"
```

### Modo desarrollo (sin API real)

Configurá `USE_MOCK=True` en el `.env` para usar datos simulados sin necesitar credenciales de ML.

---

## 📊 Gestión del proyecto

Este proyecto fue desarrollado aplicando metodología **Scrum**:

- **Herramientas:** Jira (backlog, sprints, historias de usuario) + Miro (diagramas de arquitectura, ER y flujo)
- **Sprints:** 4 sprints de 2 semanas
- **Épicas:** 7 épicas que cubren desde la configuración base hasta el deploy
- **Retrospectivas:** documentadas en Confluence al cierre de cada sprint

---

## 🔮 Próximas funcionalidades

- Soporte para Amazon y otros sitios de e-commerce
- Provider de scraping genérico configurable por URL
- Integración con ERP propio (en desarrollo)
- Autenticación de usuarios múltiples

---

## 👨‍💻 Autor

**Arturo Gonzalez**
Estudiante de Licenciatura en Sistemas
[GitHub](https://github.com/arturr92)
