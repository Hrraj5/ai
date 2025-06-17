class Tokenizer:
    def encoder(self,tokens):
        vectors=[]
        for char in tokens:
            vectors.append(ord(char))

        return vectors
    
    def decoder(self,vectors):
        token = ""
        for e in vectors:
            token = token + chr(e)

        return token
    


tokenImp = Tokenizer()
vectorRep = tokenImp.encoder("My name is Hrithik")
tokenRep = tokenImp.decoder(vectorRep)
print(vectorRep)
print(tokenRep)