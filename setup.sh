#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y portaudio19-dev python3-pyaudio

# Verify installation
ls -la /usr/lib/x86_64-linux-gnu/libportaudio*
