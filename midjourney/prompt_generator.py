#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midjourney Prompt Generator — Dog College Franken Übungsbuch
Fragt die Platzhalter ab und gibt den fertigen Prompt als Kopiervorlage aus.
"""

import sys

# ── Farben für Terminal-Ausgabe ───────────────────────────────────────────────
class Farbe:
    GRUEN       = "\033[32m"
    DUNKELGRUEN = "\033[32;1m"
    GELB        = "\033[33m"
    CYAN        = "\033[36m"
    FETT        = "\033[1m"
    RESET       = "\033[0m"
    GRAU        = "\033[90m"
    WEISS       = "\033[97m"
    BG_GRUEN    = "\033[42m"

def trennlinie(zeichen="─", breite=78):
    print(Farbe.GRUEN + zeichen * breite + Farbe.RESET)

def doppellinie(breite=78):
    print(Farbe.DUNKELGRUEN + "═" * breite + Farbe.RESET)

def header(titel):
    doppellinie()
    print(Farbe.DUNKELGRUEN + Farbe.FETT +
          f"  {titel}".center(78) + Farbe.RESET)
    print(Farbe.GRUEN + "  Dog College Franken — Übungsbuch".center(78) + Farbe.RESET)
    doppellinie()

def frage(bezeichnung, beispiele, pflicht=True):
    """Fragt einen Platzhalter ab und zeigt Beispiele an."""
    print()
    print(Farbe.FETT + Farbe.CYAN + f"  [{bezeichnung}]" + Farbe.RESET)
    for bsp in beispiele:
        print(Farbe.GRAU + f"    z.B. {bsp}" + Farbe.RESET)
    print()
    while True:
        antwort = input(Farbe.GELB + "  → " + Farbe.RESET).strip()
        if antwort:
            return antwort
        if not pflicht:
            return ""
        print(Farbe.GELB + "  Bitte einen Wert eingeben." + Farbe.RESET)

def frage_stilreferenz():
    """Fragt optional nach einer Style Reference URL und Style Weight."""
    print()
    trennlinie()
    print(Farbe.FETT + Farbe.CYAN + "  [STYLE REFERENCE — optional]" + Farbe.RESET)
    print(Farbe.GRAU + "    Möchtest du ein Referenzbild verwenden um den Stil zu übernehmen?" + Farbe.RESET)
    print(Farbe.GRAU + "    Bild-URL aus Discord/Imgur einfügen, oder ENTER zum Überspringen." + Farbe.RESET)
    print()

    url = input(Farbe.GELB + "  URL (oder ENTER überspringen): " + Farbe.RESET).strip()

    if not url:
        return ""

    print()
    print(Farbe.FETT + Farbe.CYAN + "  [STYLE WEIGHT --sw]" + Farbe.RESET)
    print(Farbe.GRAU + "    Wie stark soll das Referenzbild den Stil beeinflussen?" + Farbe.RESET)
    print(Farbe.GRAU + "     50  = leichte Anlehnung" + Farbe.RESET)
    print(Farbe.GRAU + "    100  = Standard" + Farbe.RESET)
    print(Farbe.GRAU + "    300  = empfohlen für einheitliche Bildserie  ←" + Farbe.RESET)
    print(Farbe.GRAU + "    500  = Stil dominiert stark" + Farbe.RESET)
    print(Farbe.GRAU + "   1000  = Maximum" + Farbe.RESET)
    print()

    while True:
        sw = input(Farbe.GELB + "  Style Weight (Standard: 300): " + Farbe.RESET).strip()
        if sw == "":
            sw = "300"
        if sw.isdigit() and 1 <= int(sw) <= 1000:
            break
        print(Farbe.GELB + "  Bitte eine Zahl zwischen 1 und 1000 eingeben." + Farbe.RESET)

    return f" --sref {url} --sw {sw}"

def ausgabe(prompt):
    """Gibt den fertigen Prompt als Kopiervorlage aus."""
    print()
    doppellinie()
    print(Farbe.DUNKELGRUEN + Farbe.FETT +
          "  FERTIGER PROMPT — jetzt kopieren:" + Farbe.RESET)
    doppellinie()
    print()
    print(Farbe.WEISS + prompt + Farbe.RESET)
    print()
    doppellinie()
    print(Farbe.DUNKELGRUEN + Farbe.FETT +
          "  ↑ Diesen Text komplett in Midjourney einfügen ↑" + Farbe.RESET)
    doppellinie()
    print()

# ── FESTER PROMPT-KERN: Seitenansicht ────────────────────────────────────────
KERN_SEITENANSICHT = """\
A female dog trainer standing upright seen from the side,
{handzeichen},
{hundeposition},
{rasse_alter},
side view full body shot, calm and focused atmosphere,
clean simple comic illustration style, bold outlines,
flat colors with minimal shading, no photorealism,
not cartoonish or playful, professional and clean graphic novel aesthetic,
female trainer wearing dark forest green jacket and
beige sand-colored trousers, sturdy outdoor shoes,
woman in her 30s, athletic build, hair tied back in a ponytail,
confident and calm expression,
solid plain off-white background (#F2F7F2) uniformly filled,
thin clean border frame around the entire image,
border color dark forest green (#2E6B2E), border width 8px,
no gradients in background, no vignette, no drop shadow,
color palette restricted to forest green, dark brown, black,
tan, off-white and warm grey,
no speech bubbles, no text, no watermark
--ar 3:2 --style raw --v 6.1 --seed 1182697702"""

# ── FESTER PROMPT-KERN: Draufsicht ───────────────────────────────────────────
KERN_DRAUFSICHT = """\
Top-down training diagram,
{anzahl},
{positionen},
{pfeile},
minimalist flat vector illustration, strict color palette only:
dark forest green (#1E4D1E) for human silhouettes,
medium green (#4A8C3F) for dog shapes,
warm orange-gold (#F5A623) for movement arrows and direction lines,
solid plain off-white background (#F2F7F2) uniformly filled,
thin clean border frame around the entire image,
border color dark forest green (#2E6B2E), border width 8px,
no gradients in background, no vignette, no drop shadow,
light warm grey (#C8C4B8) for position zones and ground markings,
simple geometric human figures, tiny stylized dog shapes,
bold clear arrows showing movement flow,
clean infographic style, no gradients, no shadows, flat design,
no text, no photorealism, no clutter
--ar 3:2 --style raw --no gradients --v 6.1 --seed 1182697702"""

# ── KURZREFERENZEN ───────────────────────────────────────────────────────────
HANDZEICHEN_REF = [
    ("Sitz",       "right arm raised, index finger pointing straight up as hand signal"),
    ("Platz",      "right arm extended downward, index finger pointing to the ground"),
    ("Bleib",      "open right hand, palm facing toward the dog as stop signal"),
    ("Hier/Abruf", "both arms open wide, welcoming gesture toward the body"),
    ("Fuß",        "left hand pointing down along the left leg"),
    ("Aus",        "open hand, palm facing down, pushing gesture downward"),
]

UEBUNG_REF = [
    ("Sitz/Platz",    "human stationary, dog moves to position in front, stops"),
    ("Abruf",         "human on one end, dog starts far away, straight arrow toward human"),
    ("Leinenführig",  "human and dog move together, parallel arrow along a path"),
    ("Slalom",        "dog weaves between markers, curved zigzag arrow"),
    ("Bleib+Abstand", "human steps away from sitting dog, dashed arrow showing distance"),
    ("Begegnung",     "two humans with dogs approaching, arrows converging"),
]

def zeige_referenz(eintraege, titel):
    print()
    trennlinie("·")
    print(Farbe.GRAU + f"  {titel}:" + Farbe.RESET)
    for name, text in eintraege:
        print(Farbe.GRAU + f"    {name:<14} → {text}" + Farbe.RESET)
    trennlinie("·")

# ── PROMPT 1: Seitenansicht ───────────────────────────────────────────────────
def prompt_seitenansicht():
    header("SEITENANSICHT — Comic-Stil")

    print(Farbe.GRUEN + """
  Fülle die Platzhalter aus. Die Beispiele helfen dir beim Formulieren.
  Drücke ENTER um deine Eingabe zu bestätigen.
""" + Farbe.RESET)

    zeige_referenz(HANDZEICHEN_REF, "Kurzreferenz Handzeichen")

    handzeichen = frage(
        "HANDZEICHEN",
        ["right arm raised, index finger pointing straight up as hand signal",
         "open right hand, palm facing toward the dog as stop signal"]
    )

    hundeposition = frage(
        "HUNDEPOSITION & VERHALTEN",
        ["dog sitting attentively in front of the trainer looking up at the hand signal",
         "dog lying flat on the ground, head resting on paws, eyes looking up",
         "dog standing still beside the trainer, looking forward"]
    )

    hund = frage(
        "HUND — RASSE, ALTER, FARBE & FELL",
        ["medium to large adult dog, fluffy dense double coat, tiger brindle coat pattern, dark brown and black striped fur with tan markings",
         "small puppy, floppy ears, golden yellow fur, short smooth coat",
         "large senior dog, broad chest, black and white patches, medium length wavy coat"]
    )

    sref = frage_stilreferenz()

    prompt = KERN_SEITENANSICHT.format(
        handzeichen=handzeichen,
        hundeposition=hundeposition,
        rasse_alter=hund,
    ) + sref
    ausgabe(prompt)

# ── PROMPT 2: Draufsicht ──────────────────────────────────────────────────────
def prompt_draufsicht():
    header("DRAUFSICHT — Diagramm-Stil")

    print(Farbe.GRUEN + """
  Fülle die Platzhalter aus. Die Beispiele helfen dir beim Formulieren.
  Drücke ENTER um deine Eingabe zu bestätigen.
""" + Farbe.RESET)

    zeige_referenz(UEBUNG_REF, "Kurzreferenz Übungsszenarien")

    anzahl = frage(
        "ANZAHL PERSONEN & HUNDE",
        ["one human, one dog",
         "two humans standing apart, one dog in the middle",
         "one human, three dogs arranged in a semicircle"]
    )

    positionen = frage(
        "ÜBUNGSABLAUF & POSITIONEN",
        ["human figure standing on the left, dog figure sitting directly in front",
         "human on the right side, dog starting position on the far left, end position sitting in front of human",
         "two humans facing each other 5 meters apart, dog in the center"]
    )

    pfeile = frage(
        "PFEILE & BEWEGUNGSLINIEN",
        ["single straight orange arrow from left to right showing dog moving toward human",
         "curved orange arrow showing dog running in a wide arc around the human",
         "two arrows: one showing dog moving away, one showing dog returning"]
    )

    sref = frage_stilreferenz()

    prompt = KERN_DRAUFSICHT.format(
        anzahl=anzahl,
        positionen=positionen,
        pfeile=pfeile,
    ) + sref
    ausgabe(prompt)

# ── HAUPTMENÜ ─────────────────────────────────────────────────────────────────
def hauptmenue():
    while True:
        header("MIDJOURNEY PROMPT GENERATOR")
        print(Farbe.WEISS + """
  Welchen Prompt möchtest du erstellen?

    1  →  Seitenansicht  (Comic-Stil, Trainerin + Hund)
    2  →  Draufsicht     (Diagramm-Stil, Vogelperspektive)
    q  →  Beenden
""" + Farbe.RESET)

        auswahl = input(Farbe.GELB + "  Auswahl: " + Farbe.RESET).strip().lower()

        if auswahl == "1":
            prompt_seitenansicht()
        elif auswahl == "2":
            prompt_draufsicht()
        elif auswahl in ("q", "quit", "exit"):
            print(Farbe.GRUEN + "\n  Tschüss! Viel Erfolg mit den Bildern. 🐾\n" + Farbe.RESET)
            sys.exit(0)
        else:
            print(Farbe.GELB + "\n  Bitte 1, 2 oder q eingeben.\n" + Farbe.RESET)

        print()
        input(Farbe.GRAU + "  [ ENTER ] für das Hauptmenü..." + Farbe.RESET)

if __name__ == "__main__":
    try:
        hauptmenue()
    except KeyboardInterrupt:
        print(Farbe.GRUEN + "\n\n  Abgebrochen. Tschüss! 🐾\n" + Farbe.RESET)
        sys.exit(0)
