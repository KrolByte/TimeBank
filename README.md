# ⏳ TimeBank — Plataforma de Intercambio de Habilidades Estudiantiles

**TimeBank** es una aplicación web desarrollada en Django que funciona como un banco de tiempo universitario. Permite a los estudiantes ofrecer tutorías, asesorías y habilidades a otros compañeros utilizando **horas** como moneda de intercambio, para luego redimir el tiempo acumulado por certificados de servicio social o incentivos académicos.

---

## 🎯 Propósito del Proyecto

* **Economía colaborativa estudiantil:** Facilita el apoyo académico y técnico entre pares sin barreras económicas.
* **Sistema de horas:** Cada estudiante cuenta con un saldo disponible para solicitar servicios (`hours_balance`) y un historial de tiempo ganado (`accumulated_hours`).
* **Incentivos institucionales:** Las horas acumuladas pueden canjearse por certificados de servicio social, incentivos de calificación, bonos de cafetería o cupos en cursos presenciales.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Django (ORM, MVT, Django Admin)
* **Base de datos:** SQLite3 (con respaldo de datos iniciales en JSON mediante *fixtures*)
* **Frontend:** HTML5, Django Template Language (DTL), Bootstrap 5, Bootstrap Icons

---

## 🗄️ Arquitectura de Datos (`Services`)

El modelo relacional de la aplicación está compuesto por las siguientes entidades:

* **`UserProfile`:** Extiende el modelo `User` de Django (`OneToOneField`) con código estudiantil, teléfono, propósito en la plataforma, saldo de horas y horas acumuladas.
* **`Category`:** Clasificación de los servicios ofrecidos (ej. Programación, Académico, Diseño, Idiomas).
* **`ServiceOffer`:** Servicios publicados por los estudiantes, vinculados a un proveedor (`UserProfile`) y una categoría.
* **`Schedule`:** Disponibilidad horaria (día de la semana, hora de inicio y fin) asociada a cada oferta de servicio.
* **`Exchange`:** Registro de transacciones entre un solicitante y un proveedor, soportando intercambio por horas o trueque directo (`offered_back`), estado y calificación.
* **`Benefit`:** Historial de beneficios institucionales solicitados y redimidos por los estudiantes.

---

## 📌 Funcionalidades Implementadas (Fase Actual: Consultas `Read`)

* **Catálogo de Servicios (`/`):** Visualización dinámica de las ofertas registradas en la base de datos junto con su categoría, proveedor, estado y horarios disponibles.
* **Historial de Intercambios (`/intercambios/`):** Consulta tabular de los intercambios registrados, modalidad (saldo de horas o trueque), duración, estado y calificación.
* **Beneficios Redimidos (`/beneficios/`):** Listado de incentivos institucionales solicitados, horas descontadas y estado de entrega.
* **Panel Administrativo (`/admin/`):** Gestión completa de registros y relaciones del sistema.

---

## 🚀 Instalación y Ejecución en otro Equipo

Para levantar el proyecto en un computador nuevo y cargar los datos de prueba:

1. **Clonar el repositorio e ingresar a la carpeta:**
   ```bash
   git clone https://github.com/KrolByte/TimeBank.git
   cd TimeBank
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar Django:**
   ```bash
   pip install django
   ```

4. **Construir las tablas de la base de datos:**
   ```bash
   python manage.py migrate
   ```

5. **Cargar los datos iniciales desde el fixture:**
   ```bash
   python manage.py loaddata initial_data.json
   ```

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   Accede a la aplicación en `http://127.0.0.1:8000/` y al panel administrativo en `http://127.0.0.1:8000/admin/`.