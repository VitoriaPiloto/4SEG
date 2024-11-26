using System.IdentityModel.Tokens.Jwt;
using Autenticator.Dtos;
using Autenticator.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace Autenticator.Controllers
{
    [ApiController]
    [Route("api/logs")]
    public class LogsController : ControllerBase
    {
        private readonly AppDbContext _dbContext;

        public LogsController(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpGet("getLogs")]
        public IQueryable<SecurityLog> ObterLogs()
        {
            return _dbContext.LogsSeguranca.AsQueryable();
        }
    }
}
