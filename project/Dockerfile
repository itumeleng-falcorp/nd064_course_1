# Use an official Python runtime as a parent image
FROM python:3.8

# Set the maintainer
LABEL maintainer="Itumeleng Tshabalala"

# Copy the application files into the container
COPY . /project

# Set the working directory in the container
WORKDIR /project

# Expose the application
EXPOSE 3111

# Install dependencies
RUN pip install -r techtrends/requirements.txt

# Run the application
RUN python techtrends/init_db.py
