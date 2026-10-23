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
YOUTUBE = "#"
FACEBOOK = "#"

ICON_YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-3.2.5-4.8s-.1-3.2-.5-4.8ZM9.7 15.1V8.9l5.8 3.1-5.8 3.1Z"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7.1V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12Z"/></svg>'
ICON_PLAY = '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path fill="#e62117" d="M8 5v14l11-7z"/></svg>'


def social_btns():
    return (f'<div class="social-btns"><a class="sbtn yt" href="{YOUTUBE}" target="_blank" rel="noopener">{ICON_YT}YouTube</a>'
            f'<a class="sbtn fb" href="{FACEBOOK}" target="_blank" rel="noopener">{ICON_FB}Facebook</a></div>')


def social_icons():
    return (f'<div class="social-icons"><a href="{YOUTUBE}" target="_blank" rel="noopener" aria-label="YouTube">{ICON_YT}</a>'
            f'<a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{ICON_FB}</a></div>')


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
    <a class="give-pill" href="ofrendar.html">{t("Ofrendar", "Give")}</a>
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
  var targets = document.querySelectorAll('main section .wrap > *:not(.hero-frame), .quick > a, .services > div, .events > div, .min-list > article, .hl-grid > article, .gallery > img, .expect > div');
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
PHOTOS["pastores.html"][2] = ("pastores-pareja.jpg", "center 30%")
PHOTOS["pastores.html"][3] = ("familia-toirac.jpg", "center")
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Instrument+Sans:wght@400..700&display=swap">
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
     "Una noche para profundizar juntos en las Escrituras.", "A night to dig deeper into Scripture together."),
    ("oracion.jpg", "center", "Viernes", "Friday", "7:00", "PM", "Servicio de Oración", "Prayer Service",
     "Nos reunimos para buscar a Dios en oración unida.", "We gather to seek God together in prayer."),
]


def service_cards():
    out = ""
    for img, pos, des, den, time, ap, nes, nen, des2, den2 in SERVICES:
        out += f"""
      <div class="service">
        <img class="service-img" src="images/{img}" alt="" loading="lazy" style="object-position: {pos}">
        <p class="eyebrow">{t(des, den)}</p>
        <div class="when">{time}<span>{ap}</span></div>
        <h3>{t(nes, nen)}</h3>
        <p>{t(des2, den2)}</p>
      </div>"""
    return f'<div class="services">{out}\n    </div>'


