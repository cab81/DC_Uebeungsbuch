#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Übungs-Generator — Dog College Franken Übungsbuch
Führt durch den Erstellungsprozess einer Übung und erzeugt
fertigen LaTeX-Code der direkt in die Kapitel-Datei eingefügt werden kann.
"""

import sys
import os

# ── Farben ────────────────────────────────────────────────────────────────────
class F:
    GRUEN  = "\033[32m"
    DGRUEN = "\033[32;1m"
    GELB   = "\033[33m"
    CYAN   = "\033[36m"
    FETT   = "\033[1m"
    RESET  = "\033[0m"
    GRAU   = "\033[90m"
    WEISS  = "\033[97m"
    ROT    = "\033[31m"

def linie(z="─", b=78): print(F.GRUEN + z * b + F.RESET)
def dlinie(b=78):        print(F.DGRUEN + "═" * b + F.RESET)

def header(titel):
    dlinie()
    print(F.DGRUEN + F.FETT + f"  {titel}".center(78) + F.RESET)
    print(F.GRUEN + "  Dog College Franken — Übungsbuch".center(78) + F.RESET)
    dlinie()

def frage(bezeichnung, beispiele=None, pflicht=True, optionen=None):
    print()
    print(F.FETT + F.CYAN + f"  {bezeichnung}" + F.RESET)
    if optionen:
        for key, val in optionen.items():
            print(F.GRAU + f"    {key} = {val}" + F.RESET)
    if beispiele:
        for bsp in beispiele:
            print(F.GRAU + f"    z.B. {bsp}" + F.RESET)
    print()
    while True:
        antwort = input(F.GELB + "  → " + F.RESET).strip()
        if antwort:
            if optionen and antwort not in optionen:
                print(F.ROT + f"  Bitte eine der Optionen eingeben: {', '.join(optionen.keys())}" + F.RESET)
                continue
            return antwort
        if not pflicht:
            return ""
        print(F.GELB + "  Bitte einen Wert eingeben." + F.RESET)

def mehrere_eintraege(bezeichnung, hinweis, min_anzahl=1):
    """Fragt mehrere Einträge ab (für Schritte, Variationen, Hinweise)."""
    print()
    linie()
    print(F.FETT + F.CYAN + f"  {bezeichnung}" + F.RESET)
    print(F.GRAU + f"  {hinweis}" + F.RESET)
    print(F.GRAU + "  Leere Eingabe = fertig" + F.RESET)
    eintraege = []
    i = 1
    while True:
        print()
        eintrag = input(F.GELB + f"  {i}. → " + F.RESET).strip()
        if not eintrag:
            if len(eintraege) < min_anzahl:
                print(F.ROT + f"  Mindestens {min_anzahl} Eintrag erforderlich." + F.RESET)
                continue
            break
        eintraege.append(eintrag)
        i += 1
    return eintraege

# ── LaTeX-Ausgabe ─────────────────────────────────────────────────────────────

def escape_latex(text):
    """Escaped Sonderzeichen für LaTeX."""
    ersetzungen = [
        ("&", "\\&"), ("%", "\\%"), ("$", "\\$"),
        ("#", "\\#"), ("^", "\\^{}"), ("_", "\\_"),
        ("~", "\\~{}"),
    ]
    for alt, neu in ersetzungen:
        text = text.replace(alt, neu)
    return text

def baue_schritte(schritte):
    zeilen = ["    \\begin{enumerate}[leftmargin=*, itemsep=2pt]"]
    for s in schritte:
        zeilen.append(f"      \\item {escape_latex(s)}")
    zeilen.append("    \\end{enumerate}")
    return "\n".join(zeilen)

def baue_aufzaehlung(eintraege, fett_titel=True):
    zeilen = ["    \\begin{itemize}[leftmargin=*, itemsep=4pt]"]
    for e in eintraege:
        if fett_titel and ":" in e:
            titel, rest = e.split(":", 1)
            zeilen.append(f"      \\item \\textbf{{{escape_latex(titel.strip())}:}} {escape_latex(rest.strip())}")
        else:
            zeilen.append(f"      \\item {escape_latex(e)}")
    zeilen.append("    \\end{itemize}")
    return "\n".join(zeilen)

def ziel_datei(typ, altersgruppe):
    basis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if typ == "einzeln":
        return os.path.join(basis, "chapters", "heimuebungen", f"{altersgruppe}.tex")
    else:
        return os.path.join(basis, "chapters", "gruppenuebungen", f"{altersgruppe}.tex")

def bild_pfad(typ, altersgruppe, dateiname):
    if not dateiname:
        return None
    ordner = "heimuebungen" if typ == "einzeln" else "gruppenuebungen"
    return f"images/{ordner}/{altersgruppe}/{dateiname}"

# ── Übungs-Erstellung ─────────────────────────────────────────────────────────

def erstelle_uebung(typ):
    typname = "Einzelübung (Heimübung)" if typ == "einzeln" else "Gruppenübung"
    header(f"NEUE {typname.upper()} ERSTELLEN")

    print(F.GRUEN + "\n  Beantworte die Fragen. Alle Felder außer Bild sind Pflichtfelder.\n" + F.RESET)

    # ── Metadaten ─────────────────────────────────────────────────────────────
    linie()
    print(F.FETT + F.WEISS + "  SCHRITT 1 — Metadaten" + F.RESET)

    titel = frage("Titel der Übung",
                  ["Sitz", "Abruf im Freien", "Geduld an der Tür", "Hundebegegnung"])

    altersgruppe = frage("Altersgruppe",
                         optionen={
                             "welpen":    "Welpen & Junghunde",
                             "pubertaet": "Pubertät",
                             "erwachsen": "Erwachsene Hunde"
                         })

    kategorie = frage("Kategorie",
                      ["Grundkommando", "Abruf", "Geduld", "Begrüßung",
                       "Leinenführigkeit", "Impulskontrolle", "Sozialisation"])

    schwierigkeit = frage("Schwierigkeit (1–5)",
                          optionen={
                              "1": "sehr leicht",
                              "2": "leicht",
                              "3": "mittel",
                              "4": "schwer",
                              "5": "sehr schwer"
                          })

    # ── Bild ──────────────────────────────────────────────────────────────────
    linie()
    print(F.FETT + F.WEISS + "  SCHRITT 2 — Bild (optional)" + F.RESET)
    ordner = "heimuebungen" if typ == "einzeln" else "gruppenuebungen"
    print(F.GRAU + f"\n  Bilddatei liegt in: images/{ordner}/{altersgruppe}/" + F.RESET)
    print(F.GRAU + "  Nur Dateinamen eingeben (z.B. sitz.png) oder ENTER überspringen." + F.RESET)
    bild = frage("Dateiname des Bildes", pflicht=False)
    if typ == "gruppe":
        print(F.GRAU + "  Zweites Bild (Draufsicht, optional):" + F.RESET)
        bild2 = frage("Dateiname Draufsicht-Bild", pflicht=False)
    else:
        bild2 = ""

    # ── Beschreibung ──────────────────────────────────────────────────────────
    linie()
    print(F.FETT + F.WEISS + "  SCHRITT 3 — Beschreibung" + F.RESET)

    einleitung = frage("Einleitungssatz (was lernt der Hund?)",
                       ["Der Hund lernt, auf das Kommando 'Sitz' zuverlässig zu reagieren.",
                        "Zwei Hunde werden kontrolliert aneinander herangeführt."])

    if typ == "gruppe":
        print()
        print(F.GRAU + "  Gruppenaufbau:" + F.RESET)
        teilnehmer = frage("Anzahl Personen & Hunde", ["2 Personen, 2 Hunde", "alle Teilnehmer"])
        aufstellung = frage("Startaufstellung", ["Kreis", "Reihe", "gegenüber in 5 m Abstand"])
        material = frage("Material", ["Leine, Clicker, Leckerlis", "nur Leckerlis"])

    schritte = mehrere_eintraege(
        "Schritte",
        "Beschreibe den Ablauf Schritt für Schritt.",
        min_anzahl=2
    )

    # ── Variationen ───────────────────────────────────────────────────────────
    linie()
    print(F.FETT + F.WEISS + "  SCHRITT 4 — Variationen" + F.RESET)
    print(F.GRAU + "  Format: 'Titel: Beschreibung' (der Teil vor dem : wird fett)" + F.RESET)
    variationen = mehrere_eintraege(
        "Variationen",
        "Wie kann die Übung abgewandelt werden?",
        min_anzahl=1
    )

    # ── Trainer-Hinweise ──────────────────────────────────────────────────────
    linie()
    print(F.FETT + F.WEISS + "  SCHRITT 5 — Trainer-Hinweise" + F.RESET)
    hinweise = mehrere_eintraege(
        "Trainer-Hinweise",
        "Worauf sollen Trainer besonders achten?",
        min_anzahl=1
    )

    # ── LaTeX generieren ──────────────────────────────────────────────────────
    bild_zeile = ""
    if bild:
        pfad = bild_pfad(typ, altersgruppe, bild)
        bild_zeile = f"\n  \\uebungsbild{{{pfad}}}\n"

    bild2_zeile = ""
    if bild2:
        pfad2 = bild_pfad(typ, altersgruppe, bild2)
        bild2_zeile = f"  % Draufsicht-Bild\n  \\uebungsbild{{{pfad2}}}\n"

    if typ == "gruppe":
        aufbau_block = (
            f"    \\textbf{{Aufbau:}}\n"
            f"    \\begin{{itemize}}[leftmargin=*, itemsep=2pt]\n"
            f"      \\item Teilnehmer: {escape_latex(teilnehmer)}\n"
            f"      \\item Aufstellung: {escape_latex(aufstellung)}\n"
            f"      \\item Material: {escape_latex(material)}\n"
            f"    \\end{{itemize}}\n\n    \\vspace{{6pt}}\n"
        )
    else:
        aufbau_block = ""

    latex = f"""
