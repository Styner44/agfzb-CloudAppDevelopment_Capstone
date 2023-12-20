<<<<<<< HEAD
FROM python:3.8.2
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
RUN apt-get update \
    && apt-get install -y netcat
ENV APP=/app
WORKDIR $APP
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt
COPY . $APP
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
=======
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
>>>>>>> 703d4fecd3350f0489f88599927cd1e28bd70420
