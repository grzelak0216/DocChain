FROM node:18

WORKDIR /app

# Skopiuj zależności
COPY package.json ./
COPY hardhat.config.js ./

# Zainstaluj zależności
RUN npm install

# Uruchom lokalny node przez zainstalowanego hardhata
CMD ["npx", "hardhat", "node"]
