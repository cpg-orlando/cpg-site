"""Builds the static pages of the CPG site from shared parts.

Run:  python3 src/build.py
Each page is written to the repo root as a standalone .html file.
Text is bilingual: t("español", "English") renders both; the page shows one.
"""
import os
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / "src/style.css").read_text()
# Social links: replace "#" with the church's real pages.
YOUTUBE = "https://www.youtube.com/@casaportadoresdegloria"
FACEBOOK = "https://www.facebook.com/PortadoresCPG"
INSTAGRAM = "https://www.instagram.com/casaportadoresdegloria"

ICON_YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-3.2.5-4.8s-.1-3.2-.5-4.8ZM9.7 15.1V8.9l5.8 3.1-5.8 3.1Z"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7.1V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12Z"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 4.6a5.2 5.2 0 1 0 0 10.4 5.2 5.2 0 0 0 0-10.4Zm0 8.6a3.4 3.4 0 1 1 0-6.8 3.4 3.4 0 0 1 0 6.8Zm5.4-9.9a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4Z"/></svg>'
ICON_PLAY = '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path fill="#e62117" d="M8 5v14l11-7z"/></svg>'


def social_btns():
    return (f'<div class="social-btns"><a class="sbtn yt" href="{YOUTUBE}" target="_blank" rel="noopener">{ICON_YT}YouTube</a>'
            f'<a class="sbtn fb" href="{FACEBOOK}" target="_blank" rel="noopener">{ICON_FB}Facebook</a>'
            f'<a class="sbtn ig" href="{INSTAGRAM}" target="_blank" rel="noopener">{ICON_IG}Instagram</a></div>')


def social_icons():
    return (f'<div class="social-icons"><a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="YouTube">{ICON_YT}</a>'
            f'<a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{ICON_FB}</a>'
            f'<a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{ICON_IG}</a></div>')


GIVE_URL = "https://give.tithe.ly/?formId=1d0a6db2-1fd2-4e47-a150-3e891cfab3f8&amp;locationId=8738e6ec-eb21-4808-9f24-1148a0f17b5d&amp;fundId=c3bb9a7b-24f9-4adc-bb63-8488060e0ea7"
MAPS = "https://www.google.com/maps/search/?api=1&query=5200+Old+Cheney+Highway+Orlando+FL+32807"


def t(es, en):
    return f'<span class="es">{es}</span><span class="en">{en}</span>'


# (file, es, en)
MENU = [
    ("Inicio", "Home", [("index.html", "Bienvenidos", "Welcome")]),
    ("Nosotros", "About", [
        ("nosotros.html", "Quiénes somos", "Who we are"),
        ("pastores.html", "Nuestros pastores", "Our pastors"),
        ("creencias.html", "Lo que creemos", "Our beliefs"),
    ]),
    ("Reuniones", "Gatherings", [
        ("servicios.html", "Servicios semanales", "Weekly services"),
        ("eventos.html", "Eventos", "Events"),
        ("destacados.html", "Momentos destacados", "Highlights"),
        ("ministerios.html", "Ministerios", "Ministries"),
    ]),
    ("Conéctate", "Connect", [
        ("visitanos.html", "Planea tu visita", "Plan a visit"),
        ("oracion.html", "Peticiones de oración", "Prayer requests"),
        ("membresia.html", "Hazte miembro", "Become a member"),
        ("ofrendar.html", "Ofrendar", "Give"),
    ]),
]


def header(current):
    groups = ""
    for ges, gen, items in MENU:
        cur = ' aria-current="page"'
        links = "".join(
            f'<a href="{f}"{cur if f == current else ""}>{t(es, en)}</a>'
            for f, es, en in items
        )
        groups += f'<div class="menu-group"><h2>{t(ges, gen)}</h2>{links}</div>'
    return f"""
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img class="logo" src="images/logo.png" alt="Casa Portadores de Gloria" width="600" height="511"></a>
    <a class="give-pill" href="{GIVE_URL}" target="_blank" rel="noopener">{t("Ofrendar", "Give")}</a>
    <div class="lang" role="group" aria-label="Idioma / Language">
      <button type="button" id="lang-es" data-set-lang="es" aria-pressed="true">ES</button>
      <button type="button" id="lang-en" data-set-lang="en" aria-pressed="false">EN</button>
    </div>
    <button type="button" class="menu-btn" id="menu-open" aria-controls="menu" aria-expanded="false">
      <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="label">{t("Menú", "Menu")}</span>
    </button>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <div class="wrap">
    <div class="menu-top">
      <img class="logo" src="images/logo.png" alt="Casa Portadores de Gloria" width="600" height="511">
      <button type="button" class="menu-close" id="menu-close">{t("Cerrar", "Close")}</button>
    </div>
    <nav class="menu-groups" aria-label="Principal">{groups}</nav>
    {social_icons()}
  </div>
</div>
"""


FOOTER = f"""
<footer>
  <div class="wrap">
    <p class="big">{t("Hay un lugar <em>para ti.</em>", "There's a place <em>for you.</em>")}</p>
    <div class="cols">
      <div>
        <img class="logo logo-lg" src="images/logo.png" alt="Casa Portadores de Gloria" width="600" height="511" loading="lazy">
        <span>5200 Old Cheney Highway<br>Orlando, FL 32807</span>
        <a href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar →", "Get directions →")}</a>
      </div>
      <div>
        <h2>{t("Horarios", "Service times")}</h2>
        <span><strong style="color:#fff;font-weight:600">{t("Servicio Principal", "Main Service")}</strong><br>{t("Domingo", "Sunday")} · 11:00 AM</span>
        <span><strong style="color:#fff;font-weight:600">{t("Estudio Bíblico", "Bible Study")}</strong><br>{t("Miércoles", "Wednesday")} · 7:00 PM</span>
        <span><strong style="color:#fff;font-weight:600">{t("Servicio de Oración", "Prayer Service")}</strong><br>{t("Viernes", "Friday")} · 7:00 PM</span>
      </div>
      <div>
        <h2>{t("Conéctate", "Connect")}</h2>
        <a href="visitanos.html">{t("Planea tu visita", "Plan a visit")}</a>
        <a href="oracion.html">{t("Peticiones de oración", "Prayer requests")}</a>
        <a href="membresia.html">{t("Hazte miembro", "Become a member")}</a>
        <a href="ofrendar.html">{t("Ofrendar", "Give")}</a>
      </div>
      <div>
        <h2>{t("Síguenos", "Follow us")}</h2>
        <span>{t("Servicios en vivo y prédicas", "Live services and sermons")}</span>
        {social_icons()}
      </div>
    </div>
    <p class="legal">© 2026 Casa Portadores de Gloria</p>
  </div>
</footer>
"""

