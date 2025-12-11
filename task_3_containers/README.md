

устанавливаем и проверяем, что десктоп версия докера запущена.

![123](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/01.png)


Устанавливаем brew
![2](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/02.png)
с помощью brew устанавливаем кубер (kubectl и minicube)
![3](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/03.png)
проверяем версию куб-контрола.

![4](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/04.png)
Запускаем кластер командой 
```bash
minikube start --driver=docker
```
![5](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/05.png)
Проверяем контейнеры Docker:
![6](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/06.png)

kubectl config view
kubectl get nodes

![7](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/07.png)
## Сделаем сразу правильный вариант 
```
Для постгреса перенести POSTGRES_USER и POSTGRES_PASSWORD из конфигмапы в секреты.
```

![8](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/08.png)

Порядок имеет значение для объектов, от которых зависят другие (ConfigMap/Secret → Deployment). Сервис можно создавать в любое время, но удобнее после Podов.

![9](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/09.png)




![10](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/10.png)

![11](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/11.png)

![12](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/12.png)


![13](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/13.png)

видно тип `Opaque` и размер, но не пароль:
![14](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/14.png)

![17](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/17.png)

![18](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/18.png)

![19](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/19.png)

![20](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/20.png)

![21](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/21.png)


![22](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/22.png)
- При `replicas=0` pod Postgres удаляется, а вместе с ним и все данные, потому что мы не настраивали PersistentVolume — база хранится в файловой системе контейнера.
    
- При `replicas=1` под создаётся заново с пустой БД.  
    В результате Nextcloud либо предлагает сделать повторную установку, либо выдаёт ошибку — прежние пользователи и данные пропали.
![23](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/23.png)


> Важен ли порядок выполнения этих манифестов? Почему?
 Важен для зависимостей:  Сначала ConfigMap/Secret, потом Deployment, который их использует. Иначе pod может не стартовать или будет в CrashLoop из-за отсутствия переменных/volume. Service можно создавать до или после Podов — он просто появится без Endpoints, пока Pod не запущен.




