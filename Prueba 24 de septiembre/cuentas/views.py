import math
import random
import secrets
import time

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache

from .forms import CodigoForm, RegistroForm

CODIGO_MINUTOS = 10
MAX_INTENTOS = 5


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # no puede ingresar hasta validar
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)  # token único por usuario
            enlace = request.build_absolute_uri(
                reverse("activar_cuenta", kwargs={"uidb64": uid, "token": token})
            )
            send_mail(
                "Activa tu cuenta en Patitas & Co.",
                f"Hola {user.username}:\n\n"
                f"Abre este enlace para validar tu cuenta:\n{enlace}\n\n"
                f"En la página verás un código de 6 dígitos que debes escribir para terminar el registro.\n"
                f"Si no creaste esta cuenta, ignora este correo.",
                None,
                [user.email],
            )
            return render(request, "cuentas/revisa_correo.html", {"email": user.email})
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})


def _usuario_desde_uid(uidb64):
    try:
        return User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return None


@never_cache
def activar(request, uidb64, token):
    user = _usuario_desde_uid(uidb64)
    if user is None or not default_token_generator.check_token(user, token):
        return render(request, "cuentas/token_invalido.html")
    if user.is_active:
        messages.info(request, "Tu cuenta ya estaba activa. Ingresa con tu usuario.")
        return redirect("login")

    datos = request.session.get("verificacion")
    if not datos or datos.get("uid") != user.pk or datos.get("expira", 0) < time.time():
        datos = {
            "uid": user.pk,
            "codigo": f"{secrets.randbelow(1_000_000):06d}",
            "expira": time.time() + CODIGO_MINUTOS * 60,
            "intentos": 0,
        }
        request.session["verificacion"] = datos

    form = CodigoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if secrets.compare_digest(form.cleaned_data["codigo"], datos["codigo"]):
            user.is_active = True
            user.save(update_fields=["is_active"])
            del request.session["verificacion"]
            messages.success(request, "¡Listo! Tu cuenta quedó registrada. Ya puedes ingresar.")
            return redirect("login")
        datos["intentos"] += 1
        if datos["intentos"] >= MAX_INTENTOS:
            del request.session["verificacion"]
            messages.error(request, "Demasiados intentos. Te mostramos un código nuevo.")
            return redirect(request.path)
        request.session["verificacion"] = datos
        form.add_error("codigo", f"Código incorrecto. Te quedan {MAX_INTENTOS - datos['intentos']} intentos.")

    return render(request, "cuentas/verificar_codigo.html", {"form": form, "minutos": CODIGO_MINUTOS, "ts": int(time.time())})


# ---- Imagen del código: se dibuja con trazos (no es texto), así no se puede copiar ----
SEGMENTOS = {  # siete segmentos: a b c d e f g
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd",
}
PUNTOS = {"a": ((0, 0), (1, 0)), "b": ((1, 0), (1, 1)), "c": ((1, 1), (1, 2)),
          "d": ((0, 2), (1, 2)), "e": ((0, 1), (0, 2)), "f": ((0, 0), (0, 1)), "g": ((0, 1), (1, 1))}


@never_cache
def imagen_codigo(request):
    datos = request.session.get("verificacion")
    if not datos or datos.get("expira", 0) < time.time():
        raise Http404
    rnd = random.SystemRandom()
    ancho, alto = 360, 110
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
              f'<rect width="100%" height="100%" rx="14" fill="#fff7ec"/>']
    for _ in range(14):  # ruido de fondo
        partes.append(f'<line x1="{rnd.randint(0, ancho)}" y1="{rnd.randint(0, alto)}" x2="{rnd.randint(0, ancho)}" '
                      f'y2="{rnd.randint(0, alto)}" stroke="#e9b98a" stroke-width="1.5" opacity="0.6"/>')
    for i, digito in enumerate(datos["codigo"]):
        ox, oy = 30 + i * 52 + rnd.randint(-4, 4), 22 + rnd.randint(-6, 6)
        ang, esc = rnd.uniform(-12, 12), rnd.uniform(28, 33)
        trazos = []
        for s in SEGMENTOS[digito]:
            (x1, y1), (x2, y2) = PUNTOS[s]
            trazos.append(f"M{x1 * esc * 0.8 + rnd.uniform(-1.5, 1.5):.1f} {y1 * esc + rnd.uniform(-1.5, 1.5):.1f} "
                          f"L{x2 * esc * 0.8 + rnd.uniform(-1.5, 1.5):.1f} {y2 * esc + rnd.uniform(-1.5, 1.5):.1f}")
        partes.append(f'<path transform="translate({ox} {oy}) rotate({ang:.1f} 12 30)" d="{" ".join(trazos)}" '
                      f'stroke="#3b2a20" stroke-width="5" stroke-linecap="round" fill="none"/>')
    for _ in range(3):  # curvas encima para dificultar lectura automática
        y = rnd.randint(25, 85)
        partes.append(f'<path d="M0 {y} Q {ancho / 2} {y + rnd.randint(-40, 40)} {ancho} {rnd.randint(25, 85)}" '
                      f'stroke="#f08a4b" stroke-width="2" fill="none" opacity="0.7"/>')
    partes.append("</svg>")
    resp = HttpResponse("".join(partes), content_type="image/svg+xml")
    resp["Content-Disposition"] = "inline"
    return resp
