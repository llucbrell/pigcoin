# PigCoin Wallet Generator

## Descripción
Este script permite generar una billetera Bitcoin (P2PKH) utilizando la librería `bitcoinlib`. También cifra la clave privada con BIP38 para mayor seguridad. Adicionalmente, el programa genera códigos QR de la dirección y clave privada, un archivo PDF con toda la información relevante y modelos 3D en formato STL que pueden ser impresos.

El script ofrece dos funcionalidades principales:
1. **Generación de una nueva billetera Bitcoin**, con claves cifradas usando BIP38.
2. **Desencriptado de claves privadas BIP38**, para recuperar la clave WIF y la dirección Bitcoin.

## Funcionalidades

### Generación de una Wallet
- Crea una dirección Bitcoin (P2PKH) y su clave privada.
- Cifra la clave privada con BIP38 utilizando una contraseña proporcionada por el usuario.
- Genera códigos QR de la dirección y de la clave privada cifrada.
- Guarda la información en un **archivo PDF** dentro de una carpeta específica.
- Genera un modelo 3D de una moneda con el QR en relieve o embutido.
- Genera un modelo 3D del código QR sobre una base plana.

### Desencriptar Clave BIP38
- Permite recuperar la clave privada en formato WIF a partir de la clave cifrada con BIP38 y la contraseña original.

## Ejecución

El script puede ejecutarse manualmente de la siguiente manera:
```bash
python pigcoin.py
```
Luego, selecciona la opción deseada en el menú interactivo.

### Uso con Entorno Virtual y `requirements.txt`
Para ejecutar el script en un entorno virtual con las dependencias correctas, sigue estos pasos:

1. Crea un entorno virtual:
```bash
python -m venv venv
```
2. Activa el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```
4. Ejecuta el script:
```bash
python pigcoin.py
```

## Generación del Ejecutable
Este proyecto incluye un archivo `pigcoin.spec` que permite la creación de un ejecutable utilizando `pyinstaller`. Un ejecutable ya generado se encuentra en la carpeta `dist/`.

### Construcción del ejecutable manualmente:
Si deseas crear el ejecutable desde el código fuente, usa:
```bash
pyinstaller --onefile --windowed pigcoin.spec
```
Esto generará un archivo `.exe` en la carpeta `dist/`.

## Dependencias
El archivo `requirements.txt` contiene todas las dependencias necesarias para ejecutar el script. Algunas de las librerías clave son:
- `bitcoinlib` para la gestión de claves Bitcoin.
- `qrcode` para la generación de códigos QR.
- `fpdf` para la generación del PDF.
- `numpy` y `trimesh` para la creación de modelos 3D.

### Instalación de dependencias manualmente
Si necesitas instalar las dependencias de forma manual, usa:
```bash
pip install bitcoinlib qrcode fpdf numpy trimesh
```

## Estructura del Proyecto
```
/
├── pigcoin.py         # Código principal
├── pigcoin.spec       # Archivo para generar el ejecutable con pyinstaller
├── requirements.txt   # Lista de dependencias
├── dist/              # Carpeta donde se encuentra el ejecutable
├── output/            # Carpeta donde se guardan las wallets generadas
│   ├── wallet_xxxxxx/ # Carpeta específica de cada wallet generada
│   │   ├── wallet_data_xxxxxx.pdf  # PDF con la información de la wallet
│   │   ├── qr_address_xxxxxx.png   # QR de la dirección Bitcoin
│   │   ├── qr_bip38_xxxxxx.png     # QR de la clave privada BIP38
│   │   ├── moneda_qr_xxxxxx.stl    # Modelo 3D de la moneda con QR
│   │   ├── qr_only_xxxxxx.stl      # Modelo 3D del QR sobre una base
└── sources/            # Carpeta con imágenes y recursos adicionales
```

## Notas Finales
Este script es útil para la generación rápida y segura de billeteras Bitcoin, con respaldo físico en PDF y modelos 3D. **Asegúrate de mantener tus claves privadas seguras y de no compartirlas con nadie.**

