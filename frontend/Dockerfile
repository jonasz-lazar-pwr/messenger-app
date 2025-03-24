# Stage 1: Build Angular app
FROM node:18-alpine AS builder

WORKDIR /app
COPY . .
RUN npm install && npm run build --configuration=production

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Install envsubst (part of gettext) for env variable substitution
RUN apk add --no-cache gettext

WORKDIR /usr/share/nginx/html

# Copy built Angular app
COPY --from=builder /app/dist/frontend/browser .

# Copy nginx template (not yet final config)
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Dynamic config generation and Nginx run
CMD ["/bin/sh", "-c", "envsubst '$BACKEND_HOST $BACKEND_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

EXPOSE 80

## Skopiuj zbudowaną aplikację do katalogu serwowanego przez Nginx
#COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html
#
## Skopiuj niestandardową konfigurację Nginx (jeśli jest potrzebna)
#COPY nginx.conf /etc/nginx/conf.d/default.conf
#
#EXPOSE 80
#
#CMD ["nginx", "-g", "daemon off;"]
