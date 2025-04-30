import flet as ft
import sqlite3

# Ruta de la base de datos SQLite
database_path = '/home/batoi/Escritorio/TrabajoFinal/comarsal/assets/Liga'

# Consulta para obtener los datos de clasificación
consulta_clasificacion = """
SELECT
    e.nombre AS equipo,
    c.puntos,
    c.partidos_jugados,
    c.partidos_ganados,
    c.partidos_empatados,
    c.partidos_perdidos,
    c.goles_favor,
    c.goles_encontra
FROM Clasificacion c
JOIN Equipos e ON c.id_equipo = e.id
ORDER BY c.puntos DESC, c.goles_favor - c.goles_encontra DESC;
"""

# Consulta para obtener los partidos terminados
consulta_partidos = """
SELECT
    el.nombre AS equipo_local,
    ev.nombre AS equipo_visitante,
    p.goles_local,
    p.goles_visitante,
    p.jornada,
    p.fecha_hora
FROM Partidos p
JOIN Equipos el ON p.id_equipo_local = el.id
JOIN Equipos ev ON p.id_equipo_visitante = ev.id
WHERE p.partido_acabado = 1
ORDER BY p.fecha_hora DESC;
"""

# Consulta para obtener las jornadas
consulta_jornadas = """
SELECT DISTINCT jornada FROM Partidos ORDER BY jornada;
"""

# Consulta para obtener los partidos de una jornada específica
consulta_partidos_por_jornada = """
SELECT
    el.nombre AS equipo_local,
    ev.nombre AS equipo_visitante,
    p.goles_local,
    p.goles_visitante,
    p.partido_acabado,
    p.fecha_hora
FROM Partidos p
JOIN Equipos el ON p.id_equipo_local = el.id
JOIN Equipos ev ON p.id_equipo_visitante = ev.id
WHERE p.jornada = ?
ORDER BY p.fecha_hora;
"""

# Cabecera de la tabla de clasificación
cabecera = ['Equipo', 'Puntos', 'Partidos Jugados', 'Partidos Ganados', 'Partidos Empatados', 'Partidos Perdidos', 'Goles a Favor', 'Goles en Contra']

def fetch_clasificacion():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(consulta_clasificacion)
    datos_clasificacion = cursor.fetchall()
    conn.close()
    return datos_clasificacion

def fetch_partidos():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(consulta_partidos)
    datos_partidos = cursor.fetchall()
    conn.close()
    return datos_partidos

def fetch_jornadas():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(consulta_jornadas)
    datos_jornadas = cursor.fetchall()
    conn.close()
    return [jornada[0] for jornada in datos_jornadas]

def fetch_partidos_por_jornada(jornada):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(consulta_partidos_por_jornada, (jornada,))
    datos_partidos = cursor.fetchall()
    conn.close()
    return datos_partidos

def main(page: ft.Page):
    page.title = "Liga de Fútbol Sala"

    def load_actualidad():
        page.controls.clear()
        page.controls.append(menu_bar)
        datos_partidos = fetch_partidos()
        for partido in datos_partidos:
            equipo_local, equipo_visitante, goles_local, goles_visitante, jornada, fecha_hora = partido
            partido_control = ft.Container(
                content=ft.Column([
                    ft.Text(f"{equipo_local} vs {equipo_visitante}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Fecha y hora: {fecha_hora}", color="gray"),
                    ft.Divider(),
                    ft.Row([
                        ft.Text(f"Jornada: {jornada}", color="gray"),
                        ft.Text(f"Resultado: {goles_local}-{goles_visitante}", color="gray")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=10,
                margin=10,
                border_radius=10,
                border=ft.Border(
                    left=ft.BorderSide(1, "gray"),
                    top=ft.BorderSide(1, "gray"),
                    right=ft.BorderSide(1, "gray"),
                    bottom=ft.BorderSide(1, "gray")
                )
            )
            page.controls.append(partido_control)
        page.update()

    def load_clasificacion():
        datos_clasificacion = fetch_clasificacion()
        tabla = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(columna)) for columna in cabecera],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(celda))) for celda in fila]
                ) for fila in datos_clasificacion
            ],
        )
        page.controls.clear()
        page.controls.append(menu_bar)
        page.controls.append(tabla)
        page.update()

    def load_calendario():
        page.controls.clear()
        page.controls.append(menu_bar)
        jornadas = fetch_jornadas()
        for jornada in jornadas:
            jornada_button = ft.ElevatedButton(f"Jornada {jornada}", on_click=lambda e, j=jornada: show_jornada(j))
            page.controls.append(jornada_button)
        page.update()
    
    def show_jornada(jornada):
        partidos = fetch_partidos_por_jornada(jornada)
        page.controls.clear()
        page.controls.append(menu_bar)
        back_button = ft.ElevatedButton("Volver al Calendario", on_click=load_calendario)
        page.controls.append(back_button)
        for partido in partidos:
            equipo_local, equipo_visitante, goles_local, goles_visitante, partido_acabado, fecha_hora = partido
            resultado = f"{goles_local}-{goles_visitante}" if partido_acabado else "Pendiente"
            partido_control = ft.Container(
                content=ft.Column([
                    ft.Text(f"{equipo_local} vs {equipo_visitante}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Fecha y hora: {fecha_hora}", color="gray"),
                    ft.Divider(),
                    ft.Row([
                        ft.Text(f"Resultado: {resultado}", color="gray")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=10,
                margin=10,
                border_radius=10,
                border=ft.Border(
                    left=ft.BorderSide(1, "gray"),
                    top=ft.BorderSide(1, "gray"),
                    right=ft.BorderSide(1, "gray"),
                    bottom=ft.BorderSide(1, "gray")
                )
            )
            page.controls.append(partido_control)
        page.update()



    def on_menu_click(e):
        if e.control.text == "Actualidad":
            load_actualidad()
        elif e.control.text == "Clasificación":
            load_clasificacion()
        elif e.control.text == "Calendario":
            load_calendario()
        elif e.control.text == "Estadísticas":
            pass  # Implementa la lógica para cargar Estadísticas
        elif e.control.text == "Equipos":
            pass  # Implementa la lógica para cargar Equipos
        elif e.control.text == "Información":
            pass  # Implementa la lógica para cargar Información

    menu_items = ["Actualidad", "Clasificación", "Calendario", "Estadísticas", "Equipos", "Información"]
    menu_bar = ft.Row([
        ft.TextButton(item, on_click=on_menu_click) for item in menu_items
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    load_actualidad()



