3. 
- 1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные у пользователя, а можно статически задать в коде. Для взаимодействия с пользователем можно использовать функцию Scanf:
```
package main

import "fmt"

func main() {
    fmt.Print("Enter a number: ")
    var input float64
    fmt.Scanf("%f", &input)

    output := input * 2

    fmt.Println(output)    
}
```
Ответ:
```
package main
import "fmt"
func main() {
	fmt.Print("Enter a number: ")
	var input float64
	fmt.Scanf("%f", &input)
	output := input / 0.3048
	fmt.Println("Итого: ", output, " футов")
}
```
- 2.Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
```
x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
```
Ответ:
```
package main
import "fmt"
func main() {
	x := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17}
	if len(x) > 0 {
		var min = x[0]
		for i := 1; i < len(x); i++ {
			if x[i] < min {
				min = x[i]
			}
		}
		fmt.Println("Минимальный элемент: ", min)
	} else {
		fmt.Println("Пусто!!!")
	}
}
```

- 3. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть (3, 6, 9, …).
Ответ:
```
package main
import "fmt"
func main() {
	fmt.Println("Числа, делящиеся на 3:")
	for i := 1; i <= 100; i++ {
		if i%3 == 0 {
			fmt.Println(i)
		}
	}
}
```
