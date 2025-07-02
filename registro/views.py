from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import RegistroForm
from django.http import JsonResponse
from .models import Registro  # Importa tu modelo, si lo tienes
from datetime import datetime

# from weasyprint import HTML
# from django.template.loader import render_to_string  # Asegúrate de importar esta función
from django.http import HttpResponse
from django.utils import timezone  # Si es necesario para la fecha

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)  # Subir archivos (pdf) con request.FILES

        if form.is_valid():
            
            # Obtener los datos del formulario
            cleaned_data = form.cleaned_data
            tipo_usuario = cleaned_data.get('tipo_participante')  # 'estudiante (pregrado)' o 'participante'
            hoy = datetime.now()
            fecha_limite = datetime(2025, 6, 30)  # 30 de junio de 2025

            # Lógica para calcular el monto según la fecha y el tipo de usuario
            if hoy <= fecha_limite:
                if tipo_usuario == 'estudiante (pregrado)':
                    monto = 50.00
                elif tipo_usuario == 'participante':
                    monto = 100.00
            else:  # 30 de junio en adelante
                if tipo_usuario == 'estudiante (pregrado)':
                    monto = 80.00
                elif tipo_usuario == 'participante':
                    monto = 150.00

            # Asignamos el monto calculado al formulario antes de guardar
            form.instance.monto = monto
            
            print('Formulario válido:', form.cleaned_data)
            
            try:
                form.save()
                print('Registro guardado con éxito')
                return redirect('registro_constancia', dni=form.cleaned_data['dni'])
            
            except IntegrityError as e:
                # Aquí manejamos la excepción de violación de unicidad
                if 'dni' in str(e):
                    form.add_error('dni', 'El DNI ya existe. Por favor, ingrese un DNI único.')
                elif 'email' in str(e):
                    form.add_error('email', 'El correo electrónico ya está registrado.')
                elif 'celular' in str(e):
                    form.add_error('celular', 'El número de celular ya está registrado.')

                print('Error al guardar el registro:', e)
        else:
            print('Errores del formulario:', form.errors)
    else:
        form = RegistroForm()

    return render(request, 'registro/registro.html', {'form': form})


def validar_duplicados(request):
    # Obtener los parámetros enviados desde el frontend
    
    dni = request.GET.get('dni')
    email = request.GET.get('email')
    celular = request.GET.get('celular')
    
    # Crear un diccionario para los errores
    response_data = {}

    # Validar si el DNI ya está registrado
    if Registro.objects.filter(dni=dni).exists():  # Ajusta esto según tu modelo
        response_data['dni'] = 'El DNI ya está registrado.'

    # Validar si el correo electrónico ya está registrado
    if Registro.objects.filter(email=email).exists():  # Ajusta esto según tu modelo
        response_data['email'] = 'El correo electrónico ya está registrado.'

    # Validar si el celular ya está registrado
    if Registro.objects.filter(celular=celular).exists():  # Ajusta esto según tu modelo
        response_data['celular'] = 'El número de celular ya está registrado.'

    # Si existen duplicados, devolver los errores
    if response_data:
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': True})  # Si no hay duplicados, devolver éxito
    

def registro_constancia(request, dni):
    return render(request, 'registro/registro-constancia.html', {'dni': dni})


# Definir los márgenes (en puntos, 1 pulgada = 72 puntos)
MARGEN_SUPERIOR = 72  # 1 pulgada de margen superior
MARGEN_IZQUIERDO = 72  # 1 pulgada de margen izquierdo
MARGEN_INFERIOR = 72  # 1 pulgada de margen inferior
MARGEN_DERECHO = 72  # 1 pulgada de margen derecho

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", 
    "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

