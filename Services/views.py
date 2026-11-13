#from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.
#def Saludo(request):
 #   return HttpResponse("Holita, bienvenido a TimeBank")

def index(request):
    ofertas_prueba = [
        {
            "titulo": "Tutoría de Cálculo Diferencial",
            "categoria": "Académico",
            "proveedor": "Camila Restrepo",
            "horario": "Lun y Mié • 2:00 PM - 4:00 PM",
            "descripcion": "Refuerzo en límites, derivadas y preparación para parciales.",
        },
        {
            "titulo": "Diseño de Presentaciones y Flyers",
            "categoria": "Diseño",
            "proveedor": "Mateo Gómez",
            "horario": "Mar y Jue • 10:00 AM - 12:00 PM",
            "descripcion": "Creación de diapositivas profesionales en Canva o Figma para exposiciones.",
        },
        {
            "titulo": "Asesoría en Python y Django Básico",
            "categoria": "Programación",
            "proveedor": "Valentina Ríos",
            "horario": "Vie • 3:00 PM - 6:00 PM",
            "descripcion": "Ayuda con lógica de programación, modelos y configuración de proyectos.",
        },
    ]
    return render(request, "index.html", {"ofertas": ofertas_prueba})


def exchanges(request):
    lista_intercambios = [
        {
            "id": 101,
            "servicio_recibido": "Tutoría de Cálculo Diferencial",
            "servicio_devuelto": "Diseño de Presentaciones (Trueque)",
            "fecha": "15 Nov 2026",
            "horas": "2.0 hrs",
            "estado": "Aceptado",
            "badge": "success",
        },
        {
            "id": 102,
            "servicio_recibido": "Conversación en Inglés B1",
            "servicio_devuelto": "Pago con saldo de horas",
            "fecha": "18 Nov 2026",
            "horas": "1.0 hr",
            "estado": "Pendiente",
            "badge": "warning",
        },
    ]
    return render(
        request, "exchanges.html", {"exchanges": lista_intercambios}
    )


def benefits(request):
    lista_beneficios = [
        {
            "nombre": "Incentivo Académico - Nota 5.0",
            "horas": 50,
            "descripcion": "Homologación de nota máxima en una actividad o seguimiento avalado.",
            "icono": "bi-award",
        },
        {
            "nombre": "Certificado de Servicio Social",
            "horas": 80,
            "descripcion": "Certificación oficial válida como requisito de grado o beca.",
            "icono": "bi-file-earmark-check",
        },
        {
            "nombre": "Bono de Almuerzo en Cafetería",
            "horas": 80,
            "descripcion": "Tiquetera de almuerzos estudiantiles dentro del campus.",
            "icono": "bi-cup-hot",
        },
        {
            "nombre": "Cupo Curso Presencial Dpto.",
            "horas": 100,
            "descripcion": "Acceso gratuito a cursos de extensión o talleres certificados.",
            "icono": "bi-mortarboard",
        },
    ]
    return render(request, "benefits.html", {"benefits": lista_beneficios})