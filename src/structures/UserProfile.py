class UserProfile():
    def __init__(self, username, form, id) -> None:
        self.username = username
        self.form = form
        self.rating = int()
        self.id = id
    
    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username
    
    def setForm(self, form):
        self.form = form

    def getForm(self):
        return self.form
    
    def setRating(self, rating):
        self.rating = rating
    
    def getRating(self):
        return self.rating