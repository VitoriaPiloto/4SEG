using System.Net.Mail;
using System.Net;
using SendGrid;
using SendGrid.Helpers.Mail.Model;
using SendGrid.Helpers.Mail;

namespace Autenticator.Services
{
    public class EmailService
    {
        private readonly IConfiguration _configuration;

        public EmailService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public async Task SendEmailAsync(string to, string subject, string body)
        {
            var apiKey = _configuration["Smtp:Key"];
            var client = new SendGridClient(apiKey);

            var from = new EmailAddress("vitoriapiloto477@gmail.com", "Autenticator API");
            var toEmail = new EmailAddress(to, "Usuario");

            var htmlContent = body;

            var msg = MailHelper.CreateSingleEmail(from, toEmail, subject, body, htmlContent);

            var response = await client.SendEmailAsync(msg);

            return;
        }
    }
}
