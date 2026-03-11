# Calculadora Básica en Consola

def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\n--- Menu ---")
    print("1 - Sumar")
    print("2 - Restar")
    print("3 - Multiplicar")
    print("4 - Dividir")
    print("5 - Salir")

def calculadora():
    """Función principal que ejecuta la lógica de la calculadora."""
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        # Salir del programa si la opción es 5
        if opcion == '5':
            print("¡Hasta luego! Gracias por usar la calculadora.")
            break

        # Verificar si la opción es una operación matemática (1 a 4)
        if opcion in ['1', '2', '3', '4']:
            try:
                # Solicitar dos números al usuario y convertirlos a float
                num1 = float(input("Introduce el primer número: "))
                num2 = float(input("Introduce el segundo número: "))

                # Realizar la operación correspondiente
                if opcion == '1':
                    resultado = num1 + num2
                    print(f"El resultado de la suma es: {resultado}")
                elif opcion == '2':
                    resultado = num1 - num2
                    print(f"El resultado de la resta es: {resultado}")
                elif opcion == '3':
                    resultado = num1 * num2
                    print(f"El resultado de la multiplicación es: {resultado}")
                elif opcion == '4':
                    # Controlar la división por cero
                    if num2 == 0:
                        print("Advertencia: No se puede dividir entre cero.")
                    else:
                        resultado = num1 / num2
                        print(f"El resultado de la división es: {resultado}")
            
            except ValueError:
                # Capturar error si no se introducen números válidos
                print("Error: Introduce solo números válidos.")
        
        else:
            # Mensaje para opciones fuera del rango 1-5
            print("Error: Opción no válida. Por favor, elige una opción del 1 al 5.")

# Iniciar la calculadora
if __name__ == "__main__":
    calculadora()