# Use a imagem oficial Node.js (versão LTS)
FROM node:18-alpine

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia package.json e package-lock.json para instalar dependências
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia todo o código da aplicação para dentro do container
COPY . .

# Build da aplicação Next.js
RUN npm run build

# Expor a porta que o Next.js usa (default 3000)
EXPOSE 3000

# Comando para rodar a aplicação em produção
CMD ["npm", "start"]
