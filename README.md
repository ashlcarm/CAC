# Lingrow demo (simple GUI)

Este es un demo pequeño para tu app Lingrow. Muestra cómo integrar tu imagen PNG de Canva en una ventana y probar funciones básicas de sugerencias de texto.

Archivos añadidos:
- `main.py` — aplicación Tkinter que carga una imagen PNG, permite escribir texto, generar 3 tipos de sugerencias y guardar entradas en `saved_texts.json`.

Cómo usar
1. Coloca tu imagen PNG (por ejemplo `lingrow_mockup.png`) en la misma carpeta que `main.py`.
2. Desde la carpeta abre un terminal y corre:

```bash
python main.py
```

3. Si no pones la imagen con ese nombre, haz clic en "Load Image" y elige tu PNG.
4. Escribe en el cuadro "Write something" y usa los botones "Professional", "Neutral" o "Cultural" para ver sugerencias.
5. Haz clic en "Save entry" para guardar en `saved_texts.json`.

Notas
- Este proyecto usa sólo la librería estándar. Para mejorar la escala de imágenes instala Pillow:

```bash
pip install pillow
```

- El código está pensado para aprendizaje: las sugerencias son reglas simples y educativas.

Problemas o mejoras sugeridas
- Añadir validación de entradas y más pruebas unitarias.
- Mejorar el manejo de imágenes y el diseño de la interfaz.
1# Lingrow AI Writing Tool

## Overview

Lingrow is an AI-powered writing tool designed for people learning a new language. Our app helps users express themselves more confidently by offering alternative ways to write their text. It provides suggestions for professional, neutral, or culturally appropriate language, making writing in another language easier and more natural.

## Features

- **Welcome Screen:** Displays the Lingrow logo and a friendly introduction.
- **Text Input:** Users can type their text in a simple box, similar to a text editor.
- **AI Suggestions:** Shows the original writing alongside AI-generated alternatives.
- **User Choice:** Suggestions include different styles (professional, neutral, culturally appropriate) to help users find the best way to express their ideas.

## How It Works

1. The user enters their text.
2. The app displays the original text and offers AI suggestions.
3. Users can view and choose from different writing options.

## Getting Started

1. Clone the repository from GitHub Classroom.
2. Open the project in Visual Studio Code.
3. Run the Python files to start using the app.

## Code Guidelines

- Simple Python code using functions and variables.
- Clear comments explaining each part of the code.
- Easy-to-understand variable and function names.
- No advanced Python features or external libraries unless requested.

## Learning Goals

Lingrow is built by students, for students. Our goal is to learn Python, work together as a team, and create an app that helps language learners improve their writing skills.

## Contributing

If you want to help, please:
- Write readable and beginner-friendly code.
- Add helpful comments.
- Suggest ways to organize the code for clarity.

Thank you for supporting our learning journey!

Easy open (one-click on macOS or from terminal)
---------------------------------------------

I added two small scripts to make it easier to open the app:

- `run.sh` — runner script. If a `.venv` exists it activates it, otherwise runs system Python.
- `run.command` — macOS double-clickable file that runs `run.sh` when opened from Finder.

Make the files executable (one-time step):

```bash
cd "/Users/ashlcarm18/Computer sciencie /CAC"
chmod +x run.sh run.command
```

Then you can:
- Double-click `run.command` in Finder to open the app.
- Or run from terminal:

```bash
./run.sh
```

If you want me to add a small AppleScript app wrapper (so it appears as a normal macOS app you can double-click), I can add instructions and a script for that.

Generate example assets
-----------------------

If you don't have icon images yet, you can generate simple example assets used by the app:

```bash
python3 scripts/generate_assets.py
```

This will create:
- `assets/lingrow_logo.png` — a simple logo placeholder
- `icons/home.png`, `icons/explore.png`, `icons/write.png`, `icons/profile.png`

Install Pillow first if needed:

```bash
pip install pillow
```