FROM nginx:alpine

# Install envsubst for runtime variable substitution
RUN apk add --no-cache gettext

WORKDIR /usr/share/nginx/html

# Copy built Angular app
COPY dist/frontend/browser ./

# Copy dynamic config template
COPY dist/frontend/browser/assets/config/app.config.template.js assets/config/app.config.template.js

# Copy Nginx config template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Replace env variables & start Nginx
SHELL ["/bin/sh", "-c"]

CMD envsubst '${BACKEND_HOST} ${BACKEND_PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && \
    envsubst '${API_URL} ${COGNITO_LOGOUT_URL} ${COGNITO_AUTHORITY} ${REDIRECT_URL} ${POST_LOGOUT_URI} ${CLIENT_ID} ${SCOPE} ${RESPONSE_TYPE}' < assets/config/app.config.template.js > assets/config/app.config.js && \
    nginx -g 'daemon off;'

EXPOSE 80
