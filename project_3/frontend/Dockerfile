# Stage 1: Build Angular app
FROM node:18-alpine AS builder

WORKDIR /app
COPY . .
RUN npm install && npx ng build --configuration production

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Install envsubst for dynamic env replacement
RUN apk add --no-cache gettext

WORKDIR /usr/share/nginx/html

# Copy built Angular app
COPY --from=builder /app/dist/frontend/browser ./

# Copy config template (dynamic JS config)
COPY --from=builder /app/dist/frontend/browser/assets/config/app.config.template.js assets/config/app.config.template.js

# Copy nginx.conf template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Expose port
EXPOSE 80

# Replace env variables & start Nginx
CMD ["/bin/sh", "-c", "\
    envsubst '${API_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && \
    envsubst '${API_URL} ${COGNITO_LOGOUT_URL} ${COGNITO_AUTHORITY} ${COGNITO_REDIRECT_URL} ${COGNITO_POST_LOGOUT_URI} ${COGNITO_CLIENT_ID} ${COGNITO_SCOPE} ${COGNITO_RESPONSE_TYPE}' < assets/config/app.config.template.js > assets/config/app.config.js && \
    nginx -g 'daemon off;'"]
