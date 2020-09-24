FROM node:alpine

WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json /frontend

RUN npm install --silent
RUN npm install react-scripts -g --silent

COPY . ./

CMD ["npm","start"]