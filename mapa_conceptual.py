"""Actividad 4 | Mapa conceptual: Circuitería alternativa de E/S.

Ejecutar:
    python mapa_conceptual.py

El programa crea un archivo SVG vectorial y lo abre en el navegador.
Utiliza únicamente la biblioteca estándar de Python.
"""

from html import escape
from pathlib import Path
import argparse
import webbrowser

ANCHO, ALTO = 1600, 1180
CARPETAS = Path(__file__).resolve().parent
SALIDA = CARPETAS / "mapa_circuiteria_es.svg"


def texto(x, y, contenido, tam=20, color="#28344B", peso="normal", ancla="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{ancla}" '
        f'font-size="{tam}" font-weight="{peso}" fill="{color}" '
        f'font-family="Arial, Helvetica, sans-serif">{escape(contenido)}</text>'
    )


def cuadro(x, y, ancho, alto, titulo, descripcion, borde, relleno, icono=""):
    """Crea un concepto en un recuadro; los conceptos no son párrafos."""
    partes = [
        f'<g class="nodo"><title>{escape(titulo + ". " + descripcion)}</title>',
        f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" '
        f'rx="24" fill="{relleno}" stroke="{borde}" stroke-width="2.5" filter="url(#sombra)"/>',
        f'<rect x="{x}" y="{y}" width="7" height="{alto}" rx="3" fill="{borde}"/>',
    ]
    if icono:
        partes.append(texto(x + 30, y + 43, icono, tam=28, color=borde, ancla="start"))
    titulo_y = y + 40
    partes.append(texto(x + ancho / 2, titulo_y, titulo, 24, "#23314A", "bold"))
    partes.append(texto(x + ancho / 2, y + 76, descripcion, 17, "#53647F"))
    partes.append('</g>')
    return "\n".join(partes)


def linea(ruta, color="#8090AF", punteada=False):
    guiones = ' stroke-dasharray="9,7"' if punteada else ""
    return f'<path d="{ruta}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#punta)"{guiones}/>'


def etiqueta(x, y, valor, color="#566682", ancho=None):
    """Coloca palabras de enlace sobre una pastilla de fondo claro."""
    if ancho is None:
        ancho = max(78, len(valor) * 9 + 25)
    return (f'<rect x="{x-ancho/2}" y="{y-22}" width="{ancho}" height="29" '
            'rx="12" fill="#FFFFFF" fill-opacity="0.98"/>'
            + texto(x, y-2, valor, 15, color, "bold"))


