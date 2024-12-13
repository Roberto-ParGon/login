# Servicio web de DataShield

Aplicación web segura ante inyecciones de código. Y servicio web para la capacitación de phishing de la empresa DataShield.

## Instalación

Instalar librerías con pip.

```bash
pip install flask mysql-connector-python bcrypt
```

## Levantar el servicio

Levantar el servicio de la página web, naturalmente en el puerto 8081 para evitar paridad con algún servicio web, pero naturalmente con puerto 80 en la máquina virtual.

```bash
python3 app.py
```

Levantar el servicio de phishing, naturalmente en el puerto 8081 para evitar paridad con algún servicio web, pero naturalmente con puerto 80 en la máquina virtual.

```bash
python3 phishing.py
```

## Llamados al API

#### Registrar usuario

```http
  POST /register
```

| Parámetro  | Tipo     | Descripción            |
| :--------- | :------- | :--------------------- |
| `username` | `string` | Nombre del usuario     |
| `password` | `string` | Contraseña del usuario |

#### Validar usuario

```http
  POST /api/authenticate
```

| Parámetro  | Tipo     | Descripción            |
| :--------- | :------- | :--------------------- |
| `username` | `string` | Nombre del usuario     |
| `password` | `string` | Contraseña del usuario |

#### Uso con CURL

##### Registrar

```bash
curl -X POST http://127.0.0.1:8081/register -H "Content-Type: application/json" -d '{"username":"test", "password":"test123"}'
```

##### Validar

```bash
curl -X POST http://127.0.0.1:8081/api/authenticate -H "Content-Type: application/json" -d '{"username":"test", "password":"test123"}'
```

## Tecnologías

**Cliente:** HTTML, CSS, JavaScript.

**Servidor:** Python, Flask, Bcrypt.

**Base de datos:** MySQL.
