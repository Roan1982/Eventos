# ✅ CHECKLIST DE TESTING - REJUNTADA

## 🔧 Error Corregido
✅ **TemplateSyntaxError en detail.html**
- **Problema:** `{% with %}` mal anidado en líneas 140-143
- **Solución:** Usé `{% with m=event.cover_media|default:media_list.0 %}` para simplificar
- **Solución 2:** Eliminé `{% endwith %}` sobrante en línea 179

## 📋 Tests Funcionales a Realizar

### 1. ✅ Autenticación (Login/Signup)

#### Login
- [ ] Acceder a `/accounts/login/`
- [ ] Verificar que aparece card centrada con diseño moderno
- [ ] Intentar login con credenciales incorrectas → debe mostrar error en alert rojo
- [ ] Login exitoso → debe redirigir a home (`/`) NO a perfil
- [ ] Verificar que aparece el nombre de usuario en navbar
- [ ] Verificar botón "Salir" visible

#### Signup
- [ ] Acceder a `/accounts/signup/`
- [ ] Verificar card centrada con diseño moderno
- [ ] Intentar registrar con contraseñas que no coinciden → debe mostrar error
- [ ] Intentar registrar con username ya existente → debe mostrar error
- [ ] Registro exitoso → debe crear cuenta y hacer login automático
- [ ] Verificar que aparece link "Inicia sesión aquí" en footer

### 2. ✅ Perfil de Usuario

- [ ] Estando logueado, ir a `/accounts/profile/`
- [ ] Verificar layout de 2 columnas (avatar izquierda, info derecha)
- [ ] Verificar que el avatar actual se muestra (si existe)
- [ ] Cambiar avatar → seleccionar imagen nueva
- [ ] Modificar nombre, apellido, teléfono, bio
- [ ] Click en "Guardar Cambios" → debe actualizar y mostrar mensaje de éxito
- [ ] Click en "Cancelar" → debe volver al home sin guardar
- [ ] Verificar que todos los labels tienen iconos FontAwesome

### 3. ✅ Home Page

- [ ] Acceder a `/`
- [ ] Verificar hero section azul con búsqueda
- [ ] Verificar sección de categorías con iconos
- [ ] Hacer click en una categoría → debe filtrar eventos
- [ ] Verificar "Últimos Eventos" con cards
- [ ] Hover en card de evento → debe elevarse y tener sombra
- [ ] Click en evento → debe ir a detalle

### 4. ✅ Explorar Eventos (List)

- [ ] Acceder a `/eventos/`
- [ ] Verificar sidebar con filtros organizados
- [ ] **Probar Select2 en desplegables:**
  - [ ] Click en select "Categoría" → debe abrir con búsqueda
  - [ ] Escribir en búsqueda → debe filtrar opciones
  - [ ] Seleccionar categoría → debe aplicar filtro
  - [ ] Click en "X" en select → debe limpiar selección
  - [ ] Verificar que select tiene estilo Bootstrap 5
- [ ] Filtrar por ciudad → debe mostrar resultados
- [ ] Filtrar por rango de precios → debe funcionar
- [ ] Ordenar por fecha, precio, nombre → debe reordenar
- [ ] Verificar grid de cards responsive
- [ ] Verificar badges con iconos (categoría, precio, fecha)
- [ ] Paginación → navegar entre páginas

### 5. ✅ Detalle de Evento

- [ ] Entrar a un evento con multimedia (ej: `/eventos/filetest/`)
- [ ] Verificar hero con imagen de portada y overlay
- [ ] Verificar que se muestra la imagen de portada correctamente
- [ ] Verificar galería/carousel de multimedia
- [ ] Click en flechas prev/next → debe cambiar imagen
- [ ] Verificar meta info con iconos (fecha, ubicación, precio, capacidad)
- [ ] Scroll a sección de reseñas
- [ ] Si hay reseñas, verificar que se muestran con estrellas
- [ ] Verificar formulario de contacto (si está habilitado)
- [ ] Botones de compartir (Twitter, Facebook, WhatsApp, Telegram)

### 6. ✅ Crear Evento

- [ ] Estando logueado, ir a `/eventos/crear/`
- [ ] Verificar título "Crear Nuevo Evento" con icono
- [ ] Verificar botón "Cancelar" en esquina superior derecha

#### Campos Básicos
- [ ] Llenar título, descripción
- [ ] **Probar Select2 en Categoría:**
  - [ ] Click en select → debe abrir con búsqueda
  - [ ] Buscar "Música" → debe filtrar y mostrar
  - [ ] Seleccionar categoría
  - [ ] Verificar que se puede buscar las 35 categorías

