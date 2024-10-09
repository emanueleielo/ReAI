# base image
FROM node:16.14.0 as builder

ARG CONFIGURATION


WORKDIR /app

# Install npm 9.7.2
RUN npm install -g npm@9.7.2

# Copy project files to the docker image
COPY . .

# install angular/cli globally (latest version, change this to the version you are using)
#RUN npm i -g  @angular/cli@12.0.1
#RUN npm i -D @angular-builders/custom-webpack@12.0.0 --save
# if you prefer npm, replace the above command with
# RUN npm install @angular/cli@latest -g

# install packages

RUN npm install

# FOR NPM
# npm install

# Build Angular Application in Production
RUN node --max_old_space_size=4000 ./node_modules/@angular/cli/bin/ng build --configuration=$CONFIGURATION

#### STAGE 2
#### Deploying the application

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*

# Copy the build files from the project
# replace "angular-docker-environment-variables" with your angular project name
COPY --from=builder /app/dist/reai /usr/share/nginx/html

# Copy Nginx Files
COPY --from=builder /app/.config/.nginx/nginx.conf /etc/nginx/nginx.conf

# EXPOSE Port 80
EXPOSE 80
