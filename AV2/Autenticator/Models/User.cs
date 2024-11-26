namespace Autenticator.Models
{
    public class User
    {
        public int Id { get; set; }
        
        public string Nome { get; set; }
        
        public string Email { get; set; }

        public string SenhaHash { get; set; }
        
        public DateTime? UltimoLogin { get; set; }

        public int TentativasFalhas { get; set; }
    }

}
