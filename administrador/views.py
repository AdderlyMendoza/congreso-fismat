from django.shortcuts import render, redirect
from registro.models import Registro
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import Asistencia
from django.utils import timezone

from openpyxl import Workbook

from .forms import EntradaForm, SalidaForm


from datetime import timedelta

from django.db import IntegrityError
from django.utils.timezone import make_naive

from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


from django.http import HttpResponse
from django.utils import timezone

from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.http import JsonResponse





def index(request):
    # CANTIDADES
    inscritos_count = Registro.objects.all().count()
    inscritosValidados_count = Registro.objects.filter(validado=True).count() 
    
    # Obtener los conteos de entradas y salidas por fecha
    asistencias = Asistencia.objects.values('fecha') \
                                    .annotate(
                                        entradas_count=Count('entrada', filter=~Q(entrada=None)),
                                        salidas_count=Count('salida', filter=~Q(salida=None))
                                    ) \
                                    .order_by('-fecha')
    
    return render(request, 'administrador/index-inscritos.html', {
        'inscritos_count': inscritos_count,
        'inscritosValidados_count': inscritosValidados_count,
        'asistencias': asistencias
    })




# def lista_inscritos(request):
#     inscritos = Registro.objects.all().order_by('-fecha_registro')
#     return render(request, 'administrador/lista-inscritos.html', {'inscritos': inscritos})

def lista_inscritos(request):
    # Obtén todos los registros de inscritos ordenados por fecha
    inscritos = Registro.objects.all().order_by('-fecha_registro')

    # Paginación
    paginator = Paginator(inscritos, 5)  # Muestra 10 inscritos por página
    page_number = request.GET.get('page')  # Obtén el número de página desde la URL

    try:
        page_obj = paginator.page(page_number)  # Obtén los registros correspondientes a esa página
    except EmptyPage:
        page_obj = paginator.page(1)  # Si la página no existe o es vacía, muestra la primera página
    except:
        page_obj = paginator.page(paginator.num_pages)  # Si la página no existe, muestra la última página

    return render(request, 'administrador/lista-inscritos.html', {'page_obj': page_obj})



# def validar_inscrito(request, id):
#     if request.method == 'POST':
#         id = request.POST.get('id', id)  # Usamos el id del formulario si está presente, o el id de la URL por defecto
    
#     inscrito = Registro.objects.get(id=id)
#     inscrito.validado = 0 if inscrito.validado == 1 else 1
#     inscrito.save()
#     return redirect('lista-inscritos')

def validar_inscrito(request, id):
    if request.method == 'POST':
        try:
            inscrito = Registro.objects.get(id=id)
            inscrito.validado = not inscrito.validado
            inscrito.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_state': inscrito.validado
                })
                
            referer = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referer if referer else 'lista-inscritos')
            
        except Registro.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)


# def excel_inscritos_validados(request):
#     # Filtra los registros validados
#     inscritos = Registro.objects.filter(validado=1)

#     # Organiza los datos en un diccionario
#     data = {
#         'DNI': [inscrito.dni for inscrito in inscritos],
#         'Nombre': [inscrito.nombres for inscrito in inscritos],
#         'Apellido Paterno': [inscrito.apellido_paterno for inscrito in inscritos],
#         'Apellido Materno': [inscrito.apellido_materno for inscrito in inscritos],
#         'Email': [inscrito.email for inscrito in inscritos],
#         'Celular': [inscrito.celular for inscrito in inscritos],
#         'Fecha de registro': [
#             # Accede a los atributos correctamente usando la notación de puntos
#             make_naive(inscrito.fecha_registro).strftime('%Y-%m-%d %H:%M:%S') if inscrito.fecha_registro else None
#             for inscrito in inscritos
#         ],
#         # 'Validado': [inscrito.validado for inscrito in inscritos],
#     }

#     # Crea un DataFrame de pandas
#     df = pd.DataFrame(data)

#     # Crea la respuesta HTTP con el tipo de contenido adecuado
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=inscritos_validados.xlsx'

#     # df.to_excel(response, index=False)

#     with pd.ExcelWriter(response, engine='openpyxl') as writer:

#         df.to_excel(writer, index=False, sheet_name='Inscritos', startrow=4)  # Iniciar en 4

#         worksheet = writer.sheets['Inscritos']
        
#         worksheet.merge_cells('A1:G1')         

