# Task 5.2

## Part 1

Патч с исправлениями в файле [metrics.patch](metrics.patch).

## Part 2

Для автоматической регистрации таргета при запуске `Oncall` нужно просто добавить описание таргета в конфигерацию `prometheus.yml`:

```yaml
  # Make metrics for oncall-web.
  - job_name: "oncall-web"
    # We use custom path. Prometheus uses /metrics as default.
    metrics_path: /
    static_configs:
      - targets:
          [ "oncall-web:8081" ]
```

`oncall-web` - имя контейнера

`8081` - открытый порт контейнера для метрик

Файл с примером конфигурацией: [prometheus.yml](prometheus.yml).


