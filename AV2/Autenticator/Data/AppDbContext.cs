using System.Collections.Generic;
using Autenticator.Models;
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Usuarios { get; set; }
    public DbSet<_2FA> TwoFactor { get; set; }
    public DbSet<SecurityLog> LogsSeguranca { get; set; }
    public DbSet<Blacklist> BlacklistTokens { get; set; }
}
