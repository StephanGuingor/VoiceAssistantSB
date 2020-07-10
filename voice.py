"""
Voice Class
"""

import pyttsx3

class LOCALE:
    EN_US = [11,33]
    ES_MX = [15,31]


class SEX:
    M = 0
    F = 1

class InvalidLanguage(BaseException):
    pass

class Voice:
    
    def __init__(self,lang=LOCALE.EN_US,volume=1.0,rate=200,sex=SEX.F):
        self.lang = lang
        self.volume = volume
        self.rate = rate
        self.sex = sex

        self.engine = self._settings()

    def _settings(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume',self.volume)

        voices =  engine.getProperty('voices')

        
        if (self.lang,LOCALE in LOCALE.__dict__.values()) and (self.sex in SEX.__dict__.values()):
            engine.setProperty('voice', voices[self.lang[self.sex]].id)
        else:
            raise InvalidLanguage("Language has to be of type LOCALE and sex type SEX")
        
        engine.connect('started-word', self._onStartWord)
        engine.connect('error', self._onError)

        return engine

    def _onError(self,**kwargs):
        if 'exception' in kwargs:
            print(kwargs['exception'])

    def _onStartWord(self,**kwargs):
        print('starting', kwargs)

    def say(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()


if __name__ == "__main__":
    myVoice = Voice(lang=LOCALE.EN_US,sex=SEX.M)
    myVoice.say("Hola Sexy, Como Estas")
  
    