#         worksheet['A2'] = 'CONGRESO CIMAC 2025'
#         worksheet['A3'] = 'LISTA DE PERSONAS INSCRITAS'
        
     
     
#         worksheet['A2'].font = Font(bold=True, size=16, color="000000")  
#         worksheet['A2'].fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid") 
        
#         worksheet.merge_cells('A2:G2')
#         worksheet.row_dimensions[2].height = 30
#         worksheet['A2'].alignment = Alignment(horizontal='center', vertical='center')
        
        
#         worksheet['A3'].font = Font(bold=True, size=14, color="000000") 
#         worksheet['A3'].fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid") 
        
#         worksheet.merge_cells('A3:G3') 
#         worksheet.row_dimensions[3].height = 20
#         worksheet['A3'].alignment = Alignment(horizontal='center', vertical='center')
        
#         worksheet.merge_cells('A4:G4')         
                
#         def ajustar_ancho_columnas(worksheet, dataframe):
            
#             border = Border(
#                 left=Side(border_style="thin", color="000000"),
#                 right=Side(border_style="thin", color="000000"),
#                 top=Side(border_style="thin", color="000000"),
#                 bottom=Side(border_style="thin", color="000000")
#             )
            
#             for i, col in enumerate(dataframe.columns, 1):
#                 max_len = max(dataframe[col].astype(str).map(len).max(), len(col))  # Considera el largo del encabezado
#                 worksheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = max_len + 2  # Añadir un margen
                
#             # Agregar bordes a todas las celdas
#             for row in worksheet.iter_rows(min_row=6, min_col=1, max_row=worksheet.max_row, max_col=len(dataframe.columns)):
#                 for cell in row:
#                     cell.border = border

#         # Ajustar ancho de columnas
#         ajustar_ancho_columnas(worksheet, df)

#     return response


def excel_inscritos_validados(request):
    inscritos = Registro.objects.filter(validado=1).values_list(
        'dni', 'nombres', 'apellido_paterno', 'apellido_materno', 
        'email', 'celular', 'fecha_registro'
    )

    # Crear el libro de Excel directamente con OpenPyXL
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inscritos_validados.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = "Inscritos"

    # Estilos reutilizables
    header_font = Font(bold=True, size=12)
    title_font = Font(bold=True, size=16)
    subtitle_font = Font(bold=True, size=14)
    center_alignment = Alignment(horizontal='center', vertical='center')
    thin_border = Border(
        left=Side(border_style="thin"), 
        right=Side(border_style="thin"),
        top=Side(border_style="thin"), 
        bottom=Side(border_style="thin")
    )

    # Cabeceras y títulos
    ws.merge_cells('A1:G1')
    ws['A2'] = 'CONGRESO CIMAC 2025'
    ws['A3'] = 'LISTA DE PERSONAS INSCRITAS'
    
    # Aplicar estilos a los títulos
    for row in [2, 3]:
        ws.merge_cells(f'A{row}:G{row}')
        ws.row_dimensions[row].height = 30 if row == 2 else 20
        cell = ws[f'A{row}']
        cell.font = title_font if row == 2 else subtitle_font
        cell.alignment = center_alignment

    # Encabezados de columna
    columns = [
        'DNI', 'Nombre', 'Apellido Paterno', 
        'Apellido Materno', 'Email', 'Celular', 'Fecha de registro'
    ]
    
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=5, column=col_num, value=column_title)
        cell.font = header_font

    # Datos
    for row_num, inscrito in enumerate(inscritos, 6):
        for col_num, cell_value in enumerate(inscrito, 1):
            if col_num == 7 and cell_value:  # Fecha de registro
                cell_value = make_naive(cell_value).strftime('%Y-%m-%d %H:%M:%S')
            ws.cell(row=row_num, column=col_num, value=cell_value).border = thin_border

    # Ajustar ancho de columnas
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response



