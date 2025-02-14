FROM node:lts-alpine
ENV NODE_ENV=production
RUN mkdir -p /home/node/webservEx/node_modules && chown -R node:node /home/node/webservEx
WORKDIR /home/node/webservEx
COPY package*.json ./
RUN npm install
COPY --chown=node:node . .
EXPOSE 8080
CMD [ "node", "server.js" ]