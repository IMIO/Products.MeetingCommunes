from Products.PloneMeeting.browser.discuss import Discuss

class CustomDiscuss(Discuss):

    #just override the Discuss.available method
    def available(self):
        return True