SCRIPT = """
<script>
(function () {
  var root = document.documentElement;
  // Always open a new page at the top (phones and in-app viewers otherwise keep the old scroll spot)
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  function toTop() { if (!location.hash) window.scrollTo(0, 0); }
  toTop(); window.addEventListener('load', toTop); window.addEventListener('pageshow', toTop);
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$=".html"]');
    if (a) { document.body.style.overflow = ''; window.scrollTo(0, 0); }
  });
  function setLang(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-set-lang') === lang));
    });
    try { localStorage.setItem('cpg-lang', lang); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem('cpg-lang'); } catch (e) {}
  setLang(saved === 'en' ? 'en' : 'es');
  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.getAttribute('data-set-lang')); });
  });

  var menu = document.getElementById('menu'), openBtn = document.getElementById('menu-open'), closeBtn = document.getElementById('menu-close');
  function setMenu(open) {
    menu.hidden = !open;
    openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    (open ? closeBtn : openBtn).focus();
  }
  openBtn.addEventListener('click', function () { setMenu(true); });
  closeBtn.addEventListener('click', function () { setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) setMenu(false); });

  // Forms are not connected to a service yet: show a clear note instead of pretending to send.
  document.querySelectorAll('form[data-preview]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = f.querySelector('.form-note');
      if (note) note.hidden = false;
    });
  });
  root.classList.add('js');

  // Header shadow after scrolling
  var hdr = document.querySelector('.site-header');
  function onScroll() { if (hdr) hdr.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Gentle rise-in for blocks as they scroll into view (content is visible either way)
  var targets = document.querySelectorAll('main section .wrap > *:not(.hero-frame), .quick > a, .services > div, .events > div, .min-bento > article, .hl-grid > article, .gallery > img, .expect > div');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight) return; // already on screen: leave as is
      el.classList.add('rv'); el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el);
    });
  }

  // Next-service countdown (times are Orlando / Eastern time)
  var card = document.getElementById('next-card');
  if (card) {
    var SVCS = [
      { dow: 0, h: 11, m: 0, es: 'Servicio Principal', en: 'Main Service', wes: 'Domingo · 11:00 AM', wen: 'Sunday · 11:00 AM' },
      { dow: 3, h: 19, m: 0, es: 'Estudio Bíblico', en: 'Bible Study', wes: 'Miércoles · 7:00 PM', wen: 'Wednesday · 7:00 PM' },
      { dow: 5, h: 19, m: 0, es: 'Servicio de Oración', en: 'Prayer Service', wes: 'Viernes · 7:00 PM', wen: 'Friday · 7:00 PM' }
    ];
    var DAYS = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    function nyNow() {
      var parts = {};
      new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
      return { dow: DAYS[parts.weekday], min: (+parts.hour % 24) * 60 + (+parts.minute) };
    }
    function tick() {
      var now = nyNow(), nowWeek = now.dow * 1440 + now.min, best = null, live = null;
      SVCS.forEach(function (s) {
        var start = s.dow * 1440 + s.h * 60 + s.m;
        var since = (nowWeek - start + 10080) % 10080;
        if (since < 120) live = s;                       // within two hours of starting
        var until = (start - nowWeek + 10080) % 10080;
        if (!best || until < best.until) best = { s: s, until: until };
      });
      var s = live || best.s, mins = live ? 0 : best.until;
      card.classList.toggle('is-live', !!live);
      document.getElementById('next-name').innerHTML = '<span class="es">' + s.es + '</span><span class="en">' + s.en + '</span>';
      document.getElementById('next-when').innerHTML = '<span class="es">' + s.wes + '</span><span class="en">' + s.wen + '</span>';
      card.querySelector('[data-live-es]').textContent = live ? 'En vivo ahora' : 'Próximo servicio';
      card.querySelector('[data-live-en]').textContent = live ? 'Happening now' : 'Next service';
      document.getElementById('cd-d').textContent = Math.floor(mins / 1440);
      document.getElementById('cd-h').textContent = Math.floor((mins % 1440) / 60);
      document.getElementById('cd-m').textContent = mins % 60;
    }
    tick(); setInterval(tick, 30000);
  }

  // Gallery: small preview, expand on demand
  var gal2 = document.getElementById('gallery'), gtog = document.getElementById('gallery-toggle');
  if (gal2 && gtog) {
    var total = gal2.querySelectorAll('img').length;
    if (total > 3) gal2.style.setProperty('--more', '"+' + (total - 2) + '"');
    if (total > 2) gal2.style.setProperty('--more-m', '"+' + (total - 1) + '"');
    var pos = document.getElementById('gal-pos'), tot = document.getElementById('gal-total');
    if (tot) tot.textContent = total;
    gal2.addEventListener('scroll', function () {
      var first = gal2.querySelector('img'); if (!first || !pos) return;
      var step = first.getBoundingClientRect().width + 10;
      pos.textContent = Math.min(total, Math.round(gal2.scrollLeft / step) + 1);
    }, { passive: true });
    gtog.addEventListener('click', function () {
      var open = gal2.classList.toggle('expanded');
      gtog.setAttribute('aria-expanded', String(open));
      gtog.querySelector('.open-label').hidden = open;
      gtog.querySelector('.close-label').hidden = !open;
      if (!open) gal2.scrollIntoView({ block: 'center', behavior: 'smooth' });
    });
  }

  // Copy address
  document.querySelectorAll('.loc-copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var txt = b.getAttribute('data-copy');
      function done() { b.querySelector('.c1').hidden = true; b.querySelector('.c2').hidden = false;
        setTimeout(function () { b.querySelector('.c1').hidden = false; b.querySelector('.c2').hidden = true; }, 1800); }
      try { navigator.clipboard.writeText(txt).then(done, function () { window.prompt && done(); }); } catch (e) { done(); }
    });
  });

  // Tap-to-enlarge gallery
  var gal = Array.prototype.slice.call(document.querySelectorAll('.gallery img'));
  if (gal.length) {
    var lb = document.createElement('div'), idx = 0;
    lb.className = 'lightbox'; lb.hidden = true; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<img alt=""><button type="button" class="lb-btn lb-close" aria-label="Cerrar">✕</button>' +
      '<button type="button" class="lb-btn lb-prev" aria-label="Anterior">←</button><button type="button" class="lb-btn lb-next" aria-label="Siguiente">→</button>';
    document.body.appendChild(lb);
    var big = lb.querySelector('img');
    function show(i) { idx = (i + gal.length) % gal.length; big.src = gal[idx].src; big.alt = gal[idx].alt; }
    function close() { lb.hidden = true; document.body.style.overflow = ''; }
    gal.forEach(function (img, i) {
      img.tabIndex = 0;
      function open() { show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); }
      img.addEventListener('click', open);
      img.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1);
    });
  }
  // Verse words light up as the reader scrolls through it
  var verse = document.querySelector('[data-scroll-verse]');
  if (verse) {
    var groups = Array.prototype.map.call(verse.children, function (g) { return g.querySelectorAll('span'); });
    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function paint() {
      var r = verse.getBoundingClientRect(), vh = window.innerHeight;
      var prog = calm ? 1 : Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (vh * 0.55)));
      groups.forEach(function (ws) {
        var lit = Math.round(prog * ws.length);
        ws.forEach(function (w, i) { w.classList.toggle('lit', i < lit); });
      });
    }
    paint(); window.addEventListener('scroll', function () { requestAnimationFrame(paint); }, { passive: true });
  }

  // Cursor spotlight on glass cards
  document.querySelectorAll('.quick a, .service, .event, .min-row, .expect > div, .way, .value, .soon-block, .next-card, .hl').forEach(function (el) {
    el.classList.add('spot');
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // Slow parallax on hero photos
  var heroImg = document.querySelector('.hero-frame > img');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (heroImg && !still) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 900);
        heroImg.style.transform = 'translateY(' + (y * 0.22) + 'px)';
        ticking = false;
      });
    }, { passive: true });
  }
})();
</script>
"""


# ---------------------------------------------------------------- Photos
# Every photo spot on a page is numbered in order (1, 2, 3...). Unassigned spots show a
# numbered placeholder. Assign a photo with: PHOTOS["index.html"][1] = ("file.jpg", "center 40%")
PAGE_LABELS = {
    "index.html": "Inicio", "nosotros.html": "Nosotros", "pastores.html": "Pastores",
    "servicios.html": "Servicios", "eventos.html": "Eventos", "ministerios.html": "Ministerios",
    "ofrendar.html": "Ofrendar", "destacados.html": "Destacados", "creencias.html": "Creencias",
    "oracion.html": "Oración", "visitanos.html": "Visítanos", "membresia.html": "Membresía",
}
PHOTOS = {f: {} for f in PAGE_LABELS}
PHOTOS["index.html"][1] = ("equipo-alabanza.jpg", "8% 30%")
PHOTOS["index.html"][3] = ("cruz-verde.jpg", "center 35%")
PHOTOS["index.html"][2] = ("pastores-avatar.jpg", "center")
PHOTOS["servicios.html"][2] = ("alabanza-domingo.jpg", "45% 40%")
# --- photo picks (Oct 23)
P = PHOTOS
P["index.html"].update({4: ("equipo-pulpito.jpg", "50% 60%"), 5: ("mama-nino-biblia.jpg", "55% center"),
    6: ("pastor-congregacion.jpg", "40% center"), 7: ("saludo-mayores.jpg", "45% center"),
    8: ("pasillo-hermanos.jpg", "45% center"), 9: ("ninos-biblias-2.jpg", "35% center"),
    10: ("circulo-oracion.jpg", "35% center"), 11: ("congregacion-orando.jpg", "45% center"),
    12: ("transmision-biblia.jpg", "60% 40%")})
P["nosotros.html"].update({1: ("pasillo-saludo.jpg", "center 55%"), 2: ("entrada-saludo.jpg", "60% center"),
    3: ("cruz.jpg", "center 35%")})
P["servicios.html"].update({1: ("pastor-luces.jpg", "55% 40%"), 3: ("nino-biblia.jpg", "55% center"),
    4: ("circulo-oracion.jpg", "35% 40%"), 5: ("transmision.jpg", "50% center")})
P["ministerios.html"].update({1: ("ninos-biblias.jpg", "40% 45%"),
    2: ("hombres-orando.jpg", "50% center"), 3: ("damas-oracion.jpg", "45% 55%"),
    4: ("youth-grupo.jpg", "50% 55%"), 5: ("ninos-clase.jpg", "45% center"),
    6: ("alabanza-cantante.jpg", "50% 30%"), 7: ("entrada-saludo.jpg", "55% center"),
    8: ("noche-internacional.jpg", "40% center"), 9: ("hermanos-ventana.jpg", "45% center")})
P["eventos.html"][1] = ("salon-reunion.jpg", "center 60%")
P["ofrendar.html"][1] = ("manos-alzadas.jpg", "40% center")
P["creencias.html"][1] = ("cruz-adoracion.jpg", "60% 45%")
P["oracion.html"][1] = ("abrazo-oracion.jpg", "30% center")
P["visitanos.html"][1] = ("saludo-jovenes.jpg", "50% 35%")
P["membresia.html"][1] = ("ancianos-risas.jpg", "50% 30%")
P["destacados.html"].update({1: ("adoracion-manos.jpg", "center 55%"),
    2: ("noche-internacional.jpg", "40% center"), 3: ("bautismos.jpg", "50% 65%"), 4: ("conferencia-mujeres.jpg", "50% 42%"),
    5: ("pastora-abrazo.jpg", "center 35%"), 6: ("mujeres-orando.jpg", "40% center"), 7: ("glory-night-grupo.jpg", "center 60%"),
    8: ("abrazo-hermanos.jpg", "50% center"), 9: ("risas-puerta.jpg", "60% center"), 10: ("lider-escenario.jpg", "45% center"),
    11: ("predicador-invitado.jpg", "center 40%"), 12: ("noche-internacional-2.jpg", "30% center"), 13: ("abrazo-joven.jpg", "55% center"),
    14: ("pastor-brazos.jpg", "center 30%"), 15: ("saludo-hermanas.jpg", "65% center"), 16: ("jovenes-sonrisa.jpg", "center 30%"), 17: ("mujeres-risas.jpg", "30% 45%"), 18: ("mujeres-convivio.jpg", "center 55%")})
PHOTOS["pastores.html"][1] = ("pastora-adorando.jpg", "center 22%")
PHOTOS["pastores.html"][2] = ("pastores-pareja.jpg", "center 20%")
PHOTOS["pastores.html"][3] = ("pastor-predicando.jpg", "50% center")
PHOTOS["pastores.html"][4] = ("familia-toirac.jpg", "center")
SLOTS = {}