#### Fechas
- [ ] Seleccionar fecha inicio y hora
- [ ] Seleccionar fecha fin y hora
- [ ] Intentar fecha fin antes de inicio → debe dar error al enviar

#### Ubicación
- [ ] Llenar nombre del lugar, dirección, ciudad

#### Detalles
- [ ] Precio (puede ser 0 para gratis)
- [ ] Capacidad
- [ ] **Probar Select2 en Estado:**
  - [ ] Click en select → debe abrir con búsqueda
  - [ ] Seleccionar "Publicado"

#### Multimedia con FilePond
- [ ] **Verificar FilePond NO tapa botón "Guardar"**
- [ ] **Probar Drag & Drop:**
  - [ ] Arrastrar 1 imagen → debe mostrar preview
  - [ ] Arrastrar múltiples imágenes (3-5) → deben aparecer todas
  - [ ] Verificar que cada preview tiene altura de 170px
  - [ ] Arrastrar 10+ archivos → debe permitir solo 10
  - [ ] Scroll en lista de archivos si hay muchos
- [ ] **Probar Click para Seleccionar:**
  - [ ] Click en área FilePond → debe abrir explorador
  - [ ] Seleccionar imágenes → deben agregarse
- [ ] **Probar Validación:**
  - [ ] Intentar subir archivo de 15MB → debe rechazar (max 10MB)
  - [ ] Intentar subir PDF → debe rechazar (solo image/video)
- [ ] **Eliminar archivo de FilePond:**
  - [ ] Click en botón "Eliminar" de un preview → debe quitar archivo
- [ ] Enviar formulario con archivos → debe crear evento y subir media
- [ ] **Verificar que el botón "Guardar" está visible y accesible**

### 7. ✅ Editar Evento

- [ ] Ir a un evento propio → click "Editar"
- [ ] Verificar título "Editar Evento"
- [ ] Verificar alert info con fechas guardadas
- [ ] Modificar título, descripción

#### Multimedia Existente
- [ ] Verificar sección "Multimedia existente"
- [ ] Verificar que cada archivo tiene número
- [ ] **Probar Hover Overlay:**
  - [ ] Pasar mouse sobre una imagen → debe aparecer overlay oscuro
  - [ ] Verificar botones de basura (🗑️) y estrella (⭐)
  - [ ] Click en botón basura → imagen debe ponerse opaca con borde rojo
  - [ ] Click nuevamente en basura → debe volver a normal
  - [ ] Click en estrella → imagen debe marcarse como portada (borde amarillo)
  - [ ] Verificar que solo 1 imagen puede ser portada a la vez
- [ ] Marcar 2 imágenes para eliminar
- [ ] Cambiar imagen de portada
- [ ] Agregar 3 imágenes nuevas con FilePond
- [ ] Guardar cambios → verificar que se eliminaron, se cambió portada y se agregaron nuevas

#### Verificación Post-Edición
- [ ] Volver a editar el evento
- [ ] Verificar que las imágenes marcadas se eliminaron
- [ ] Verificar que la nueva portada tiene borde amarillo
- [ ] Verificar que las nuevas imágenes aparecen en multimedia existente

### 8. ✅ Eliminar Evento

- [ ] Ir a un evento propio → click "Eliminar"
- [ ] Verificar card de advertencia con diseño moderno
- [ ] Verificar que muestra preview del evento
- [ ] Verificar lista de consecuencias (eliminación de media, reseñas, etc.)
- [ ] Click en "Cancelar" → debe volver al evento
- [ ] Click nuevamente en "Eliminar" → click en "Confirmar Eliminación"
- [ ] Verificar que el evento fue eliminado
- [ ] Intentar acceder a la URL del evento eliminado → debe dar 404

## 🎨 Tests de UI/UX

### Responsive Design
- [ ] Probar en móvil (< 768px)
- [ ] Probar en tablet (768px - 1024px)
- [ ] Probar en desktop (> 1024px)
- [ ] Navbar collapsa en móvil
- [ ] Cards se apilan en móvil (1 columna)
- [ ] Formularios ocupan full width en móvil
- [ ] Select2 funciona bien en móvil (teclado virtual)

### Accesibilidad
- [ ] Navegación con teclado (Tab)
- [ ] Select2 accesible con teclado (Enter para abrir, flechas para navegar)
- [ ] Contraste de colores adecuado
- [ ] Iconos tienen texto alternativo

### Interacciones
- [ ] Hover en cards → elevación y sombra
- [ ] Hover en botones → cambio de color
- [ ] Hover en media cards → overlay aparece suavemente
- [ ] Transiciones suaves (300ms)
- [ ] Loading states en formularios

