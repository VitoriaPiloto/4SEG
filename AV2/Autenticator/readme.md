
# API de Autenticação

Uma API de autenticação simples e segura, projetada para gerenciar usuários, autenticar credenciais e proteger recursos com tokens de acesso.

## 🛠️ Tecnologias utilizadas

- **Linguagem:** C#
- **Framework:** Entity Framework
- **Banco de Dados:** SQL SERVER
- **Autenticação:** JWT (JSON Web Token)
- **Outras dependências:** Send grid, 2FA

---

## 🚀 Funcionalidades

- **Registro de Usuários:** Permite criar novas contas de usuário.
- **Login:** Autentica usuários registrados com email e senha.
- **Recuperação de Senha:** Gera links/token para redefinição de senha.
- **Tokens de Acesso:** Geração e validação de tokens JWT.
- **Proteção de Rotas:** Recursos protegidos que requerem autenticação.
- Outras funcionalidades adicionais, como autenticação por 2FA, integração com provedores OAuth, etc.

---

## 🛠️ Como configurar e executar

### Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- C#
- SQL SERVER

### Passo a Passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/sua-api-de-autenticacao.git
   cd sua-api-de-autenticacao
   ```
2. Configure as variáveis de ambiente no appsettings

    ```bash
    "jwt": {
    "key": "chave jwt"
     },
     "Smtp": {
       "Key": "chave api grid mail",
     }
    ```
3. Execute a aplicação

---

## 🔍 Documentação da API

A API segue os padrões REST. Abaixo estão os principais endpoints:

Autenticação
 
- ```POST /api/users/register```
  
Registro de um novo usuário.
Body:

```bash
{
  "name": "Seu Nome",
  "email": "email@exemplo.com",
  "password": "sua_senha"
}
```

- ```POST /api/login```
    
Autentica um usuário existente.
Body:

```bash
{
  "email": "email@exemplo.com",
  "password": "sua_senha"
}
```

- ```POST /api/logout```
    
Desautentica um token.


- ```GET /api/refresh```
    
Cria um novo token.

- ```POST /api/validate```
    
Valida o token

- ```GET /api/logs/getLogs```
    
Obtém os logs do sistema.

- ```POST /api/2fa/generate```

Gera um código para autenticação de dois fatores.
Body:

```bash
{
  "email@exemplo.com"
}
```

- ```POST /api/2fa/verify```
    
Autentica um usuário existente.
Body:

```bash
{
  "email": "email@exemplo.com",
  "codigo": "codigo"
}
```

---

## 🛡️ Segurança
- As senhas são armazenadas de forma segura usando bcrypt (ou similar).
- Tokens JWT possuem tempo de expiração configurado.