def construir_svg():
    secciones = [
        {"x": 60, "titulo": "GENERALIDADES DE E/S", "color": "#468BD7", "relleno": "#EAF5FF",
         "relacion": "se basa en", "conceptos": [
            ("Puertos GPIO", "Pines para leer o enviar señales", "utiliza"),
            ("Registros de control", "Configuran la dirección de pines", "ajusta"),
            ("Circuitos de interfaz", "Adaptan señales y manejan cargas", "emplea"),
         ]},
        {"x": 568, "titulo": "VISUALIZACIÓN", "color": "#DB71AF", "relleno": "#FFF0F9",
         "relacion": "permite", "conceptos": [
            ("LED y matrices", "Indican estados mediante luz", "emplea"),
            ("Pantallas LCD", "Muestran texto y datos", "emplea"),
            ("OLED y TFT", "Representan gráficos e imágenes", "incluye"),
         ]},
        {"x": 1076, "titulo": "CODIFICADORES DE POSICIÓN", "color": "#8D71D4", "relleno": "#F2EDFF",
         "relacion": "recibe datos de", "conceptos": [
            ("Encoder incremental", "Genera pulsos al desplazarse", "incluye"),
            ("Encoder absoluto", "Da un código por posición", "incluye"),
            ("Aplicaciones", "Robótica, motores y medición", "aplica en"),
         ]},
    ]

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" width="{ANCHO}" height="{ALTO}" role="img" aria-label="Mapa conceptual de circuitería alternativa de entrada y salida">',
           '<defs><linearGradient id="fondo" x2="1" y2="1"><stop stop-color="#F4F8FF"/><stop offset="1" stop-color="#FFF6FC"/></linearGradient>'
           '<filter id="sombra" x="-15%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#737EA7" flood-opacity=".16"/></filter>'
           '<marker id="punta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#8090AF"/></marker></defs>',
           '<style>.nodo{transition:opacity .15s ease}.nodo:hover{opacity:.78}</style>',
           f'<rect width="{ANCHO}" height="{ALTO}" fill="url(#fondo)"/>',
           '<circle cx="98" cy="100" r="100" fill="#DBE9FF" opacity=".50"/>',
           '<circle cx="1517" cy="1118" r="130" fill="#F4DDF0" opacity=".45"/>',
           texto(800, 58, "ACTIVIDAD 4  ·  SISTEMAS PROGRAMABLES", 20, "#775AB9", "bold"),
           texto(800, 108, "Mapa conceptual: Circuitería alternativa de E/S", 37, "#23314A", "bold"),
           texto(800, 145, "Entrada / Salida en microcontroladores", 20, "#687892"),
           '<rect x="429" y="174" width="742" height="112" rx="32" fill="#5440A5" filter="url(#sombra)"/>',
           texto(800, 218, "CIRCUITERÍA ALTERNATIVA", 29, "#FFFFFF", "bold"),
           texto(800, 255, "Interfaz entre microcontrolador y entorno", 22, "#F1EAFE"),
           '<path d="M 800 286 V 306 H 292 V 335 M 800 306 V 335 M 800 306 H 1308 V 335" '
           'fill="none" stroke="#8390AD" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>',
           ]

    # Encabezados de las tres ramas, ordenados de lo general a lo particular.
    for sec in secciones:
        x = sec["x"]
        cx = x + 232
        svg.append(f'<rect x="{x}" y="335" width="464" height="93" rx="25" fill="{sec["color"]}" filter="url(#sombra)"/>')
        svg.append(texto(cx, 390, sec["titulo"], 21, "white", "bold"))
        svg.append(etiqueta(cx, 322, sec["relacion"], sec["color"]))

        # Ramificaciones con palabras de enlace: relación + concepto = proposición.
        eje_x = x + 33
        x_nodo = x + 93
        svg.append(f'<path d="M {eje_x} 428 V 1012" stroke="{sec["color"]}" stroke-width="3.5" opacity=".65" fill="none"/>')
        svg.append(f'<path d="M {cx} 428 H {eje_x}" stroke="{sec["color"]}" stroke-width="3.5" fill="none"/>')

        for i, (nombre, detalle, verbo) in enumerate(sec["conceptos"]):
            y = 488 + i * 182
            svg.append(linea(f'M {eje_x} {y+52} H {x_nodo-8}', sec["color"]))
            svg.append(etiqueta(eje_x + 24, y + 21, verbo, sec["color"], 93))
            svg.append(cuadro(x_nodo, y, 356, 109, nombre, detalle, sec["color"], sec["relleno"]))

    # Conexión cruzada entre ramas (regla importante del mapa conceptual).
    svg.extend([
        '<path d="M 509 579 L 657 579" fill="none" stroke="#5E9B9A" stroke-width="3.5" stroke-dasharray="8,6" marker-end="url(#punta)"/>',
        etiqueta(583, 630, "controla", "#328B87", 98),
        '<rect x="238" y="1066" width="1124" height="65" rx="22" fill="#E8E8FA"/>',
        texto(800, 1092, "ENLACE CRUZADO: GPIO → controla → LED", 20, "#51469B", "bold"),
        texto(800, 1119, "Ejemplo aplicado: un microcontrolador recibe datos y activa indicadores visuales", 17, "#5E6B88"),
        texto(800, 1163, "Generado con Python  ·  Mapa jerárquico con conceptos, palabras de enlace y conexiones", 15, "#8B93A7"),
        '</svg>'
    ])
    return "\n".join(svg)


def main():
    parser = argparse.ArgumentParser(description="Genera un mapa conceptual de circuitería E/S en SVG")
    parser.add_argument("--sin-abrir", action="store_true", help="No abrir el navegador automáticamente")
    args = parser.parse_args()

    SALIDA.write_text(construir_svg(), encoding="utf-8")
    print(f"Mapa conceptual generado correctamente: {SALIDA}")
    if not args.sin_abrir:
        try:
            webbrowser.open(SALIDA.as_uri())
        except Exception:
            print("Abre el archivo SVG manualmente con tu navegador.")


if __name__ == "__main__":
    main()
