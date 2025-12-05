import math
import numpy as np
import pandas as pd
from scipy.integrate import quad

#########METODO DEL PUNTO FIJO###########
def punto_fijo(g, x0, tol, max_iter):
    """
    Método del punto fijo para encontrar una raíz de la ecuación x = g(x)

    Variables que usaremos:
    - g: función iterativa g(x)
    - x0: valor inicial (estimación inicial de la raíz)
    - tol: tolerancia del error (criterio de parada)
    - max_iter: número máximo de iteraciones permitidas

    nos dara esto:
    - Aproximación de la raíz
    - Número de iteraciones realizadas
    """
    iteraciones = 0  # Contador de iteraciones
    # Bucle principal del método para iterar
    while iteraciones < max_iter: #aqui se condiciona el codigo
        x1 = g(x0)  # Calculamos el siguiente valor usando la función g
        error = abs(x1 - x0)  # Aqui es donde se resta el resultado con el primer valor
        # Mostramos el progreso de cada iteración
        print(f"Iteración {iteraciones+1}: x = {x1:.6f}, error = {error:.6f}")
        # Si el error es menor que la tolerancia, consideramos que hemos encontrado la raíz
        if error < tol:
            return x1, iteraciones + 1  # Retornamos la raíz aproximada y el número de iteraciones (resultado)
        # Actualizamos el valor de x0 para la siguiente iteración
        x0 = x1
        iteraciones += 1
    # Si no se alcanza la tolerancia en el número máximo de iteraciones, se muestra una advertencia
    print("Advertencia: No se alcanzó la convergencia.")
    return x0, iteraciones  # Retornamos la última estimación aunque no haya convergido


# Aqui es donde Ingresan los valores de las variables
def ejecutar_punto_fijo(): #Aqui ejecuta el archivo directamente
    # Definimos la función g(x) que se usará en el método
    expr = input("Ingresa la función g(x) en términos de x (ejemplo: math.sqrt((x+5)/2)): ")
    # En este caso: g(x) = sqrt((x + 5) / 2)
    g = lambda x: eval(expr, {"__builtins__": None, "math": math}, {"x": x}) #lo que hace math aqui es que calcula la ecuacion
    # Solicitamos al usuario los parámetros necesarios
    x0 = float(input("Ingresa el1 valor inicial x0: "))        # Estimación inicial
    tol = float(input("Ingresa la tolerancia del error: "))   # Tolerancia
    max_iter = int(input("Ingresa el número máximo de iteraciones: "))  # Límite de iteraciones
    # Ejecutamos el método de punto fijo con los datos ingresados
    raiz, pasos = punto_fijo(g, x0, tol, max_iter)
    # Mostramos el resultado final
    print(f"\nRaíz aproximada: {raiz:.6f} en {pasos} iteraciones")
    
############METODO DE BISECCION##########
import math #se importa la libreria math

def biseccion(funcion, a, b, error_pct, max_iter=50): #se crean la variables
    fa, fb = funcion(a), funcion(b) #esto evalua las funciones
    if fa * fb > 0: #esto verifica si los intervalos son validos
        print("El intervalo inicial no es válido: no hay cambio de signo.")
        return None

    print(f"{'Iter':<5}{'a':<12}{'b':<12}{'m':<12}{'f(m)':<15}{'Error':<12}")
    for i in range(1, max_iter+1):
        m = (a + b) / 2  #Aqui se aplica la formula de m
        fm = funcion(m) #se crea ka variable f(m)
        error = abs(b - a) / 2 #Aqui se consigue el error absoluto

        print(f"{i:<5}{a:<12.6f}{b:<12.6f}{m:<12.6f}{fm:<15.6f}{error:<12.6f}")

        # criterio de parada: error relativo
        if abs(error) <= error_pct * abs(m) or fm == 0: #si el error es menor se para el programa
            print(f"\nRaíz aproximada encontrada: x ≈ {m:.6f}")
            return m

        # decidir nuevo intervalo
        # aqui es donde se hacen los cambios cuando el valor es negativo
        # o positivo
        if fa * fm < 0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm

    print("\nSe alcanzó el número máximo de iteraciones.") 
    return (a+b)/2


