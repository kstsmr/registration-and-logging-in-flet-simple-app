import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = 'Registration'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.width_window = 400

    def vdata(e):
        if all([uslog.value, uspass.value]):
            btn.disabled=False
            btnau.disabled=False
        else:
            btn.disabled=True
            btnau.disabled=True
        page.update()

    def register(e):
        db = sqlite3.connect('sm.kst')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT
        )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{uslog.value}', '{uspass.value}')")

        uslog.value = ''
        uspass.value = ''
        btn.text = 'Added succesfully'

        db.commit()
        db.close()
        page.update()

    def authus(e):
        db = sqlite3.connect('sm.kst')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{uslog.value}' AND pass = '{uspass.value}'")
        if (cur.fetchone()) != None:
            uslog.value = ''
            uspass.value = ''
            btnau.text = 'Logged in successfully'
            page.update()

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationBarDestination(
                    icon=ft.icons.BOOK_ONLINE,
                    label='Account',
                    selected_icon=ft.icons.BOOKMARK
                ))

        else:
            uslog.value = ''
            uspass.value = ''
            btnau.text = 'Incorrect data, try again'
            page.update()


        db.commit()
        db.close()
        page.update()
    
    aut = ft.Text('Log in')
    reg = ft.Text('Registration')
    uslog = ft.TextField(label='Enter your login', width=350, on_change=vdata)
    uspass = ft.TextField(label='Enter your password', password=True, width=350, on_change=vdata)
    btn = ft.OutlinedButton(text='Add', width=350, on_click=register, disabled=True)
    btnau = ft.OutlinedButton(text='Log in', width=350, on_click=authus, disabled=True)

#account

    users = ft.ListView(spacing=10, padding=20)


#acc end

    pnreg = ft.Row(
                    [
                ft.Column(
                    [
                        reg,
                        uslog,
                        uspass,
                        btn
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    pnauth = ft.Row(
                    [
                ft.Column(
                    [
                        aut,
                        uslog,
                        uspass,
                        btnau
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    pncab = ft.Row(
                    [
                ft.Column(
                    [
                        ft.Text('Your account'),
                        users
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def navi(e):
        page.clean()
        if (page.navigation_bar.selected_index) == 0:
            page.add(pnreg)
        elif (page.navigation_bar.selected_index) == 1:
            page.add(pnauth)
        elif (page.navigation_bar.selected_index) == 2:
            users.controls.clear()

            db = sqlite3.connect('sm.kst')

            cur = db.cursor()
            cur.execute("SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for user in res:
                    print(user)
                    users.controls.append(ft.Row([
                        ft.Text(f'User {user[1]}'),
                        ft.Icon(ft.icons.PEOPLE_ALT)
                    ]))

            db.commit()
            db.close()
            page.add(pncab)


    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_BALANCE, label = 'Register'),
            ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_BALANCE_SHARP, label = 'Log in')
        ], on_change=navi
    )

    page.add(pnreg)

ft.app(target=main)