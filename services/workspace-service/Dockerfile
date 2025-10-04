FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --production || true
COPY . .
EXPOSE 9000
CMD ["node","index.js"]
