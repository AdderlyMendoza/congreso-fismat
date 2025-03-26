# #!/usr/bin/env bash
# # Exit on error
# set -o errexit

# # pip install -r requirements.txt

# # Convert static asset files
# python manage.py collectstatic --no-input

# # Apply any outstanding database migrations
# python manage.py migrate


#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear directorios necesarios
mkdir -p staticfiles
mkdir -p media

# 3. Colectar archivos estáticos (con limpieza)
python manage.py collectstatic --noinput --clear

# 4. Aplicar migraciones
python manage.py migrate

# 5. Opcional: Comprimir estáticos (para WhiteNoise)
python manage.py compress --force