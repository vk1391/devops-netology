1. Предложите решение для обеспечения развертывания, запуска и управления приложениями.
Решение может состоять из одного или нескольких программных продуктов и должно описывать способы и принципы их взаимодействия.

Ответ:

Требования/Решения |   K8S  |  Docker Swarm
-------------------|   ---  |  ------------
Поддержка контейнеров |  +  |  +  
Обеспечивать обнаружение сервисов и маршрутизацию запросов |  +  |  +  
Обеспечивать возможность горизонтального масштабирования | +  |  +
Обеспечивать возможность автоматического масштабирования | +  |  -
Обеспечивать явное разделение ресурсов доступных извне и внутри системы | +  |  -
Обеспечивать возможность конфигурировать приложения<br>с помощью переменных среды, в том числе с возможностью безопасного <br>хранения чувствительных данных таких как пароли, ключи доступа,<br>ключи шифрования и т.п. | +  |  +

Выбор пал на Kubernates так как удовлетворяет всем требованиям, более стабилен, структурирован, имеет шаблонизатор(Helm)