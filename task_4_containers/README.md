## 1. Цель работы
Развернуть собственные сервисы в Kubernetes (Minikube) по аналогии с ЛР3, используя подход из ЛР2: минимум 2 контейнера + 1 init-контейнер, а также ConfigMap/Secret, Service, probes, volume и labels.


## 2. Подготовка окружения
Проверяем запуск Docker Desktop.

![S01](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S01.png)

Проверяем версии kubectl и minikube.

![S02](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S02.png)

Запускаем minikube.

![S03](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S03.png)

Проверяем состояние кластера.

![S04](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S04.png)

## 3. Сборка кастомных образов
Сборка FastAPI образа.

![S05](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S05.png)

Сборка JupyterHub образа.

![S06](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S06.png)

## 4. Проверка созданных ресурсов
Проверяем все ресурсы в namespace.

![S11](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S11.png)
![S12](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S12.png)
![S13](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S13.png)
![S14](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S14.png)

## 5. Проверка доступа к сервисам
### 5.1 FastAPI
Открываем сервис через `minikube service fastapi-service --url` и убеждаемся, что `/` возвращает JSON.

![S15_1](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S15_1.png)
![S15_2](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S15_2.png)

### 5.2 JupyterHub
Открываем сервис через `minikube service jupyterhub-service --url`.

![S16_1](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S16_1.png)
![S16_2](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S16_2.png)

## 6. Kubernetes Dashboard
Запускаем `minikube dashboard --url` и проверяем deployments/pods.

![S17_1](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S17_1.png)
![S17_2](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_4_containers/screenshots_lab4/S17_2.png)

## 7. Заключение
- Создано 3 deploymentа (postgres, jupyterhub, fastapi).
- Кастомный образ: fastapi-itmo:1.0 и jupyterhub-itmo:1.0.
- initContainer: в Deployment `jupyterhub` (`wait-postgres`).
 - volume: в postgres (`emptyDir` для данных), в fastapi (`emptyDir` /tmp), в jupyterhub (configMap volume).
- ConfigMap/Secret: используются для postgres и jupyterhub, также fastapi-configmap.
- Service: созданы postgres-service, jupyterhub-service, fastapi-service.
- Probes: настроены в fastapi (readiness/liveness).
- Labels: добавлены дополнительные (`tier`, `lab`, `owner`).


В ходе работы развернуты связанные сервисы в Kubernetes: PostgreSQL (хранилище данных), JupyterHub (web UI) и FastAPI (пользовательский сервис). Настроены манифесты Deployment/Service, применены ConfigMap/Secret, добавлены initContainer, probes и volume. Работоспособность подтверждена через `kubectl` и Minikube Dashboard, а также доступом к сервисам из браузера.

