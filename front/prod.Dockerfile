FROM node:17-alpine as build

WORKDIR /app

COPY package.json /app
RUN yarn install

COPY . /app
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN yarn build

FROM nginx:latest

COPY --from=build /app/build/ /usr/share/nginx/html

