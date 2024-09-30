class Aluno(db.Model):
   identificador = db.Column(db.int, primary_key=True)
   nome = db.Column(db.String(50))

   @property
   def as_json(self):
       return {
           'id': self.identificador,
           'nome': self.nome,
       }