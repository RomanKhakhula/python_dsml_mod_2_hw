--Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
select t.* from tasks t where user_id = 10; 

--Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
select t.* from tasks t where t.status_id in(select s.id from statuses s where s.name in('new', 'completed'));

--Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
update tasks t set status_id = 2 where id = 9 and status_id = 1;

--Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
select u.* from users u where u.id not in (select distinct t.user_id from tasks t order by 1);

--Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
insert into tasks(title, description, status_id, user_id) values('update scrip', 'Update triger script.', 1, 15);

--Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
select t.* from tasks t where t.status_id in(select s.id from statuses s where s.name <> 'completed');

--Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
delete from tasks t where id = 20;

--Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
select * from users u where email like '%.net';

--Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
update users u set fullname = 'Tanner Sullivan' where u.fullname = 'Tarner Sullivan'; 

--Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
select s.name, count(t.id)  from tasks t join statuses s on t.status_id = s.id group by s.name order by count desc;

--Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
--Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, 
--чия електронна пошта містить певний домен (наприклад, '%@example.com').
select t.*, u.email  from tasks t join users u  on t.user_id = u.id where u.email like '%@example.com';

--Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
select t.* from tasks t where t.description is null or length(t.description) < 1; 

--Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
--Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
select u.*, t.*  from tasks t join users u  on t.user_id = u.id join statuses s on t.status_id = s.id where s.name = 'in progress';

--Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
select u.*,
count(case when t.status_id = 1 then 1 else null end) as new_tasks,
count(case when t.status_id = 2 then 1 else null end) as tasks_in_progress,
count(case when t.status_id = 3 then 1 else null end) as completed_tasks
from users u left join tasks t  on u.id = t.user_id group by 1, 2, 3 order by 1;