def placeholder(label, n):
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice">'
        '<rect width="400" height="300" fill="#14141d"/>'
        '<g fill="none" stroke="#4a4d66" stroke-width="3" stroke-linejoin="round">'
        '<rect x="176" y="104" width="48" height="36" rx="6"/><circle cx="200" cy="122" r="9"/></g>'
        f'<text x="200" y="176" text-anchor="middle" font-family="Arial, sans-serif" font-size="26" font-weight="700" fill="#8a8daa">{label} · {n}</text>'
        '</svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg)


def slotify(fname, html):
    n = 0
    label = PAGE_LABELS.get(fname, fname)

    def sub(m):
        nonlocal n
        tag = m.group(0)
        if 'src="images/' not in tag or "logo.png" in tag:
            return tag
        n += 1
        tag = re.sub(r'\sstyle="[^"]*"', "", tag)
        chosen = PHOTOS.get(fname, {}).get(n)
        if chosen:
            file, pos = chosen
            return re.sub(r'src="images/[^"]+"', f'src="images/{file}" style="object-position: {pos}"', tag)
        return re.sub(r'src="images/[^"]+"', f'src="{placeholder(label, n)}" data-slot="{label} {n}"', tag)

    return re.sub(r"<img\b[^>]*>", sub, html), n


def page(fname, title, body):
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Casa Portadores de Gloria — iglesia cristiana bilingüe en Orlando, Florida.">
<link rel="icon" href="images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Figtree:wght@400;500;600;700&display=swap">
<style>
{CSS}
</style>
</head>
<body>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div><div class="grain" aria-hidden="true"></div>
{header(fname)}
<main>
{body}
</main>
{FOOTER}
{SCRIPT}
</body>
</html>
"""
    html, count = slotify(fname, html)
    SLOTS[fname] = count
    (ROOT / fname).write_text(html)


def banner(img, eyebrow, title, sub="", pos="center"):
    subp = f'<p class="sub">{sub}</p>' if sub else ""
    return f"""
<section class="page-hero">
  <div class="wrap hero-wrap">
    <div class="hero-frame">
      <img src="images/{img}" alt="" style="object-position: {pos}">
      <div class="hero-copy">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        {subp}
      </div>
    </div>
  </div>
</section>"""


def head(eyebrow, title, lead=""):
    leadp = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="section-head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>{leadp}</div>'


def form_note():
    return f'<p class="form-note" hidden>{t("Vista previa: este formulario todavía no está conectado, así que no se envió nada. Muy pronto estará activo.", "Preview: this form isn&#39;t connected yet, so nothing was sent. It will be active soon.")}</p>'


SERVICES = [
    ("domingo.jpg", "center", "Domingo", "Sunday", "11:00", "AM", "Servicio Principal", "Main Service",
     "Adoración, la Palabra y comunión para toda la familia.", "Worship, the Word, and fellowship for the whole family."),
    ("estudio-biblico.jpg", "center 35%", "Miércoles", "Wednesday", "7:00", "PM", "Estudio Bíblico", "Bible Study",
     "Cada grupo de edad tiene su propio estudio para profundizar en las Escrituras.", "Each age group has its own study to dig deeper into Scripture."),
    ("oracion.jpg", "center", "Viernes", "Friday", "7:00", "PM", "Servicio de Oración", "Prayer Service",
     "Una noche para buscar el rostro de Dios juntos e interceder por nuestra comunidad, nuestra ciudad y las naciones.", "A night to seek God's face together and intercede for our community, our city, and the nations."),
]


AGES = (f'<ul class="ages">'
        f'<li>{t("Niños", "Children")}</li>'
        f'<li>{t("Jóvenes y Jóvenes Adultos", "Youth &amp; Young Adults")}</li>'
        f'<li>{t("Adultos 30+", "Adults 30+")}</li></ul>')


def service_cards():
    out = ""
    for img, pos, des, den, time, ap, nes, nen, des2, den2 in SERVICES:
        out += f"""
      <div class="service">
        <img class="service-img" src="images/{img}" alt="" loading="lazy" style="object-position: {pos}">
        <p class="eyebrow">{t(des, den)}</p>
        <div class="when">{time}<span>{ap}</span></div>
        <h3>{t(nes, nen)}</h3>
        <p>{t(des2, den2)}</p>{AGES if den == "Wednesday" else ""}
      </div>"""
    return f'<div class="services">{out}\n    </div>'


EVENTS = [
    ("Oct", "29", "Para todos", "Everyone", "CPG Sports Day",
     "Jueves, 6:30 PM en Brush Arbor Christian School. Baloncesto, voleibol y comunión. ¡Todos son bienvenidos!",
     "Thursday, 6:30 PM at Brush Arbor Christian School. Basketball, volleyball, and fellowship. Everyone is welcome!"),
    ("Nov", "4", "CPG Youth", "CPG Youth", "Glory Night",
     "Miércoles, 7:00 PM. Una noche de adoración y Palabra para jóvenes y jóvenes adultos. ¡El último Glory Night del año!",
     "Wednesday, 7:00 PM. A night of worship and the Word for youth and young adults. The last Glory Night of the year!"),
    ("Nov", "14", "CPG Youth", "CPG Youth", "Abide Conference",
     "Sábado, 12:00–7:00 PM. 26134 Leeward St., Eustis, FL.",
     "Saturday, 12:00–7:00 PM. 26134 Leeward St., Eustis, FL."),
]


def live_band():
    return f"""
<section class="live">
  <div class="wrap">
    <div class="stack">
      <span class="live-badge">{t("En vivo", "Live")}</span>
      <h2>{t("Míranos en vivo", "Watch us live")}</h2>
      <p>{t("¿No puedes venir en persona? Acompáñanos en línea los domingos a las 11:00 AM y vuelve a ver las prédicas cuando quieras.",
            "Can't make it in person? Join us online Sundays at 11:00 AM and rewatch sermons anytime.")}</p>
      {social_btns()}
    </div>
    <div class="shot">
      <img src="images/consola.jpg" alt="" loading="lazy" style="object-position: center 55%">
      <a class="play" href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="YouTube"><span>{ICON_PLAY}</span></a>
    </div>
  </div>
</section>"""


def event_list(limit=None):
    out = ""
    for m, d, tes, ten, name, des, den in EVENTS[:limit]:
        out += f"""
      <div class="event">
        <div class="date"><span class="m">{m}</span><span class="d">{d}</span></div>
        <div>
          <span class="tag">{t(tes, ten)}</span>
          <h3>{name}</h3>
          <p>{t(des, den)}</p>
        </div>
      </div>"""
    return f'<div class="events">{out}\n    </div>'


# ---------------------------------------------------------------- 1. Welcome
page("index.html", "Casa Portadores de Gloria", f"""
<section class="hero" id="inicio">
  <div class="wrap hero-wrap">
    <div class="hero-frame">
      <picture>
        <source media="(max-width: 600px)" srcset="images/pastora-adorando.jpg">
        <img src="images/oracion-grupo.jpg" alt="Adoración en Casa Portadores de Gloria" fetchpriority="high" style="object-position: 50% 45%">
      </picture>
      <div class="hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">Casa Portadores de Gloria · Orlando</p>
          <h1>{t('Bienvenidos<br>a <em>casa.</em>', 'Welcome<br><em>home.</em>')}</h1>
          <p>{t("Una iglesia bilingüe donde las familias adoran, crecen en la Palabra y llevan la gloria de Dios a Orlando.",
                "A bilingual church where families worship, grow in the Word, and carry God's glory to Orlando.")}</p>
          <div class="actions">
            <a class="btn btn-primary" href="visitanos.html">{t("Planea tu visita", "Plan your visit")} <span class="arr">→</span></a>
            <a class="btn btn-ghost" href="servicios.html">{t("Horarios", "Service times")}</a>
          </div>
        </div>
        <div class="next-card" id="next-card" aria-live="polite">
          <span class="lbl"><span class="dot"></span><span class="es" data-live-es>Próximo servicio</span><span class="en" data-live-en>Next service</span></span>
          <span class="name" id="next-name">{t("Servicio Principal", "Main Service")}</span>
          <span class="when" id="next-when">{t("Domingo · 11:00 AM", "Sunday · 11:00 AM")}</span>
          <div class="count">
            <div><b id="cd-d">–</b><small>{t("días", "days")}</small></div>
            <div><b id="cd-h">–</b><small>{t("horas", "hours")}</small></div>
            <div><b id="cd-m">–</b><small>{t("min", "min")}</small></div>
          </div>
          <a class="btn btn-primary" href="visitanos.html">{t("Acompáñanos", "Join us")} <span class="arr">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="verse-band">
  <div class="wrap">
    <p class="eyebrow">{t("Nuestro versículo", "Our scripture")}</p>
    <blockquote class="scroll-verse" data-scroll-verse>
      <span class="es"><span>Mas</span> <span>vosotros</span> <span>sois</span> <span>linaje</span> <span>escogido,</span> <span>real</span> <span>sacerdocio,</span> <span>nación</span> <span>santa,</span> <span>pueblo</span> <span>adquirido</span> <span>por</span> <span>Dios,</span> <span>para</span> <span>que</span> <span>anunciéis</span> <span>las</span> <span>virtudes</span> <span>de</span> <span>aquel</span> <span>que</span> <span>os</span> <span>llamó</span> <span>de</span> <span>las</span> <span>tinieblas</span> <span>a</span> <span>su</span> <span class="g">luz</span> <span class="g">admirable.</span></span><span class="en"><span>But</span> <span>you</span> <span>are</span> <span>a</span> <span>chosen</span> <span>people,</span> <span>a</span> <span>royal</span> <span>priesthood,</span> <span>a</span> <span>holy</span> <span>nation,</span> <span>God&#39;s</span> <span>special</span> <span>possession,</span> <span>that</span> <span>you</span> <span>may</span> <span>declare</span> <span>the</span> <span>praises</span> <span>of</span> <span>him</span> <span>who</span> <span>called</span> <span>you</span> <span>out</span> <span>of</span> <span>darkness</span> <span>into</span> <span>his</span> <span class="g">wonderful</span> <span class="g">light.</span></span>
    </blockquote>
    <p class="verse-ref">{t("1 Pedro 2:9", "1 Peter 2:9")}</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="stack">
      <p class="eyebrow">{t("Te damos la bienvenida", "We're glad you're here")}</p>
      <h2>{t("Una casa para llevar su gloria", "A house that carries His glory")}</h2>
      <p class="lead">{t("Somos una familia de fe en Orlando, donde la Palabra se predica en español con traducción al inglés. Ya sea tu primera vez en una iglesia o estés buscando un hogar espiritual, aquí eres bienvenido.",
                        "We're a family of faith in Orlando, where the Word is preached in Spanish with English translation. Whether it's your first time in church or you're looking for a spiritual home, you're welcome here.")}</p>
      <div class="pastors">
        <img src="images/pastor-pulpito.jpg" alt="Pastor Esdras Toirac" loading="lazy" style="object-position: 55% 22%">
        <div><span class="names">Esdras &amp; Magnolia Toirac</span><span class="role">{t("Pastores", "Senior Pastors")} · <a href="pastores.html">{t("Conócelos", "Meet them")}</a></span></div>
      </div>
    </div>
    <img class="photo" src="images/predicacion-logo.jpg" alt="Predicación en Casa Portadores de Gloria" loading="lazy" style="object-position: 45% center">
  </div>
