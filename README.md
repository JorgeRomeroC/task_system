# 🚀 Sistema de Gestión de Tareas - Besimplit Challenge

Sistema completo de gestión de tareas desarrollado con Django, Django Rest Framework, HTMX y Tailwind CSS. Implementa todas las funcionalidades requeridas y los tres bonus opcionales del desafío técnico.

## 📋 Características Implementadas

### ✅ Funcionalidades Principales (Requeridas)
- ✅ **CRUD completo de tareas** (Crear, Leer, Actualizar, Eliminar)
- ✅ **Interacciones sin recargar página** usando HTMX
- ✅ **API REST completa** con Django Rest Framework
- ✅ **Interfaz moderna y responsive** con Tailwind CSS
- ✅ **Filtros y búsqueda** en tiempo real
- ✅ **Toggle de estado** (completada/pendiente)
- ✅ **Validaciones** de datos

### 🎁 Bonus Implementados
## Plantilla Admin: https://tailadmin.com/docs/installation

#### Bonus A: UI/UX Mejorado ✨
- Animaciones suaves en todas las interacciones
- Transiciones CSS personalizadas
- Filtros interactivos (completadas/pendientes/todas)
- Búsqueda en tiempo real con delay de 300ms
- Estados hover mejorados con efectos visuales
- Diseño responsive para móviles, tablets y desktop
- Tarjetas de estadísticas con iconos

#### Bonus B: Dashboard Analítico 📊
- Métricas en tiempo real (Total, Completadas, Pendientes)
- Estadísticas visuales con tarjetas informativas
- Cálculo automático de porcentajes

#### Bonus C: Exportación de Reportes 📄
- **Exportar a CSV**: Compatible con Excel, codificación UTF-8
- **Exportar a Excel (.xlsx)**: 
  - Hoja de Tareas con formato profesional
  - Hoja de Estadísticas con métricas
  - Estilos: colores, bordes, alineación
- **Exportar a PDF**: 
  - Reporte profesional con estadísticas
  - Tabla de tareas formateada
  - Diseño con colores corporativos

## 🛠️ Stack Tecnológico

- **Backend:** Django 5.2.7
- **API:** Django Rest Framework 3.16.1
- **Frontend:** HTMX 1.9.10 + Tailwind CSS (CDN)
- **Interactividad:** Alpine.js 3.x
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Exportación:** ReportLab (PDF) + OpenPyXL (Excel)
- **Testing:** Django Test Framework
- **Iconos:** Font Awesome 6.5.1

## 📦 Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)
- **Node.js 18+** y npm (para el template admin)
- Git

### Pasos de Instalación

#### 1. Clonar el repositorio

```bash
git clone https://github.com/JorgeRomeroC/task_system.git
cd task_system
```

#### 2. Crear y activar entorno virtual

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

#### 3.1 Instalar dependencias de Node.js (Template Admin)

```bash
npm install
```

Las dependencias de Python incluyen:
- Django 5.2.7
- djangorestframework 3.16.1
- django-cors-headers 4.3.1
- openpyxl 3.1.2 (Excel)
- reportlab 4.0.7 (PDF)
- django-extensions 3.2.3


#### 5. Crear directorios necesarios

```bash
mkdir -p static
mkdir -p media
```

#### 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Esto creará:
- Base de datos SQLite (`db.sqlite3`)
- Tablas necesarias para el sistema
- Índices optimizados para consultas

#### 7. Crear datos de demostración (Recomendado)

```bash
# Crear tareas de prueba
python manage.py create_demo_tasks

#Crear usuarios de prueba
python manage.py create_test_users

# Este comando genera:
- **Superusuario**: admin@test.com / admin123
- **Usuario regular**: user@test.com / user123
```

**Opciones del comando:**
```bash
# Eliminar tareas existentes y crear 15 nuevas (default)
python manage.py create_demo_tasks --clear

# Crear 30 tareas de demostración
python manage.py create_demo_tasks --count=30

# Combinar opciones
python manage.py create_demo_tasks --clear --count=25
```

Este comando creará tareas de ejemplo relacionadas con desarrollo de software, con estados mixtos (completadas/pendientes).

