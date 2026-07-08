import datetime 
import validaciones as valid
import database as db 
from colorama import Back, Fore, init, Style


init(autoreset=True)

# Menú de opciones
menu = f'''{Fore.BLUE}{Style.BRIGHT}
********* Menú de Opciones **********
1. Registrar nuevo producto
2. Visualizar todos los productos
3. Actualizar producto (por ID)
4. Eliminar producto (por ID)
5. Buscar producto (por ID)
6. Reporte de bajo stock
7. Salir
*************************************{Style.RESET_ALL}'''

def mostrar_mje_exito(mensaje):
    """Muestra un mensaje de éxito destacado en verde."""
    print(f"{Fore.GREEN}{Style.BRIGHT}{mensaje}")

def mostrar_mje_error(mensaje):
    """Muestra un mensaje de error destacado en rojo."""
    print(f"{Fore.RED}{Style.BRIGHT}{mensaje}")

def obtener_fecha_actual():
    """Retorna un string con la fecha y hora actual en formato DD/MM/AAAA HH:MM"""
    ahora = datetime.datetime.now()
    return ahora.strftime("%d/%m/%Y %H:%M")

# =====================================================================
# FUNCIONES DE LAS OPCIONES DEL MENÚ
# =====================================================================

def menu_registrar_producto():
    print(f"\n{Fore.CYAN}--- Registrar Nuevo Producto ---")
    nombre = valid.validar_texto("Nombre del producto: ", "El nombre no puede quedar vacío.").title()
    descripcion = input("Descripción (opcional): ").strip()
    cantidad = valid.solicitar_cantidad("Cantidad disponible: ")
    precio = valid.solicitar_precio("Precio del producto: ")
    categoria = valid.validar_texto("Categoría: ", "La categoría no puede quedar vacía.").lower() 
    
    db.crear_producto(nombre, descripcion, cantidad, precio, categoria)
    fecha_registro = obtener_fecha_actual()
    mostrar_mje_exito(f"\n*** ¡Producto '{nombre}' registrado con éxito el {fecha_registro}! ***\n")

def menu_visualizar_productos():
    print(f"\n{Fore.CYAN}***** Listado de Productos Registrados *****\n")
    lista = db.obtener_productos()
    
    if not lista:
        mostrar_mje_error("El inventario está vacío. No hay productos registrados.\n")
    else:
        for prod in lista:
            #tupla: (id, nombre, descripcion, cantidad, precio, categoria)
            print(f"ID: {prod[0]} | Nombre: {prod[1]} | Desc: {prod[2]} | Stock: {prod[3]} u. | Precio: ${prod[4]} | Cat: {prod[5]}")
        print() 

def menu_actualizar_producto():
    print(f"\n{Fore.CYAN}--- Actualizar Producto ---")
    id_buscar = valid.solicitar_id("Ingrese el ID del producto que desea actualizar: ")
    
    # buscamos si el producto existe para mostrar los datos 
    prod = db.buscar_producto_por_id(id_buscar)
    
    if prod:
        print(f"\nProducto encontrado: {prod[1]} (Stock actual: {prod[3]} | Precio actual: ${prod[4]})")
        nueva_cantidad = valid.solicitar_cantidad("Ingrese la NUEVA cantidad disponible: ")
        nuevo_precio = valid.solicitar_precio("Ingrese el NUEVO precio: ")
        
        db.actualizar_producto_precio_stock(id_buscar, nueva_cantidad, nuevo_precio)
        mostrar_mje_exito(f"\n*** Producto con ID {id_buscar} actualizado correctamente. ***\n")
    else:
        mostrar_mje_error(f"\nNo se encontró ningún producto con el ID: {id_buscar}\n")

def menu_eliminar_producto():
    print(f"\n{Fore.CYAN}--- Eliminar Producto ---")
    id_eliminar = valid.solicitar_id("Ingrese el ID del producto a eliminar: ")
    
    # Intentamos eliminarlo directamente desde la base de datos
    fue_eliminado = db.eliminar_producto_por_id(id_eliminar)
                 
    if fue_eliminado:
        mostrar_mje_exito(f"\n*** El producto con ID {id_eliminar} fue eliminado correctamente del sistema. ***\n")
    else:
        mostrar_mje_error(f"\nNo se pudo eliminar: El ID {id_eliminar} no existe en la base de datos.\n")

def menu_buscar_producto():
    print(f"\n{Fore.CYAN}--- Buscar Producto por ID ---")
    id_buscar = valid.solicitar_id("Ingrese el ID del producto a buscar: ")
    
    prod = db.buscar_producto_por_id(id_buscar)
        
    if prod:
        mostrar_mje_exito("\n¡Producto Encontrado!")
        print(f"-> ID: {prod[0]}")
        print(f"-> Nombre: {prod[1]}")
        print(f"-> Descripción: {prod[2]}")
        print(f"-> Stock Disponible: {prod[3]} unidades")
        print(f"-> Precio: ${prod[4]}")
        print(f"-> Categoría: {prod[5]}\n") 
    else:
        mostrar_mje_error(f"\nEl producto con ID {id_buscar} no existe en el sistema.\n")

def menu_reporte_bajo_stock():
    print(f"\n{Fore.CYAN}--- Reporte de Bajo Stock ---")
    limite = valid.solicitar_cantidad("Especifique el límite máximo de stock para el reporte: ")
    
    lista_reporte = db.reporte_bajo_stock(limite)
    
    print(f"\n{Fore.YELLOW}***** Productos con stock igual o inferior a {limite} *****\n")
    if not lista_reporte:
        print("No se encontraron productos en alerta de stock.\n")
    else:
        for prod in lista_reporte:
            print(f"ID: {prod[0]} | Nombre: {prod[1]} | Stock Actual: {prod[3]} u. | Cat: {prod[5]}")
        print()

# =====================================================================
# BUCLE PRINCIPAL DE LA APLICACIÓN
# =====================================================================
print(f"{Fore.BLUE}{Style.BRIGHT}\n***----- Bienvenidos al Sistema de Gestión de Inventario -----***\n")

# Inicializar la base de datos
db.inicializar_db()

while True:
    print(menu)
    option = input("\nPor favor ingrese la opción deseada (1-7): ").strip()
    
    match option:
        case "1":
            menu_registrar_producto()
        case "2":
            menu_visualizar_productos()
        case "3":
            menu_actualizar_producto()
        case "4":
            menu_eliminar_producto()
        case "5":
            menu_buscar_producto()
        case "6":
            menu_reporte_bajo_stock()
        case "7":
            print(f"\n{Fore.BLUE}{Style.BRIGHT}Gracias por utilizar el gestor de inventario. ¡Hasta luego!\n")
            break
        case _:
            mostrar_mje_error("\nOpción no válida. Por favor, seleccione un número del 1 al 7.")