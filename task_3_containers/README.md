

устанавливаем и проверяем, что десктоп версия докера запущена.

![123](https://github.com/MadMan911/watermelon_container_labs/blob/main/task_3_containers/screenshots_lab3/01.png)


Устанавливаем brew
![[./screenshots_lab3/2.png]]
с помощью brew устанавливаем кубер (kubectl и minicube)
![[./screenshots_lab3/3.png]]
проверяем версию куб-контрола.

![[./screenshots_lab3/4.png]]
Запускаем кластер командой 
```bash
minikube start --driver=docker
```
![[./screenshots_lab3/5.png]]
Проверь контейнеры Docker:
![[./screenshots_lab3/6.png]]

kubectl config view
kubectl get nodes

![[./screenshots_lab3/7.png]]
## Сделаем сразу правильный вариант 
```
Для постгреса перенести POSTGRES_USER и POSTGRES_PASSWORD из конфигмапы в секреты.
```

![[./screenshots_lab3/7.png]]

Порядок имеет значение для объектов, от которых зависят другие (ConfigMap/Secret → Deployment). Сервис можно создавать в любое время, но удобнее после Podов.

![[./screenshots_lab3/8.png]]




![[./screenshots_lab3/9.png]]

![[./screenshots_lab3/10.png]]

![[./screenshots_lab3/11.png]]


![[./screenshots_lab3/12.png]]

видно тип `Opaque` и размер, но не пароль:
![[./screenshots_lab3/13.png]]
![[./screenshots_lab3/14.png]]

![[./screenshots_lab3/15.png]]![[./screenshots_lab3/16.png]]
![[./screenshots_lab3/17.png]]

![[./screenshots_lab3/18.png]]

![[./screenshots_lab3/19.png]]


![[./screenshots_lab3/20.png]]
- При `replicas=0` pod Postgres удаляется, а вместе с ним и все данные, потому что мы не настраивали PersistentVolume — база хранится в файловой системе контейнера.
    
- При `replicas=1` под создаётся заново с пустой БД.  
    В результате Nextcloud либо предлагает сделать повторную установку, либо выдаёт ошибку — прежние пользователи и данные пропали.
![[./screenshots_lab3/21.png]]


> Важен ли порядок выполнения этих манифестов? Почему?
 Важен для зависимостей:  Сначала ConfigMap/Secret, потом Deployment, который их использует. Иначе pod может не стартовать или будет в CrashLoop из-за отсутствия переменных/volume. Service можно создавать до или после Podов — он просто появится без Endpoints, пока Pod не запущен.