#### 8. Crear superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear usuario, email y contraseña.

#### 8.1 Compilar assets del template admin (Opcional)

Si deseas usar el template admin completo con Webpack:

```bash
npm run dev
```

Este comando compilará los assets CSS y JS del template admin.

#### 9. Ejecutar servidor de desarrollo

**Opción 1: Solo Django (recomendado para empezar)**

```bash
python manage.py runserver
```

O especificar puerto:
```bash
python manage.py runserver 8000
```

**Opción 2: Django + Webpack Dev Server (con hot reload del template admin)**

Terminal 1 - Django:
```bash
python manage.py runserver
```

Terminal 2 - Webpack (en paralelo):
```bash
npm run start
```

Esta opción es útil si estás desarrollando/modificando el template admin y quieres ver los cambios en tiempo real.

### ✅ Verificación de Instalación

Después de ejecutar el servidor, deberías poder acceder a:

- **Aplicación principal:** http://localhost:8000
- **API REST:** http://localhost:8000/api/tasks/
- **Panel de administración:** http://localhost:8000/admin
- **Documentación API (navegable):** http://localhost:8000/api/tasks/

Si todo está correcto, verás:
- 15 tareas de demostración (si ejecutaste el comando)
- Métricas en las tarjetas superiores
- Barra de búsqueda funcional
- Botón de exportación

## 🔗 Endpoints y Funcionalidades

### Frontend (Interfaz Web con HTMX)

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Vista principal con lista de tareas |
| `/create/` | POST | Crear nueva tarea (HTMX) |
| `/<id>/` | GET | Obtener formulario de edición |
| `/<id>/update/` | POST | Actualizar tarea existente |
| `/<id>/toggle/` | POST | Alternar estado completado/pendiente |
| `/<id>/delete/` | DELETE | Eliminar tarea |
| `/partial/` | GET | Actualización parcial de lista (filtros/búsqueda) |

### API REST (JSON)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/tasks/` | GET | Listar todas las tareas |
| `/api/tasks/` | POST | Crear nueva tarea |
| `/api/tasks/{id}/` | GET | Detalle de una tarea |
| `/api/tasks/{id}/` | PUT/PATCH | Actualizar tarea |
| `/api/tasks/{id}/` | DELETE | Eliminar tarea |
| `/api/tasks/{id}/toggle/` | POST | Toggle de estado |

**Filtros disponibles en API:**
- `?search=texto` - Buscar en título y descripción
- `?completed=true` - Solo tareas completadas
- `?completed=false` - Solo tareas pendientes

### Exportación de Reportes

| Ruta | Formato | Descripción |
|------|---------|-------------|
| `/export/csv/` | CSV | Archivo CSV compatible con Excel |
| `/export/excel/` | XLSX | Excel con 2 hojas (Tareas + Estadísticas) |
| `/export/pdf/` | PDF | Reporte PDF profesional |

**Acceso:** Click en el botón "Exportar" en la interfaz y selecciona el formato deseado.

## 🎨 Uso de la Aplicación

### Crear una Tarea

1. En la sección "Nueva Tarea", ingresa:
   - **Título** (obligatorio, mínimo 3 caracteres)
   - **Descripción** (opcional)
2. Click en "Crear Tarea"
3. La tarea aparecerá inmediatamente en la lista (sin recargar)

### Editar una Tarea

1. Pasa el mouse sobre una tarea
2. Click en el icono de **editar** (lápiz)
3. Modifica los campos
4. Click en "Guardar" o "Cancelar"

### Completar/Reactivar Tarea

- Click en el **círculo** a la izquierda de la tarea
- El estado cambia instantáneamente
- Las completadas muestran ✓ y estilo diferente

### Eliminar Tarea

1. Pasa el mouse sobre una tarea
2. Click en el icono de **eliminar** (papelera)
3. Confirma la acción
4. La tarea desaparece con animación

### Buscar y Filtrar

**Búsqueda:**
- Escribe en el campo "Buscar tareas..."
- Los resultados se actualizan automáticamente (300ms delay)
- Busca en título y descripción

