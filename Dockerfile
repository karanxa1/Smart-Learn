FROM python:3.9

WORKDIR /code

USER root

# Upgrade pip first
RUN pip install --upgrade pip

# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*


# Install the dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Install EasyOCR dependencies
RUN apt-get update && apt-get install -y  tesseract-ocr
# Copy the rest of the application code
COPY . /code

RUN mkdir -p /code/uploads /code/speech && \
    chmod 775 /code/uploads /code/speech

CMD ["python", "app.py"]