namespace Autenticator.Models
{
    public class Blacklist
    {
        public int Id { get; set; } 
        public string Token { get; set; } 
        public DateTime DataRevogacao { get; set; } 
    }
}
