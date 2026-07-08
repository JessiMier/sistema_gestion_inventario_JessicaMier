def validar_texto(mensaje_input, mensaje_error):
    """Solicita un texto al usuario por consola y valida que no esté vacío."""
    while True:
        texto = input(mensaje_input).strip()
        if texto != "":
            return texto  
        print(mensaje_error)

def solicitar_precio(mensaje_input):
    """Solicita un precio por consola y valida que sea un número decimal positivo."""
    while True:
        precio_ingresado = input(mensaje_input).strip()
        try:
            precio = float(precio_ingresado)
            if precio > 0:
                return precio 
            else:
                print("Error: El precio debe ser mayor que 0.")
        except ValueError:
            print("Error: Por favor ingrese un número decimal válido (ej: 100 o 80.50).")

def solicitar_cantidad(mensaje_input):
    """Solicita una cantidad en stock y valida que sea un entero no negativo."""
    while True:
        cantidad_ingresada = input(mensaje_input).strip()
        try:
            cantidad = int(cantidad_ingresada)
            if cantidad >= 0:
                return cantidad
            else:
                print("Error: La cantidad no puede ser un número negativo.")
        except ValueError:
            print("Error: Por favor ingrese un número entero válido (ej: 10, 0, 50).")

def solicitar_id(mensaje_input):
    """Solicita un ID único y valida que sea un número entero positivo."""
    while True:
        id_ingresado = input(mensaje_input).strip()
        try:
            id_producto = int(id_ingresado)
            if id_producto > 0:
                return id_producto
            else:
                print("Error: El ID debe ser un número mayor a 0.")
        except ValueError:
            print("Error: Por favor ingrese un ID numérico válido.")