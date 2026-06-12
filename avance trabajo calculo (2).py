import customtkinter as ctk
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================
# CONFIGURACIÓN DE LA VENTANA
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Calculadora y Visualizador de Límites")
ventana.geometry("600x600")

# ==========================
# TÍTULO
# ==========================

titulo = ctk.CTkLabel(
    ventana,
    text="Calculadora y Visualizador de Límites",
    font=("Arial", 22, "bold")
)
titulo.pack(pady=15)

# ==========================
# ENTRADA FUNCIÓN
# ==========================

label_funcion = ctk.CTkLabel(
    ventana,
    text="Ingrese la función f(x)"
)
label_funcion.pack()

entrada_funcion = ctk.CTkEntry(
    ventana,
    width=350
)
entrada_funcion.pack(pady=10)

# ==========================
# ENTRADA h
# ==========================

label_h = ctk.CTkLabel(
    ventana,
    text="Ingrese el valor h"
)
label_h.pack()

entrada_h = ctk.CTkEntry(
    ventana,
    width=150
)
entrada_h.pack(pady=10)

# ==========================
# RESULTADOS
# ==========================

resultado = ctk.CTkTextbox(
    ventana,
    width=700,
    height=180
)
resultado.pack(pady=15)

resultado.configure(state="disabled")

# ==========================
# FRAME GRÁFICA
# ==========================

frame_grafica = ctk.CTkFrame(
    ventana,
    width=700,
    height=350
)
frame_grafica.pack(
    pady=15,
    fill="both",
    expand=True
)

# Mensaje inicial

mensaje_grafica = ctk.CTkLabel(
    frame_grafica,
    text="Ingrese una función y presione 'Calcular Límite'",
    font=("Arial", 16)
)

mensaje_grafica.pack(expand=True)

# ==========================
# FIGURA MATPLOTLIB
# ==========================

figura = plt.Figure(figsize=(6, 4))
grafico = figura.add_subplot(111)

canvas = FigureCanvasTkAgg(
    figura,
    master=frame_grafica
)

# ==========================
# FUNCIÓN CALCULAR
# ==========================

def calcular():

    try:

        resultado.configure(state="normal")
        resultado.delete("1.0", "end")

        funcion_texto = entrada_funcion.get()
        h_texto = entrada_h.get()

        x = symbols("x")

        funcion = sympify(funcion_texto)
        h = sympify(h_texto)

        pasos = ""

        pasos += "=== DESARROLLO DEL ALGORITMO ===\n\n"

        # PASO 1

        num, den = fraction(funcion)

        pasos += "PASO 1: Separar numerador y denominador\n"
        pasos += f"Numerador = {num}\n"
        pasos += f"Denominador = {den}\n\n"

        # PASO 2

        num_eval = num.subs(x, h)
        den_eval = den.subs(x, h)

        pasos += "PASO 2: Sustitución directa\n"
        pasos += f"Numerador evaluado = {num_eval}\n"
        pasos += f"Denominador evaluado = {den_eval}\n\n"

        # CASO 1

        if den_eval != 0:

            resultado_final = funcion.subs(x, h)

            pasos += "PASO 3: No existe indeterminación\n"
            pasos += "Método utilizado: Sustitución directa\n\n"

            pasos += f"LÍMITE = {resultado_final}"

        # CASO 2

        elif num_eval == 0 and den_eval == 0:

            pasos += "PASO 3: Indeterminación 0/0 detectada\n\n"

            funcion_simplificada = simplify(funcion)

            pasos += "PASO 4: Simplificación algebraica\n"
            pasos += f"Función simplificada = {funcion_simplificada}\n\n"

            resultado_final = funcion_simplificada.subs(x, h)

            pasos += "PASO 5: Evaluar nuevamente\n\n"
            pasos += f"LÍMITE = {resultado_final}"

        # CASO 3

        else:

            pasos += "El límite presenta división por cero.\n"
            pasos += "Se requiere un análisis más avanzado."

        resultado.insert("1.0", pasos)
        resultado.configure(state="disabled")

        # ==========================
        # GRÁFICA
        # ==========================

        try:
            mensaje_grafica.destroy()
        except:
            pass

        grafico.clear()

        valores_x = []
        valores_y = []

        x_actual = -10

        while x_actual <= 10:

            try:

                    y = funcion.subs(x, x_actual)

                    if y.is_real:

                        valores_x.append(float(x_actual))
                        valores_y.append(float(y))


            except:
             pass
            x_actual += 0.1

        grafico.plot(
            valores_x,
            valores_y,
            label="f(x)"
        )

        try:

            grafico.axvline(
                float(h),
                linestyle="--",
                color="red",
                linewidth=2
            )

            y_h = funcion.subs(x, h)

            if y_h.is_real:

                grafico.plot(
                    float(h),
                    float(y_h),
                    marker="o",
                    color="red",
                    markersize=8,
                    label="Punto h"
                )

        except:
            pass

        grafico.set_title("Gráfica de la función")
        grafico.set_xlabel("x")
        grafico.set_ylabel("f(x)")
        grafico.grid(True)
        grafico.legend()

        if not canvas.get_tk_widget().winfo_ismapped():

            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

        canvas.draw()

    except Exception as error:

        resultado.configure(state="normal")

        resultado.delete("1.0", "end")

        resultado.insert("1.0", f"Error: {error}")
        resultado.configure(state="disabled")

# ==========================
# BOTÓN
# ==========================

boton = ctk.CTkButton(
    ventana,
    text="Calcular Límite",
    command=calcular
)
boton.pack(pady=15)

# ==========================
# EJECUTAR
# ==========================

ventana.mainloop()