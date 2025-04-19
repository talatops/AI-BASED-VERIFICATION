FROM node:16-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies with legacy peer deps to handle React version conflicts
RUN npm install --legacy-peer-deps

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 3000

# Run the app
CMD ["npm", "start"] 