**Filtros:**
- **Todas:** Muestra todas las tareas
- **Pendientes:** Solo tareas sin completar
- **Completadas:** Solo tareas completadas

### Exportar Reportes

1. Click en botón verde "Exportar"
2. Selecciona formato (CSV, Excel o PDF)
3. El archivo se descarga automáticamente con timestamp

**Contenido de cada formato:**
- **CSV:** Lista simple de tareas
- **Excel:** 2 hojas (Tareas detalladas + Estadísticas)
- **PDF:** Reporte visual con gráficos y tablas

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests del proyecto
python manage.py test apps.tasks

```

### Cobertura de Tests

El proyecto incluye tests para:
- ✅ Modelo Task (creación, métodos, validaciones)
- ✅ API REST (CRUD completo, filtros, búsquedas)
- ✅ Serializadores (validaciones)
- ✅ Toggle de estado
- ✅ Eliminación de tareas

**Resultado esperado:** 12 tests pasando

## 📁 Estructura del Proyecto

```
task_system/
│
├── apps/
│   └── tasks/
│       ├── management/
│       │   └── commands/
│       │       └── create_demo_tasks.py    # Comando para datos demo
│       ├── migrations/                      # Migraciones de BD
│       ├── __init__.py
│       ├── admin.py                         # Configuración admin Django
│       ├── api_views.py                     # ViewSets API REST
│       ├── apps.py                          # Configuración de la app
│       ├── export_views.py                  # Vistas de exportación
│       ├── models.py                        # Modelo Task
│       ├── serializers.py                   # Serializadores DRF
│       ├── tests.py                         # Tests unitarios
│       ├── urls.py                          # URLs de la app
│       └── views.py                         # Vistas frontend (HTMX)
│
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                          # Configuración base
│   │   ├── local.py                         # Config desarrollo
│   │   └── prod.py                          # Config producción
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py                              # URLs principales
│   └── wsgi.py
│
├── templates/
│   ├── tasks/
│   │   ├── partials/
│   │   │   ├── task_edit_form.html          # Formulario edición
│   │   │   ├── task_form.html               # Formulario creación
│   │   │   ├── task_item.html               # Card de tarea
│   │   │   └── task_list_partial.html       # Lista actualizable
│   │   └── task_list.html                   # Vista principal
│   └── base.html                            # Template base
│
├── static/                                  # Archivos estáticos
│   ├── css/
│   ├── images/
│   ├── js/
│   └── partials/
│
├── .env                                     # Variables de entorno (ignorado en git) ENVIADO POR CORREO
├── .gitignore                               # Archivos ignorados
├── .gitattributes
├── db.sqlite3                               # Base de datos (ignorado en git)
├── manage.py                                # CLI de Django
├── requirements.txt                         # Dependencias Python
└── README.md                                # Este archivo
```

## 💡 Decisiones Técnicas

### Arquitectura del Backend

#### 1. Modularización de Settings
Se separó la configuración en tres archivos:
- **`base.py`**: Configuración común para todos los entornos
- **`local.py`**: Configuración específica de desarrollo (DEBUG=True, logging)
- **`prod.py`**: Configuración de producción (seguridad, optimizaciones)

**Ventajas:**
- Fácil cambio entre entornos
- Evita errores de configuración en producción
- Configuraciones sensibles separadas

#### 2. Separación de Vistas
Se crearon tres archivos de vistas con responsabilidades específicas:
- **`views.py`**: Vistas que renderizan HTML (frontend con HTMX)
- **`api_views.py`**: ViewSets para API REST (Django REST Framework)
- **`export_views.py`**: Funciones de exportación (CSV, Excel, PDF)

**Ventajas:**
- Código más organizado y mantenible
- Separación de responsabilidades
- Facilita testing y debugging

#### 3. Modelo Task Optimizado
```python
class Task(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['completed']),
        ]
