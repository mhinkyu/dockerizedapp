#docker file template to be added to the projects
FROM python:3.9-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev zlib-dev build-base libjpeg-turbo libjpeg-turbo-dev
RUN apk add python3-dev py3-setuptools
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade --no-cache-dir --target="/install" -r /requirements.txt
RUN find /install \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM base
COPY --from=builder /install /app
COPY . /app
WORKDIR /app
EXPOSE 5001

ENTRYPOINT [ "python3" ]
# These commands will be replaced if user provides any command by himself
CMD ["/app/app.py"]