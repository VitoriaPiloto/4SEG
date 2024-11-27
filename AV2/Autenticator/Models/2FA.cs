namespace Autenticator.Models
{
    public class _2FA
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string Codigo { get; set; }
        public DateTime Expiracao { get; set; }
        public int Usado { get; set; }
    }
}
