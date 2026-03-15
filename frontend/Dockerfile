FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