def generar_pdf(request, dni):
    
    
    # Suponiendo que tienes un modelo Registro
    try:
        usuario = Registro.objects.get(dni=dni)
    except Registro.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)

    # Crear una respuesta HTTP de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="inscripcion.pdf"'

    # Crear un lienzo de ReportLab
    c = canvas.Canvas(response, pagesize=letter)

    # Establecer el título del PDF
    c.setTitle("Constancia de Inscripción - CIMAC 2025")  # Aquí se establece el título


    width, height = letter

    # Agregar márgenes
    c.translate(MARGEN_IZQUIERDO, height - MARGEN_SUPERIOR)


    # Insertar imagen del voucher de pago
    c.drawImage("static/images/logos/logo-cimac-fondo.png", -20, -40, width=70, height=70)  # Ajusta la ubicación de la imagen
    c.drawImage("static/images/logos/logo-unap-fondo.jpg", 420, -40, width=70, height=70)  # Ajusta la ubicación de la imagen
    
    c.setFont("Helvetica", 14)
    c.drawString(120, 5, "CONGRESO INTERNACIONAL DE")
    c.drawString(80, -15, "MATEMÁTICA APLICADA Y COMPUTACIONAL")
    c.drawString(120, -35, "XII CIMAC 2025 - PUNO - PERÚ")
    
    c.line(-20, -55, 490, -55)  # linea


    # Título del congreso
    c.setFont("Helvetica-Bold", 22)
    c.drawString(70, -120, "CONSTANCIA DE INSCRIPCIÓN")

    # Crear un estilo para el texto
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    para_style = ParagraphStyle(name='Justified', parent=normal_style, alignment=4, fontSize=14, leading=18)  # Justificado

    right_style = ParagraphStyle(name='RightAligned', parent=normal_style, alignment=2, fontSize=14, leading=18)  # Alineado a la derecha
    
    
    # Obtener la fecha en formato español
    fecha_registro = usuario.fecha_registro
    # Formatear la fecha en español, ejemplo: "02 de marzo de 2025"
    fecha_formateada = f"{fecha_registro.day} de {MESES[fecha_registro.month - 1]} de {fecha_registro.year}"
    
    nombre_completo = f"{usuario.nombres.upper()} {usuario.apellido_paterno.upper()} {usuario.apellido_materno.upper()}"
    

    # Texto principal del documento
    text = f"""
    Se hace constar que: <br/><br/><br/>
    
    <b>{nombre_completo}</b>, identificado con el documento de identidad N°. <b>{usuario.dni}</b>,
    
    ha completado exitosamente el proceso de inscripción y se encuentra registrado como <b>{usuario.tipo_participante.upper()}</b>. Además, ha realizado el pago correspondiente de <b>{usuario.monto} soles</b> (*a verificar) para participar en el: <br/><br/>
    
    <b>XII CONGRESO INTERNACIONAL DE MATEMÁTICA APLICADA Y COMPUTACIONAL (CIMAC)</b>, que se llevará a cabo del 11 al 15 de agosto de 2025 en Puno, Perú.<br/><br/>
    
    Este evento congregará a destacados expertos, investigadores y profesionales del ámbito de la matemática aplicada y computacional, con el propósito de fomentar el intercambio de conocimientos, la colaboración académica y el avance en la investigación dentro de estas disciplinas. <br/><br/><br/>
    
    """

    text2 = f"""
    Puno, {fecha_formateada}.<br/>
    """

    # Agregar párrafos al PDF con justificación y estilo
    p = Paragraph(text, style=para_style)
    p_width, p_height = p.wrap(width - (MARGEN_IZQUIERDO + MARGEN_DERECHO), height - (MARGEN_SUPERIOR + MARGEN_INFERIOR))
    p.drawOn(c, 0, -160 - p_height)

    # Segundo párrafo (la fecha) alineado a la derecha
    p2 = Paragraph(text2, style=right_style)
    p2_width, p2_height = p2.wrap(width - (MARGEN_IZQUIERDO + MARGEN_DERECHO), height - (MARGEN_SUPERIOR + MARGEN_INFERIOR))
    p2.drawOn(c, 0, -170 - p_height - p2_height)  # Posiciona justo después del anterior


    # Guardar el archivo PDF
    c.save()

    return response
