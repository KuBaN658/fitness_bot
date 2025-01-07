# fitness_bot

### Запуск через докер
```
docker build . -t <название образа>

docker run --rm -e BOT_TOKEN=<токен бота> -e ADMIN_ID=<telegram id админа> -e OPENWEATHERMAP_API_KEY=<api ключ openweathermap> -e FOLDER_ID=<id каталога yandex cloud> -e IAM_TOKEN=<iam token yandex cloud> -v logs_volume:/app/logs -v users_volume:/app/data <название образа>
```
