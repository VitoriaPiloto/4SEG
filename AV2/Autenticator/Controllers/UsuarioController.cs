using System.IdentityModel.Tokens.Jwt;
using Autenticator.Dtos;
using Autenticator.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace Autenticator.Controllers
{
    [ApiController]
    [Route("api/users")]
    public class UsuarioController : ControllerBase
    {
        private readonly AppDbContext _dbContext;

        public UsuarioController(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterDto registerDto)
        {
            if (_dbContext.Usuarios.Any(u => u.Email == registerDto.Email))
                return BadRequest("Email já registrado.");

            var user = new User
            {
                Nome = registerDto.Name,
                Email = registerDto.Email,
                SenhaHash = BCrypt.Net.BCrypt.HashPassword(registerDto.Password),
                UltimoLogin = null,
                TentativasFalhas = 0
            };

            _dbContext.Usuarios.Add(user);
            await _dbContext.SaveChangesAsync();

            var log = new SecurityLog
            {
                UsuarioId = user.Id,
                Tipo = "Usuario Registrado",
                DataHora = DateTime.Now
            };

            _dbContext.LogsSeguranca.Add(log);
            await _dbContext.SaveChangesAsync();

            return Ok("Usuário registrado com sucesso.");
        }

        [Authorize]
        [HttpGet]
        public IQueryable<User> GetUsers()
        {
            var token = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last(); // Pega o token do header

            if (_dbContext.BlacklistTokens.Any(x => x.Token == token))
            {
                throw new Exception("Token já invalidado");
            }

            return _dbContext.Usuarios.AsQueryable();
        }
    }
}
