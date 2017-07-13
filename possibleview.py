class View:
    baseurl = "https://gist.githubusercontent.com/"

    def __init__(self, name, description, key,thumb):
        self.name = name
        self.description = description
        self.key = key
        self.url = ""
        self.thumb =thumb

    def getcompleteurl(self):
        return View.baseurl + self.name + "/" + self.key+"/"

    def show(self):
        return self.name + "\n" + self.description + "\n" + self.key + "\n" + self.thumb +"\n"+"-----------------------"

    def getlocation(self):
        return self.name+":_"+self.description.replace(" ","_")+".html"

    def getthumb(self):
        return self.name + "_" + self.description.replace(" ", "_") + "_thumb.png"