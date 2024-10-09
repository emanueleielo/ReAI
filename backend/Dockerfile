FROM python:3.10

WORKDIR /backend

COPY requirements.txt .

RUN pip install torch==2.2.2 --extra-index-url https://download.pytorch.org/whl/cpu


RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

#RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.24 --force-reinstall --upgrade --no-cache-dir


RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY . .

ENV PYTHONPATH /backend


CMD ["python", "server/app.py"]
