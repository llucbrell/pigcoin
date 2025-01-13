import qrcode
import io
import os
from bitcoinlib.keys import Key, bip38_encrypt, bip38_decrypt
from fpdf import FPDF
import numpy as np
from stl import mesh
import trimesh

from bitcoinlib.keys import HDKey
# import bitcoinlib
# print(bitcoinlib.__path__)


def generar_wallet(password: str):
    """
    Genera una nueva wallet Bitcoin P2PKH utilizando bitcoinlib y cifra la clave privada con BIP38.
    """

    key = Key()
    address = key.address()
    wif = key.wif()
    private_hex = key.private_hex
    
    bip38_key = bip38_encrypt(private_hex, address, password)

    print("\n\n=== NUEVA WALLET GENERADA ===")
    print(f"Dirección Bitcoin (P2PKH)   : {address}")
    print(f"Clave Privada (WIF)         : {wif}")
    print(f"Clave Privada BIP38         : {bip38_key}")
    
    qr_addr = qrcode.make(address)
    qr_bip38 = qrcode.make(bip38_key)
    
    qr_addr.show()
    qr_bip38.show()


    # Obtener prefijo único
    prefijo = address[:6]  # Usa los primeros 6 caracteres de la dirección

    # Crear subdirectorio específico para la wallet
    output_dir = os.path.join("output", f"wallet_{prefijo}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Guardar en PDF
    generar_pdf(address, wif, bip38_key, qr_addr, qr_bip38, output_dir, prefijo)
    
    # Crear modelo 3D
    generar_moneda_3d(address, output_dir, prefijo)
    generar_qr_3d(address, output_dir, prefijo, embutir=False)
    
def generar_pdf(address, wif, bip38_key, qr_addr, qr_bip38, output_dir, prefijo):
    """ Genera un PDF con los datos de la wallet y lo guarda en su subdirectorio correspondiente """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)

    # 📌 Página de título
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=24)  # Fuente grande y en negrita
    pdf.ln(40)  # Espacio superior
    # 📌 Imagen centrada (Asegúrate de que "logo.png" exista en la carpeta)
    image_path = "sources/pigcoin_pet.png"  # Cambia por la ruta correcta de tu imagen
    if os.path.exists(image_path):
        pdf.image(image_path, x=60, y=50, w=90)  # Ajusta X, Y y el ancho (W) según sea necesario

    # 📌 Texto centrado
    pdf.ln(100)  # Espacio debajo de la imagen
    pdf.cell(190, 10, "PigCoin Wallet Generator", ln=True, align="C")

    # 📌 Nueva página para los datos de la wallet
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    # Título
    pdf.cell(190, 10, "Bitcoin Wallet", ln=True, align='C')
    pdf.ln(5)

    # Dirección y claves
    pdf.set_font("Arial", size=9)
    pdf.cell(190, 6, f"Dirección Bitcoin: {address}", ln=True)
    pdf.cell(190, 6, f"Clave Privada (WIF): {wif}", ln=True)
    pdf.cell(190, 6, f"Clave Privada BIP38: {bip38_key}", ln=True)
    pdf.ln(5)

    # Guardar códigos QR en archivos temporales
    qr_addr_path = os.path.join(output_dir, f"qr_address_{prefijo}.png")
    print(f"Imagen QR de dirección generada: {qr_addr_path}")
    qr_bip38_path = os.path.join(output_dir, f"qr_bip38_{prefijo}.png")
    print(f"Imagen QR de clave privada BIP38 generada: {qr_bip38_path}")

    qr_addr.save(qr_addr_path)
    qr_bip38.save(qr_bip38_path)

    # Etiquetas para los QR
    pdf.cell(95, 6, "Dirección Bitcoin (QR)", ln=False, align="C")
    pdf.cell(95, 6, "Clave Privada BIP38 (QR)", ln=True, align="C")
    
    # Insertar imágenes QR en la misma línea
    x_start = 30
    y_position = pdf.get_y() + 2
    pdf.image(qr_addr_path, x=x_start, y=y_position, w=50)
    pdf.image(qr_bip38_path, x=x_start + 95, y=y_position, w=50)
    
    # Guardar PDF
    pdf_filename = os.path.join(output_dir, f"wallet_data_{prefijo}.pdf")
    pdf.output(pdf_filename)
    print(f"PDF generado: {pdf_filename}")

    # Eliminar archivos temporales
    # os.remove(qr_addr_path)
    # os.remove(qr_bip38_path)



