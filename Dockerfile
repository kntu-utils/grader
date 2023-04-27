FROM python:3.10 AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM deps AS collector
COPY . .
RUN python manage.py collectstatic --noinput

FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

FROM nginx:latest AS server
COPY --from=builder /app/build /usr/share/nginx/html
COPY --from=collector /app/collector /usr/share/nginx/html/collector
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

FROM deps AS runner
RUN apt-get update
RUN apt-get install -y gettext
WORKDIR /app
COPY . .
RUN python manage.py compilemessages
EXPOSE 8000
CMD ["python", "-m", "daphne"]
