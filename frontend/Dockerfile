FROM node:alpine

WORKDIR /usr/src/frontend

ENV PATH /usr/src/frontend/node_modules/.bin:$PATH

COPY package*.json .

RUN yarn install --silent
RUN yarn global add react-scripts

COPY . ./

CMD ["npm","start"]