## 🐛 Tests de Errores

### Validación de Formularios
- [ ] Enviar form de evento vacío → debe mostrar errores en campos requeridos
- [ ] Enviar form con fecha inválida → debe mostrar error específico
- [ ] Enviar form con precio negativo → debe rechazar
- [ ] Enviar form con capacidad 0 → debe rechazar

### Permisos
- [ ] Sin login, intentar crear evento → debe redirigir a login
- [ ] Sin login, intentar editar evento → debe redirigir a login
- [ ] Con login, intentar editar evento de otro usuario → debe denegar acceso (403)
- [ ] Con login, intentar eliminar evento de otro usuario → debe denegar acceso

### Casos Edge
- [ ] Evento sin multimedia → no debe romper detalle
- [ ] Evento sin reseñas → debe mostrar "No hay reseñas"
- [ ] Evento sin categoría → debe funcionar
- [ ] Usuario sin avatar → debe mostrar placeholder

## 📊 Tests de Rendimiento

- [ ] Cargar home con 50+ eventos → debe ser fluido
- [ ] Cargar listado con paginación → < 2 segundos
- [ ] Subir 10 imágenes a la vez → debe procesar sin timeout
- [ ] Navegación entre páginas → sin lag

## 🔍 Tests de Funcionalidad Específica

### FilePond
- [ ] Preview de imágenes se ve correctamente
- [ ] Preview de videos muestra thumbnail
- [ ] Límite de 10MB por archivo funciona
- [ ] Límite de 10 archivos total funciona
- [ ] Archivos se envían correctamente con el formulario
- [ ] No hay errores de JavaScript en consola

### Select2
- [ ] Búsqueda en categorías funciona
- [ ] Las 35 categorías aparecen
- [ ] Se puede limpiar selección (X)
- [ ] Placeholder "Seleccionar..." aparece
- [ ] Texto "No hay resultados" aparece al buscar algo inexistente
- [ ] Funciona en todos los selects (categoría, estado, precio, orden)

### Hover Overlay
- [ ] Overlay solo aparece al hacer hover
- [ ] Botones son clicables
- [ ] Checkbox oculto se sincroniza con botón visual
- [ ] Radio button de portada se sincroniza
- [ ] Borde amarillo de portada se muestra correctamente
- [ ] Solo puede haber 1 portada a la vez

### Gallery Carousel
- [ ] Botón prev navega a imagen anterior
- [ ] Botón next navega a siguiente
- [ ] Click en thumbnail cambia imagen principal
- [ ] Videos se reproducen con controles
- [ ] Navegación circular (última → primera)

## ✅ Checklist de Integración

- [ ] Todos los templates usan el mismo diseño
- [ ] Todos los formularios tienen iconos en labels
- [ ] Todos los botones tienen iconos
- [ ] Todas las cards tienen sombras consistentes
- [ ] Todos los selects usan Select2
- [ ] Todas las subidas de archivos usan FilePond (donde aplica)
- [ ] Todos los mensajes de error son claros
- [ ] Todos los redirects funcionan correctamente

## 🎯 Bugs Conocidos Corregidos

✅ Login redirigía a perfil → Ahora redirige a home
✅ Templates inconsistentes → Todos uniformes
✅ FilePond tapaba botón guardar → Altura limitada
✅ No había Select2 → Implementado en todos los selects
✅ Perfil sin estilo → Rediseñado con 2 columnas
✅ TemplateSyntaxError en detail.html → Corregido `{% with %}` y `{% endwith %}`
✅ Debug prints en consola → Eliminados de views.py
✅ Solo 7 categorías → Ampliado a 35 categorías
✅ Sin hover actions en media → Implementado overlay con eliminar/portada

## 📝 Reporte de Bugs

Si encuentras algún bug durante el testing, documéntalo así:

```
### Bug #1: [Título descriptivo]
- **Página:** /eventos/crear/
- **Pasos para reproducir:**
  1. Ir a crear evento
  2. Hacer X
  3. Observar Y
- **Resultado esperado:** Debería hacer Z
- **Resultado actual:** Hace W
- **Severidad:** Alta / Media / Baja
- **Screenshot:** [Opcional]
```

## 🚀 Testing Completado

Una vez completado todo el checklist:
- [ ] Marcar todos los items con ✅
- [ ] Documentar bugs encontrados
- [ ] Priorizar correcciones
- [ ] Hacer testing de regresión después de cada fix

---

**Última actualización:** 23 de Octubre, 2025
**Versión:** 1.0
**Estado:** ✅ Listo para testing
