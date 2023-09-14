FROM ghcr.io/puppeteer/puppeteer:19.0.0
COPY package*.json ./
RUN npm ci --omit=dev
COPY --chown=pptruser:pptruser . .
ENTRYPOINT ["node", "runner.js"]
