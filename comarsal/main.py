import flet as ft
import sqlite3
from screens.table import main as main_app  # Importa la función main desde table.py

# Ruta de la base de datos SQLite
database_path = '/home/batoi/Escritorio/TrabajoFinal/ProyectoFinal/assets/Liga'

def main(page: ft.Page):
    page.title = "Login"
    page.bgcolor = ft.colors.BLUE_GREY_200  # Establecer el color de fondo azul grisáceo

    def registrar_click(e):
        if txt_usuario.value and txt_email.value and txt_contrasena.value:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Usuarios (nombre_usuario, correo, contrasena) VALUES (?, ?, ?)",
                               (txt_usuario.value, txt_email.value, txt_contrasena.value))
                conn.commit()
                page.clean()
                page.add(ft.Text(f"Registrado exitosamente, {txt_usuario.value}!"))
            except sqlite3.IntegrityError:
                lbl_error.value = "El usuario o correo ya está registrado."
                page.update()
            except sqlite3.OperationalError as e:
                lbl_error.value = f"Error en la base de datos: {str(e)}"
                page.update()
            finally:
                conn.close()
        else:
            lbl_error.value = "Por favor, complete todos los campos."
            page.update()

    def iniciar_sesion_click(e):
        if txt_usuario.value and txt_contrasena.value:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("SELECT correo FROM Usuarios WHERE nombre_usuario = ? AND contrasena = ?", 
                           (txt_usuario.value, txt_contrasena.value))
            user = cursor.fetchone()
            conn.close()
            if user:
                page.clean()
                main_app(page)  # Llama a la función main del archivo table.py
            else:
                lbl_error.value = "Usuario o contraseña incorrectos."
                page.update()
        else:
            lbl_error.value = "Por favor, ingrese su usuario y contraseña."
            page.update()

    def continuar_sin_registro_click(e):
        page.clean()
        main_app(page)

    def show_registration_layout(e):
        page.clean()
        txt_email.visible = True
        btn_registrar.visible = True
        btn_cancelar.visible = True
        btn_iniciar_sesion.visible = False
        btn_continuar_sin_registro.visible = False
        btn_registrarse.visible = False
        page.add(img_logo_container, txt_usuario, txt_email, txt_contrasena, btn_registrar, btn_cancelar, lbl_error)
        page.update()

    def show_login_layout(e):
        page.clean()
        txt_email.visible = False
        btn_registrar.visible = False
        btn_cancelar.visible = False
        btn_iniciar_sesion.visible = True
        btn_continuar_sin_registro.visible = True
        btn_registrarse.visible = True
        page.add(img_logo_container, txt_usuario, txt_contrasena, btn_iniciar_sesion, btn_registrarse, btn_continuar_sin_registro, lbl_error)
        page.update()

    
    img_logo = ft.Image(src="assets/ilogin.png", width=100, height=100)
    img_logo_container = ft.Container(content=img_logo, alignment=ft.alignment.center)

    txt_usuario = ft.TextField(label="Nombre de Usuario")
    txt_email = ft.TextField(label="Correo Electrónico")
    txt_contrasena = ft.TextField(label="Contraseña", password=True)

    btn_registrar = ft.ElevatedButton("Registrarse", on_click=registrar_click)
    btn_iniciar_sesion = ft.ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion_click)
    btn_continuar_sin_registro = ft.ElevatedButton("Continuar sin registrarte", on_click=continuar_sin_registro_click)
    btn_registrarse = ft.ElevatedButton("Registrarse", on_click=show_registration_layout)
    btn_cancelar = ft.ElevatedButton("Cancelar", on_click=show_login_layout)

    txt_email.visible = False
    btn_registrar.visible = False
    btn_cancelar.visible = False

    lbl_error = ft.Text(color="red")

    # Organizar los botones en una columna
    button_column = ft.Column(
        [
            btn_iniciar_sesion,
            btn_registrarse,
            btn_continuar_sin_registro,
            btn_registrar,
            btn_cancelar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Añadir elementos a la página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    img_logo_container,
                    txt_usuario,
                    txt_contrasena,
                    button_column,
                    lbl_error
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_GREY_200,
            border_radius=10
        )
    )

ft.app(target=main)
