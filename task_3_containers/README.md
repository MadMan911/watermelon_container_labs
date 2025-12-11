# Лабораторная работа №3  
**«Развёртывание многоконтейнерного приложения в Kubernetes (Nextcloud + PostgreSQL)»**

---

## Ответы на вопросы из методички

**1. Важен ли порядок выполнения манифестов? Почему?**

Да, порядок важен для объектов, от которых зависят другие ресурсы:

- Сначала создаются **ConfigMap** и **Secret**, так как они содержат конфигурацию и чувствительные данные (логины/пароли), которые используются подами.
- Затем создаётся **Deployment**, который при старте пода считывает переменные окружения и тома из ConfigMap/Secret.
- Если попытаться создать Deployment раньше, чем соответствующие ConfigMap/Secret, контейнер может:
  - не стартовать,
  - уйти в состояние **CrashLoopBackOff** из-за отсутствующих переменных или томов.

**Service** можно создавать как до, так и после Pod’ов — если поды ещё не существуют, у сервиса просто временно не будет Endpoints.

---

**2. Что произойдёт, если отскейлить `deployment/postgres` до `replicas=0`, а затем обратно до `replicas=1` (без PersistentVolume)?**

- При `replicas=0` pod с PostgreSQL **удаляется**, а вместе с ним удаляется и файловая система контейнера, где хранится база данных (так как PersistentVolume не настроен).
- При возврате к `replicas=1` создаётся **новый pod с пустой БД**.  
  В результате:
  - все прежние данные и пользователи пропадают,
  - Nextcloud при обращении к БД либо предлагает выполнить начальную установку заново,
  - либо выдаёт ошибку (например, при попытке открыть уже существующую установку — появляется страница *Internal Server Error*).

---

## 1. Цель работы

Ознакомиться с развёртыванием многоконтейнерных приложений в Kubernetes, применением объектов **ConfigMap** и **Secret**, созданием **Deployment** и **Service**, а также проверкой корректности работы кластера на примере приложения Nextcloud с базой данных PostgreSQL.

---

## 2. Ход выполнения работы

### 2.1. Подготовка окружения и запуск Docker Desktop

На хост-машине была установлена и запущена десктоп-версия Docker.  
Скриншот показывает открытое меню Docker Desktop со статусом **Docker Desktop is running**.

  
![1](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/01.png)
 

---

### 2.2. Установка Homebrew

Далее был установлен пакетный менеджер **Homebrew**.
После завершения установки терминал предложил добавить `brew` в `PATH`. Эти команды были выполнены, после чего проверена версия Homebrew.

  
![2](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/02.png)
 

---

### 2.3. Установка `kubectl` и `minikube`

С помощью Homebrew были установлены:

* клиент Kubernetes — `kubectl`;
* утилита для локального запуска кластеров — `minikube`.

  
![3](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/03.png)
 

После установки проверены версии:
`kubectl version --client`
`minikube version`

  
![4](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/04.png)
 

---

### 2.4. Запуск локального кластера Kubernetes в Minikube

Кластер Kubernetes был запущен командой:

```bash
minikube start --driver=docker
``` 

На скриншоте видно, как minikube подготавливает кластер, настраивает CNI и включает необходимые дополнения.

  
![5](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/05.png)
 

Затем была проверена работа Docker — команда `docker ps` показывает контейнер `minikube`, в котором работает кластер:

  
![6](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/06.png)
 

С помощью команд:

``` bash
kubectl config view
kubectl get nodes
```

проверена конфигурация kubectl и состояние узла кластера (**node minikube Ready**):

  
![7](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/07.png)
 

---

### 2.5. Подготовка манифестов для PostgreSQL

#### 2.5.1. ConfigMap для PostgreSQL

В редакторе были созданы YAML-манифесты для PostgreSQL.
На скриншоте показан файл `pg-configmap.yml`, в котором задаётся имя базы данных:

  
![8](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/08.png)
 

#### 2.5.2. Secret, Service и Deployment для PostgreSQL

В отличие от варианта из методички, чувствительные данные (`POSTGRES_USER` и `POSTGRES_PASSWORD`) были **перенесены из ConfigMap в Secret**, что является более правильной практикой.

Далее поочерёдно применены манифесты:

 bash
