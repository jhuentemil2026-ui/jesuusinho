import customtkinter as ctk
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Calculadora y Visualizador de Límites")
ventana.geometry("600x600")

titulo = ctk.CTkLabel(
    ventana,
    text="Calculadora y Visualizador de Límites",
    font=("Arial", 22, "bold")
)
titulo.pack(pady=15)

ctk.CTkLabel(ventana, text="Ingrese la función f(x)").pack()
entrada_funcion = ctk.CTkEntry(ventana, width=350)
entrada_funcion.pack(pady=10)

ctk.CTkLabel(ventana, text="Ingrese el valor h").pack()
entrada_h = ctk.CTkEntry(ventana, width=150)
entrada_h.pack(pady=10)

resultado = ctk.CTkTextbox(ventana, width=700, height=180)
resultado.pack(pady=15)
resultado.configure(state="disabled")

frame_grafica = ctk.CTkFrame(ventana, width=700, height=350)
frame_grafica.pack(pady=15, fill="both", expand=True)

mensaje_grafica = ctk.CTkLabel(
    frame_grafica,
    text="Ingrese una función y presione 'Calcular Límite'",
    font=("Arial", 16)
)
mensaje_grafica.pack(expand=True)

figura = plt.Figure(figsize=(6, 4))
grafico = figura.add_subplot(111)

canvas = FigureCanvasTkAgg(figura, master=frame_grafica)

# ==========================
# FUNCIÓN MEJORADA
# ==========================

def calcular():

    try:
        resultado.configure(state="normal")
        resultado.delete("1.0", "end")

        x = symbols("x")

        f = sympify(entrada_funcion.get())
        h = sympify(entrada_h.get())

        pasos = "=== ANÁLISIS DE LÍMITE ===\n\n"

        # ==========================
        # DETECTAR INFINITO
        # ==========================

        es_infinito = (h == oo or h == -oo)

        # ==========================
        # CASO LÍMITE FINITO
        # ==========================

        if not es_infinito:

            num, den = fraction(f)

            num_eval = num.subs(x, h)
            den_eval = den.subs(x, h)

            pasos += f"Numerador: {num}\nDenominador: {den}\n\n"

            # ✔ CASO NORMAL
            if den_eval != 0:
                lim = f.subs(x, h)
                pasos += "Método: Sustitución directa\n"
                pasos += f"LÍMITE = {lim}"

            # ✔ CASO 0/0 → LÍMITES LATERALES
            elif num_eval == 0 and den_eval == 0:

                pasos += "Indeterminación 0/0 → uso de límites laterales\n\n"

                lim_izq = limit(f, x, h, dir='-')
                lim_der = limit(f, x, h, dir='+')

                pasos += f"Límite izquierda = {lim_izq}\n"
                pasos += f"Límite derecha  = {lim_der}\n\n"

                if lim_izq == lim_der:
                    pasos += f"LÍMITE EXISTE = {lim_izq}"
                else:
                    pasos += "❌ EL LÍMITE NO EXISTE (izquierda ≠ derecha)"

            # ✔ CASO DIVISIÓN POR 0
            else:

                pasos += "División por cero detectada → análisis lateral\n\n"

                lim_izq = limit(f, x, h, dir='-')
                lim_der = limit(f, x, h, dir='+')

                pasos += f"Límite izquierda = {lim_izq}\n"
                pasos += f"Límite derecha  = {lim_der}\n\n"

                if lim_izq == lim_der:
                    pasos += f"LÍMITE = {lim_izq}"
                else:
                    pasos += "❌ EL LÍMITE NO EXISTE"

        # ==========================
        # CASO INFINITO
        # ==========================

        else:

            pasos += "Límite en infinito detectado\n\n"

            lim = limit(f, x, h)

            pasos += f"LÍMITE = {lim}"

        # ==========================
        # MOSTRAR RESULTADO
        # ==========================

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
                y = f.subs(x, x_actual)

                if y.is_real:
                    valores_x.append(float(x_actual))
                    valores_y.append(float(y))

            except:
                pass

            x_actual += 0.1

        grafico.plot(valores_x, valores_y, label="f(x)")

        if not es_infinito:
            try:
                grafico.axvline(float(h), linestyle="--", color="red")
            except:
                pass

        grafico.set_title("Gráfica de la función")
        grafico.grid(True)
        grafico.legend()

        if not canvas.get_tk_widget().winfo_ismapped():
            canvas.get_tk_widget().pack(fill="both", expand=True)

        canvas.draw()

    except Exception as e:
        resultado.configure(state="normal")
        resultado.delete("1.0", "end")
        resultado.insert("1.0", f"Error: {e}")
        resultado.configure(state="disabled")


boton = ctk.CTkButton(
    ventana,
    text="Calcular Límite",
    command=calcular
)
boton.pack(pady=15)

ventana.mainloop()
