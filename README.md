5. гигабайт ОЗУ 40 гб на диске
8.1. 1985:history-size (unset)
8.2. ignoreboth не сохраняет строки начинающиеся с символа <пробел>, и не сохраняет строки, совпадающие с последней выполненной командой
9. 786 {} Скобки необходимы, чтобы избежать конфликтов при раскрытии имени пути
"When a positional parameter consisting of more than a single digit is expanded, it must be enclosed in braces"  на 421 строке
 что дословно:
"Когда позиционный параметр, состоящий более чем из одной цифры, раскрывается, он должен быть заключен в фигурные скобки."
А более точно описано в разделе -EXPANSION c 814 строки по 867( Brace Expansion на 829).
10. touch arg{1..100000} 100000 создает, 300000 нет,я так понимаю как то связано с со stack-size но как не понял
11. grep: Unmatched [, [^, [:, [., or [=
12. не могу понять где не прав,добавляю путь, echo $PATH
/tmp/new_path_directory/:/tmp/new_path_directory:/tmp/new_path_directory:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:
/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/tmp/new_path_directory:/tmp/new_path_directory/bash
а в type -a bash строка не добавляется
13. команда at используется для назначения одноразового задания на заданное время, а команда batch — 
для назначения одноразовых задач, которые должны выполняться, когда загрузка системы становится меньше 0,8
