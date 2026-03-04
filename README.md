# Demo Docker Compose - Fernando Agustín Hernández Rivas - Sistemas Distribuidos

## Descripción
Este proyecto es una demostración sencilla de cómo construir y ejecutar una aplicación de backend utilizando **Docker Compose** para orquestar múltiples servicios.  

La aplicación consiste en una **API desarrollada con Flask** que se conecta a dos servicios adicionales:

- **PostgreSQL** como base de datos relacional
- **Redis** como sistema de cache en memoria

# Arquitectura del sistema

La aplicación está compuesta por tres contenedores principales:

1. **API (Flask)**
   - Expone endpoints REST
   - Se conecta a PostgreSQL para almacenamiento
   - Utiliza Redis para almacenamiento temporal de datos

2. **PostgreSQL**
   - Base de datos relacional
   - Guarda información de usuarios

3. **Redis**
   - Base de datos en memoria
   - Se utiliza como contador de visitas para la API

### Descripción de archivos

**docker-compose.yml**

Define los servicios de la aplicación y cómo se conectan entre sí.

**Dockerfile**

Define la imagen de Docker utilizada para ejecutar la aplicación Flask.

**main.py**

Contiene la lógica principal de la API.

**requirements.txt**

Lista de dependencias necesarias para ejecutar la aplicación.

---
# Endpoints de la API

## Endpoint principal

```
GET /
```

Devuelve información básica de la API.

---

## Health Check

```
GET /health
```

Verifica el estado de los servicios conectados.

---

## Contador de visitas

```
GET /visits
```

Incrementa y devuelve el número de visitas almacenado en Redis.

---

## Crear usuario

```
POST /users
```

Ejemplo de body:

```json
{
  "name": "Anton",
  "email": "anton@example.com"
}
```

---

## Obtener usuarios

```
GET /users
```

---

# Base de datos

Al iniciar la aplicación se crea automáticamente la tabla de usuarios:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);
```

---

# Tecnologías utilizadas

- Python
- Flask
- PostgreSQL
- Redis
- Docker
- Docker Compose

---