def desencriptar_bip38(bip38_key_encrypted: str, password: str):
    """
    Desencripta una clave privada BIP38 y muestra la clave privada en WIF y la dirección Bitcoin.
    """
    try:
        # Desencriptar la clave privada (devuelve una tupla)
        priv_bytes, _, compressed, _ = bip38_decrypt(bip38_key_encrypted, password)

        # Crear un objeto Key a partir de los bytes de la clave privada
        key_obj = Key(import_key=priv_bytes, is_private=True, compressed=compressed)

        # Imprimir resultados
        print("\n=== CLAVE PRIVADA DESENCRIPTADA ===")
        print(f" - Clave Privada (WIF)  : {key_obj.wif()}")
        print(f" - Dirección (P2PKH)    : {key_obj.address()}")
        print("===================================\n\n")
        
    except Exception as e:
        print(f"Error al desencriptar la clave: {e}")


def generar_moneda_3d(address, output_dir, prefijo, embutir=False):
    """ Genera un modelo STL con un QR en relieve o embutido en la moneda sin errores de superficie. """
    
    # 📌 Generar código QR y convertirlo en matriz
    qr = qrcode.make(address)
    qr_matrix = qr.get_image().convert("1")  # Convertir a blanco y negro (1 bit)
    qr_array = np.array(qr_matrix)

    qr_size = qr_array.shape[0]  # Tamaño del QR (es cuadrado)

    # 📌 Parámetros de la moneda
    radius = 20      # Radio de la moneda
    height = 3       # Grosor de la moneda
    qr_depth = 1.0   # Profundidad del relieve o embutido

    # 📌 Crear la moneda usando `trimesh` en lugar de hacerlo manualmente
    moneda = trimesh.creation.cylinder(radius=radius, height=height, sections=100)

    # 📌 Escalar QR para que encaje bien en la moneda
    qr_scale = (radius * 1.5) / qr_size  # Ajustar tamaño QR al tamaño de la moneda
    qr_offset = height / 2 if not embutir else (height / 2) - qr_depth  # Relieve o embutido

    # 📌 Crear la malla del QR en relieve o embutido
    qr_pixels = []
    for i in range(qr_size):
        for j in range(qr_size):
            if qr_array[i, j] == 0:  # Si el píxel es negro (parte del QR)
                x = (i - qr_size / 2) * qr_scale
                y = (j - qr_size / 2) * qr_scale
                z_start = qr_offset  # Posición base del relieve o grabado
                z_end = qr_offset + qr_depth if not embutir else qr_offset - qr_depth  # Tope del relieve o grabado

                # 📌 Crear un "pilar" por cada píxel negro
                voxel = trimesh.creation.box(extents=[qr_scale, qr_scale, qr_depth])
                voxel.apply_translation([x, y, (z_start + z_end) / 2])  # Centrar el bloque
                qr_pixels.append(voxel)

    # 📌 Fusionar todas las partes en una sola malla
    if qr_pixels:
        qr_mesh = trimesh.util.concatenate(qr_pixels)
        moneda = trimesh.boolean.union([moneda, qr_mesh])  # Fusionar la moneda con el QR

    # 📌 Guardar el archivo STL en el subdirectorio
    stl_filename = os.path.join(output_dir, f"moneda_qr_{prefijo}.stl")
    moneda.export(stl_filename)
    print(f"Modelo 3D generado: {stl_filename}")

    # **🔧 REPARAR LA MALLA STL 🔧**
    # print("Reparando el modelo 3D...")
    mesh_reparado = trimesh.load_mesh(stl_filename)

    # 🔥 **Corrección de la malla** 🔥
    mesh_reparado.fix_normals()  # Asegura que todas las normales sean correctas
    mesh_reparado.fill_holes()   # Cierra cualquier agujero en la malla


    # Exportar la malla reparada
    stl_repaired_filename = os.path.join(output_dir, f"moneda_qr_{prefijo}_repaired.stl")
    mesh_reparado.export(stl_repaired_filename)

    #print(f"✅ Modelo 3D final reparado: {stl_repaired_filename}")
    print(f"Modelo 3D revisado: {stl_repaired_filename}")

