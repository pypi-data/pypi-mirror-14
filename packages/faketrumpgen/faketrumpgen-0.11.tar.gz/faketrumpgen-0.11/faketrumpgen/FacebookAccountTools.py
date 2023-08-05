from urllib import parse


class FacebookAccountTools:
    def __init__(self, url):
        self.url = url

    # Parses url, gets name, adds /picture to end
    def get_picture_url(self):
        parsed_url = parse.urlparse(self.url)
        path = parsed_url.path
        if not str(path).endswith("/"):
            path += "/"
        return "https://graph.facebook.com" + path + "picture"

    # Firstname and Lastname need first letter to be capitalized for this to work
    # Returns tuple (firstname, lastname)
    def get_name(self):
        parsed_url = parse.urlparse(self.url)
        path = parsed_url.path
        nom = str(path).replace("/", "")

        first_name = nom[0]
        last_name = ""
        is_last_name = False

        for lettre in nom[1: len(nom)]:
            if lettre.islower() and is_last_name is False:
                first_name += lettre
            elif lettre.isupper() and is_last_name is False:
                last_name += lettre
                is_last_name = True
            else:
                last_name += lettre
        return first_name, last_name
