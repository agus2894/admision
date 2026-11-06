# 🏥 Sistema de Gestión de Admisiones UTI - Guía Completa

Documento único con toda la información que necesitas.

---

## 🚀 ACCESO INMEDIATO

**El sistema ya está funcionando. Accede directamente:**

```
URL:        http://localhost:8000
Usuario:    demo
Contraseña: Demo123!
```

---

## 🎯 Elige tu Sección

### 👤 Soy Usuario Final (Médico, Enfermero, Administrativo)
→ [Ir a Guía de Usuario](#-guía-para-usuarios-finales)

### 🔧 Soy Técnico o Administrador  
→ [Ir a Guía Técnica](#-guía-técnica)

### ❓ No sé por dónde empezar
→ [Ir a Primeros Pasos](#-primeros-pasos)

---

## 📖 Guía para Usuarios Finales

### Acceder al Sistema

1. Abre tu navegador (Chrome, Firefox, Safari)
2. Ve a: **http://localhost:8000**
3. Inicia sesión:
   - Usuario: `demo`
   - Contraseña: `Demo123!`

### Panel Principal (Dashboard)

Verás el estado general de la UTI con:
- Cantidad de pacientes
- Camas ocupadas  
- Alertas activas
- Métricas del mes

### Crear un Nuevo Paciente

1. Ve a **"Pacientes"** → **"+ Nuevo Paciente"**
2. Completa:
   - Nombre y Apellido
   - Documento (DNI/CI)
   - Fecha de nacimiento
   - Teléfono de emergencia (opcional)
3. Presiona **"Guardar"**

### Registrar Nueva Admisión

**Paso 1: Iniciar**
1. Ve a **"Nueva Admisión"**
2. Selecciona el paciente
3. Presiona **"Siguiente"**

**Paso 2: Datos de Ingreso**
- Cama/Unidad: `Cama 04 - UTI`
- Procedencia: Guardia / Quirófano / Sala General
- Diagnóstico: Describe el diagnóstico principal
- Motivo: Explica brevemente por qué ingresa
4. Presiona **"Siguiente"**

**Paso 3: Completar Checklist**

Responde las preguntas organizadas por categoría:

| Categoría | Ejemplos de Preguntas |
|-----------|----------------------|
| 🫁 Respiratorio | Estado respiratorio, Frecuencia, Oxigenación |
| ❤️ Cardiovascular | Presión arterial, Frecuencia cardíaca |
| 🧠 Neurológico | Nivel de conciencia, Pupilas |
| 💧 Fluidos | Balance de entrada/salida |
| 👤 Otros | Temperatura, Peso |

**Tipos de respuesta:**
- **Sí/No**: Presiona el botón
- **Número**: Escribe el valor (ej: 120)
- **Opciones**: Elige de la lista
- **Texto**: Describe lo que observas

5. Presiona **"Guardar Checklist"**

### Revisar y Responder Alertas

El sistema genera alertas automáticamente:

🔴 **CRÍTICA** → Peligro inmediato → ¡Atiende YA!
🟠 **ALTA** → Importante → Atiende pronto
🟡 **MEDIA** → Debes saber → Revisa en el turno
⚪ **BAJA** → Información → Solo referencia

Para cada alerta:
1. Lee el problema detectado
2. Revisa las sugerencias de acción
3. Toma las acciones necesarias
4. Presiona "Alerta Revisada"

### Actualizar Datos

1. Busca la admisión del paciente
2. Presiona **"Editar Checklist"**
3. Actualiza los valores que cambiaron
4. Presiona **"Actualizar"**

El sistema reevalúa automáticamente y genera nuevas alertas si es necesario.

### Imprimir Resumen

1. Abre la admisión del paciente
2. Presiona **"Imprimir Resumen"**
3. Presiona `Ctrl + P` para imprimir o guardar PDF

Se imprimirá:
- Datos del paciente
- Información de ingreso
- Respuestas del checklist
- Todas las alertas

### Cerrar una Admisión

Cuando el paciente se da de alta:

1. Abre la admisión
2. Presiona **"Cerrar Admisión"**
3. Selecciona motivo:
   - ✅ Alta de UTI
   - ➡️ Derivación
   - ☠️ Óbito
4. Presiona **"Confirmar Cierre"**

### Cambiar tu Contraseña

1. Presiona tu nombre (esquina superior derecha)
2. Elige **"Cambiar Contraseña"**
3. Ingresa contraseña actual y nueva
4. Presiona **"Actualizar"**

### Cerrar Sesión

1. Presiona tu nombre (arriba a la derecha)
2. Elige **"Cerrar Sesión"**

---

## 🔧 Guía Técnica

### Requisitos Previos

- Python 3.8+
- Conexión a internet local
- Navegador web

### Estado del Sistema

✅ **Verificado y Funcionando:**
- Entorno virtual creado
- Django 4.2.28 instalado
- Base de datos SQLite configurada
- Catálogo clínico cargado (5 categorías, 11 ítems)
- Usuario demo creado
- Servidor en http://localhost:8000

### Iniciar el Servidor

En Linux/Mac:
```bash
cd /home/Agustin/Escritorio/Admision
source .venv/bin/activate
python manage.py runserver
```

En Windows:
```bash
cd Admision
.venv\Scripts\activate
python manage.py runserver
```

Verás: `Starting development server at http://127.0.0.1:8000/`

### Detener el Servidor

Presiona en la terminal: `Ctrl + C`

### Crear Nuevo Usuario

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para ingresar:
- Username
- Email
- Contraseña

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Preparar Base de Datos

```bash
python manage.py migrate
python manage.py seed_uti_catalog
```

### Acceder al Panel Admin

1. Ve a: http://localhost:8000/admin
2. Inicia sesión con usuario y contraseña
3. Acceso a:
   - Pacientes
   - Admisiones
   - Checklists
   - Alertas
   - Reglas clínicas

---

## ❓ Primeros Pasos

### Si es tu Primera Vez

**Tiempo total: 30 minutos**

1. **Accede al sistema** (2 min)
   - URL: http://localhost:8000
   - Usuario: demo / Demo123!

2. **Explora el Dashboard** (5 min)
   - Revisa las métricas
   - Entiende la interfaz

3. **Crea un paciente de prueba** (5 min)
   - Nombre: Juan García
   - DNI: 12345678
   - Fecha: 1980-05-15

4. **Registra una admisión** (10 min)
   - Cama: 01
   - Diagnóstico: Neumonía
   - Completa checklist

5. **Revisa las alertas** (3 min)
   - Ve a Alertas
   - Observa las generadas automáticamente

6. **Practica más** (5 min)
   - Crea otros pacientes
   - Completa más checklists
   - Experimenta con el sistema

### Si Necesitas Ayuda

| Problema | Solución |
|----------|----------|
| No puedo acceder | Verifica: http://localhost:8000 y usuario/contraseña |
| El servidor no inicia | Activa el entorno: `source .venv/bin/activate` |
| Error de base de datos | Ejecuta: `python manage.py migrate` |
| Datos no se guardan | Recarga la página (F5) y intenta de nuevo |
| Olvidé la contraseña | Crea un nuevo usuario: `python manage.py createsuperuser` |
| El puerto está en uso | Usa otro puerto: `python manage.py runserver 8001` |

---

## 📊 Características del Sistema

### Gestión de Pacientes
- ✅ Fichas clínicas completas
- ✅ Información personal
- ✅ Historial de admisiones
- ✅ Contactos de emergencia

### Admisiones a UTI
- ✅ Registro de ingreso
- ✅ Asignación de cama
- ✅ Información de procedencia
- ✅ Diagnóstico y motivo

### Checklist Clínico
- ✅ 5 categorías de evaluación
- ✅ 11 parámetros de seguimiento
- ✅ Tipos: Booleano, Selección, Numérico, Texto
- ✅ Detección automática de parámetros críticos

### Alertas Automáticas
- ✅ Motor de reglas clínicas
- ✅ 4 niveles de severidad
- ✅ Generación automática
- ✅ Sugerencias de acciones
- ✅ Historial completo

### Dashboard y Reportes
- ✅ Métricas de la UTI
- ✅ Ocupación de camas
- ✅ Reportes imprimibles
- ✅ Análisis de datos

### Seguridad
- ✅ Autenticación de usuarios
- ✅ Control de acceso
- ✅ Registro de auditoría
- ✅ Contraseñas encriptadas

---

## 🎓 Preguntas Frecuentes

**P: ¿Se pierden los datos si se apaga la computadora?**
R: No, los datos se guardan en la base de datos SQLite.

**P: ¿Puedo trabajar sin internet?**
R: No necesitas internet externa, pero sí conexión local.

**P: ¿Quién puede ver mis datos?**
R: Solo otros usuarios del sistema con acceso.

**P: ¿Puedo editar datos antiguos?**
R: Sí, presiona "Editar" en cualquier admisión.

**P: ¿Qué pasa si ingreso un valor incorrecto?**
R: Abre la admisión y corrígelo en "Editar Checklist".

**P: ¿Se recuperan datos borrados?**
R: Contacta al administrador, puede haber copias de seguridad.

**P: ¿Cuánto tiempo tarda el sistema en reaccionar?**
R: Las alertas se generan automáticamente al guardar.

**P: ¿Puedo crear múltiples usuarios?**
R: Sí, ejecuta: `python manage.py createsuperuser`

---

## 💡 Consejos Importantes

✅ **Sé preciso** con los datos que ingresas → Afectan las alertas
✅ **Completa regularmente** el checklist → Mejor seguimiento
✅ **Revisa todas las alertas** → No ignores notificaciones
✅ **Documenta todo** → Usa el campo de notas
✅ **Actualiza cambios rápido** → Sistema reacciona en tiempo real
✅ **Cierra sesión** → Seguridad de tus datos
✅ **Haz backups** → Guarda copias de la base de datos

---

## 🗂️ Estructura del Proyecto

```
Admision/
├── manage.py              # Comando principal de Django
├── db.sqlite3            # Base de datos
├── requirements.txt      # Dependencias (Django 4.2.28)
├── README.md            # Presentación
├── GUIA_COMPLETA.md     # Este archivo
├── .venv/               # Entorno virtual
├── apps/
│   ├── pacientes/       # Gestión de pacientes
│   ├── admisiones/      # Admisiones a UTI
│   ├── reglas/          # Motor de alertas
│   └── dashboard/       # Panel de métricas
├── config/              # Configuración de Django
├── static/              # CSS, JS, imágenes
└── templates/           # HTML del proyecto
```

---

## 📚 Información Adicional

### Motor de Alertas

El sistema evalúa automáticamente los datos contra reglas clínicas y genera alertas. Cada alerta incluye:
- Descripción del problema
- Nivel de severidad
- Sugerencias de acción
- Timestamp de generación

### Catálogo Clínico Disponible

| # | Categoría | Ítems | Ejemplos |
|---|-----------|-------|----------|
| 1 | Sistema Respiratorio | 3 | Estado, Frecuencia, Oxigenación |
| 2 | Sistema Cardiovascular | 2 | Presión, Frecuencia cardíaca |
| 3 | Sistema Neurológico | 2 | Conciencia, Pupilas |
| 4 | Balance de Fluidos | 2 | Entrada, Salida |
| 5 | Otros Parámetros | 2 | Temperatura, Peso |

**Total: 11 ítems de evaluación**

### Mejoras Incluidas en esta Versión

✅ README mejorado (atractivo para usuarios)
✅ Motor de alertas automático
✅ Interfaz simplificada
✅ Documentación completa en español
✅ Sistema de usuarios seguro
✅ Datos de demostración listos
✅ Guía única consolidada

---

## 🚀 Checklist Final

Antes de comenzar:
- [ ] Accedí a http://localhost:8000
- [ ] Inicié sesión con demo / Demo123!
- [ ] Vi el dashboard
- [ ] Creé un paciente de prueba
- [ ] Registré una admisión
- [ ] Completé un checklist
- [ ] Revisé las alertas generadas
- [ ] Guardé esta guía para referencia futura

---

## 📞 Soporte Rápido

| Necesitas... | Consulta... |
|-------------|-----------|
| Empezar YA | Accede a http://localhost:8000 |
| Guía simple | Lee la sección "Guía para Usuarios Finales" |
| Información técnica | Lee la sección "Guía Técnica" |
| Problema específico | Ve a la sección "Primeros Pasos" |
| Saber qué hacer | Lee "Preguntas Frecuentes" |
| Crear usuarios | Lee "Crear Nuevo Usuario" en Guía Técnica |

---

## ✅ Estado del Sistema

```
✓ Servidor:        Funcionando en http://localhost:8000
✓ Base de datos:   Lista y configurada
✓ Usuario demo:    Disponible (demo / Demo123!)
✓ Catálogo:        Cargado (5 categorías, 11 ítems)
✓ Motor alertas:   Operacional
✓ Seguridad:       Implementada
✓ Documentación:   Completa en español
```

**Todo está listo para usar. Solo accede y comienza.** 🎉

---

*Sistema de Gestión de Admisiones UTI - v1.0*
*Actualizado: Noviembre 2026*
