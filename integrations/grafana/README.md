1. Сейчас доекрфайл пока состоит только из базового образа, в котором есть
  * Grafana
  * Graphite
  * Statsd
  * Carbon
2. Поднять контейнер, в котором все это есть, можно так: *bash run.sh*
3. В этом контейнеры открыты следующие порты:
  * 80: the Grafana web interface.
  * 81: the Graphite web port
  * 2003: the Graphite data port
  * 2004: the Graphite pickle protocol port
  * 8125: the StatsD port.
  * 8126: the StatsD administrative port.
4. После поднятия контейнера, в UI нужно добавить datasource на основе *graphite*. (Пока руками. Потом при поднятии контейнера просто подсунем нужный файл с конфигами датасурсов)
  * Заходим на <hostname>:80 в браузере. Логинимся admin:admin
  * Жмем на вкладку Data Sources -> Add new
  * Называем как угодно; type: Graphite -> url: http://<hostname>:81
  * Жмем Add

Все, теперь можно начать отправлять метрики:
1) Через graphite(через сокеты):
  - echo "<metric.name.to.send> <metic-value-to-send> `date +%s`" | nc <hostname> 2003
  - Название метрики будет совпадать с <metric.name.to.send>
2) Через statsd
  - Через сокеты: echo "new.metric.for.test:123|c" | nc -u <hostname> 8125
  - Через питоновский клиент: 
      import statsd
 
 
      client = statsd.StatsClient(host='localhost', port=8125)
      client.incr('new.metric.for.test', 123)
  - Название метрики в графане будет таким: stats.<metric.name.to.send> или stats_counts.<metric.name.to.send> (по префиксу stats_counts -- без аггрегации)
