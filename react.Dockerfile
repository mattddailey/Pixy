FROM node:alpine

COPY frontend/package.json ./
COPY frontend/package-lock.json ./

RUN npm install

WORKDIR /frontend