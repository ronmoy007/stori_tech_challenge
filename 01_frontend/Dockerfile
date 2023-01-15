FROM node:latest

WORKDIR /app

COPY 01_frontend/package*.json ./

RUN npm install

COPY 01_frontend .

CMD ["npm", "start"]
