using Autenticator.Dtos;
using Autenticator.Models;
using Autenticator.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Autenticator.Controllers
{
    [ApiController]
    [Route("api/2fa")]
    public class TwoFactorController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private readonly AppDbContext _dbContext;

        public TwoFactorController(AppDbContext dbContext, IConfiguration configuration)
        {
            _dbContext = dbContext;
            _configuration = configuration;
        }

        [Authorize]
        [HttpPost("generate")]
        public async Task<IActionResult> GenerateTwoFactorCode([FromBody] string email)
        {
            if (string.IsNullOrEmpty(email))
                return BadRequest("E-mail não pode estar vazio.");

            var random = new Random();
            var codigo = random.Next(1000, 9999).ToString();

            var twoFactor = new _2FA
            {
                Email = email,
                Codigo = codigo,
                Expiracao = DateTime.UtcNow.AddMinutes(5),
                Usado = 0
            };

            // Salvar no banco
            await _dbContext.TwoFactor.AddAsync(twoFactor);
            await _dbContext.SaveChangesAsync();

            // Enviar o e-mail (pode usar um serviço de envio de e-mails)
            var emailService = new EmailService(_configuration);
            await emailService.SendEmailAsync(email, "Código de Autenticação", $"Seu código é: {codigo}");

            return Ok("Código enviado para o e-mail.");
        }

        [Authorize]
        [HttpPost("verify")]
        public async Task<IActionResult> VerifyTwoFactorCode([FromBody] _2FADto Dto)
        {
            var query = _dbContext.TwoFactor.AsQueryable();
            var record = query.FirstOrDefault(r => r.Email == Dto.Email && r.Codigo == Dto.Codigo);

            if (record == null)
                return BadRequest("Código inválido.");

            if (record.Expiracao < DateTime.UtcNow)
                return BadRequest("Código expirado.");

            if (record.Usado == 1)
                return BadRequest("Código já foi utilizado.");

            // Atualizar o status para verificado
            record.Usado = 1;
            await _dbContext.SaveChangesAsync();

            return Ok("Código verificado com sucesso.");
        }

    }
}