def entrada_inscritos(request):
    
    inicio_dia = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.min.time()))
    fin_dia = inicio_dia + timedelta(days=1) - timedelta(seconds=1)
    
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                # Buscar al usuario con el DNI proporcionado
                usuario = Registro.objects.get(dni=dni)

                # Verificar si ya existe un registro de asistencia para este usuario y la fecha actual
                asistencia = Asistencia.objects.filter(usuario=usuario, fecha=timezone.now().date()).first()
                # print("registro de entrada: ", timezone.localtime(timezone.now()))

                if not asistencia:
                    # Si no existe el registro, creamos uno nuevo con la hora de entrada
                    hora_ajustada = timezone.localtime(timezone.now()) - timedelta(hours=5)
                    
                    try:
                        # Intentamos crear el registro
                        asistencia = Asistencia.objects.create(
                            usuario=usuario,
                            entrada=hora_ajustada,
                            fecha=timezone.now().date()
                        )

                    except IntegrityError:
                        # Si ocurre un error de integridad (duplicado), se maneja aquí
                        form.add_error('dni', 'DNI ya registrado.')
         
                else:
                    # Si ya existe el registro, no hacemos nada
                    form.add_error('dni', 'DNI ya registrado.')
                    pass

                # return redirect('entrada-inscritos')  # Redirige después de registrar
                return render(request, 'administrador/entrada-inscritos.html', {'form': form, 'asistenciaEntrada': Asistencia.objects.all().order_by('-entrada'), 'asistenciaEntradaHoyCount': Asistencia.objects.filter(entrada__gte=inicio_dia, entrada__lt=fin_dia).count()})            
            except Registro.DoesNotExist:
                form.add_error('dni', 'DNI no existe.')
    else:
        form = EntradaForm()

        
    asistenciaEntrada = Asistencia.objects.all().order_by('-entrada')
    asistenciaEntradaHoyCount = Asistencia.objects.filter(entrada__gte=inicio_dia, entrada__lt=fin_dia).count()


    
    return render(request, 'administrador/entrada-inscritos.html', 
                { 
                    'form': form, 
                    'asistenciaEntrada':asistenciaEntrada,
                    'asistenciaEntradaHoyCount':asistenciaEntradaHoyCount,
                })



def salida_inscritos(request):
    
    inicio_dia = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.min.time()))
    fin_dia = inicio_dia + timedelta(days=1) - timedelta(seconds=1)
    
    if request.method == 'POST':
        form = SalidaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                # Buscar al usuario con el DNI proporcionado
                usuario = Registro.objects.get(dni=dni)

                ## LA ENTRADA TIENE QUE ALMACENARSE CON HORA Y LA SALIDA TAMBIEN, LA COLUMNA FECHA QUE SIGA SIENDO SOLO AÑO/MES/DIA
                asistencia = Asistencia.objects.filter(usuario=usuario, fecha=timezone.localtime(timezone.now()).date()).first()
                # print("registro de salida: ", timezone.localtime(timezone.now()))
                
                if asistencia:
                    if asistencia.entrada is not None and asistencia.salida is None:
                        # Si ya existe un registro de entrada y no tiene salida, actualizamos la salida
                        hora_ajustada = timezone.localtime(timezone.now()) - timedelta(hours=5)
                        asistencia.salida = hora_ajustada
                        asistencia.save()
                    else:
                        # Si no tiene entrada o ya tiene salida, mostramos un error
                        form.add_error('dni', 'DNI sin entrada hoy.')
                else:
                    # Si no existe el registro de asistencia, mostramos un error
                    form.add_error('dni', 'DNI sin entrada hoy.')

                # return redirect('salida-inscritos')  # Redirige después de registrar
                return render(request, 'administrador/salida-inscritos.html', {'form': form, 'asistenciaSalida': Asistencia.objects.all().order_by('-salida'), 'asistenciaSalidaHoyCount': Asistencia.objects.filter(salida__gte=inicio_dia, entrada__lt=fin_dia).count()})

            
            except Registro.DoesNotExist:
                form.add_error('dni', 'DNI no existe.')
    else:
        form = SalidaForm()

    asistenciaSalida = Asistencia.objects.all().order_by('-salida')
    asistenciaSalidaHoyCount = Asistencia.objects.filter(salida__gte=inicio_dia, entrada__lt=fin_dia).count()
    
    return render(request, 'administrador/salida-inscritos.html', 
                  {
                      'form': form, 
                      'asistenciaSalida':asistenciaSalida,
                      'asistenciaSalidaHoyCount':asistenciaSalidaHoyCount,
               })



def ver_pdf(request):
    context = {'pdf_url': '/media/pdfs/'}
    return render(request, 'show_pdf.html', context)



# CRAER Y LOGIN DEL ADMINISTRADOR

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index-inscritos')  # Redirige a la página de inicio
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario y/o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'administrador/login-administrador.html', {'form': form})



def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de login o cualquier otra página pública



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige al login después de crear la cuenta
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = UserCreationForm()

    return render(request, 'administrador/crear-administrador.html', {'form': form})