from login import verificar_login

usuario = input("Usuario: ")
contraseña = input("Contraseña: ")

login_exitoso, id_usuario = verificar_login(usuario, contraseña)

if login_exitoso:
    print(f"✅ Bienvenido, ID usuario: {id_usuario}")
else:
    print("❌ Usuario o contraseña incorrectos.")
