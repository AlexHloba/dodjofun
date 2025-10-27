# Используем современный образ Node.js
FROM node:20-alpine

# Устанавливаем рабочую директорию
WORKDIR /frontend

# ✅ Переключаемся на стабильный npm registry (высокая доступность)
RUN npm config set registry https://registry.npmmirror.com/ \
    && npm config set fetch-retries 5 \
    && npm config set fetch-retry-factor 2 \
    && npm config set fetch-timeout 60000 \
    && npm install -g npm@latest

# Копируем package.json (и lock, если есть)
COPY package*.json ./

# Устанавливаем зависимости (с фолбэком)
RUN npm install --legacy-peer-deps || npm install --force

# Копируем весь фронтенд-код
COPY . .

# Открываем порт
EXPOSE 3000

# Запускаем Next.js в режиме разработки
CMD ["npm", "run", "dev"]