</section>

<section style="padding-block: 0 clamp(56px, 9vw, 104px)">
  <div class="wrap strip">
    <img src="images/domingo.jpg" alt="Equipo de alabanza" loading="lazy">
    <img src="images/abrazo.jpg" alt="Un abrazo de bienvenida" loading="lazy" style="object-position: 65% 30%">
    <img src="images/ninos.jpg" alt="Niños con sus Biblias" loading="lazy" style="object-position: 35% center">
    <img src="images/risas.jpg" alt="Hermanos riendo" loading="lazy" style="object-position: 65% center">
  </div>
</section>

<section class="band">
  <div class="wrap">
    {head(t("Empieza aquí", "Start here"), t("¿Cómo te podemos ayudar?", "How can we help?"))}
    <div class="quick">
      <a href="visitanos.html"><img src="images/q1.jpg" alt=""><b>{t("Planea tu visita", "Plan a visit")}</b><span class="d">{t("Qué esperar y cómo llegar.", "What to expect and how to get here.")}</span><span class="go">→</span></a>
      <a href="ministerios.html"><img src="images/q2.jpg" alt=""><b>{t("Ministerios", "Ministries")}</b><span class="d">{t("Caballeros, damas, jóvenes, niños, alabanza y más.", "Men, women, youth, kids, worship, and more.")}</span><span class="go">→</span></a>
      <a href="oracion.html"><img src="images/q3.jpg" alt=""><b>{t("Pide oración", "Ask for prayer")}</b><span class="d">{t("Nuestro equipo orará por ti.", "Our team will pray for you.")}</span><span class="go">→</span></a>
      <a href="ofrendar.html"><img src="images/q4.jpg" alt=""><b>{t("Ofrendar", "Give")}</b><span class="d">{t("Diezmos y ofrendas.", "Tithes and offerings.")}</span><span class="go">→</span></a>
    </div>
  </div>
</section>

{live_band()}

<section class="events-band">
  <div class="wrap">
    {head(t("Próximamente", "Coming up"), t("Lo que viene", "What's next"))}
    {event_list(2)}
    <div class="cta-row" style="margin-top:24px"><a class="btn btn-outline" href="eventos.html">{t("Ver todos los eventos", "See all events")}</a></div>
  </div>
</section>
""")

APPLE_MAPS = "https://maps.apple.com/?q=Casa+Portadores+de+Gloria&address=5200+Old+Cheney+Hwy,+Orlando,+FL+32807"
MAP_SVG = """<svg class="loc-map" viewBox="0 0 600 340" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="600" height="340" fill="#0f1f36"/>
  <g stroke="#1d3354" stroke-width="1">
    <path d="M0 40H600M0 95H600M0 150H600M0 205H600M0 260H600M0 315H600"/>
    <path d="M60 0V340M140 0V340M220 0V340M380 0V340M460 0V340M540 0V340"/>
  </g>
  <rect x="70" y="105" width="60" height="38" rx="3" fill="#13284a"/><rect x="390" y="50" width="60" height="38" rx="3" fill="#13284a"/>
  <rect x="470" y="215" width="62" height="38" rx="3" fill="#13284a"/><rect x="150" y="215" width="62" height="38" rx="3" fill="#13284a"/>
  <path d="M-10 250 C120 230 200 190 300 172 S480 120 610 96" fill="none" stroke="#2a4670" stroke-width="18" stroke-linecap="round"/>
  <path d="M-10 250 C120 230 200 190 300 172 S480 120 610 96" fill="none" stroke="#d6a84a" stroke-width="2" stroke-dasharray="10 9" opacity=".75"/>
  <path d="M300 -10V350" stroke="#22395c" stroke-width="12"/>
  <text x="430" y="132" fill="#6f84a6" font-family="Figtree, Arial, sans-serif" font-size="13" letter-spacing="2" transform="rotate(-13 430 132)">OLD CHENEY HWY</text>
  <g class="loc-pin" transform="translate(300 172)">
    <circle class="loc-pulse" r="18" fill="#d6a84a" opacity=".35"/>
    <circle class="loc-pulse d2" r="18" fill="#d6a84a" opacity=".25"/>
    <path d="M0 -6 C-14 -6 -22 -18 -22 -30 C-22 -43 -12 -52 0 -52 C12 -52 22 -43 22 -30 C22 -18 14 -6 0 -6Z" transform="translate(0 6)" fill="#d6a84a"/>
    <circle cy="-24" r="7.5" fill="#0b1626"/>
  </g>
</svg>"""



MAP_EMBED = "https://maps.google.com/maps?q=5200%20Old%20Cheney%20Highway%2C%20Orlando%2C%20FL%2032807&z=15&output=embed"


def where_section():
    rows = [
        (t("Dom", "Sun"), "11:00 AM", t("Servicio Principal", "Main Service")),
        (t("Mié", "Wed"), "7:00 PM", t("Estudio Bíblico", "Bible Study")),
        (t("Vie", "Fri"), "7:00 PM", t("Servicio de Oración", "Prayer Service")),
    ]
    times = "".join(f'<li><span class="d">{d}</span><b>{h}</b><span class="n">{n}</span></li>' for d, h, n in rows)
    return f"""
<section class="where" id="ubicacion">
  <div class="wrap where-grid">
    <figure class="where-fig">
      <div class="where-map">
        {MAP_SVG}
        <iframe src="{MAP_EMBED}" title="Mapa / Map: Casa Portadores de Gloria" loading="lazy" referrerpolicy="no-referrer-when-downgrade" tabindex="-1"></iframe>
        <span class="where-tint" aria-hidden="true"></span>
        <span class="where-ring" aria-hidden="true"><i></i><i></i></span>
        <span class="where-tag">5200 Old Cheney Hwy</span>
        <a class="where-open" href="{MAPS}" target="_blank" rel="noopener" aria-label="Abrir en Google Maps / Open in Google Maps"><span>{t("Abrir mapa", "Open map")} ↗</span></a>
      </div>
      <img class="where-photo" src="images/edificio.jpg" alt="Pasillo exterior de la iglesia" loading="lazy">
      <figcaption>Casa Portadores de Gloria · Orlando, FL</figcaption>
    </figure>
    <div class="where-info">
      {head(t("Ubicación", "Location"), t("Dónde <em>estamos</em>", "Where <em>we are</em>"))}
      <address><b>5200 Old Cheney Highway</b><span>Orlando, FL 32807</span></address>
      <ul class="where-times">{times}</ul>
      <p class="where-note">{t("Estacionamiento gratis en el lugar. Mensaje en español con traducción al inglés.",
                              "Free parking on site. Message in Spanish with English translation.")}</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} <span class="arr">→</span></a>
        <a class="btn btn-outline" href="{APPLE_MAPS}" target="_blank" rel="noopener">Apple Maps</a>
        <button type="button" class="btn btn-outline loc-copy" data-copy="5200 Old Cheney Highway, Orlando, FL 32807">
          <span class="c1">{t("Copiar dirección", "Copy address")}</span><span class="c2" hidden>{t("¡Copiada!", "Copied!")}</span>
        </button>
      </div>
      <a class="where-plan" href="visitanos.html">{t("¿Primera vez? Planea tu visita", "First time? Plan your visit")} <span class="arr">→</span></a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- "Qué esperar" icons (gold line icons, 24px grid)
