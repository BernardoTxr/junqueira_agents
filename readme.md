# JUNQUEIRA AGENTS

📅 **Data:** 05/06/2025  
👤 **Autor:** Bernardo Teixeira  
📧 **Email:** bernardoteixeira@usp.br  

---

## 🧠 PROJETOS DESENVOLVIDOS

### 📌 1. Agente de Notícias (Agente Jornalista)
Responsável por monitorar, agrupar, resumir e enviar por e-mail as principais notícias técnicas da semana sobre IA, tecnologias e criptomoedas.  

**Funcionalidades:**
- Varredura semanal (mas com ativação **manual**) de **9 sites especializados**
- Geração de **resumo automático**
- Envio de **newsletter** com notícias relevantes

**🌐 Fontes monitoradas:**
- https://arstechnica.com/ai/
- https://www.zdnet.com/topic/artificial-intelligence/
- https://deepmind.google/
- https://ai.meta.com/blog/
- https://www.ibm.com/quantum/blog
- https://decrypt.co/news
- https://blog.chain.link/
- https://cryptoslate.com/defi/

---

### 📌 2. Agente Analista de FIDCs
Processa relatórios PDF para extração e estruturação de dados importantes para análise de FIDCs.  

**Entregas:**
- Resumo em **PDF** por relatório
- Planilha **CSV** consolidando todos os dados relevantes

---

## ☁️ INFRAESTRUTURA NA NUVEM

💻 Ambos os agentes estão hospedados em uma **VM (e2-small)** no Google Cloud Platform  
🧱 As aplicações rodam em **containers**, garantindo restauração automática ao reiniciar a VM  

💸 **Custos mensais aproximados:**
- IP Estático: **R$ 60/mês**
- Disco da VM: **R$ 10/mês**
- Uso sob demanda da VM: **Desprezível**

**🔻 Total estimado:** **R$ 70/mês**

⚠️ Lembre-se de **parar manualmente** a máquina após o uso para evitar cobranças extras.

---

## 🚀 COMO USAR OS AGENTES

### 🖥️ Acesse a VM

1. Acesse: [Google Cloud Virtual Machines](https://console.cloud.google.com/compute/instances?hl=en&inv=1&invt=AbzWGg&project=projeto-de-agent)  
2. Localize a VM `junqueira-vm`  
3. Clique em **Start**  
4. Aguarde cerca de **10 minutos**

---

### 📬 Agente Jornalista (via N8N)

- Acesse: [http://104.154.164.226:5678/](http://104.154.164.226:5678/)
- Login: `junqueira@gmail.com`  
- Senha: `Junqueira123`

**Etapas:**
1. Acesse o workflow `agente-jornalista`
2. Altere o destinatário no último nó (campo `To email`)
3. Clique em `Test workflow` no canto inferior

🔚 Finalizado? Volte à VM e clique em **Stop ou Parar** (⚠️ **e não em Suspender**).

---

### 📊 Agente FIDC (Analista de Relatórios)

- Acesse: [http://104.154.164.226:3000/](http://104.154.164.226:3000/)
- Envie os PDFs pelo botão no lado esquerdo
- O Excel será gerado automaticamente
- O download inicia assim que o processo termina

🔚 Finalizado? Volte à VM e clique em **Stop ou Parar** (⚠️ **e não em Suspender**).

---

## 📧 CONFIGURAR CREDENCIAL DE EMAIL NO N8N

1. Ative a **verificação em duas etapas** na sua conta Gmail  
2. Acesse: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)  
3. Gere e copie a **App Password**

### ⚙️ No N8N:

- Vá em `Overview > Credentials`
- Clique em `Create Credentials`
- Selecione `SMTP`
- Preencha:
  - **User:** seu email
  - **Password:** app password gerada
  - **Host:** `smtp.gmail.com`
- Clique em **Save**

---

📎 Dúvidas? Fale com: **bernardoteixeira@usp.br**
