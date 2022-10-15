FROM ghcr.io/puppeteer/puppeteer:latest
COPY package*.json ./
RUN npm ci --omit=dev
COPY --chown=pptruser:pptruser . .
ENTRYPOINT ["node", "runner.js"]
