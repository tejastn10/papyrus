FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Build application for production
RUN npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "start"]
