# CozyChaos-Resourcepack

Freiwilliges Server-Resourcepack für die **CozyChaosCommunity** (Minecraft 26.3, Pack-Format 97.1).
Es enthält nur eigene Texturen – alles andere bleibt Vanilla.

Das Plugin **CozyChaosCustoms** (Modul `pack`) holt sich automatisch das neueste Release aus diesem Repo
und bietet das Pack den Spielern beim Beitreten an. In der `server.properties` wird **nichts** eingetragen.

## Was ist drin?
| Was | Wie bekommt man es? |
|---|---|
| Drachenei | automatisch, jedes Drachenei (Block und Item) |
| Filter (Trichter) | Eisennugget am Amboss in **Filter** umbenennen (großes F) |
| Eiswaffel | Goldene Karotte am Amboss in **Eiswaffel** umbenennen |
| Spaghettieis | Rote-Bete-Suppe am Amboss in **Spaghettieis** umbenennen |
| Downfall | Streitkolben (Mace) am Amboss in **Downfall** umbenennen |
| Breakthrough | Streitkolben (Mace) am Amboss in **Breakthrough** umbenennen |
| Cola | Wasserflasche am Amboss in **Cola** umbenennen |
| Pommes | Ofenkartoffel am Amboss in **Pommes** umbenennen |
| Milchshake | Honigflasche am Amboss in **Milchshake** umbenennen |
| Verzierte Tierrüstung | Pferde-, Wolfs- oder Nautilusrüstung am **Schmiedetisch** mit Vorlage + Material verzieren (braucht das Datapack auf dem Server) |

## Ordner
```
pack/                 <- das eigentliche Resourcepack (nur dieser Ordner landet in der Zip)
  pack.mcmeta
  pack.png
  assets/
    minecraft/        <- Vanilla-Dateien, die wir ersetzen (z. B. items/iron_nugget.json)
    cozychaos/        <- unsere eigenen Modelle und Texturen
datapack/             <- Datapack für den Server (world/datapacks/): macht Tierrüstung verzierbar
.github/workflows/    <- die zwei Automatiken (Pack prüfen, Pack veröffentlichen)
CHANGELOG.md          <- was sich in welcher Version geändert hat
```

## Neue Texturen für umbenannte Items
Beispiel „Filter“ (Eisennugget):
1. Textur nach `pack/assets/cozychaos/textures/item/<name>.png` (16x16 oder 32x32).
2. Modell nach `pack/assets/cozychaos/models/item/<name>.json`.
3. In `pack/assets/minecraft/items/<vanilla-item>.json` unter `cases` einen Eintrag mit `"when": "<Name am Amboss>"` ergänzen.
   Gibt es die Datei für das Item noch nicht, `iron_nugget.json` als Vorlage kopieren und den Fallback anpassen
   (z. B. `minecraft:item/netherite_sword`).
4. Lokal testen: den Inhalt von `pack/` zippen und in `.minecraft/resourcepacks` legen.

## Neue Version veröffentlichen
1. Änderungen per GitHub Desktop hochladen („Commit to main“, dann „Push origin“).
2. Oben im `CHANGELOG.md` die neue Version eintragen.
3. Auf GitHub: **Actions** → **Pack veröffentlichen** → **Run workflow** → Version eintragen (z. B. `1.0.1`) → starten.
4. Die Automatik baut die Zip, rechnet die SHA-1-Prüfsumme aus und legt ein Release mit beiden Dateien an
   (`CozyChaos-Resourcepack-<Version>.zip` und `.sha1`).
5. Im Spiel: `/ccc pack update` – das Plugin holt die neue Version und bietet sie allen an, die online sind.

Bei jedem Hochladen läuft außerdem **Pack prüfen**: Es meldet kaputte JSON-Dateien, fehlende Texturen und
falsche Bildgrößen, bevor etwas veröffentlicht wird.

## Verzierte Tierrüstung (ab 1.6.0)
- Texturen: `pack/assets/minecraft/textures/trims/entity/<horse_body|wolf_body|nautilus_body>/<muster>.png`,
  Graustufen mit den 8 Grauwerten der Vanilla-Palette `trim_base`, dazu je eine `.png.mcmeta` mit
  `{"palette": {"base_palette": "trim_base"}}`. Die Materialfarbe setzt das Spiel selbst ein.
- Datapack `datapack/cozychaos-tiertrims.zip` erweitert den Item-Tag `minecraft:trimmable_armor` um alle Tierrüstungen.

## Regeln
- Einzigartige Items dürfen eigene Texturen bekommen (derzeit: Drachenei).
- Jedes Mitglied darf sich anfangs bis zu 3 eigene Texturen für umbenannte Items/Blöcke wünschen.
- Keine Nachbauten geschützter Designs aus anderen Spielen oder Filmen.
