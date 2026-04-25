# Entrega - Tech Challenge (Fase 1)

**Curso:** FIAP Pós Tech - Machine Learning Engineering
**Turma:** 9MLET

**Autores (Grupo 85):**
* Bruno Machado Abreu (RM372965)
* Renan Prado Gonzalez (RM374089)
* Davi Coene Rosa (RM371466)

---

## 🔗 Links Oficiais do Projeto

1. **Repositório do Código (Github):**
   * [https://github.com/fiap-postech-9mlet-grupo85/tech-challenge-fase01](https://github.com/fiap-postech-9mlet-grupo85/tech-challenge-fase01)
   * *Nota 1:* Todo o código fonte, documentação da arquitetura (ML Canvas, Dicionário de Dados) e arquivos de provisionamento da nuvem AWS (Terraform) encontram-se neste repositório.
   * *Nota 2 (Git Flow e Avaliação de Commits):* A branch `main` possui proteção estrita e só aceita commits oriundos de Pull Requests (PRs). Para manter o histórico limpo, utilizamos a estratégia de **Squash and Merge**. Portanto, para acompanhar a granularidade mais detalhada do trabalho e da evolução do código, solicitamos que os avaliadores analisem as abas de **Pull Requests** (fechados), pois cada commit na branch `main` possui em sua mensagem o link direto para o PR correspondente contendo todos os commits originais.

2. **Apresentação do Projeto (Vídeo STAR):**

   [![Pitch - Tech Challenge](https://img.youtube.com/vi/3OpsjKj8Zlw/hqdefault.jpg)](https://www.youtube.com/watch?v=3OpsjKj8Zlw)
   
   > *Nota:* Vídeo pitch explicativo detalhando a Situação, Tarefa, Ações e Resultados do projeto.

3. **API em Produção na Nuvem (AWS):**
   * **Swagger UI:** [https://api.telcochurn.cloud-ip.cc/docs](https://api.telcochurn.cloud-ip.cc/docs)
   * **Health Check:** [https://api.telcochurn.cloud-ip.cc/health](https://api.telcochurn.cloud-ip.cc/health)
   * *Nota de Segurança (Geo-Blocking):* A API está hospedada na AWS e protegida por HTTPS via CloudFront. Para evitar ataques de bots globais, o CloudFront possui uma restrição geográfica ativa. A API é acessível publicamente **apenas por IPs localizados no Brasil e em Portugal**. Acessos de outros países retornarão erro HTTP 403 (Forbidden).
