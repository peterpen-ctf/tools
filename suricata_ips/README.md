Инструкция - дропать пакеты с определенным текстовым содержимым с помощью Suricata

Если не установлена:

sudo apt-get install Suricata

Добавляем правила в iptables

iptables -t mangle -A PREROUTING -p tcp -m tcp --dport 80 -m mark ! --mark 0x1/0x1 -j NFQUEUE --queue-num 0

# детектируем пакет, на который сработало правило
iptables -t mangle -A PREROUTING -p tcp -m tcp --dport 80 -m mark --mark 0x2/0xfe -j LOG --log-prefix "python packet detected"


Идем в папку /etc/suricata

	копируем файл suricata-debian.yaml в файл suricata.yaml


Находим строчку с default-log-dir

	Меняем на default-log-dir: /var/log/suricata/

Находим строчку "nfq".
	Меняем на строчки 
	
	nfq:
 		mode: repeat
 		repeat-mark: 1
 		repeat-mask: 1

Все остальное что относилось к разделу nfq должно быть закомменчено

Находим строчку "rule-files:"
Все файлы ниже с правилами закомментить
Добавить строчку "   - test.rules"


Сохраняем файл. Создаем в этой же директории (/etc/suricata) файл test.rules


Добавляем строчку

drop tcp any any -> any any (content: "python"; msg: "python detected!"; nfq_set_mark:0x2/0xffffffff; sid:53911;)

Сохраняем. Закрываем.


Запускаем командой: suricata -q 0 -c /etc/suricata/suricata.yaml

Дропать будет соответственно пакет, в которых есть текст "python". Менять правило дропа в файл test.rules 
Менять сообщение в логе в тексте правила второго (в этом документе) для iptables
Смотреть лог в файл /vat/log/suricata/fast.log
