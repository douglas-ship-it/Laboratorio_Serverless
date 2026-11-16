import json
import uuid
import hashlib
import platform
import socket
from datetime import datetime, timezone
from urllib.parse import parse_qs
from html import escape


def handle(event, context):
    if event.method == "GET":
        formulario = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro Serverless</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            padding: 50px 20px;
        }
        .contenedor {
            max-width: 450px;
            margin: auto;
            padding: 30px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }
        h2 {
            margin-top: 0;
            margin-bottom: 8px;
            color: #0f172a;
        }
        p.subtitulo {
            margin-top: 0;
            margin-bottom: 20px;
            color: #475569;
            font-size: 14px;
        }
        label {
            display: block;
            font-weight: bold;
            color: #1e293b;
            font-size: 14px;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0 16px;
            box-sizing: border-box;
            border-radius: 6px;
            font-size: 14px;
        }
        input {
            border: 1px solid #cbd5e1;
        }
        button {
            background-color: #0369a1;
            color: white;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #075985;
        }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Registro de Ejecución Serverless</h2>
        <p class="subtitulo">Introducción al Cómputo de la Nube</p>
        <form method="POST" action="/">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" name="nombre" required>

            <label for="apellido">Apellido</label>
            <input type="text" id="apellido" name="apellido" required>

            <label for="email">Correo del aula virtual</label>
            <input type="email" id="email" name="email" required>

            <button type="submit">Generar archivo JSON</button>
        </form>
    </div>
</body>
</html>"""
        return {
            "statusCode": 200,
            "body": formulario,
            "headers": {
                "Content-Type": "text/html; charset=utf-8"
            }
        }

    elif event.method == "POST":
        body_str = event.body.decode("utf-8") if isinstance(event.body, bytes) else str(event.body)
        datos_form = parse_qs(body_str)

        nombre = escape(datos_form.get("nombre", [""])[0].strip())
        apellido = escape(datos_form.get("apellido", [""])[0].strip())
        email = escape(datos_form.get("email", [""])[0].strip())

        token_unico = str(uuid.uuid4())
        fecha_utc = datetime.now(timezone.utc).isoformat()

        registro = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "token": token_unico,
            "fecha_utc": fecha_utc,
            "sistema_operativo": platform.system(),
            "version_so": platform.release(),
            "arquitectura": platform.machine(),
            "procesador": platform.processor(),
            "version_python": platform.python_version(),
            "hostname_contenedor": socket.gethostname(),
            "plataforma": "OpenFaas",
            "funcion": "registro-serverless",
            "estado": "Ejecucion exitosa"
        }

        contenido_base = json.dumps(registro, sort_keys=True, ensure_ascii=False)
        firma_sha256 = hashlib.sha256(contenido_base.encode("utf-8")).hexdigest()
        registro["firma_sha256"] = firma_sha256

        json_final = json.dumps(registro, indent=4, ensure_ascii=False)
        nombre_archivo = f"registro_{token_unico}.json"

        return {
            "statusCode": 200,
            "body": json_final,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Content-Disposition": f'attachment; filename="{nombre_archivo}"'
            }
        }

    return {
        "statusCode": 405,
        "body": "Método no permitido",
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
        }
    }
