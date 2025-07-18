# SubscrybeFlow

### Sistema de Gestão de Assinaturas e Planos
Controle, análise e acompanhamento de assinaturas de forma prática e eficiente.

## 📄 Descrição do Sistema

Este sistema tem como objetivo facilitar a gestão de assinaturas e planos diversos, permitindo que usuários possam cadastrar seus serviços, acompanhar valores, vencimentos, status de pagamento, entre outras funcionalidades. A aplicação oferece também um painel administrativo onde é possível analisar informações dos usuários, gerar relatórios e gerenciar dados de forma centralizada e intuitiva.

---
## ✨ Funcionalidades

- Cadastro e gerenciamento de assinaturas
- Alteração de dados pessoais e senha do usuário
- Tela de login para acesso seguro
- Acesso diferenciado para administradores
- Controle de Pagamentos e prazos de vencimentos das assinaturas
- Área de Lembretes para acompanhamento 
- Visualização e Exportação de Relátorios Mensais

Painel administrativo com:
- Análise de usuários
- Controle de assinaturas e pagamentos
- Notificações visuais para ações importantes
- Interface responsiva e amigável

---

## 🚀 Aplicação

O sistema está sendo desenvolvido com foco em funcionalidades essenciais e experiência do usuário. Ele pode ser executado localmente ou implantado em um servidor web compatível com Django.
Para rodar localmente:

git clone <https://github.com/Ayram450/gerenciador-de-assinaturas-planos>
cd gerenciador-de-assinaturas-planos
python manage.py runserver

---

## 📚 Documentação

✅ RAD – Rapid Application Development
    
    O projeto foi desenvolvido com Django, framework que permite criação rápida de aplicações robustas por meio de arquitetura MVC, uso de ORM, admin automático e sistema de autenticação nativo.

💻 UI/UX

    Interface construída com Tailwind CSS, garantindo responsividade, clareza e boa experiência visual.
    Páginas como painéis administrativos, relatórios e listagem de usuários seguem boas práticas de usabilidade.

🔐 Segurança e Controle de Acesso

    Controle de acesso com sistema de login e logout usando o django-allauth.
    Áreas protegidas com @login_required.
    Ações críticas, como exclusão de dados, exigem confirmação explícita.

🔒 Criptografia de Dados Sensíveis

    Senhas e autenticações seguem os padrões do Django (uso de PBKDF2).

🧾 Persistência e Conformidade com LGPD

    Dados armazenados de forma persistente com relacionamentos entre modelos.
    Suporte à deleção lógica e integridade referencial: ao remover um usuário ou assinatura, o sistema evita perda de integridade.

🔗 Integração com API Externa

    Integração com a API do Gmail, permitindo envio automático de relatórios em PDF para o e-mail do usuário.

📈 Geração de Relatórios

    Geração de relatórios mensais em PDF, com estatísticas úteis (gastos, status de pagamento, economia).
    Funcionalidade voltada ao apoio à tomada de decisão financeira do usuário.

🗃️ Versionamento de Código

    Projeto versionado com Git, permitindo rastreamento de alterações e trabalho colaborativo.
    Organização por branches (main, dev) e commits semânticos.

---

## Relatórios exigidos para diciplina

Links:

- Relatório de reuniões para andamento do sistema: -> https://docs.google.com/document/d/1dFZD27cnANoPbzX8ywF9a7OdUSWnH2q0vwKlOw7xDvo/edit?usp=sharing

- Relatório Individual Marya Clara: -> https://docs.google.com/document/d/1JXIXjnyKwc3GIlmYD8X8cupm35-2s9bg2Kg0hZPkvGg/edit?usp=sharing

- Relatório Individual de Vitória: -> 
---

## 📚 Prototipação

A prototipação foi realizada utilizando o Figma.

- Link para as telas do protótipo do sistema: -> https://drive.google.com/file/d/149PllvA4eCWwya2PxE9LwjA0iv83myKQ/view?usp=sharing

---

## 🛠 Tecnologias utilizadas

| Camada         | Tecnologias                     |
|----------------|---------------------------------|
| Front-end      | HTML                            |
| Estilização    | Tailwind CSS                    |
| Back-end       | Django (Python)                 |
| Banco de dados | SQLite3                         |

---

## 🔗 Acesso ao projeto

- Repositório GitHub: [https://github.com/Ayram450/gerenciador-de-assinaturas-planos](#)

---

## 👩‍💻 Desenvolvedores

- **Marya Clara** – [Ayram450](#) – Back-end  
- **Vitória Oliveira** – [vyvisz](#) – Front-end  

---

