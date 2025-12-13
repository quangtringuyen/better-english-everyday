# Build Stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Build the app strictly
RUN npm run build

# Production Stage
FROM nginx:alpine
# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy resources folder (if volume mapping fails, this is a fallback, but volume is better)
# But strictly we rely on volume mapping for resources as they are large.

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
