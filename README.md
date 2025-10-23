# Plataforma de Eventos (Django)

Proyecto Django 4.x con SQLite que permite publicar y buscar eventos, con subida de multimedia como BLOB en la base de datos. Incluye autenticación con verificación por email (backend de consola), CRUD de eventos con slug, reseñas y calificaciones, búsqueda/filtrado/paginación, y API básica con DRF.

## Requisitos

- Python 3.10+
- pip

## Instalación

1. Crear y activar entorno virtual (opcional pero recomendado):

   - Windows:
     python -m venv .venv
     .venv\\Scripts\\activate

2. Instalar dependencias:

   pip install -r requirements.txt

3. Migraciones y superusuario:

   python manage.py migrate
   python manage.py createsuperuser

4. Ejecutar servidor de desarrollo:

   python manage.py runserver

   Email backend usa consola en dev, verás los emails de verificación en la terminal.

## Funcionalidades clave

- Registro, login/logout, perfil de usuario con avatar (BLOB) y datos de contacto.
- Verificación de email al registrarse (enlace en consola).
- CRUD de eventos con campos solicitados. Slug y metatags Open Graph para compartir.
- Subida de fotos/videos como BLOB (BinaryField) en SQLite y entrega desde vistas con Content-Type.
- Búsqueda por título/descripcion, filtros por ciudad, precio, categoría, orden por destacados/populares y paginación.
- Reseñas con calificación 1-5 y promedio visible, moderación por creador/admin.
- Sección de contacto/mensajería básica para enviar dudas al creador (guardado en BD y notificación simple).
- Admin para gestionar usuarios, eventos, reseñas y mensajes.
- API DRF para eventos y reseñas con autenticación por sesión/token.

## Rutas principales

- Home: /
- Eventos: /eventos/
- Detalle: /eventos/<slug>/
- Crear evento: /eventos/crear/
- Cuenta: /accounts/ (login/logout), /accounts/signup/, /accounts/profile/

## Subida de BLOBs

- Límite de 10MB por archivo (configurable en settings.py)
- Tipos permitidos: imágenes (jpeg/png/gif) y video (mp4/webm). Ajustable en settings.

## API

- /api/events/
- /api/reviews/

Para autenticación por token:

python manage.py drf_create_token <username>

o crear tokens desde admin (Token).

## Pruebas

Ejecutar:

python manage.py test

Incluye pruebas básicas para creación de evento, búsqueda, subida/lectura de BLOB y promedio de reseñas.

## Fixtures / datos de ejemplo

Tras migrar, las categorías se crean automáticamente por migración. Puedes crear datos de ejemplo con el admin o ejecutar un script de seed opcional:

python manage.py loaddata fixtures/seed.json

## Notas de seguridad

- CSRF habilitado por defecto.
- Permisos: solo creador o admin puede editar/eliminar.
- Sanitización básica mediante escapes en templates de Django. Evita contenido HTML peligroso.
- Para producción, configurar SECRET_KEY, DEBUG=False, y un backend de email real en settings.py (ver comentarios).

## Decisiones

- Archivos multimedia se almacenan como BLOBs en tablas MediaBlob relacionadas a eventos y perfiles. No se usa almacenamiento externo por defecto. Puede integrarse uno opcionalmente en el futuro.