def generar_qr_3d(address, output_dir, prefijo, embutir=False):
    """ Genera un modelo STL con solo el código QR en relieve o embutido, con el mismo tamaño y posición que el de la moneda, añadiendo una base cuadrada."""
    
    # 📌 Generar código QR y convertirlo en matriz
    qr = qrcode.make(address)
    qr_matrix = qr.get_image().convert("1")  # Convertir a blanco y negro (1 bit)
    qr_array = np.array(qr_matrix)

    qr_size = qr_array.shape[0]  # Tamaño del QR (es cuadrado)

    # 📌 Parámetros del QR en 3D
    radius = 20      # Radio de la moneda
    height = 3       # Grosor de la moneda
    qr_depth = 1.0   # Profundidad del relieve o embutido
    qr_scale = (radius * 1.5) / qr_size  # Ajustar tamaño QR al tamaño de la moneda
    qr_offset = height / 2 if not embutir else (height / 2) - qr_depth  # Relieve o embutido

    # 📌 Crear la base cuadrada para el QR
    base_size = radius * 1.5  # Tamaño de la base cuadrada
    base_thickness = 1.0  # Grosor de la base
    base = trimesh.creation.box(extents=[base_size, base_size, base_thickness])
    base.apply_translation([0, 0, base_thickness / 2])  # Centrar la base

    # 📌 Crear la malla del QR en relieve o embutido
    qr_pixels = []
    for i in range(qr_size):
        for j in range(qr_size):
            if qr_array[i, j] == 0:  # Si el píxel es negro (parte del QR)
                x = (i - qr_size / 2) * qr_scale
                y = (j - qr_size / 2) * qr_scale
                z_start = base_thickness  # La base del relieve comienza sobre la base cuadrada
                z_end = z_start + qr_depth if not embutir else z_start - qr_depth  # Tope del relieve o grabado

                # 📌 Crear un "pilar" por cada píxel negro
                voxel = trimesh.creation.box(extents=[qr_scale, qr_scale, qr_depth])
                voxel.apply_translation([x, y, (z_start + z_end) / 2])  # Centrar el bloque
                qr_pixels.append(voxel)

    # 📌 Fusionar la base y el QR en una sola malla
    if qr_pixels:
        qr_mesh = trimesh.util.concatenate(qr_pixels)
        final_mesh = trimesh.boolean.union([base, qr_mesh])  # Fusionar la base con el QR

        # 📌 Guardar el archivo STL en el subdirectorio
        stl_filename = os.path.join(output_dir, f"qr_only_{prefijo}.stl")
        final_mesh.export(stl_filename)
        print(f"Modelo 3D del QR generado: {stl_filename}")

        # **🔧 REPARAR LA MALLA STL 🔧**
        mesh_reparado = trimesh.load_mesh(stl_filename)

        # 🔥 **Corrección de la malla** 🔥
        mesh_reparado.fix_normals()  # Asegura que todas las normales sean correctas
        mesh_reparado.fill_holes()   # Cierra cualquier agujero en la malla

        # Exportar la malla reparada
        stl_repaired_filename = os.path.join(output_dir, f"qr_only_{prefijo}_repaired.stl")
        mesh_reparado.export(stl_repaired_filename)

        print(f"Modelo 3D del QR revisado: {stl_repaired_filename}")
        print(f"============================\n\n")


if __name__ == "__main__":
    print("¿Qué deseas hacer?")
    print(" [1] Generar nueva wallet (cifrar con BIP38)")
    print(" [2] Desencriptar clave privada (BIP38)")
    choice = input("Elige [1/2]: ")

    if choice == "1":
        pwd = input("Introduce tu contraseña: ")
        generar_wallet(pwd)
    elif choice == "2":
        bip38_key_input = input("Introduce la clave privada en formato BIP38: ")
        pwd = input("Introduce la contraseña: ")
        desencriptar_bip38(bip38_key_input, pwd)
    else:
        print("Opción no válida. Saliendo.")
