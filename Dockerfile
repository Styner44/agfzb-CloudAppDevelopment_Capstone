# Use an official Node.js runtime as the base image
FROM node:12

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the code to the working directory
COPY . .

# Make the container's port 8080 available to the outside world
EXPOSE 8080

# Run the app when the container launches
CMD ["node", "getDealerships.js"]