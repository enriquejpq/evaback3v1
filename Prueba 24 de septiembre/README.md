# Patitas & Co. — tienda de mascotas

Proyecto Django preparado para la evaluación de autenticación, validaciones y persistencia con MySQL/XAMPP.

## 1. Preparar XAMPP
1. Abre XAMPP y enciende **Apache** y **MySQL**.
2. Entra a `http://localhost/phpmyadmin`.
3. Abre **SQL**, pega el contenido de `crear_base_datos.sql` y ejecútalo.

## 2. Instalar el proyecto (Windows)
```bat
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Si `mysqlclient` no se instala, abre XAMPP Control Panel > Shell y confirma que MySQL esté disponible. Como alternativa académica, instala Microsoft C++ Build Tools y vuelve a ejecutar el comando.

## 3. Crear las tablas y el usuario
```bat
py manage.py migrate
py manage.py createsuperuser
py manage.py cargar_demo
py manage.py runserver
```
Abre `http://127.0.0.1:8000`. El catálogo es público; **Gestión** exige iniciar sesión. Todo producto creado, editado o eliminado desde Gestión se persiste en la tabla `productos_producto` de MySQL. Usuarios y sesiones se guardan en las tablas de Django (`auth_user`, `django_session`, etc.).

## 4. Comprobar las tablas
En phpMyAdmin abre `tienda_mascotas_db`. Después de `migrate` deben aparecer `productos_producto`, `auth_user`, `django_session` y las demás tablas internas. Crea un producto en Gestión y pulsa **Examinar** en `productos_producto` para demostrar la persistencia.

## 5. Pruebas
```bat
set DB_ENGINE=sqlite
py manage.py test
```
Las pruebas cubren catálogo público, login obligatorio, creación persistente, validación y eliminación segura.

## 6. Trabajo colaborativo sugerido
Cada integrante debe crear su propia rama y commits reales. Ejemplo: `git switch -c autenticacion`, `git switch -c validaciones`, `git switch -c diseno`. Integren con `git merge` y documenten cualquier conflicto. No inventen historial: el docente debe poder comprobar los aportes.

## Flujo para la demostración
1. Mostrar catálogo sin sesión.
2. Intentar abrir Gestión y comprobar que solicita login.
3. Iniciar sesión y crear un producto; mostrar el mensaje de éxito.
4. Ver la fila nueva en phpMyAdmin.
5. Probar una descripción corta o precio negativo y mostrar que no se guarda.
6. Editar y eliminar el producto, confirmando cada cambio en MySQL.


## Registro con token y código de 6 dígitos
1. Entra a `/cuenta/registro/` (botón **Crear cuenta**).
2. Se crea el usuario desactivado y se envía un correo con un enlace con token único.
3. Al abrir el enlace la página muestra un código de 6 dígitos como imagen (no se puede copiar ni pegar).
4. Escribe el código y la cuenta queda activa. Luego ingresa con tu usuario.

Sin configurar correo, el email aparece en la consola donde corre `runserver` (copia el enlace desde ahí).
