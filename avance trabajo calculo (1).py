import customtkinter as ctk
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Calculadora de Límites")
ventana.geometry("800x700")

# Título
titulo = ctk.CTkLabel(
    ventana,
    text="Calculadora y Visualizador de Límites",
    font=("Arial", 20)
)
titulo.pack(pady=20)

# Función
label_funcion = ctk.CTkLabel(
    ventana,
    text="Ingrese la función f(x):"
)
label_funcion.pack()

entrada_funcion = ctk.CTkEntry(
    ventana,
    width=300
)
entrada_funcion.pack(pady=10)

# Valor h
label_h = ctk.CTkLabel(
    ventana,
    text="Ingrese el valor h:"
)
label_h.pack()

entrada_h = ctk.CTkEntry(
    ventana,
    width=100
)
entrada_h.pack(pady=10)

# Resultado
resultado = ctk.CTkLabel(
    ventana,
    text="Resultado:"
)
resultado.pack(pady=20)

# Frame para la gráfica
frame_grafica = ctk.CTkFrame(
    ventana,
    width=600,
    height=300
)
frame_grafica.pack(pady=20, fill="both", expand=True)

# Figura de Matplotlib
figura = plt.Figure(figsize=(5, 3))
grafico = figura.add_subplot(111)

canvas = FigureCanvasTkAgg(
    figura,
    master=frame_grafica
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)

# Función calcular
def calcular():

    try:

        funcion_texto = entrada_funcion.get()
        h_texto = entrada_h.get()

        x = symbols('x')

        funcion = sympify(funcion_texto)
        h = sympify(h_texto)

        resultado_limite = limit(funcion, x, h)

        resultado.configure(
            text=f"Resultado: {resultado_limite}"
        )

        # Limpiar gráfica anterior
        grafico.clear()

        valores_x = []
        valores_y = []

        for i in range(-10, 11):

            try:
                y = funcion.subs(x, i)

                valores_x.append(i)
                valores_y.append(float(y))

            except:
                pass

        # Dibujar función
        grafico.plot(valores_x, valores_y)

        # Línea vertical en h
        try:
            grafico.axvline(float(h), linestyle="--")
        except:
            pass

        grafico.set_title("Gráfica de la función")
        grafico.set_xlabel("x")
        grafico.set_ylabel("f(x)")
        grafico.grid(True)

        canvas.draw()

    except Exception as error:

        resultado.configure(
            text=f"Error: {error}"
        )

# Botón
boton = ctk.CTkButton(
    ventana,
    text="Calcular",
    command=calcular
)
boton.pack(pady=20)

ventana.mainloop()