EVENTS = [
    ("Oct", "28", "CPG Youth", "CPG Youth", "Glory Night",
     "Miércoles, 7:00 PM. Una noche de adoración y Palabra para jóvenes y jóvenes adultos.",
     "Wednesday, 7:00 PM. A night of worship and the Word for youth and young adults."),
    ("Oct", "29", "Para todos", "Everyone", "CPG Sports Day",
     "Jueves, 6:30 PM en Brush Arbor Christian School. Baloncesto, voleibol y comunión. ¡Todos son bienvenidos!",
     "Thursday, 6:30 PM at Brush Arbor Christian School. Basketball, volleyball, and fellowship. Everyone is welcome!"),
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
      <img src="images/oracion-grupo.jpg" alt="Hermanos abrazados orando juntos en Casa Portadores de Gloria" fetchpriority="high" style="object-position: 50% 45%">
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
          <a class="btn btn-primary" href="visitanos.html">{t("Te esperamos", "Save my seat")} <span class="arr">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    {"".join(f'<span>{w}</span>' for w in ["Adoración", "Palabra", "Familia", "Oración", "Gloria", "Comunidad"] * 4)}
  </div>
</div>

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
      <a href="ministerios.html"><img src="images/q2.jpg" alt=""><b>{t("Ministerios", "Ministries")}</b><span class="d">{t("Niños, jóvenes, hombres, mujeres y ancianos.", "Kids, youth, men, women, and elders.")}</span><span class="go">→</span></a>
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
    </div>
    <img class="photo" src="images/bienvenida.jpg" alt="Saludos al final del servicio" loading="lazy" style="object-position: 60% center">
  </div>
</section>
<section class="band" id="ubicacion">
  <div class="wrap split">
    <img class="photo" src="images/edificio.jpg" alt="Pasillo exterior de la iglesia" loading="lazy">
    <div class="stack">
      {head(t("Ubicación", "Location"), t("Dónde estamos", "Where we are"))}
      <address class="lead" style="font-style:normal"><strong style="color:var(--ink)">5200 Old Cheney Highway</strong><br>Orlando, FL 32807</address>
      <p class="lead">{t("Hay estacionamiento disponible en el lugar.", "Parking is available on site.")}</p>
      <div class="cta-row">
        <a class="btn btn-ink" href="{MAPS}" target="_blank" rel="noopener">{t("Abrir en Google Maps", "Open in Google Maps")}</a>
        <a class="btn btn-outline" href="visitanos.html">{t("Planea tu visita", "Plan a visit")}</a>
      </div>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 3. Pastors
page("pastores.html", "Nuestros Pastores · CPG", f"""
{banner("predicacion.jpg", t("Nosotros", "About"), t("Nuestros pastores", "Our pastors"), pos="center 40%")}
<section>
  <div class="wrap pastor-card">
    <img src="images/pastor-pulpito.jpg" alt="Pastor Esdras Toirac predicando" loading="lazy">
    <div class="stack">
      <p class="eyebrow">{t("Pastores principales", "Senior Pastors")}</p>
      <h2>Esdras &amp; Magnolia Toirac</h2>
      <p class="lead">{t("Los pastores Esdras y Magnolia Toirac guían a la familia de Casa Portadores de Gloria con amor por Dios, por su Palabra y por la gente de Orlando.",
                        "Pastors Esdras and Magnolia Toirac lead the Casa Portadores de Gloria family with a love for God, His Word, and the people of Orlando.")}</p>
      <div class="soon-block" style="padding:20px 22px">
        <span class="soon">{t("Próximamente", "Coming soon")}</span>
        <p style="color:var(--muted)">{t("Su historia y su llamado.", "Their story and their calling.")}</p>
      </div>
    </div>
  </div>
</section>
<section class="band" style="padding-top:0">
  <div class="wrap">
    {head(t("Su familia", "Their family"), t("La familia <em>Toirac</em>", "The <em>Toirac</em> family"))}
    <figure class="family">
      <img src="images/familia-toirac.jpg" alt="Los pastores Esdras y Magnolia Toirac con sus hijos" loading="lazy">
    </figure>
  </div>
</section>
""")

# ---------------------------------------------------------------- 4. Services
page("servicios.html", "Servicios · CPG", f"""
{banner("mano-alzada.jpg", t("Reuniones", "Gatherings"), t("Servicios semanales", "Weekly services"), t("Tres noches, una familia. Te esperamos.", "Three gatherings, one family. We'll save you a seat."))}
<section>
  <div class="wrap">
    {service_cards()}
    <div class="visit">
      <address>5200 Old Cheney Highway<span>Orlando, FL 32807</span></address>
      <a class="btn btn-ink" href="{MAPS}" target="_blank" rel="noopener">{t("Cómo llegar", "Get directions")}</a>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head(t("Tu primera vez", "Your first time"), t("Qué esperar", "What to expect"))}
    <div class="expect">
      <div><h3>{t("Adoración", "Worship")}</h3><p>{t("Música en vivo con nuestro equipo de alabanza.", "Live music with our worship team.")}</p></div>
      <div><h3>{t("La Palabra", "The Word")}</h3><p>{t("Una enseñanza bíblica clara y práctica.", "Clear, practical Bible teaching.")}</p></div>
      <div><h3>{t("Bilingüe", "Bilingual")}</h3><p>{t("Mensaje en español, con traducción al inglés.", "Message in Spanish, with English translation.")}</p></div>
      <div><h3>{t("Para la familia", "For families")}</h3><p>{t("Hay un lugar para los niños.", "There's a place for the kids.")}</p></div>
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
      <a class="btn btn-ink" href="https://instagram.com/cpgyouth" target="_blank" rel="noopener">@cpgyouth</a>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 6. Ministries
MINS = [
    ("ninos-oracion.jpg", "center 45%", "Niños", "Kids", "Para los más pequeños", "For the little ones",
     "Un lugar seguro y alegre donde los niños aprenden la Palabra de Dios y crecen en su fe.",
     "A safe, joyful place where kids learn God's Word and grow in their faith.", None),
    ("estudio.jpg", "center 60%", "Jóvenes y Jóvenes Adultos", "Youth &amp; Young Adults", "CPG Youth", "CPG Youth",
     "Estudio bíblico los miércoles, Glory Night el último miércoles de cada mes, deportes y mucha comunión.",
     "Wednesday Bible study, Glory Night on the last Wednesday of every month, sports, and plenty of fellowship.",
     ("https://cpgyouth.vercel.app", "Visitar CPG Youth →", "Visit CPG Youth →")),
    ("edificio.jpg", "center", "Hombres", "Men", "Hermandad", "Brotherhood",
     "Hombres que se apoyan, oran juntos y crecen como líderes en su hogar y en la iglesia.",
     "Men who support each other, pray together, and grow as leaders at home and in the church.", None),
    ("oracion.jpg", "center", "Mujeres", "Women", "Hermandad", "Sisterhood",
     "Mujeres que se animan en la fe, oran unas por otras y sirven con amor.",
     "Women who encourage each other in faith, pray for one another, and serve with love.", None),
    ("comunion.jpg", "55% center", "Ancianos", "Elders", "Sabiduría y experiencia", "Wisdom and experience",
     "Hombres y mujeres de fe probada que bendicen a la iglesia con su sabiduría, oración y ejemplo.",
     "Men and women of proven faith who bless the church with their wisdom, prayer, and example.", None),
]


def min_rows():
    out = ""
    for img, pos, nes, nen, wes, wen, des, den, link in MINS:
        more = (f'<a class="more" href="{link[0]}" target="_blank" rel="noopener">{t(link[1], link[2])}</a>' if link
                else f'<a class="more" href="visitanos.html">{t("Quiero participar →", "I want to join →")}</a>')
        out += f"""
      <article class="min-row">
        <img src="images/{img}" alt="" loading="lazy" style="object-position: {pos}">
        <div class="body">
          <span class="who">{t(wes, wen)}</span>
          <h3>{t(nes, nen)}</h3>
          <p>{t(des, den)}</p>
          {more}
        </div>
      </article>"""
    return f'<div class="min-list">{out}\n    </div>'


page("ministerios.html", "Ministerios · CPG", f"""
{banner("ninos.jpg", t("Reuniones", "Gatherings"), t("Ministerios", "Ministries"), t("Hay un lugar para cada etapa de la vida.", "There's a place for every season of life."), pos="40% 30%")}
<section>
  <div class="wrap">
    {min_rows()}
  </div>
</section>
""")

# ---------------------------------------------------------------- 7. Giving
page("ofrendar.html", "Ofrendar · CPG", f"""
{banner("adoracion.jpg", t("Conéctate", "Connect"), t("Diezmos y ofrendas", "Tithes and offerings"), t("Tu generosidad sostiene la obra de Dios en esta casa y en nuestra ciudad.", "Your generosity supports God's work in this house and in our city."), pos="center 35%")}
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
      <div class="way">
        <h3>{t("En persona", "In person")}</h3>
        <p>{t("Durante cualquiera de nuestros servicios.", "During any of our services.")}</p>
      </div>
      <div class="way">
        <span class="soon">{t("Próximamente", "Coming soon")}</span>
        <h3>{t("En línea", "Online")}</h3>
        <p>{t("Pronto podrás diezmar y ofrendar de forma segura desde aquí.", "Soon you'll be able to tithe and give securely right here.")}</p>
      </div>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 8. Highlights
HLS = [
    ("cantante-azul.jpg", "center 25%", "Noches de Adoración", "Worship Nights",
     "Noches dedicadas a la presencia de Dios a través de la alabanza.", "Nights devoted to God's presence through worship."),
    (None, None, "Servicio de Misiones", "Missions Service",
     "Celebramos y apoyamos la obra de Dios más allá de nuestras paredes.", "We celebrate and support God's work beyond our walls."),
    (None, None, "Bautismos", "Baptisms",
     "Celebramos juntos cada paso público de fe.", "We celebrate every public step of faith together."),
    ("reconocimiento.jpg", "center 40%", "Celebraciones", "Celebrations",
     "Momentos para honrar y celebrar a nuestra familia de fe.", "Moments to honor and celebrate our church family."),
    ("oracion.jpg", "center", "Noches de Oración", "Prayer Nights",
     "La iglesia unida buscando a Dios.", "The church united in seeking God."),
    ("joven-cantando.jpg", "center 35%", "Glory Night", "Glory Night",
     "Una noche mensual de CPG Youth para adorar y escuchar la Palabra.", "A monthly CPG Youth night of worship and the Word."),
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
    <div class="gallery">
      <img class="g1" src="images/domingo.jpg" alt="Equipo de alabanza" loading="lazy">
      <img src="images/abrazo.jpg" alt="Un abrazo de bienvenida" loading="lazy" style="object-position: 65% 30%">
      <img src="images/risas.jpg" alt="Hermanos riendo juntos" loading="lazy" style="object-position: 65% center">
      <img src="images/adoracion-pareja.jpg" alt="Hermanos adorando" loading="lazy" style="object-position: 70% center">
      <img src="images/bateria.jpg" alt="Baterista adorando" loading="lazy" style="object-position: center 40%">
      <img src="images/biblia-familia.jpg" alt="Leyendo la Biblia juntos en el servicio" loading="lazy" style="object-position: center 60%">
      <img src="images/comunion.jpg" alt="Dos hermanos riendo" loading="lazy" style="object-position: 55% center">
      <img src="images/cantante-morado.jpg" alt="Adoración en el servicio" loading="lazy" style="object-position: center 25%">
      <img src="images/guitarra.jpg" alt="Líder de alabanza con su guitarra" loading="lazy" style="object-position: center 40%">
    </div>
  </div>
</section>
""")

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
      <div><h3>{t("Cuándo", "When")}</h3><p>{t("Domingos a las 11:00 AM. Llega unos minutos antes.", "Sundays at 11:00 AM. Come a few minutes early.")}</p></div>
      <div><h3>{t("Dónde", "Where")}</h3><p>5200 Old Cheney Highway, Orlando, FL 32807</p></div>
      <div><h3>{t("Idioma", "Language")}</h3><p>{t("Mensaje en español, con traducción al inglés.", "Message in Spanish, with English translation.")}</p></div>
      <div><h3>{t("Niños", "Kids")}</h3><p>{t("Hay un lugar para los niños.", "There's a place for the kids.")}</p></div>
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
