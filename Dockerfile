# Use an official Python runtime as the base image
FROM python:3.8.2 AS python-build
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
RUN apt-get update && apt-get install -y netcat
ENV APP=/app
WORKDIR $APP
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt
COPY . $APP
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh

# Use an official Node.js runtime as the base image
FROM node:12 AS node-build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080

# Final stage to combine the two applications
FROM python:3.8.2
COPY --from=python-build /app /python-app
COPY --from=node-build /app /node-app
CMD ["node", "/node-app/getDealerships.js"]
