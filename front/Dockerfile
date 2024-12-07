# Use the Node.js base image
FROM node:18

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first
COPY package*.json ./

# Set ownership of the files for the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Install dependencies
RUN npm cache clean --force && npm ci --production --ignore-scripts

RUN npm install

# Copy only required files first to minimize risk and leverage caching
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Start the application
CMD ["npm", "run", "dev", "--", "--host"]