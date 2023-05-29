# Deploying A Fashion Search Engine from Scratch with Beam and FashionCLIP

This is a WIP. Waiting for the blog post to be published. The code is kind of ready to use but without instructions it's not very useful.

## Introduction

This is the code for the following [blog post]().
Best way to use this is to first read the post; it will walk you through the process of deploying a fashion search engine from scratch using Beam and FashionCLIP.

This readme contains basic information on how to install Beam and deploy the search engine.

## Basic Installation
    
To install Beam. You can run the following commands in your terminal:
```bash
    curl https://raw.githubusercontent.com/slai-labs/get-beam/main/get-beam.sh -sSfL | sh
    beam configure
    pip install beam-sdk
```

## Creating Volumes and Uploading Data

```bash
  beam volume upload cache_data fashionbeam_data -a fashion-clip-app
```

## Deploying the Search Engine

```bash
    beam deploy app.py
```


