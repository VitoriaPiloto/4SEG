using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Autenticator.Dtos;
using Autenticator.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Primitives;
using Microsoft.IdentityModel.Tokens;

[ApiController]
[Route("api")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _dbContext;
    private readonly IConfiguration _configuration;
    private readonly JwtSecurityTokenHandler _tokenHandler;

    public AuthController(AppDbContext dbContext, IConfiguration configuration)
    {
        _dbContext = dbContext;
        _configuration = configuration;
        _tokenHandler = new JwtSecurityTokenHandler();
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto loginDto)
    {
        var user = _dbContext.Usuarios.FirstOrDefault(u => u.Email == loginDto.Email);
        if (user == null || !BCrypt.Net.BCrypt.Verify(loginDto.Password, user.SenhaHash))
        {
            return Unauthorized("Credenciais inválidas.");
        }

        var token = GenerateJwtToken(user);

        if (token == null)
        {
            user.TentativasFalhas += 1;
            _dbContext.Usuarios.Update(user);
            _dbContext.SaveChangesAsync();
            return Unauthorized("Não foi possível gerar o token.");
        }


        var log = new SecurityLog
        {
            UsuarioId = user.Id,
            Tipo = "Acesso Login",
            DataHora = DateTime.Now
        };

        user.UltimoLogin = DateTime.Now;
        _dbContext.Usuarios.Update(user);
        _dbContext.LogsSeguranca.Add(log);
        await _dbContext.SaveChangesAsync();

        return Ok(new { Token = token });
    }

    [Authorize]
    [HttpPost("logout")]
    public async Task<IActionResult> Logout()
    {
        var token = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last(); // Pega o token do header

        if (string.IsNullOrEmpty(token))
        {
            return Unauthorized(new { message = "Token não fornecido." });
        }

        var tokenHandler = new JwtSecurityTokenHandler();
        try
        {
            // Verifica a validade do token
            var jwtToken = tokenHandler.ReadJwtToken(token);
            var expirationDate = jwtToken.ValidTo;

            // Cria um registro de blacklist
            var blacklistToken = new Blacklist
            {
                Token = token,
                DataRevogacao = expirationDate,
            };

            _dbContext.BlacklistTokens.Add(blacklistToken);
            await _dbContext.SaveChangesAsync();

            return Ok(new { message = "Logout realizado com sucesso." });
        }
        catch (Exception ex)
        {
            return Unauthorized(new { message = "Token inválido ou erro ao processar o token.", error = ex.Message });
        }
    }

    [Authorize]
    [HttpGet("refresh")]
    public async Task<IActionResult> RefreshToken()
    {
        var refreshToken = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last(); // Pega o token do header

        var blacklistedToken = await _dbContext.BlacklistTokens
            .FirstOrDefaultAsync(t => t.Token == refreshToken);

        if (blacklistedToken != null)
        {
            throw new UnauthorizedAccessException("O token está inválido.");
        }

        var principal = RevalidateToken(refreshToken);
        if (principal == null)
        {
            throw new UnauthorizedAccessException("O token está inválido.");
        }

        var userId = int.Parse(principal.Claims.FirstOrDefault().Value); 
        var user = await _dbContext.Usuarios.FindAsync(userId);
        if (user == null) 
        {
            throw new UnauthorizedAccessException("Usuário não encontrado.");
        }

        var newAccessToken = GenerateJwtToken(user);

        return Ok(new { NovoTokenAcesso = newAccessToken });
    }

    [Authorize]
    [HttpPost("validate")]
    public SecurityToken? ValidateToken()
    {
        var token = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last(); // Pega o token do header

        if (_dbContext.BlacklistTokens.Any(x => x.Token == token))
        {
            throw new Exception("Token já invalidado");
        }

        try
        {
            var key = Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]);
            var tokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = false,
                ValidateAudience = false,
                ValidateLifetime = false, // Não vamos validar a data de expiração do token
                IssuerSigningKey = new SymmetricSecurityKey(key)
            };

            var principal = _tokenHandler.ValidateToken(token, tokenValidationParameters, out var validatedToken);

            return validatedToken;
        }
        catch
        {
            return null;
        }
    }

    private string GenerateJwtToken(User user)
    {
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.Nome),
        };
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            expires: DateTime.Now.AddMinutes(30),
            signingCredentials: creds,
            claims: claims
            );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    // Método para extrair o principal (informações do usuário) de um token expirado
    private ClaimsPrincipal RevalidateToken(string token)
    {
        try
        {
            var key = Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]);
            var tokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = false,
                ValidateAudience = false,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ClockSkew = TimeSpan.Zero
            };

            var principal = _tokenHandler.ValidateToken(token, tokenValidationParameters, out var validatedToken);

            return principal;
        }
        catch
        {
            return null;
        }
    }
}
