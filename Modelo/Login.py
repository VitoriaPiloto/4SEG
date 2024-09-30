class Login(db.Model):
   identificador = db.Column(db.int, primary_key=True)
   usuario = db.Column(db.String(20))
   senha = db.Column(db.String(20))

   @property
   def as_json(self):
       return {
           'id': self.identificador,
           'usuario': self.usuario,
           'senha': self.senha
       }