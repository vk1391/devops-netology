2. - Задача 2. Написать серверный конфиг для атлантиса.
Смысл задания – познакомиться с документацией о серверной конфигурации и конфигурации уровня репозитория.

Создай server.yaml который скажет атлантису:

Укажите, что атлантис должен работать только для репозиториев в вашем github (или любом другом) аккаунте.
На стороне клиентского конфига разрешите изменять workflow, то есть для каждого репозитория можно будет указать свои дополнительные команды.
В workflow используемом по-умолчанию сделайте так, что бы во время планирования не происходил lock состояния.
Создай atlantis.yaml который, если поместить в корень terraform проекта, скажет атлантису:

Надо запускать планирование и аплай для двух воркспейсов stage и prod.
Необходимо включить автопланирование при изменении любых файлов *.tf.
В качестве результата приложите ссылку на файлы server.yaml и atlantis.yaml.
Ответ:
- atlantis.yaml
```
version: 3
automerge: true
delete_source_branch_on_merge: true

projects:
  - workspace: stage
    dir: .
    autoplan:
      when_modified: [ "*.tf" ]
      enabled: true
    workflow: myworkflow

  - workspace: prod
    dir: .
    autoplan:
      when_modified: [ "*.tf" ]
      enabled: true
    workflow: myworkflow

workflows:
  myworkflow:
    plan:
      steps:
        - init
        - plan:
            extra_args: [ "-lock", "false" ]
        - run: echo planned
    apply:
      steps:
        - run: echo applying
        - apply
  ```
  - server.yaml
  ```
  repos:
  - id: /.*/
    branch: /.*/
    allowed_overrides: [ workflow ]

  - id: github.com/vk1391/devops-netology
    branch: /.*/
    workflow: custom
    allowed_overrides: [ workflow ]
    allow_custom_workflows: true

workflows:
  custom:
    plan:
      steps:
        - init
        - plan:
            extra_args: [ "-lock", "false" ]
        - run: echo planned
    apply:
      steps:
        - run: echo applying
        - apply
 ```
 3.Задача 3. Знакомство с каталогом модулей.
В каталоге модулей найдите официальный модуль от aws для создания ec2 инстансов.
Изучите как устроен модуль. Задумайтесь, будете ли в своем проекте использовать этот модуль или непосредственно ресурс aws_instance без помощи модуля?
В рамках предпоследнего задания был создан ec2 при помощи ресурса aws_instance. Создайте аналогичный инстанс при помощи найденного модуля.
В качестве результата задания приложите ссылку на созданный блок конфигураций.
Ответ:
 - Так как в aws не могу зарегестрироваться,по сути выполнить дз тож не могу.Среди модулей нашёл https://registry.terraform.io/modules/glavk/compute/yandex/latest. Я так понимаю это оно 
