from PIL import Image, ImageDraw, ImageFont
import re
import datetime

now = datetime.datetime.now()

background_image_path = "Planning animations\semaine_vide.png"
output_image_path = f"Planning animations\planning_semaine_{now.strftime('%Y-%m-%d_%H-%M-%S')}.png"

font_path = "Planning animations\JosefinSans-SemiBoldItalic.ttf"
font_size = 30
font = ImageFont.truetype(font_path, font_size)
image = Image.open(background_image_path)
draw = ImageDraw.Draw(image)

jours_positions = {
    "Lundi": (50, 480, 340, 730),
    "Mardi": (370, 480, 650, 730),
    "Mercredi": (680, 480, 965, 730),
    "Jeudi": (50, 835, 340, 1085),
    "Vendredi": (370, 835, 650, 1085),
    "Samedi": (680, 835, 965, 1085),
    "Dimanche": (275, 1195, 775, 1440)
}

def demander_informations(font, draw):
    animations = {}
    for jour in jours_positions.keys():
        case_x, case_y, case_x_max, case_y_max = jours_positions[jour]
        case_width = case_x_max - case_x
        case_height = case_y_max - case_y
        hauteur_nom = case_height +1
        print(f"\n--- {jour} ---")

        nom, hauteur_nom = couper_texte_en_lignes(input("Nom de l'animation (laisser vide si aucune) : "), font, case_width, draw)
        while hauteur_nom > case_height / 2:
            print("Nom trop long, veuillez entrer un texte plus court.")
            nom, hauteur_nom = couper_texte_en_lignes(input("Nom de l'animation : "), font, case_width, draw)
        while hauteur_nom == -1:
            print(f"Vous avez donné un mot trop long, veuillez raccourcir ce mot : {nom}")
            nom, hauteur_nom = couper_texte_en_lignes(input("Nom de l'animation : "), font, case_width, draw)
        if len(nom) == 0:
            nom = "Pas d'animation !"
            animations[jour] = {"nom": nom, "heure": None}
            continue

        while True:
            heure = input("Jour et heure (exemple : 01/09 - 14h00) : ")
            
            pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2]) - ([01][0-9]|2[0-3])h[0-5][0-9]$"
            
            if re.match(pattern, heure):
                break
            else:
                print("❌ Format incorrect. Veuillez respecter le format JJ/MM - HHhMM (ex: 01/09 - 14h00).")

        animations[jour] = {"nom": nom, "heure": heure}

    return animations

def get_text_size(draw, texte, font):
    bbox = draw.textbbox((0, 0), texte, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

def couper_texte_en_lignes(texte, font, max_width, draw):
    mots = texte.split()
    lignes = ""
    ligne_courante = ""
    hauteur = None

    for mot in mots:
        largeur_mot, _ = get_text_size(draw, mot, font=font)
        if largeur_mot > max_width:
            return mot, -1
        test_ligne = ligne_courante + (" " if ligne_courante else "") + mot
        largeur, _ = get_text_size(ImageDraw.Draw(Image.open(background_image_path)), test_ligne, font=font)  # ou utiliser draw.textbbox
        if largeur <= max_width:
            ligne_courante = test_ligne
        else:
            if ligne_courante:
                lignes = f"{lignes}\n{ligne_courante}" if lignes != "" else ligne_courante
            ligne_courante = mot

    if ligne_courante:
        lignes = f"{lignes}\n{ligne_courante}" if lignes != "" else ligne_courante

    _, hauteur = get_text_size(ImageDraw.Draw(Image.open(background_image_path)), lignes, font=font)

    if hauteur:
        return lignes, hauteur
    else:
        return lignes, 0

def generer_planning(animations):
    for jour, info in animations.items():
        case_x, case_y, case_x_max, case_y_max = jours_positions[jour]
        case_width = case_x_max - case_x
        case_height = case_y_max - case_y

        if info["heure"] is not None:
            texte_1 = info['nom']
            texte_2 = "-" * int((case_x_max - case_x) / 10)
            texte_3 = info['heure']
            w1, h1 = get_text_size(draw, texte_1, font)
            w2, h2 = get_text_size(draw, texte_2, font)
            w3, h3 = get_text_size(draw, texte_3, font)

            x_1 = case_x + (case_width - w1) / 2
            y_1 = case_y + case_height / 2 - h1
            x_2 = case_x + (case_width - w2) / 2
            y_2 = case_y + (case_height - h2) / 2
            x_3 = case_x + (case_width - w3) / 2
            y_3 = case_y + case_height  / 2 + h3

            draw.text((x_1, y_1), texte_1, fill="black", font=font)
            draw.text((x_2, y_2), texte_2, fill="black", font=font)
            draw.text((x_3, y_3), texte_3, fill="black", font=font)
        else:
            texte_1 = info['nom']
            w1, h1 = get_text_size(draw, texte_1, font)
            x_1 = case_x + (case_width - w1) / 2
            y_1 = case_y + case_height / 2 - h1
            draw.text((x_1, y_1), texte_1, fill="black", font=font)


    image.save(output_image_path)
    print(f"\n✅ Planning généré !")


if __name__ == "__main__":
    print("Bienvenue dans le générateur de planning des animations 🐢\n")
    animations = demander_informations(font, draw)
    if animations:
        generer_planning(animations)
    else:
        image.save(output_image_path)
        print(f"\n✅ Planning rénitialisé !")
