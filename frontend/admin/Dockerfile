FROM node:18-alpine

WORKDIR /app

RUN npm install pm2 -g

COPY package*.json .
RUN npm install

COPY . .

CMD ["pm2-runtime", "server.js"]