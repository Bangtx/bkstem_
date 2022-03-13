FROM node:14.16.1

RUN apt-get clean && apt-get update && apt-get install -yqq \
    xvfb libxtst6 libxss1 libgconf-2-4 libnss3 libasound2 libgtk2.0-0 libgtk-3-0 libnotify-dev xauth libgbm-dev

WORKDIR /app/web

COPY package*.json ./

RUN npm install

COPY . /app/web

EXPOSE 4000

CMD ["npm", "run", "serve", "--", "--port", "4000"]
