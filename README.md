# Audio Effects 

Tento projekt je aplikace pro úpravu audio souborů pomocí grafického uživatelského rozhraní (GUI) vytvořeného pomocí knihovny Kivy. Aplikace umožňuje načítat, upravovat a ukládat audio soubory pomocí efektů z knihovny Pedalboard.

## Požadavky

- Python 3.6 nebo novější
- Knihovny uvedené v `requirements.txt`

## Instalace

1. Klonujte repozitář:
    ```sh
    git clone https://github.com/uzivatel/audio-effects-editor.git
    cd audio-effects-editor
    ```

2. Nainstalujte požadované knihovny:
    ```sh
    pip install -r requirements.txt
    ```

## Spuštění aplikace

1. Spusťte hlavní soubor:
    ```sh
    python main.py
    ```

## Použití

### Načítání audio souboru

1. Klikněte na tlačítko "Načíst soubor" a vyberte WAV soubor, který chcete upravit.

### Nastavení efektů

1. Upravte hodnoty jednotlivých efektů pomocí posuvníků:
    - **Distortion**: Nastavení úrovně zkreslení.
    - **Gain**: Nastavení úrovně zesílení.
    - **Reverb**: Nastavení velikosti místnosti pro reverb.
    - **Chorus**: Nastavení frekvence chorus efektu.

### Přehrání upraveného audia

1. Klikněte na tlačítko "Play" pro přehrání upraveného audio souboru.

### Uložení upraveného audia

1. Klikněte na tlačítko "Uložit" a zadejte název souboru pro uložení upraveného audia.

## Použité knihovny

- `kivy`: Pro tvorbu GUI.
- `pedalboard`: Pro aplikování audio efektů.
- `numpy`: Pro zpracování audio dat.