EXP_ICONS = {
    "music": '<path d="M9 18V5.5l11-2V16"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/><path d="M9 9.5l11-2"/>',
    "book": '<path d="M12 6.5C10 5 7 4.5 3.5 4.5v14c3.5 0 6.5.5 8.5 2 2-1.5 5-2 8.5-2v-14C17 4.5 14 5 12 6.5z"/><path d="M12 6.5v14"/>',
    "bilingual": '<path d="M3.5 4.5h11v8h-6l-4 3.5v-3.5h-1z"/><path d="M14.5 8.5h6v8h-1V20l-4-3.5h-4.5v-4"/><path d="M6.5 8.5h5"/>',
    "family": '<circle cx="6.5" cy="6.5" r="2.2"/><path d="M3 20.5V15a3.5 3.5 0 0 1 7 0"/><circle cx="17.5" cy="6.5" r="2.2"/><path d="M14 15a3.5 3.5 0 0 1 7 0v5.5"/><circle cx="12" cy="12" r="1.7"/><path d="M9.5 20.5v-2.5a2.5 2.5 0 0 1 5 0v2.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.3a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.7" r="2.5"/>',
    "house": '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5v10h13v-10"/><path d="M10 19.5v-5h4v5"/>',
    "city": '<path d="M3 20.5h18"/><path d="M5 20.5v-9l4-2v11"/><path d="M9 20.5v-15h6v15"/><path d="M15 20.5v-8h4v8"/><path d="M11.5 8.5h1M11.5 11.5h1M11.5 14.5h1"/>',
    "nation": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.5 2.5 3.7 5.3 3.7 8.5s-1.2 6-3.7 8.5c-2.5-2.5-3.7-5.3-3.7-8.5s1.2-6 3.7-8.5z"/>',
    "kids": '<circle cx="12" cy="5.5" r="2.5"/><path d="M12 8.5v6.5M12 15l-3 5.5M12 15l3 5.5M6.5 10.5l5.5 1.5 5.5-1.5"/>',
}


def exp_box(icon, h, p):
    return (f'<div><span class="exp-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{EXP_ICONS[icon]}</svg></span>'
            f'<h3>{h}</h3><p>{p}</p></div>')

# ---------------------------------------------------------------- 2. Who we are
page("nosotros.html", "Quiénes Somos · CPG", f"""
{banner("predicacion-logo.jpg", t("Nosotros", "About"), t("Quiénes somos", "Who we are"), pos="45% center")}
<section>
  <div class="wrap split">
    <div class="stack">
      {head(t("Nuestra iglesia", "Our church"), t("Una familia que lleva su gloria", "A family that carries His glory"))}
      <p class="lead">{t("Casa Portadores de Gloria es una iglesia cristiana en Orlando. Creemos que cada persona fue creada para conocer a Jesús y reflejar su gloria en su hogar, su trabajo y su ciudad.",
                        "Casa Portadores de Gloria is a Christian church in Orlando. We believe every person was created to know Jesus and reflect His glory at home, at work, and in their city.")}</p>
      <p class="lead">{t("Somos una comunidad bilingüe: los mensajes del domingo son en español, con traducción al inglés, para que toda la familia, de todas las generaciones, se sienta en casa.",
                        "We're a bilingual community: Sunday messages are in Spanish with English translation, so the whole family, across generations, feels at home.")}</p>
      <p class="lead">{t("Somos una iglesia autónoma en compañerismo con la Asociación Bautista de Orlando, la Convención Bautista de Florida y la Convención Bautista del Sur.",
                        "We are an autonomous church in fellowship with the Greater Orlando Baptist Association, the Florida Baptist Convention, and the Southern Baptist Convention.")}</p>
      <a class="btn btn-outline" style="justify-self:start" href="creencias.html">{t("Lo que creemos", "What we believe")} <span class="arr">→</span></a>
    </div>
    <img class="photo" src="images/bienvenida.jpg" alt="Saludos al final del servicio" loading="lazy" style="object-position: 60% center">
  </div>
</section>
{where_section()}
""")

# ---------------------------------------------------------------- 3. Pastors
page("pastores.html", "Nuestros Pastores · CPG", f"""
{banner("predicacion.jpg", t("Nosotros", "About"), t("Nuestros pastores", "Our pastors"), pos="center 40%").replace('class="page-hero"', 'class="page-hero compact"')}
<section class="pastors-page">
  <div class="wrap pastor-grid">
    <div class="pastor-intro">
      <img class="pastor-photo" src="images/pastor-pulpito.jpg" alt="Pastores Esdras y Magnolia Toirac" loading="lazy">
      <div class="stack">
        <p class="eyebrow">{t("Pastores principales", "Senior Pastors")}</p>
        <h2>Esdras &amp; Magnolia Toirac</h2>
        <p class="lead">{t("Los pastores Esdras y Magnolia Toirac guían a la familia de Casa Portadores de Gloria con amor por Dios, por su Palabra y por la gente de Orlando.",
                          "Pastors Esdras and Magnolia Toirac lead the Casa Portadores de Gloria family with a love for God, His Word, and the people of Orlando.")}</p>
      </div>
    </div>
  </div>
</section>
<section class="calling">
  <div class="wrap calling-grid">
    <img class="calling-photo" src="images/pastor-predicando.jpg" alt="Pastor Esdras Toirac predicando" loading="lazy">
    <div class="stack">
      <p class="eyebrow">{t("Su llamado", "His calling")}</p>
      <h2>{t("Pastor Esdras Toirac", "Pastor Esdras Toirac")}</h2>
      <p class="lead">{t("El pastor Esdras Toirac ha predicado en Casa Portadores de Gloria desde 1996, y en agosto de 2003 asumió como pastor principal.",
                        "Pastor Esdras Toirac has been preaching at Casa Portadores de Gloria since 1996, and in August 2003 he became senior pastor.")}</p>
      <p class="lead">{t("Servir en esta casa es la pasión de su vida, junto a los extraordinarios miembros y líderes de esta increíble comunidad de creyentes.",
                        "Serving this house is the passion of his life, alongside the extraordinary members and leaders of this incredible community of believers.")}</p>
      <p class="lead">{t("Obtuvo su bachillerato y su maestría en Estudios Bíblicos y Teológicos en la UBI en Orlando, Florida (1999–2002).",
                        "He earned his bachelor's and master's degrees in Biblical and Theological Studies at UBI in Orlando, Florida (1999–2002).")}</p>
      <dl class="facts">
        <div><dt>1996</dt><dd>{t("Comienza a predicar en CPG", "Begins preaching at CPG")}</dd></div>
        <div><dt>2003</dt><dd>{t("Pastor principal", "Senior pastor")}</dd></div>
        <div><dt>B.A. · M.A.</dt><dd>{t("Estudios Bíblicos y Teológicos, UBI", "Biblical &amp; Theological Studies, UBI")}</dd></div>
      </dl>
    </div>
  </div>
</section>
<section class="family-section">
  <div class="wrap family-grid">
    <div class="stack">
      <p class="eyebrow">{t("Su familia", "Their family")}</p>
      <h2>{t("La familia Toirac", "The Toirac family")}</h2>
      <p class="lead">{t("Los pastores Esdras y Magnolia sirven a esta casa junto a sus hijos, como una familia que lleva la gloria de Dios a Orlando.",
                        "Pastors Esdras and Magnolia serve this house alongside their children, as a family carrying God&#39;s glory to Orlando.")}</p>
    </div>
    <img class="family-photo" src="images/familia-toirac.jpg" alt="Los pastores Esdras y Magnolia Toirac con sus hijos" loading="lazy">
  </div>
</section>
""")

def location_card():
    return f"""
    <div class="loc-card">
      <a class="loc-visual" href="{MAPS}" target="_blank" rel="noopener" aria-label="Abrir mapa / Open map">{MAP_SVG}
        <span class="loc-chip">{t("Te esperamos aquí", "Find us here")}</span>
      </a>
      <div class="loc-info">
        <p class="eyebrow">{t("Ubicación", "Location")}</p>
        <address><b>5200 Old Cheney Highway</b><span>Orlando, FL 32807</span></address>
        <p class="loc-note">{t("Hay estacionamiento en el lugar. ¡Llega unos minutos antes y te recibimos!", "Parking is available on site. Come a few minutes early and we&#39;ll welcome you!")}</p>
        <div class="loc-actions">
          <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")} <span class="arr">→</span></a>
          <a class="btn btn-outline" href="{APPLE_MAPS}" target="_blank" rel="noopener">Apple Maps</a>
          <button type="button" class="btn btn-outline loc-copy" data-copy="5200 Old Cheney Highway, Orlando, FL 32807">
            <span class="c1">{t("Copiar dirección", "Copy address")}</span><span class="c2" hidden>{t("¡Copiada!", "Copied!")}</span>
          </button>
        </div>
      </div>
    </div>"""


# ---------------------------------------------------------------- 4. Services
page("servicios.html", "Servicios · CPG", f"""
{banner("mano-alzada.jpg", t("Reuniones", "Gatherings"), t("Servicios semanales", "Weekly services"), t("Tres noches, una familia. Te esperamos.", "Three gatherings, one family. We'll save you a seat."))}
<section>
  <div class="wrap">
    {service_cards()}
    {location_card()}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head(t("Tu primera vez", "Your first time"), t("Qué esperar", "What to expect"))}
    <div class="expect">
      {exp_box("music", t("Adoración", "Worship"), t("Música en vivo con nuestro equipo de alabanza.", "Live music with our worship team."))}
      {exp_box("book", t("La Palabra", "The Word"), t("Una enseñanza bíblica clara y práctica.", "Clear, practical Bible teaching."))}
      {exp_box("bilingual", t("Bilingüe", "Bilingual"), t("Mensaje en español, con traducción al inglés.", "Message in Spanish, with English translation."))}
      {exp_box("family", t("Para la familia", "For families"), t("Hay un lugar para los niños.", "There's a place for the kids."))}
    </div>
  </div>
</section>
{live_band()}
""")