```

**Características:**
- **Índices**: En campos frecuentemente consultados (created_at, completed)
- **Validadores**: A nivel de modelo (MinLengthValidator)
- **Método toggle_completed()**: Encapsula lógica de cambio de estado
- **Timestamps automáticos**: created_at y updated_at

#### 4. Serializadores Múltiples
- **TaskSerializer**: Completo, para crear/actualizar (incluye fechas formateadas)
- **TaskListSerializer**: Optimizado para listados (campos reducidos)
- **TaskToggleSerializer**: Específico para cambiar estado

**Ventaja:** Reduce payload de la API y mejora rendimiento

#### 5. API REST con Respuestas Estructuradas
```json
{
  "success": true,
  "message": "Tarea creada exitosamente",
  "data": { ... }
}
```

**Beneficios:**
- Respuestas consistentes
- Fácil manejo de errores en frontend
- Mejor experiencia de desarrollo

### Frontend

#### 6. HTMX para Interactividad
Se usa HTMX para todas las interacciones dinámicas:
- Crear, editar, eliminar tareas
- Búsqueda con debounce (300ms)
- Filtros en tiempo real
- Toggle de estado

**Ventajas:**
- Sin JavaScript personalizado complejo
- Código HTML declarativo
- Menos bugs del lado del cliente
- Carga inicial más rápida

#### 7. Tailwind CSS vía CDN
**Decisión:** Usar CDN en lugar de build process

**Pros:**
- ✅ Configuración cero
- ✅ Desarrollo más rápido
- ✅ No requiere Node.js
- ✅ Suficiente para el alcance del proyecto

**Contras:**
- ❌ Archivo CSS más grande (~3MB, aunque con gzip ~300KB)
- ❌ No se puede purgar clases no usadas

**Justificación:** Para este proyecto de demostración, la rapidez de desarrollo supera las desventajas de tamaño.

#### 8. Alpine.js para Estado Local
Se usa Alpine.js solo para:
- Menú desplegable de exportación
- Estado de edición de tareas

**Ventaja:** Ligero (15KB) y perfecto para interacciones simples

### Base de Datos

#### 9. SQLite vs PostgreSQL
**Desarrollo:** SQLite
- ✅ Sin instalación adicional
- ✅ Archivo único portable
- ✅ Suficiente para demo y desarrollo

**Producción:** PostgreSQL (configurado pero no obligatorio)
- ✅ Mejor rendimiento con múltiples usuarios
- ✅ Características avanzadas
- ✅ Mejor para escalabilidad

### Exportación

#### 10. Tres Formatos de Exportación
**CSV:**
- Simplicidad y compatibilidad universal
- Codificación UTF-8 con BOM (para Excel en Windows)

**Excel (.xlsx):**
- Formato profesional con estilos
- Dos hojas: datos + estadísticas
- Usa openpyxl (librería pura Python)

**PDF:**
- Reportes profesionales con diseño
- ReportLab para generación
- Tablas, estadísticas y branding

## 🎯 Trade-offs Realizados

### 1. Tailwind CDN vs Build Process
**Elegido:** CDN
- **Ventaja:** Desarrollo 5x más rápido, sin configuración
- **Desventaja:** +2.7MB adicionales (mitigado con CDN cache)
- **Justificación:** Proyecto de demostración prioriza velocidad de desarrollo

### 2. SQLite vs PostgreSQL
**Elegido:** SQLite en desarrollo
- **Ventaja:** Cero configuración, portable
- **Desventaja:** No recomendado para producción con alta concurrencia
- **Justificación:** Adecuado para desarrollo y demo, fácil migrar a PostgreSQL

### 3. Sin Autenticación de Usuarios
**Decisión:** No implementar según requisitos del desafío
- **Ventaja:** Simplifica la demostración de funcionalidades core
- **Desventaja:** No es production-ready sin auth
- **Justificación:** Requisito explícito del desafío ("NO es necesario")

### 4. HTMX vs React/Vue
**Elegido:** HTMX
- **Ventaja:** HTML declarativo, menos complejidad, sin build step
- **Desventaja:** Limitado para SPA complejas
- **Justificación:** Perfecto para este tipo de aplicación CRUD

### 5. Templates Parciales vs JSON API + JS
**Elegido:** Templates parciales (HTMX)
- **Ventaja:** Menor complejidad, renderizado en servidor
- **Desventaja:** Menos flexible que JSON + framework JS
- **Justificación:** Mejor para este proyecto, cumple todos los requisitos

## 🚀 Mejoras Futuras (Con Más Tiempo)

### Funcionalidades
1. **Sistema de autenticación completo**
   - Login/Logout
   - Registro de usuarios
   - Tareas por usuario
   
2. **Colaboración**
   - Asignar tareas a usuarios
   - Comentarios en tareas
   - Notificaciones

3. **Gestión avanzada**
   - Categorías y etiquetas
   - Prioridades (alta, media, baja)
   - Fechas límite y recordatorios
   - Subtareas

4. **Dashboard mejorado**
   - Gráficos interactivos (Chart.js)
   - Estadísticas históricas
   - Análisis de productividad

### Técnicas
5. **WebSockets**
   - Actualizaciones en tiempo real
   - Notificaciones push
   - Sincronización multi-dispositivo

6. **Optimizaciones**
   - Caché con Redis
   - Paginación de tareas
   - Lazy loading de imágenes/datos

7. **Testing**
   - Tests E2E con Playwright
   - Cobertura >90%
   - Tests de carga

8. **DevOps**
   - Docker Compose completo
   - CI/CD con GitHub Actions
   - Deploy automático

9. **Features UX**
   - Drag & Drop para reordenar
   - Modo oscuro
   - Atajos de teclado
   - PWA (Progressive Web App)

10. **Internacionalización**
    - Soporte multi-idioma
    - Formatos de fecha/hora por región

## 📝 Comandos Útiles

### Desarrollo
```bash
# Crear nueva migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Generar datos demo
python manage.py create_demo_tasks --clear --count=20
python manage.py create_test_users

