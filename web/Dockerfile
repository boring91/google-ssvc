FROM node:20.12-alpine3.18 AS build
WORKDIR /build
RUN npm i -g npm@10.5.0
COPY package*.json ./
RUN npm install --force
COPY tsconfig.json ./
COPY tsconfig.app.json ./
COPY angular.json ./angular.json
COPY tailwind.config.js ./
COPY tailwindcss ./tailwindcss
COPY src ./src
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /build/dist/web/browser /usr/share/nginx/html
ADD default.conf /etc/nginx/conf.d/
