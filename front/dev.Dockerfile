FROM node:17-alpine

# copy package.json and package-lock.json into /usr/app
WORKDIR /app

COPY package*.json ./

RUN yarn install
ENV NODE_OPTIONS=--openssl-legacy-provider

COPY . .

EXPOSE 3000

CMD ["yarn", "start"]