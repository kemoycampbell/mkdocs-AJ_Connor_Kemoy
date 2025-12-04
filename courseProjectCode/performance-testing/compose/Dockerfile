# Dockerfile
FROM python:3.12-slim

WORKDIR /app

#adding git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Install mkdocs and pytest
RUN pip install --no-cache-dir mkdocs pytest requests beautifulsoup4
RUN git clone https://github.com/Nethereum/Nethereum.Docs.git /app/Nethereum.Docs
RUN mv Nethereum.Docs/* .
RUN rm -rf Nethereum.Docs

#edit the mkdocs.yml to to add dev_addr: '0.0.0.0:8000' at the end of the file
RUN echo "\ndev_addr: '0.0.0.0:8000'" >> mkdocs.yml

EXPOSE 8000

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
