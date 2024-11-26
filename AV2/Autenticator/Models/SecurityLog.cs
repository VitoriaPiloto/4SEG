namespace Autenticator.Models
{
    public class SecurityLog
    {
        public int Id { get; set; }
        
        public string Tipo { get; set; }
        
        public int UsuarioId { get; set; }
        
        public DateTime DataHora { get; set; }
    }
}