kubectl create -f pg-configmap.yml
kubectl create -f pg-secret.yml
kubectl create -f pg-service.yml
kubectl create -f pg-deployment.yml
 

  
![9](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/09.png)
 

После этого были проверены созданные ресурсы:

* `kubectl get configmap`
* `kubectl get secret`
* `kubectl get svc`
* `kubectl get deployments`
* `kubectl get pods`

На скриншоте видно, что ConfigMap и Secret созданы, сервис `postgres-service` имеет тип **NodePort**, а pod `postgres` находится в состоянии **Running**.

  
![10](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/10.png)
 

Команда `kubectl get all` показывает полный список созданных объектов (pod, service, deployment, replicaset):

  
![11](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/11.png)
 

---

### 2.6. Развёртывание Nextcloud и подключение к PostgreSQL

#### 2.6.1. Создание Secret и ConfigMap для Nextcloud

Для Nextcloud был создан Secret с паролем администратора:

* `nextcloud-secret.yml` с ключом `NEXTCLOUD_ADMIN_PASSWORD`.

Затем — ConfigMap с параметрами подключения к базе данных (`POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER` и т.д.).

Манифесты применены командами:

``` bash
kubectl create -f nextcloud-secret.yml
kubectl create -f nextcloud-configmap.yml
kubectl create -f nextcloud-deployment.yml
 ```

  
![12](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/12.png)
 

#### 2.6.2. Проверка созданных ресурсов

Проверяем ConfigMap и Secret:

``` bash
kubectl get configmap
kubectl get secret
 

Проверяем Deployment и Pod’ы:

``` bash
kubectl get deployments
kubectl get pods
```

Сначала pod Nextcloud имеет статус **ContainerCreating**:

  
![13](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/13.png)
 

Команда:

``` bash
kubectl describe secret nextcloud-secret
 ```

показывает, что секрет создан, имеет тип **Opaque**, указан размер значения, но сам пароль не отображается в открытом виде:

  
![14](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/14.png)
 

Просмотр логов pod’а Nextcloud подтверждает успешную установку приложения и запуск Apache/PHP:

``` bash
kubectl logs <имя-pod-nextcloud>
 ```

  
![17](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/17.png)
 

После исправления манифестов и повторного развёртывания команда `kubectl get all` показывает работающий pod PostgreSQL и сервис `postgres-service`:

  
![18](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/18.png)
 

Далее проверяем сервисы и pod’ы:

``` bash
kubectl get svc
kubectl get pods
 ```

На скриншоте видно:

* сервис `nextcloud` типа **NodePort** с портом 80:31382/TCP;
* сервис `postgres-service` для БД;
* оба pod’а (`nextcloud` и `postgres`) находятся в статусе **Running**.

  
![19](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/19.png)
 

---

### 2.7. Доступ к Nextcloud через Minikube

Для проброса сервиса Nextcloud наружу используется команда:

``` bash
minikube service nextcloud
 ```

Команда выводит URL сервиса внутри виртуальной сети и запускает туннель с локальным адресом вида `http://127.0.0.1:<порт>`.

  
![20](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/20.png)
 

Открыв полученный URL в браузере, видим страницу входа Nextcloud:

  
![21](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/21.png)
 

После авторизации отображается приветственный экран Nextcloud с рекомендованными файлами:

  
![22](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/22.png)
 

---

### 2.8. Использование Kubernetes Dashboard

Далее был включён и открыт **Kubernetes Dashboard** с помощью команды:

``` bash
minikube dashboard --url
 ```

Команда выводит URL для доступа к Dashboard:

  
![23](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/23.png)
 

В веб-интерфейсе Dashboard видно:

* два Deployment’а: `nextcloud` и `postgres`;
* два pod’а в статусе **Running**;
* соответствующие ReplicaSet’ы.

  
![24](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/24.png)
 

---

### 2.9. Эксперимент со scale и потерей данных при отсутствии PersistentVolume

Для проверки влияния масштабирования на данные в БД был выполнен эксперимент с Deployment PostgreSQL.

Сначала количество реплик уменьшено до нуля:

`` bash
kubectl scale deployment postgres --replicas=0
 ``

Pod Postgres был удалён. Затем число реплик вновь увеличено до 1:

``` bash
kubectl scale deployment postgres --replicas=1
 ```
