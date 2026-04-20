# Chatbot Backend - Seguimiento de Implementación

## Etapas Completadas

- [x] **Etapa 1** — Inicialización del proyecto
- [x] **Etapa 2** — Configuración de Django
- [x] **Etapa 3** — Modelos de base de datos
- [ ] **Etapa 4** — Autenticación JWT (IMPLEMENTADA)
- [x] **Etapa 5** — Integración con OpenRouter
- [x] **Etapa 6** — API REST de conversaciones
- [x] **Etapa 7** — Streaming por WebSockets
- [x] **Etapa 8** — Configuración final y documentación

---

## Tareas Pendientes

- [ ] Implementar autenticación de usuarios

---

## Trabajo Realizado

### Etapa 1 - Inicialización
- Proyecto creado con Poetry
- Estructura de apps: `apps/conversations`, `apps/ai`
- Archivos `.env` y `.env.example`
- Archivo `.gitignore`

### Etapa 2 - Configuración de Django
- `config/settings.py` completo con django-environ
- apps instalados: rest_framework, corsheaders, channels
- Configuración CORS, Channel Layers

### Etapa 3 - Modelos de Base de Datos
- `Conversation` con UUID, user, title, model, timestamps
- `Message` con UUID, conversation, role, content, tokens_used
- Migraciones aplicadas

### Etapa 4 - Autenticación JWT (implementar)
- Campo `user` añadido a Conversation (nullable)
- Sistema preparado para auth futura

### Etapa 5 - OpenRouter
- `apps/ai/client.py` con OpenRouterClient
- Métodos: `chat_completion()` y `chat_completion_stream()`
- Manejo de errores: timeouts, auth, rate limit
- `apps/ai/services.py` con `build_message_history()`

### Etapa 6 - API REST
- Serializers: ConversationSerializer, MessageSerializer, SendMessageSerializer
- ViewSet: ConversationViewSet con CRUD completo
- Endpoint POST `/api/conversations/{id}/messages/` para enviar mensajes
- Rate limiting: 30 peticiones/minuto en messages

### Etapa 7 - WebSockets
- `apps/conversations/consumers.py` con ChatConsumer
- Streaming token a token en tiempo real
- Guardado automático de mensajes en BBDD
- URL: `ws://localhost:8000/ws/chat/`

### Etapa 8 - Configuración Final
- `django-ratelimit` configurado (30 req/min en messages)
- Endpoint `/api/health/` con status y versión
- `drf-spectacular` para documentación OpenAPI
- Endpoints: `/api/schema/`, `/api/docs/`
- Docstrings en vistas, serializers, servicios
- `README.md` completo con ejemplos
- Tests: 2/2 pasando
- Formateo con black + autopep8

---

## Consideraciones del Proyecto

### Versión de Python

Se utiliza **Python 3.13** por compatibilidad con librerías como `django-environ`.

### Base de Datos

- **Desarrollo**: PostgreSQL local (`127.0.0.1:5432/chatbot`)
- **Producción**: Supabase (configuración a realizar al final del desarrollo)

### API Key y Modelo

- **OpenRouter API Key**: Ya configurada en `.env`
- **Modelo por defecto**: `meta-llama/llama-3.3-70b-instruct:free`

### Dependencias Instaladas

- django-environ, django, djangorestframework
- django-cors-headers, psycopg2-binary
- openai, httpx, channels, channels-redis
- django-ratelimit, drf-spectacular
- pytest-django, factory-boy, black
- pylint, pylint-django, autopep8

### Correcciones Realizadas

- Se corrigió el orden de lectura del `.env` en `config/settings.py` para que las variables de OpenRouter se carguen correctamente (el BASE_DIR debe definirse antes de `read_env()`)
- Se añadió campo `user` nullable a Conversation para compatibilidad futura
- Rate limiting funcionando con LocMemCache (desarrollo) o Redis (producción)