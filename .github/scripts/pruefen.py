"""Prüft das Resourcepack im Ordner pack/: JSON gültig, Texturen und Modelle vorhanden, Bildgrößen sinnvoll."""
import json
import struct
import sys
from pathlib import Path

PACK = Path(sys.argv[1] if len(sys.argv) > 1 else "pack")
fehler = []
hinweise = []


def ref_to_path(ref, art):
    """'cozychaos:item/filter' -> pack/assets/cozychaos/<art>/item/filter.<endung>"""
    ns, _, pfad = ref.partition(":") if ":" in ref else ("minecraft", "", ref)
    endung = ".png" if art == "textures" else ".json"
    return ns, PACK / "assets" / ns / art / (pfad + endung)


def png_size(datei):
    with open(datei, "rb") as f:
        kopf = f.read(24)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", kopf[16:24])


if not (PACK / "pack.mcmeta").is_file():
    fehler.append("pack/pack.mcmeta fehlt")

daten = {}
for datei in sorted(PACK.rglob("*")):
    if datei.suffix in (".json", ".mcmeta"):
        try:
            daten[datei] = json.loads(datei.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa: BLE001
            fehler.append(f"{datei}: kein gültiges JSON ({ex})")


def sammle(obj, schluessel, ergebnis):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == schluessel and isinstance(v, str):
                ergebnis.append(v)
            sammle(v, schluessel, ergebnis)
    elif isinstance(obj, list):
        for v in obj:
            sammle(v, schluessel, ergebnis)


for datei, inhalt in daten.items():
    teile = datei.relative_to(PACK).parts
    # Item-Definitionen (assets/<ns>/items/*.json): verwiesene Modelle prüfen
    if len(teile) > 2 and teile[2] == "items":
        refs = []
        sammle(inhalt, "model", refs)
        for ref in refs:
            ns, ziel = ref_to_path(ref, "models")
            if ns != "minecraft" and not ziel.is_file():
                fehler.append(f"{datei}: Modell {ref} fehlt ({ziel})")
    # Modelle: verwiesene Texturen und Eltern prüfen
    if len(teile) > 2 and teile[2] == "models":
        for name, ref in (inhalt.get("textures") or {}).items():
            if ref.startswith("#"):
                continue
            ns, ziel = ref_to_path(ref, "textures")
            if ns != "minecraft" and not ziel.is_file():
                fehler.append(f"{datei}: Textur {ref} ({name}) fehlt ({ziel})")
        parent = inhalt.get("parent")
        if parent:
            ns, ziel = ref_to_path(parent, "models")
            if ns != "minecraft" and not ziel.is_file():
                fehler.append(f"{datei}: Eltern-Modell {parent} fehlt")

for bild in sorted(PACK.rglob("*.png")):
    groesse = png_size(bild)
    if groesse is None:
        fehler.append(f"{bild}: keine echte PNG-Datei")
        continue
    breite, hoehe = groesse
    animiert = Path(str(bild) + ".mcmeta").is_file()
    if bild.name == "pack.png":
        if breite != hoehe:
            hinweise.append(f"{bild}: Pack-Symbol sollte quadratisch sein ({breite}x{hoehe})")
        continue
    if animiert:
        if hoehe % breite != 0:
            fehler.append(f"{bild}: animierte Textur, Höhe muss ein Vielfaches der Breite sein ({breite}x{hoehe})")
    elif breite != hoehe:
        hinweise.append(f"{bild}: nicht quadratisch ({breite}x{hoehe}) – gewollt?")
    if breite & (breite - 1):
        hinweise.append(f"{bild}: Breite {breite} ist keine Zweierpotenz (16, 32, 64 ...)")

for h in hinweise:
    print("Hinweis:", h)
for f in fehler:
    print("FEHLER:", f)
print(f"{len(daten)} JSON-Dateien, {len(list(PACK.rglob('*.png')))} Bilder geprüft, {len(fehler)} Fehler.")
sys.exit(1 if fehler else 0)