# Shell interactivo mejorado
python manage.py shell_plus  # Requiere django-extensions

# Servidor de desarrollo Django
python manage.py runserver
python manage.py runserver 0.0.0.0:8000  # Accesible en red local

# Template Admin - Compilar assets (desarrollo)
npm run dev

# Template Admin - Webpack dev server con hot reload
npm run start

# Template Admin - Build de producción
npm run build
```

### Testing
```bash
# Ejecutar tests de la aplicación
python manage.py test apps.tasks
```

### Producción
```bash
# Colectar archivos estáticos
python manage.py collectstatic --no-input

# Verificar configuración
python manage.py check --deploy

# Ejecutar con gunicorn (producción)
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 👨‍💻 Desarrollado por

**Jorge Romero**  
Desarrollador Full Stack  
Chile, Octubre 2025

## 📧 Contacto y Entrega

Este proyecto fue desarrollado como parte del desafío técnico para **Besimplit**.

**Envío:** bastian@besimplit.com

## 📄 Licencia

Este proyecto es parte de un desafío técnico para Besimplit.

---

## 🎓 Notas Adicionales

### Cumplimiento del Desafío

✅ **Funcionalidad Principal**: CRUD completo con HTMX  
✅ **Requisitos Técnicos**: Django + DRF + HTMX + Tailwind  
✅ **Bonus A (UI/UX)**: Animaciones, filtros, responsive  
✅ **Bonus B (Dashboard)**: Estadísticas en tiempo real  
✅ **Bonus C (Exportación)**: CSV + Excel + PDF  
✅ **README Completo**: Instrucciones detalladas  
✅ **Datos Demo**: Comando create_demo_tasks  
✅ **Tests**: Cobertura de funcionalidades principales  

### Tiempo de Desarrollo

- **Backend (Modelos, API, Vistas)**: ~3 horas
- **Frontend (Templates, HTMX, Tailwind)**: ~3 horas
- **Exportación (CSV, Excel, PDF)**: ~2 horas
- **Tests y Documentación**: ~2 horas
- **Total**: ~10 horas

### Recursos y Aprendizajes

Durante el desarrollo se consultaron:
- Documentación oficial de Django 5.2
- Documentación de HTMX
- Documentación de Django REST Framework
- ReportLab para generación de PDFs
- OpenPyXL para archivos Excel
- Tailwind CSS para el diseño

---

**¡Gracias por revisar este proyecto!**