# -------------------------------
# Entrada desde la terminal
# -------------------------------
def ejecutar_biseccion():
    # Pedir datos al usuario
    # aqui se agregan todos los valores
    expr = input("Ingresa la función en términos de x (ejemplo: x**3 - 2*x - 5): ")
    a = float(input("Ingresa el valor de a: "))
    b = float(input("Ingresa el valor de b: "))
    error_pct = float(input("Ingresa el porcentaje de error (ejemplo 0.001 para 0.1%): "))
    max_iter = int(input("Ingresa el número máximo de iteraciones: "))

    # Crear la función a partir de la expresión
    funcion = lambda x: eval(expr, {"__builtins__": None, "math": math}, {"x": x}) #para que python lea la funcion

    # Ejecutar bisección
    raiz = biseccion(funcion, a, b, error_pct, max_iter)

#############METODO DEL TRAPECIO COMPUESTO###############
def trapecio_compuesto(func, a, b, n):
    h = (b - a) / n #representa la formula h
    x = np.linspace(a, b, n+1) #crea los nodos de integración que se necesita para aplicar el método del trapecio.
    y = func(x) #representa la funcion
    integral = (h/2) * (y[0] + 2*np.sum(y[1:-1]) + y[-1]) #representa la formula I
    return integral

# -------------------------------
# Entrada por consola (Es para que se ingresen los valores)
def ejecutar_trapecio():
    expr = input("Ingresa la función en términos de x (ejemplo: np.exp(-x**2)): ")
    a = float(input("Ingresa el límite inferior a: "))
    b = float(input("Ingresa el límite superior b: "))
    max_n = int(input("Ingresa el número máximo de subintervalos n: "))
    error_limite = float(input("Ingresa el porcentaje de error máximo permitido (%): "))

    # Definir la función a partir de la expresión ingresada
    func = lambda x: eval(expr) #hace que pueda leer las funciones
    #eval toma el contenido de la variable expr como si fuera código Python y lo ejecuta dinámicamente.

    # Calcular valor real con scipy
    valor_real, _ = quad(func, a, b)
    #obtiene una aproximación muy precisa del valor real de la integral en el intervalo 𝑎,𝑏
    #Ese resultado se usa como referencia para comparar con el método del trapecio compuesto.

    # Crear tabla de resultados
    resultados = [] #Se crear la lista de resultados
    for n in range(1, max_n+1):
        aprox = trapecio_compuesto(func, a, b, n) #esto llama a la funcion del trapecio compuesto
        error_abs = abs(valor_real - aprox) #se calcula el error absoluto
        error_pct = (error_abs / abs(valor_real)) * 100 #se calcula el porcentaje de error
        resultados.append([n, aprox, error_abs, error_pct]) 
        #sirve para guardar en la lista los resultados los valores calculados en cada iteración del bucle.
        
        # Condición de parada
        if error_pct <= error_limite: #Es para cuando se alcance el limite error pare
            print(f"\nSe alcanzó el límite de error ({error_pct:.4f}%) con n={n}.")
            break

    # Mostrar tabla con pandas
    tabla = pd.DataFrame(resultados, columns=["n (subintervalos)", "Aproximación", "Error absoluto", "Error %"])
    print("\nTabla de resultados:")
    print(tabla.to_string(index=False))


# -------------------------------
# MENÚ PRINCIPAL
# -------------------------------
def main():
    print("\n=== MENÚ DE MÉTODOS NUMÉRICOS ===")
    print("1. Punto fijo")
    print("2. Bisección")
    print("3. Trapecio compuesto")
    opcion = int(input("Selecciona el método (1-3): "))
    if opcion == 1:
        ejecutar_punto_fijo()
    elif opcion == 2:
        ejecutar_biseccion()
    elif opcion == 3:
        ejecutar_trapecio()
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()