## Практика  

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).
```
grep -o '^[^:]*' /etc/passwd | sort
```

## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```

```
grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -rn | head -5
```

## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

```
nano banner
```

```
Текст скрипта banner:
#!/bin/bash
text="$1"
len=${#text}
line=$(printf '%*s' $((len + 2)) '' | tr ' ' '-')
echo "+$line+"
echo "| $text |"
echo "+$line+"
```

```
chmod +x banner
./banner "Hello from RTU MIREA!"
```

## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```

```
nano ids
```

```
#!/bin/bash
grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | paste -sd' '
```

```
chmod +x ids
```

```
nano hello.c
```

```
./ids hello.c
```

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```

```
nano reg
```

```
#!/bin/bash
if [ ! -f "$1" ]; then
    echo "Файл $1 не найден"
    exit 1
fi
chmod 755 "$1"
cp "$1" /usr/local/bin/
```

```
chmod +x reg
sudo ./reg banner
```

```
ls -l /usr/local/bin/banner
```

В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.

## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

```
echo '// comment' > a.c
echo 'int x;' > b.c
echo '# comment' > c.py
echo 'print(1)' > d.py
echo '// hi' > e.js
```

```
nano check_comment
```

```
#!/bin/bash
dir="${1:-.}"
find "$dir" -type f \( -name '*.c' -o -name '*.js' -o -name '*.py' \) | while IFS= read -r f; do
    first=$(head -n 1 "$f")
    case "$f" in
        *.py) pat='^[[:space:]]*#' ;;
        *)    pat='^[[:space:]]*(//|/\*)' ;;
    esac
    if echo "$first" | grep -qE "$pat"; then
        echo "$f: комментарий есть"
    else
        echo "$f: комментария нет"
    fi
done
```

```
chmod +x check_comment
./check_comment .
```

## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

```
echo 'hello' > a.txt
echo 'hello' > b.txt
echo 'world' > c.txt
mkdir sub
echo 'hello' > sub/d.txt
```

```
nano dups
```

```
#!/bin/bash
dir="${1:-.}"
find "$dir" -type f -exec md5sum {} + | sort | uniq -w32 --all-repeated=separate
```

```
chmod +x dups
./dups .
```

## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

```
mkdir test8
echo 'one' > test8/a.txt
echo 'two' > test8/b.txt
echo 'three' > test8/c.txt
echo 'int x;' > test8/d.c
```

```
nano arch
```

```
chmod +x arch
./arch txt test8
```

## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

```
printf 'a    b\n        c\nno spaces\n' > input.txt
```

```
nano spaces2tab
```

```
#!/bin/bash
sed 's/ \{4\}/\t/g' "$1" > "$2"
```

```
chmod +x spaces2tab
./spaces2tab input.txt output.txt
```

```
cat -A output.txt
```

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром. 

```
mkdir test10
touch test10/empty1.txt
touch test10/empty2.txt
echo 'text' > test10/full.txt
```
```
nano empty_files
```
```
#!/bin/bash
find "$1" -maxdepth 1 -type f -empty
```
```
chmod +x empty_files
./empty_files test10
```
