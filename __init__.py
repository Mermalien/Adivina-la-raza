import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
from dotenv import load_dotenv

load_dotenv()

images_dir = os.getenv('IMAGES_DIR')

if not images_dir:
    messagebox.showerror('Error', 'No es posible acceder a la variable de entorno')
    raise SystemExit

breeds = [
    ('ambulldog.jpg', 'Bulldog Americano'),
    ('ambully.webp', 'American Bully'),
    ('amstandf.webp', 'American Staffordshire terrier'),
    ('apbt.jpg', 'American Pitbull Terrier'),
    ('bordeaux.jpg', 'Dogo de Bordeaux'),
    ('bulldogfrances.jpeg', 'Bulldog Francés'),
    ('bullmastiff.webp', 'Bullmastiff'),
    ('bullterrier.jpg', 'Bull Terrier'),
    ('canecorso.jpg', 'Cane Corso'),
    ('dogo-arg.jpg', 'Dogo Argentino'),
    ('presacan.jpg', 'Presa Canario'),
    ('Staffie.jpg', 'Staffordshire bull terrier(STAFFY)')
]
# Contador de aciertos y razas mostradas
correct_answer_count = 0
shown_breeds = set()

#Función que elige una imagen al azar y la muestra
def show_random_breed():
    global correct_answer, shown_breeds

    # Cuando se hayan mostrado todas las razas preguntamos al usuario si quiere volver a jugar, si dice que no se cierra la aplicación
    if len(shown_breeds) == len(breeds):
        response = messagebox.askyesno('Fin del juego', f'Has acertado {correct_answer_count} razas de {len(breeds)}.¿Quieres volver a jugar?')
        if response:
            reset_game()
        else:
            root.destroy()
        return
    
    breed = random.choice(breeds)

    while breed in shown_breeds:
        breed = random.choice(breeds)
    shown_breeds.add(breed)

    image_file, correct_answer = breed
    image_path = os.path.join(images_dir, image_file)

    # Verificar que exista la imagen a mostrar
    if not os.path.isfile(image_path):
        messagebox.showerror('Error', f'No se encontró la imagen: {image_path}')
        return
    
    # Abrir y mostrar la imagen
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # Opciones
    options = random.sample(breeds, 2) # sample devuelve una lista de elementos sin repetición
    options.append(breed)
    random.shuffle(options) # Mezclamos aleatoriamente
    option_a.config(text=options[0][1])
    option_b.config(text=options[1][1])
    option_c.config(text=options[2][1])


# Verificar la respuesta del jugador
def check_answer(option):
    global correct_answer_count
    if option == correct_answer:
        correct_answer_count += 1
        messagebox.showinfo('Has acertado.', f'¡Correcto!')
    else:
        messagebox.showerror('Respuesta incorrecta.', f'La raza es {correct_answer}')
    show_random_breed()


# Función que reinicia el juego, ponemos a 0 los valores y reiniciamos la partida
def reset_game():
    global correct_answer_count, shown_breeds
    correct_answer_count = 0
    shown_breeds = set()
    show_random_breed()

# Configuración de la ventana
root = tk.Tk()
root.title('Adivina la raza, versión PPP')

# Mostrar cada imagen
image_label = tk.Label(root)
image_label.pack()

# Configuración de los botones con las opciones a elegir
option_a = tk.Button(root, text='', command=lambda: check_answer(option_a.cget('text')))
option_a.pack(fill=tk.X)
option_b = tk.Button(root, text= '', command=lambda: check_answer(option_b.cget('text')))
option_b.pack(fill=tk.X)
option_c = tk.Button(root, text='', command=lambda: check_answer(option_c.cget('text')))
option_c.pack(fill=tk.X)

# Iniciar el juego
show_random_breed()

# Ejecutar el bucle principal de la app (permite que la ventana responda a los eventos del usuario)
root.mainloop()