% ── Übung: {titel} {'─' * max(1, 60 - len(titel))}
\\begin{{uebung}}{{{escape_latex(titel)}}}{{{altersgruppe}}}{{{escape_latex(kategorie)}}}{{{schwierigkeit}}}{bild_zeile}{bild2_zeile}
  \\uebungsbeschreibung{{%
    {escape_latex(einleitung)}\\\\[6pt]
    {aufbau_block}\\textbf{{Schritte:}}
{baue_schritte(schritte)}
  }}

  \\uebungsvariationen{{%
{baue_aufzaehlung(variationen)}
  }}

  \\uebungstrainer{{%
{baue_aufzaehlung(hinweise, fett_titel=False)}
  }}

\\end{{uebung}}
"""

    # ── Ausgabe ───────────────────────────────────────────────────────────────
    print()
    dlinie()
    print(F.DGRUEN + F.FETT + "  FERTIGER LATEX-CODE" + F.RESET)
    dlinie()
    print(F.WEISS + latex + F.RESET)
    dlinie()

    # ── In Datei speichern ────────────────────────────────────────────────────
    print()
    ziel = ziel_datei(typ, altersgruppe)
    print(F.GRUEN + f"  Zieldatei: {ziel}" + F.RESET)
    print()
    speichern = input(F.GELB + "  In Kapitel-Datei einfügen? (j/n): " + F.RESET).strip().lower()

    if speichern == "j":
        try:
            with open(ziel, "a", encoding="utf-8") as f:
                f.write(latex)
            print()
            print(F.DGRUEN + F.FETT + f"  ✓ Erfolgreich eingefügt in: {ziel}" + F.RESET)
        except Exception as e:
            print(F.ROT + f"  Fehler beim Speichern: {e}" + F.RESET)
            print(F.GELB + "  Bitte den LaTeX-Code manuell kopieren." + F.RESET)
    else:
        print(F.GRAU + "  Nicht gespeichert. LaTeX-Code oben manuell kopieren." + F.RESET)

# ── HAUPTMENÜ ─────────────────────────────────────────────────────────────────
def hauptmenue():
    while True:
        header("ÜBUNGS-GENERATOR")
        print(F.WEISS + """
  Was möchtest du erstellen?

    1  →  Einzelübung   (Heimübung, eine Person + ein Hund)
    2  →  Gruppenübung  (mehrere Personen / Hunde erforderlich)
    q  →  Beenden
""" + F.RESET)

        auswahl = input(F.GELB + "  Auswahl: " + F.RESET).strip().lower()

        if auswahl == "1":
            erstelle_uebung("einzeln")
        elif auswahl == "2":
            erstelle_uebung("gruppe")
        elif auswahl in ("q", "quit", "exit"):
            print(F.GRUEN + "\n  Tschüss! Viel Spaß beim Trainieren. 🐾\n" + F.RESET)
            sys.exit(0)
        else:
            print(F.GELB + "\n  Bitte 1, 2 oder q eingeben.\n" + F.RESET)
            continue

        print()
        input(F.GRAU + "  [ ENTER ] für das Hauptmenü..." + F.RESET)

if __name__ == "__main__":
    try:
        hauptmenue()
    except KeyboardInterrupt:
        print(F.GRUEN + "\n\n  Abgebrochen. Tschüss! 🐾\n" + F.RESET)
        sys.exit(0)
