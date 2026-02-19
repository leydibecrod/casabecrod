# Prompt: Barrio Dinamarca 3D - Modelo Interactivo con Three.js

Actúa como un desarrollador senior de gráficos 3D en la web.

Tu tarea es crear una aplicación interactiva con Three.js en un solo archivo HTML (incluye CSS y JavaScript en el mismo archivo), sin frameworks adicionales.

## Contexto

Tengo un **barrio rural real** llamado "Barrio Dinamarca" en el centro poblado de Aguas Claras, Moyobamba, San Martín, Perú. Las coordenadas están en **UTM Zone 18S (EPSG:32718)** en metros. Te adjunto un JSON (`barrio_dinamarca_3d.json`) con todos los datos geoespaciales reales.

## Objetivo

Construir una escena 3D del Barrio Dinamarca usando los datos reales del JSON adjunto. Cada lote/solar debe ser un volumen 3D clickeable que muestre la información del propietario. Las calles y manzanas deben reflejar la geometría real del barrio.

## Datos disponibles en el JSON

- **24 solares** (lotes) con: nombre del propietario, 4 vértices UTM, medidas de cada lado en metros, área en m², color identificador
- **4 manzanas** (Mz29, Mz30, Mz32, Mz33) con: 4 esquinas UTM, medidas de cada lado
- **3 calles**: Jr. Moyobamba, Jr. Rioja, Av. Marginal - Fernando Belaunde Terry (con coordenadas de centro y ancho aproximado)
- **Perímetro general** del barrio con 17 vértices

## Requisitos funcionales

### 1) Escena del barrio (datos reales)
- Usa los vértices UTM del JSON para posicionar cada elemento. **Normaliza las coordenadas** restando el mínimo X/Y para que el origen quede cerca de (0,0).
- **Suelo**: Un plano base verde oscuro representando el terreno general.
- **Solares/Lotes**: Cada solar es un volumen 3D (extrusión del polígono de 4 vértices). Usa el color del JSON para cada uno. Altura por defecto: 4 metros (1 piso). Usa `ExtrudeGeometry` con el `Shape` de cada solar.
- **Calles**: Planos grises entre las manzanas, usando las coordenadas de las calles del JSON.
- **Manzanas**: Opcionalmente dibuja el contorno del perímetro de cada manzana como líneas en el suelo.
- Añade iluminación básica (ambient + directional) y sombras suaves.

### 2) Selección de objetos
- Permite seleccionar solares de la ciudad con clic del mouse (raycasting).
- Al seleccionar:
  - Resaltar visualmente el objeto (outline simple, emissive, o cambio temporal de material).
  - Mostrar información del solar en un panel UI: nombre del propietario, manzana, área, perímetro, medidas de lados.

### 3) Cambio de color
- Incluye un selector de color (input type="color") para el objeto seleccionado.
- Al cambiar el color, debe actualizarse en tiempo real sobre el solar activo.

### 4) Cambio de altura
- Incluye un slider (input type="range") para cambiar la altura del solar seleccionado (1 a 15 metros).
- La altura se actualiza en tiempo real, simulando edificios de diferentes pisos.

### 5) Movimiento de cámara
- Cámara con OrbitControls para rotar/zoom/pan.
- Posición inicial: vista aérea en ángulo que muestre todo el barrio.
- Teclas: W/S para acercar/alejar, A/D para rotar.

## Interfaz y usabilidad

- Agrega un panel UI minimalista (esquina superior derecha) con:
  - Nombre del barrio: "Barrio Dinamarca - Aguas Claras"
  - Nombre del solar seleccionado
  - Área y perímetro del solar
  - Medidas de lados
  - Color picker
  - Slider de altura
  - Botón "Deseleccionar"
  - Lista/leyenda de todos los solares (clickeable para seleccionar)
- Agrega etiquetas 3D flotantes con el nombre del propietario sobre cada solar (CSS2DRenderer o sprites).
- Mantén FPS estables (optimiza geometrías y materiales reutilizables cuando sea posible).

## Procesamiento de coordenadas

Las coordenadas UTM del JSON están en metros absolutos (ej: East ~215500, North ~9367200). Para usarlas en Three.js:

```javascript
// Encontrar el centro de todas las coordenadas
const centerX = (minEast + maxEast) / 2;
const centerY = (minNorth + maxNorth) / 2;

// Normalizar cada vértice
const x = vertex.east - centerX;
const z = -(vertex.north - centerY); // Invertir Z para que Norte apunte "arriba"
const y = 0; // Nivel del suelo
```

## Entrega

- Devuelve únicamente el código completo en un archivo HTML listo para ejecutar.
- Código bien comentado, legible y con secciones claras.
- No uses assets externos obligatorios (todo debe funcionar sin modelos descargados).
- Three.js se carga desde CDN: `https://unpkg.com/three@0.160.0/build/three.module.js`
- OrbitControls desde: `https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js`
- CSS2DRenderer desde: `https://unpkg.com/three@0.160.0/examples/jsm/renderers/CSS2DRenderer.js`

## JSON adjunto

Adjunta el archivo `barrio_dinamarca_3d.json` junto con este prompt.
