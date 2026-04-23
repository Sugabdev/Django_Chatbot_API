# Chatbot Backend

Chatbot web desarrollado con Python y Django que expone una REST API consumible por cualquier frontend. Integra modelos de lenguaje open source a través de OpenRouter, permitiendo conversaciones contextuales con historial persistente almacenado en base de datos.

## Requisitos Previos

- Python 3.13
- Poetry (gestor de dependencias)
- PostgreSQL 14+ (local)
- Redis (opcional, para WebSockets y rate limiting)

## Tecnologías

- Django 6.0
- Django REST Framework
- Channels (WebSockets)
- OpenRouter (LLM)
- PostgreSQL
- Redis (opcional)

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   poetry install
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

4. Ejecutar migraciones:
   ```bash
   poetry run python manage.py migrate
   ```

5. Iniciar el servidor:
   ```bash
   poetry run python manage.py runserver
   ```

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | (requerido) |
| `DEBUG` | Modo debug | True |
| `DATABASE_URL` | URL de conexión a PostgreSQL | psql://postgres:postgres@127.0.0.1:5432/chatbot |
| `OPENROUTER_API_KEY` | API key de OpenRouter | (requerido) |
| `OPENROUTER_BASE_URL` | URL base de OpenRouter | https://openrouter.ai/api/v1 |
| `DEFAULT_MODEL` | Modelo por defecto | openrouter/free |
| `ALLOWED_HOSTS` | Hosts permitidos | localhost,127.0.0.1 |
| `CORS_ALLOWED_ORIGINS` | Orígenes CORS permitidos | http://localhost:3000 |
| `REDIS_URL` | URL de Redis (opcional) | (vacío) |

## Endpoints de la API

### Conversaciones

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/conversations/` | Listar todas las conversaciones |
| POST | `/api/conversations/` | Crear nueva conversación |
| GET | `/api/conversations/{id}/` | Obtener detalle de una conversación |
| DELETE | `/api/conversations/{id}/` | Eliminar una conversación |
| POST | `/api/conversations/{id}/messages/` | Enviar mensaje y recibir respuesta |

#### Ejemplo: Crear conversación

```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/llama-3.3-70b-instruct:free"}'
```

Response:
```json
{
  "id": "uuid-de-la-conversacion",
  "title": null,
  "model": "meta-llama/llama-3.3-70b-instruct:free",
  "created_at": "2026-04-18T12:00:00Z",
  "updated_at": "2026-04-18T12:00:00Z",
  "messages": []
}
```

#### Ejemplo: Enviar mensaje

```bash
curl -X POST http://localhost:8000/api/conversations/{id}/messages/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Hola, ¿cómo estás?"}'
```

Response:
```json
{
  "user_message": {
    "id": "uuid",
    "role": "user",
    "content": "Hola, ¿cómo estás?",
    "created_at": "2026-04-18T12:00:00Z",
    "tokens_used": null
  },
  "assistant_message": {
    "id": "uuid",
    "role": "assistant",
    "content": "¡Hola! Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte?",
    "created_at": "2026-04-18T12:00:05Z",
    "tokens_used": null
  }
}
```

### WebSocket

| URL | Descripción |
|-----|-------------|
| `ws://localhost:8000/ws/chat/` | Streaming de mensajes en tiempo real |

#### Formato de mensaje (entrada)

```json
{
  "conversation_id": "uuid-de-la-conversacion",
  "content": "Tu mensaje aquí",
  "model": "meta-llama/llama-3.3-70b-instruct:free"
}
```

#### Formato de mensaje (salida)

Token individual:
```json
{"type": "token", "content": "..."}
```

Finalización:
```json
{"type": "done", "message_id": "uuid"}
```

Error:
```json
{"type": "error", "detail": "..."}
```

### Otros Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/health/` | Health check |
| GET | `/api/schema/` | Schema OpenAPI |
| GET | `/api/docs/` | Swagger UI |

## Rate Limiting

- Endpoint de mensajes: 30 peticiones/minuto
- El rate limiting usa Redis si está configurado, si no usa cache local (solo para desarrollo)

## Tests

```bash
poetry run pytest
```

## Formateo de Código

```bash
# Con pylint
poetry run pylint apps/

# Con autopep8
poetry run autopep8 --in-place --recursive apps/
```
## BBDD

Supabase
- https://gfsrxypbxogusivbkbpx.supabase.co

## Deployment

Render
- https://dashboard.render.com/web/srv-d7k24t8js32c73ca69ug

## Licencia

MIT
