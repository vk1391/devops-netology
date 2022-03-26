1. Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: https://github.com/hashicorp/terraform-provider-aws.git. Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.

 - 1. Найдите, где перечислены все доступные resource и data_source, приложите ссылку на эти строки в коде на гитхабе.
 - 2. Для создания очереди сообщений SQS используется ресурс aws_sqs_queue у которого есть параметр name.
       * С каким другим параметром конфликтует name? Приложите строчку кода, в которой это указано.
       * Какая максимальная длина имени?
       * Какому регулярному выражению должно подчиняться имя?

 - Ответ:
   1. нашёл в файле [provider.go](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/provider/provider.go)
   [Resource](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/provider/provider.go#L737) 737-1760 строки
   [Data_source](https://github.com/hashicorp/terraform-provider-aws/blob/main/internal/provider/provider.go#L344) 344-735 строки


   2. - конфликтует с [name_prefix](https://github.com/hashicorp/terraform-provider-aws/blob/5902887f418edd969cff285acb35464a9c435c11/internal/service/sqs/queue.go#L88)
      - Я так понимаю максимальная длина имени и регулярное выражение не заданы.
