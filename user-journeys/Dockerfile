FROM ghcr.io/puppeteer/puppeteer:16.1.0
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
ENTRYPOINT ["node", "runner.js"]
