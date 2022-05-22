## CRM for Test Task
### Как не трудно домотаться из названия, проект который я делаю для тестового задания, ТЗ описано ниже:
## ТЕСТОВОЕ ЗАДАНИЕ ДЛЯ ПОСТРОЕНИЯ API-СЕРВИСА:
Overview: Мы - сотрудники компании, которая занимается ремонтом техники, а также консультационными вопросами клиентов. Клиенты, у которых есть вопросы могут связываться с нашей компанией различными способами, но в любом случае это обращение будет регистрироваться в системе как заявка и переводиться на ответственного сотрудника, который будет заниматься данным вопросом.
Наша задача - создать CRM для регистрации и обработки входящих заявок от пользователей.
Необходимо реализовать следующий функционал:
Управление служебными данными (добавление, изменение, удаление):

* клиенты (подумать, как грамотно описать, чтобы было легко подобраться к задаче о нотификации)
* о сотрудниках компании;
* о заявках;
Фильтрация данных:

* заявок по датам создания (конкретная дата, промежуток дат);
* заявок по типам (заявка на ремонт, обслуживание, консультацию и т.д.);
* заявок по статусам (одному или нескольким: например "открыта", "в работе", "закрыта" и т.д.);

Весь функионал должен быть закрыт от несанционированного доступа (произвольным способом). Фунционал покрыть тестами.
Система оповещения* (задача со звёздочкой): Предусмотреть механизм оповещения пользователя об изменении статуса заявки посредством использования телеграм-бота и Telegram API. Пользователь должен иметь возможность подписаться на уведомления, после чего при каждом изменении в статусах заявок, которые оформлены на него в соответствующий чат должна прилетать информация об этом.

Также необходимо составить документацию, описывающую функционал сервиса и правила работы с ним.

Примечание: можно использовать любые Python-фреймворки и любые БД для решения поставленных задач.