# ---------------------------------------------------------------- 5. Events
page("eventos.html", "Eventos · CPG", f"""
{banner("alabanza.jpg", t("Reuniones", "Gatherings"), t("Eventos", "Events"), t("Lo que viene en la vida de la iglesia.", "What's coming up in the life of the church."))}
<section class="events-band">
  <div class="wrap">
    {event_list()}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="soon-block">
      <h3>{t("¿Quieres enterarte primero?", "Want to hear first?")}</h3>
      <p style="color:var(--muted)">{t("Síguenos en Instagram para los anuncios de cada semana.", "Follow us on Instagram for weekly announcements.")}</p>
      <a class="btn btn-ink" href="{INSTAGRAM}" target="_blank" rel="noopener">@casaportadoresdegloria</a>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 6. Ministries
MINS = [
    ("x.jpg", "center", "Caballeros", "Men&#39;s Ministry", "Hermandad", "Brotherhood",
     "Hombres que se apoyan, oran juntos y crecen como líderes en su hogar y en la iglesia.",
     "Men who support each other, pray together, and grow as leaders at home and in the church.", None),
    ("x.jpg", "center", "Damas", "Women&#39;s Ministry", "Hermandad", "Sisterhood",
     "Mujeres que se animan en la fe, oran unas por otras y sirven con amor.",
     "Women who encourage each other in faith, pray for one another, and serve with love.", None),
    ("x.jpg", "center", "Jóvenes y Jóvenes Adultos", "Youth &amp; Young Adults", "CPG Youth &amp; YA", "CPG Youth &amp; YA",
     "Estudio bíblico los miércoles, noches de adoración Glory Night, deportes y mucha comunión.",
     "Wednesday Bible study, Glory Night worship nights, sports, and plenty of fellowship.",
     ("https://cpgyouth.vercel.app", "Visitar CPG Youth →", "Visit CPG Youth →")),
    ("x.jpg", "center", "Niños", "Kids Ministry", "Para los más pequeños", "For the little ones",
     "Un lugar seguro y alegre donde los niños aprenden la Palabra de Dios y crecen en su fe.",
     "A safe, joyful place where kids learn God's Word and grow in their faith.", None),
    ("x.jpg", "center", "Ministerio de Alabanza", "Worship Team", "Música, producción y medios", "Music, production &amp; media",
     "Músicos, cantantes y el equipo de producción y medios que guían a la iglesia a adorar y llevan cada servicio en vivo.",
     "Musicians, singers, and the production and media team who lead the church in worship and bring every service live.", None),
    ("x.jpg", "center", "Ujieres", "Ushers", "Servir con una sonrisa", "Serving with a smile",
     "Los primeros en recibirte: dan la bienvenida, ayudan a cada familia a encontrar su lugar y cuidan el orden del servicio.",
     "The first faces you meet: they welcome you, help every family find a seat, and keep each service running smoothly.", None),
    ("x.jpg", "center", "Misiones", "Missions", "Más allá de nuestras paredes", "Beyond our walls",
     "Llevamos el evangelio y el amor de Cristo a nuestra comunidad y a las naciones.",
     "We carry the gospel and the love of Christ to our community and to the nations.", None),
    ("x.jpg", "center", "Años Dorados", "Golden Years", "Sabiduría y experiencia", "Wisdom and experience",
     "Hombres y mujeres de fe probada que bendicen a la iglesia con su sabiduría, oración y ejemplo.",
     "Men and women of proven faith who bless the church with their wisdom, prayer, and example.", None),
]


def min_rows():
    out = ""
    for img, pos, nes, nen, wes, wen, des, den, link in MINS:
        more = (f'<a class="more" href="{link[0]}" target="_blank" rel="noopener">{t(link[1], link[2])}</a>' if link
                else f'<a class="more" href="membresia.html">{t("Quiero servir →", "I want to serve →")}</a>')
        out += f"""
      <article class="min-tile" tabindex="0">
        <img src="images/{img}" alt="" loading="lazy" style="object-position: {pos}">
        <div class="body">
          <span class="who">{t(wes, wen)}</span>
          <h3>{t(nes, nen)}</h3>
          <div class="reveal"><p>{t(des, den)}</p>{more}</div>
        </div>
      </article>"""
    return f'<div class="min-bento">{out}\n    </div>'


page("ministerios.html", "Ministerios · CPG", f"""
{banner("ninos.jpg", t("Reuniones", "Gatherings"), t("Ministerios", "Ministries"), t("Nuestros ministerios para servir. Hay un lugar para ti.", "Our ministries to serve. There's a place for you."), pos="40% 30%")}
<section>
  <div class="wrap">
    {min_rows()}
    <div class="serve-note">
      <div class="stack" style="gap:8px">
        <p class="eyebrow">{t("Para servir", "To serve")}</p>
        <p class="serve-title">{t("Servir comienza con ser parte de la familia", "Serving starts with belonging")}</p>
        <p>{t("Para formar parte de cualquier ministerio es necesario ser miembro de la iglesia. Esto protege tanto a la iglesia como a cada persona que sirve.",
              "To be part of any ministry, you need to be a member of the church. This protects both the church and every person who serves.")}</p>
      </div>
      <a class="btn btn-primary" href="membresia.html">{t("Hazte miembro", "Become a member")} <span class="arr">→</span></a>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 7. Giving
page("ofrendar.html", "Ofrendar · CPG", f"""
{banner("adoracion.jpg", t("Conéctate", "Connect"), t("Diezmos y ofrendas", "Tithes and offerings"), t("Tu generosidad sostiene la obra de Dios en esta casa, en nuestra ciudad y a lo largo de la nación.", "Your generosity supports God's work in this house, in our city, and across the nation."), pos="center 35%")}
<section>
  <div class="wrap give-grid">
    <div class="stack">
      <blockquote class="verse" style="margin:0">
        {t("“Traed todos los diezmos al alfolí…”", "“Bring the whole tithe into the storehouse…”")}
        <cite>{t("Malaquías 3:10", "Malachi 3:10")}</cite>
      </blockquote>
      <p class="lead">{t("Diezmar es un acto de adoración y confianza en Dios. Gracias por sembrar en esta casa.", "Tithing is an act of worship and trust in God. Thank you for sowing into this house.")}</p>
    </div>
    <div class="ways">
      <div class="way way-online">
        <span class="soon">{t("Rápido y seguro", "Quick and secure")}</span>
        <h3>{t("En línea", "Online")}</h3>
        <p>{t("Diezma y ofrenda desde tu teléfono o computadora a través de Tithe.ly, nuestra plataforma de ofrendas.",
              "Tithe and give from your phone or computer through Tithe.ly, our giving platform.")}</p>
        <a class="btn btn-primary" href="{GIVE_URL}" target="_blank" rel="noopener">{t("Ofrendar en línea", "Give online")} <span class="arr">→</span></a>
      </div>
      <div class="way">
        <h3>{t("En persona", "In person")}</h3>
        <p>{t("Durante cualquiera de nuestros servicios.", "During any of our services.")}</p>
      </div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head(t("Tu ofrenda en acción", "Your giving at work"), t("Más allá de <em>estas paredes</em>", "Beyond <em>these walls</em>"),
          t("Cada diezmo y ofrenda sostiene la obra que Dios nos ha confiado, aquí y más allá.", "Every tithe and offering supports the work God has entrusted to us, here and beyond."))}
    <div class="expect">
      {exp_box("house", t("Esta casa", "This house"), t("Los servicios, los ministerios y el cuidado de nuestra familia de fe.", "Our services, ministries, and care for our church family."))}
      {exp_box("city", t("Nuestra ciudad", "Our city"), t("Alcanzar y servir a nuestra comunidad en Orlando.", "Reaching and serving our community in Orlando."))}
      {exp_box("nation", t("La nación", "The nation"), t("Esfuerzos a lo largo de la nación a los que CPG contribuye.", "Efforts across the nation that CPG contributes to."))}
    </div>
    <div class="cta-row" style="margin-top:28px">
      <a class="btn btn-primary" href="{GIVE_URL}" target="_blank" rel="noopener">{t("Ofrendar en línea", "Give online")} <span class="arr">→</span></a>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 8. Highlights
HLS = [
    ("noche-internacional.jpg", "center", "Servicio de Misiones", "Missions Service",
     "Celebramos y apoyamos la obra de Dios más allá de nuestras paredes.", "We celebrate and support God's work beyond our walls."),
    ("bautismos.jpg", "center", "Bautismos", "Baptisms",
     "Celebramos juntos cada paso público de fe.", "We celebrate every public step of faith together."),
    ("conferencia-mujeres.jpg", "center", "Conferencia de Mujeres", "Women&#39;s Conference",
     "Mujeres de todas las edades unidas en adoración, Palabra y comunión.", "Women of every age united in worship, the Word, and fellowship."),
    ("reconocimiento.jpg", "center 40%", "Celebraciones", "Celebrations",
     "Momentos para honrar y celebrar a nuestra familia de fe.", "Moments to honor and celebrate our church family."),
    ("oracion.jpg", "center", "Noches de Oración", "Prayer Nights",
     "La iglesia unida buscando a Dios.", "The church united in seeking God."),
    ("joven-cantando.jpg", "center 35%", "Glory Night", "Glory Night",
     "Nuestras noches especiales de adoración y Palabra, un miércoles en la noche.", "Our special nights of worship and the Word, on a Wednesday evening."),
]


def hl_cards():
    out = ""
    for img, pos, nes, nen, des, den in HLS:
        media = (f'<img src="images/{img}" alt="" loading="lazy" style="object-position: {pos}">' if img
                 else f'<div class="ph">{t("Fotos próximamente", "Photos coming soon")}</div>')
        out += f'<article class="hl">{media}<div class="body"><h3>{t(nes, nen)}</h3><p>{t(des, den)}</p></div></article>'
    return f'<div class="hl-grid">{out}</div>'


page("destacados.html", "Momentos Destacados · CPG", f"""
{banner("reconocimiento.jpg", t("Reuniones", "Gatherings"), t("Momentos destacados", "Highlights"), t("Lo que Dios está haciendo en nuestra casa.", "What God is doing in our house."), pos="center 35%")}
<section>
  <div class="wrap">
    {hl_cards()}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head(t("Galería", "Gallery"), t("La vida en CPG", "Life at CPG"))}
    <div class="gallery" id="gallery" data-count="11">
      <img src="images/domingo.jpg" alt="Equipo de alabanza" loading="lazy">
      <img src="images/abrazo.jpg" alt="Un abrazo de bienvenida" loading="lazy" style="object-position: 65% 30%">
      <img src="images/risas.jpg" alt="Hermanos riendo juntos" loading="lazy" style="object-position: 65% center">
      <img src="images/adoracion-pareja.jpg" alt="Hermanos adorando" loading="lazy" style="object-position: 70% center">
      <img src="images/bateria.jpg" alt="Baterista adorando" loading="lazy" style="object-position: center 40%">
      <img src="images/biblia-familia.jpg" alt="Leyendo la Biblia juntos en el servicio" loading="lazy" style="object-position: center 60%">
      <img src="images/comunion.jpg" alt="Dos hermanos riendo" loading="lazy" style="object-position: 55% center">
      <img src="images/cantante-morado.jpg" alt="Adoración en el servicio" loading="lazy" style="object-position: center 25%">
      <img src="images/guitarra.jpg" alt="Líder de alabanza con su guitarra" loading="lazy" style="object-position: center 40%">
      <img src="images/mujeres-risas.jpg" alt="Hermanas riendo en el convivio de la conferencia de mujeres" loading="lazy">
      <img src="images/mujeres-convivio.jpg" alt="Convivio de la conferencia de mujeres en el pasillo de la iglesia" loading="lazy">
    </div>
    <p class="swipe-hint" aria-hidden="true"><b id="gal-pos">1</b> / <span id="gal-total">9</span> · {t("Desliza para ver más →", "Swipe for more →")}</p>
    <div class="gallery-actions">
      <button type="button" class="btn btn-outline" id="gallery-toggle" aria-expanded="false" aria-controls="gallery">
        <span class="open-label">{t("Ver galería completa", "View full gallery")} (11)</span><span class="close-label" hidden>{t("Ver menos", "Show less")}</span>
      </button>
    </div>
  </div>
</section>
""")


# ---------------------------------------------------------------- Statement of faith (from the church's document)
import html as _html
SUBHEADS = {"Dios y la revelación", "Revelación escrita – Las Sagradas Escrituras.", "(La Biblia)", "La naturaleza de Dios",
            "a) El Dios trino", "b) La Santa Trinidad", "c) Los dones del Espíritu", "Sobre la salvación del hombre", "La iglesia local"}
SECTION_ES = {"I": "Las Escrituras", "II": "Sobre Dios", "III": "Sobre el hombre", "IV": "La iglesia de Cristo",
              "V": "Sobre las ordenanzas", "VI": "El propósito y la misión de la iglesia", "VII": "Sobre los últimos tiempos", "VIII": "La familia"}
SECTION_EN = {"I": "Scripture", "II": "About God", "III": "About Humanity", "IV": "The Church of Christ",
              "V": "The Ordinances", "VI": "The Purpose and Mission of the Church", "VII": "The Last Times", "VIII": "The Family"}


def _clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    return t.replace("Hch..", "Hch.").replace("Cor..", "Cor.").replace("  ", " ")


def parse_faith():
    lines = (ROOT / "src/declaracion-de-fe.txt").read_text().splitlines()
    sections, cur, buf = [], None, []

    def flush():
        if cur is not None and buf:
            cur["blocks"].append(("p", _clean(" ".join(buf))))
        buf.clear()

    for raw in lines:
        line = raw.strip()
        m = re.match(r"^([IVX]+)\.\s+(.*)$", line)
        if m and m.group(1) in SECTION_EN:
            flush(); cur = {"num": m.group(1), "title": m.group(2).strip().capitalize(), "blocks": []}; sections.append(cur); continue
        if line.startswith("IX.") or line == "QUE CREEMOS":
            flush()
            if line.startswith("IX."): cur = None
            continue
        if cur is None:
            continue
        if not line:
            # page breaks split sentences: only end the paragraph after terminal punctuation
            if buf and re.search(r"[.:)”\"]$", buf[-1]): flush()
            continue
        if line in SUBHEADS:
            flush(); cur["blocks"].append(("h", line.rstrip("."))); continue
        if line.startswith("– ") or re.match(r"^o [A-ZÁÉÍÓÚ]", line):
            flush(); buf.append(line[2:]); cur["blocks"].append(("li-start", "")); continue
        buf.append(line)
    flush()
    return sections


def faith_html():
    import json
    en = json.loads((ROOT / "src/statement-of-faith-en.json").read_text())

    def bi(key, es_txt):
        e = _html.escape(es_txt)
        tr = en.get(key)
        if tr is None:
            raise SystemExit(f"Missing English translation for statement-of-faith block {key}")
        return t(e, _html.escape(tr))

    out = []
    for i, sec in enumerate(parse_faith()):
        body, in_list = [], False
        blocks = sec["blocks"]
        k = 0
        while k < len(blocks):
            kind, txt = blocks[k]
            if kind == "li-start":
                k += 1
                item = blocks[k][1] if k < len(blocks) else ""
                if not in_list: body.append("<ul>"); in_list = True
                li_key = f"{sec['num']}.{k}"
                body.append(f"<li>{bi(li_key, item)}</li>")
            else:
                if in_list: body.append("</ul>"); in_list = False
                key = f"{sec['num']}.{k}"
                if kind == "h": body.append(f"<h4>{bi(key, txt.rstrip('.'))}</h4>")
                else: body.append(f"<p>{bi(key, txt)}</p>")
            k += 1
        if in_list: body.append("</ul>")
        title = SECTION_ES[sec["num"]]
        out.append(f"""
      <details class="faith"{" open" if i == 0 else ""}>
        <summary><span class="num">{sec["num"]}</span><span class="ttl">{t(_html.escape(title), SECTION_EN[sec["num"]])}</span><span class="chev" aria-hidden="true">+</span></summary>
        <div class="faith-body">{"".join(body)}</div>
      </details>""")
    return "".join(out)

# ---------------------------------------------------------------- 9. Beliefs
VALUES = [
    ("Salvación en Cristo", "Salvation in Christ",
     "Solamente en Cristo hay salvación.",
     "Salvation is found in Christ alone.",
     ["Hechos 4:11-12"], ["Acts 4:11-12"]),
    ("Cada persona importa", "Every person matters",
     "En CPG cada persona es importante para Dios y, por consiguiente, para la familia de Cristo que es la iglesia.",
     "At CPG every person is important to God, and therefore to the family of Christ, which is the church.",
     ["1 Corintios 3:16", "Romanos 12:4-5", "Hebreos 10:24-25"], ["1 Corinthians 3:16", "Romans 12:4-5", "Hebrews 10:24-25"]),
    ("Un solo cuerpo", "One body",
     "Somos un equipo, un cuerpo trabajando unidos bajo una misma visión y propósito.",
     "We are a team, one body working together under one vision and purpose.",
     ["Salmo 133:1", "Eclesiastés 4:9-12"], ["Psalm 133:1", "Ecclesiastes 4:9-12"]),
    ("Creatividad con propósito", "Creativity with purpose",
     "Sin alterar el fundamento de nuestra fe, creemos en presentar a Cristo de diferentes maneras, usando las artes creativas para impactar y transformar vidas.",
     "Without changing the foundation of our faith, we believe in presenting Christ in different ways, using the creative arts to impact and transform lives.",
     ["Hechos 17:22-24"], ["Acts 17:22-24"]),
    ("Cada miembro es ministro", "Every member is a minister",
     "En esta casa cada miembro es un ministro que tiene dones y talentos para ser desarrollados para el beneficio de la obra de Dios en la iglesia.",
     "In this house every member is a minister, with gifts and talents to be developed for the benefit of God's work in the church.",
     ["Efesios 2:10"], ["Ephesians 2:10"]),
    ("Crecer y rendir cuentas", "Growth and accountability",
     "Cada miembro debe comprometerse a su crecimiento espiritual y rendir cuentas honestamente.",
     "Every member should commit to their spiritual growth and be honestly accountable.",
     ["Hechos 2:44-47"], ["Acts 2:44-47"]),
    ("Un estilo de vida", "A way of life",
     "Estamos persuadidos de que la vida cristiana es un estilo de vida y, como tal, debe reflejarse en todo lo que hacemos y decimos.",
     "We are convinced that the Christian life is a way of life, and as such it should be reflected in everything we do and say.",
     ["Colosenses 3:17", "Efesios 4:29"], ["Colossians 3:17", "Ephesians 4:29"]),
]


def value_cards():
    out = ""
    for tes, ten, des, den, res, ren in VALUES:
        refs = "".join(f'<span class="ref">{t(a, b)}</span>' for a, b in zip(res, ren))
        out += f"""
      <article class="value">
        <h3>{t(tes, ten)}</h3>
        <p>{t(des, den)}</p>
        <div class="refs">{refs}</div>
      </article>"""
    return f'<div class="values">{out}\n    </div>'


page("creencias.html", "Lo Que Creemos · CPG", f"""
{banner("cruz.jpg", t("Nosotros", "About"), t("Lo que creemos", "What we believe"), t("Los valores que guían nuestra casa.", "The values that guide our house."), pos="center 20%")}
<section>
  <div class="wrap">
    {head(t("Nuestros valores", "Our values"), t("Sobre este fundamento edificamos", "The foundation we build on"))}
    {value_cards()}
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="purpose">
      <p class="eyebrow">{t("Nuestro propósito", "Our purpose")}</p>
      <p class="purpose-text">{t("Alcanzar la mayor cantidad de hombres, mujeres, jóvenes y niños para el Reino de Cristo. Equiparlos para que puedan ser <em>portadores de la gloria de Dios</em> y de esa manera ser una iglesia en continuo crecimiento, tanto física como espiritualmente, haciendo la diferencia en el lugar donde Dios nos ha puesto.",
                                 "To reach as many men, women, youth, and children as possible for the Kingdom of Christ. To equip them to be <em>bearers of God&#39;s glory</em>, and so be a church that keeps growing, both in number and in spirit, making a difference wherever God has placed us.")}</p>
    </div>
  </div>
</section>
<section id="declaracion">
  <div class="wrap faith-wrap">
    {head(t("Declaración de fe", "Statement of faith"), t("Lo que creemos", "What we believe"), t("Toca cada sección para leerla completa.", "Tap each section to read it in full."))}
    <div class="faith-list">{faith_html()}
    </div>
    <div class="affiliation">
      <p class="eyebrow">{t("Afiliación denominacional", "Denominational affiliation")}</p>
      <p>{t("Casa Portadores de Gloria de Orlando, Florida es un organismo autónomo de creyentes. La iglesia coopera y tiene compañerismo con la Asociación Bautista de Orlando (GOBA), la Convención Bautista de Florida y la Convención Bautista del Sur.",
            "Casa Portadores de Gloria in Orlando, Florida is an autonomous body of believers. The church cooperates and has fellowship with the Greater Orlando Baptist Association (GOBA), the Florida Baptist Convention, and the Southern Baptist Convention.")}</p>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="soon-block" style="background:var(--surface)">
      <h2 style="font-size:clamp(1.8rem,4vw,2.6rem)">{t("¿Tienes preguntas sobre la fe?", "Questions about faith?")}</h2>
      <p class="lead">{t("Nos encantaría conversar contigo. Visítanos un domingo o escríbenos.", "We'd love to talk with you. Visit us on a Sunday or reach out.")}</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="visitanos.html">{t("Planea tu visita", "Plan a visit")} <span class="arr">→</span></a>
        <a class="btn btn-outline" href="membresia.html">{t("Hazte miembro", "Become a member")}</a>
      </div>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 10. Prayer
page("oracion.html", "Peticiones de Oración · CPG", f"""
{banner("oracion-manos.jpg", t("Conéctate", "Connect"), t("Peticiones de oración", "Prayer requests"), t("No tienes que cargarlo solo. Nuestro equipo de oración estará orando por ti.", "You don't have to carry it alone. Our prayer team will be praying for you."), pos="40% center")}
<section>
  <div class="wrap split" style="align-items:start">
    <div class="stack">
      {head(t("Oramos contigo", "We pray with you"), t("¿Cómo podemos orar por ti?", "How can we pray for you?"))}
      <p class="lead">{t("Comparte tu petición. Puedes dejarla anónima si lo prefieres. También puedes acompañarnos cada viernes a las 7:00 PM en nuestro Servicio de Oración.",
                        "Share your request. You can leave it anonymous if you prefer. You're also welcome to join us every Friday at 7:00 PM for our Prayer Service.")}</p>
    </div>
    <form class="form" data-preview>
      <div class="row">
        <div class="field"><label for="pr-name">{t("Nombre (opcional)", "Name (optional)")}</label><input id="pr-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="pr-contact">{t("Teléfono o correo (opcional)", "Phone or email (optional)")}</label><input id="pr-contact" name="contact"></div>
      </div>
      <div class="field"><label for="pr-request">{t("Tu petición", "Your request")}</label><textarea id="pr-request" name="request" required></textarea></div>
      <label class="check"><input type="checkbox" id="pr-private" name="private"> {t("Mantener esta petición privada (solo los pastores)", "Keep this request private (pastors only)")}</label>
      <button type="submit">{t("Enviar petición", "Send request")}</button>
      {form_note()}
    </form>
  </div>
</section>
""")

# ---------------------------------------------------------------- 11. Visit
page("visitanos.html", "Planea Tu Visita · CPG", f"""
{banner("abrazo.jpg", t("Conéctate", "Connect"), t("Planea tu visita", "Plan your visit"), t("Queremos conocerte. Así es un domingo en Casa Portadores de Gloria.", "We'd love to meet you. Here's what a Sunday at Casa Portadores de Gloria looks like."), pos="65% 30%")}
<section>
  <div class="wrap">
    {head(t("Tu primera visita", "Your first visit"), t("Qué esperar", "What to expect"))}
    <div class="expect">
      {exp_box("clock", t("Cuándo", "When"), t("Domingos a las 11:00 AM. Llega unos minutos antes.", "Sundays at 11:00 AM. Come a few minutes early."))}
      {exp_box("pin", t("Dónde", "Where"), '5200 Old Cheney Highway, Orlando, FL 32807')}
      {exp_box("bilingual", t("Idioma", "Language"), t("Mensaje en español, con traducción al inglés.", "Message in Spanish, with English translation."))}
      {exp_box("kids", t("Niños", "Kids"), t("Hay un lugar para los niños.", "There's a place for the kids."))}
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap split" style="align-items:start">
    <div class="stack">
      {head(t("Avísanos", "Let us know"), t("¿Vienes pronto?", "Coming soon?"), t("Déjanos tus datos y alguien de nuestro equipo te recibirá.", "Leave your info and someone from our team will welcome you."))}
      <a class="btn btn-ink" style="justify-self:start" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")}</a>
    </div>
    <form class="form" data-preview>
      <div class="row">
        <div class="field"><label for="v-name">{t("Nombre", "Name")}</label><input id="v-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="v-contact">{t("Teléfono o correo", "Phone or email")}</label><input id="v-contact" name="contact" required></div>
      </div>
      <div class="row">
        <div class="field"><label for="v-when">{t("¿Qué servicio?", "Which service?")}</label>
          <select id="v-when" name="service">
            <option>{t("Domingo 11:00 AM", "Sunday 11:00 AM")}</option>
            <option>{t("Miércoles 7:00 PM", "Wednesday 7:00 PM")}</option>
            <option>{t("Viernes 7:00 PM", "Friday 7:00 PM")}</option>
          </select></div>
        <div class="field"><label for="v-people">{t("¿Cuántas personas?", "How many people?")}</label><input id="v-people" name="people" type="number" min="1" value="1"></div>
      </div>
      <div class="field"><label for="v-notes">{t("¿Algo que debamos saber?", "Anything we should know?")}</label><textarea id="v-notes" name="notes" style="min-height:90px"></textarea></div>
      <button type="submit">{t("Enviar", "Send")}</button>
      {form_note()}
    </form>
  </div>
</section>
""")

# ---------------------------------------------------------------- 12. Membership
page("membresia.html", "Hazte Miembro · CPG", f"""
{banner("familia-abrazo.jpg", t("Conéctate", "Connect"), t("Hazte miembro", "Become a member"), t("Ser miembro es decir: esta es mi casa y esta es mi familia.", "Membership means saying: this is my house, and this is my family."), pos="center 36%")}
<section>
  <div class="wrap split" style="align-items:start">
    <div class="stack">
      {head(t("Membresía", "Membership"), t("Echa raíces en esta casa", "Put down roots in this house"))}
      <p class="lead">{t("Si Casa Portadores de Gloria se ha vuelto tu hogar, nos encantaría caminar contigo en el siguiente paso. Déjanos tus datos y los pastores te contactarán con los detalles.",
                        "If Casa Portadores de Gloria has become your home, we'd love to walk with you in the next step. Leave your info and the pastors will contact you with the details.")}</p>
      <p class="lead">{t("La membresía también es el primer paso para servir en cualquiera de nuestros ministerios.",
                        "Membership is also the first step to serving in any of our ministries.")}</p>
      <div class="soon-block" style="padding:20px 22px">
        <span class="soon">{t("Próximamente", "Coming soon")}</span>
        <p style="color:var(--muted)">{t("Los pasos y las fechas de la clase de membresía.", "Membership steps and class dates.")}</p>
      </div>
    </div>
    <form class="form" data-preview>
      <div class="row">
        <div class="field"><label for="m-name">{t("Nombre completo", "Full name")}</label><input id="m-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="m-phone">{t("Teléfono", "Phone")}</label><input id="m-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <div class="field"><label for="m-email">{t("Correo electrónico", "Email")}</label><input id="m-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="m-time">{t("¿Cuánto tiempo llevas asistiendo?", "How long have you been attending?")}</label>
        <select id="m-time" name="attending">
          <option>{t("Menos de 3 meses", "Less than 3 months")}</option>
          <option>{t("3 a 12 meses", "3 to 12 months")}</option>
          <option>{t("Más de un año", "More than a year")}</option>
        </select></div>
      <button type="submit">{t("Quiero ser miembro", "I want to become a member")}</button>
      {form_note()}
    </form>
  </div>
</section>
""")

print("built", SLOTS)
