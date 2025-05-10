# Start from base python
FROM python:3.13.1
LABEL authors="Tripify"

# Set default enviroment to production, can be overriden
ENV enviroment=production

WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]