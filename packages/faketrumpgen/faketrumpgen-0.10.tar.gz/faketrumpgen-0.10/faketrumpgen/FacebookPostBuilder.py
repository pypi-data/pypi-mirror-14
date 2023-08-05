from PIL import Image, ImageDraw, ImageFont
from faketrumpgen import FacebookAccountTools
import os.path
import urllib.request, io
import base64
import time

__author__ = 'Max'


class CreateTrumpPost:
    def __init__(self, msg, temps, save_path, prenom="Donald", nom="Trump",
                 facebook_profile_url="https://www.facebook.com/DonaldTrump/", debug=False):
        self.save_path = save_path
        self.msg = msg
        self.temps = temps
        self.post_number = "0"
        self.prenom = prenom
        self.nom = nom
        self.debug = debug

        self.profileTools = FacebookAccountTools.FacebookAccountTools(facebook_profile_url)
        self.pictureBytes = io.BytesIO(urllib.request.urlopen(self.profileTools.get_picture_url()).read())

        self.path_dir = os.path.dirname(os.path.abspath(__file__))
        self.profilePicture = Image.open(self.pictureBytes)
        self.lowBarPicture = Image.open(self.path_dir + "/pictures/lowBar.png")
        self.arrowPicture = Image.open(self.path_dir + "/pictures/arrow.png")

        self.post_image = None

    def create_phrases(self):
        phrases = []
        phrase = ""

        # Seperate phrases and put them in phrases array
        for lettre in range(0, len(self.msg)):
            phrase += self.msg[lettre]
            if len(phrase) == 70:
                phrases.append(phrase)
                phrase = ""
            elif lettre == len(self.msg) - 1:
                phrases.append(phrase)

        # Create white image with size == (493, 19 * numberOfLines)
        self.post_image = Image.new('RGBA', (493, (len(phrases) * 19) + 115), color="white")

        # Add lowbar under text
        self.post_image.paste(self.lowBarPicture, (5, 19 * len(phrases) + 75))

        # Add profile picture
        self.post_image.paste(self.profilePicture, (14, 14))

        # Add arrow
        self.post_image.paste(self.arrowPicture, (470, 14))

        # Add drawing panel
        drawing = ImageDraw.Draw(self.post_image)

        # Add date
        fnt = ImageFont.truetype(self.path_dir + "/fonts/facebookFont.ttf", 11)
        drawing.text((71, 46), self.temps, font=fnt, fill=(130, 130, 130))

        # Loop number of lines add lines to drawing
        fnt = ImageFont.truetype(self.path_dir + "/fonts/facebookFont.ttf", 13)
        for ligne in range(0, len(phrases)):
            drawing.text((15, 19 * ligne + 77), phrases[ligne], font=fnt, fill=(0, 0, 0, 0))

        # Add firstname lastname
        fnt = ImageFont.truetype(self.path_dir + "/fonts/tahomabd.ttf", 15)
        drawing.text((72, 19), self.prenom + " " + self.nom, font=fnt, fill=(59, 89, 152))

        # Gives name to picture.
        if len(os.listdir(self.save_path)) == 0:
            self.post_number = "0"
        else:
            post_number = 0
            for fn in os.listdir(self.save_path):
                post_number += 1
                if int(fn.rstrip(".jpeg")) != post_number - 1:
                    post_number -= 1
                    break
            self.post_number = str(post_number)

        self.post_image.save(self.save_path + "/" + self.post_number + ".jpeg", "JPEG")

        if self.debug is True:
            self.post_image.show()

    def get_image_base64(self):
        if self.post_image is not None:
            return base64.b64encode(self.post_image.tobytes())

    def delete_pic(self):
        while not os.path.exists(self.save_path + "/" + self.post_number + ".jpeg"):
            time.sleep(1)
        os.remove(self.save_path + "/" + self.post_number + ".jpeg")


if __name__ == "__main__":
    post = CreateTrumpPost("You look so bloated from eating all that cake. Yuk!", "December 16 at 6:23pm", os.path.dirname(os.path.abspath(__file__)) + "/posts", debug=True)
    post.create_phrases()
    post.delete_pic()
