FROM ghcr.io/puppeteer/puppeteer:16.1.0
COPY --chown=pptruser:pptruser package*.json ./
RUN npm ci --omit=dev
COPY --chown=pptruser:pptruser . .
ENTRYPOINT ["node", "runner.js"]
